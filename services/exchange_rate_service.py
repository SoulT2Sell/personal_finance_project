import logging
import requests
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from apps.common.models import ExchangeRate, Currency

logger = logging.getLogger(__name__)


class ExchangeRateService:
    """Service to fetch exchange rates from free API with database fallback."""

    # Free API endpoints (no API key required)
    API_ENDPOINTS = [
        "https://api.frankfurter.app/latest",
        "https://open.er-api.com/v6/latest",
        "https://api.exchangerate.host/latest",
    ]

    CACHE_TIMEOUT = 3600  # 1 hour

    @classmethod
    def get_rate_from_api(cls, from_currency: str, to_currency: str = None) -> Decimal | dict | None:
        """Fetch exchange rates from free APIs.

        Caches the entire rate set for ``from_currency`` so that a single API
        call populates the cache for every target currency, eliminating
        per-transaction HTTP round-trips.

        Different APIs use different parameter names ('base' vs 'from'), so we
        try both.  We also verify the response ``base`` field matches the
        requested currency, since some APIs (e.g. open.er-api.com) silently
        ignore unknown params and fall back to their default base (USD).
        """
        cache_key = f"exchange_rates_{from_currency}"
        cached_rates = cache.get(cache_key)
        if cached_rates is not None:
            if to_currency is None:
                return cached_rates
            rate = cached_rates.get(to_currency)
            return Decimal(str(rate)) if rate else None

        for endpoint in cls.API_ENDPOINTS:
            # Different APIs use different parameter names; try both
            for param_name in ("base", "from"):
                try:
                    params = {param_name: from_currency}
                    response = requests.get(endpoint, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()

                    rates = data.get("rates", data.get("data", {}))
                    if not rates:
                        continue

                    # Verify the API actually used the correct base currency.
                    response_base = data.get("base")
                    if response_base and response_base.upper() != from_currency.upper():
                        logger.debug(
                            f"API {endpoint} returned base {response_base}, "
                            f"expected {from_currency} - skipping"
                        )
                        continue

                    cache.set(cache_key, rates, cls.CACHE_TIMEOUT)
                    logger.info(
                        f"Cached {len(rates)} rates from {endpoint} (base={from_currency})"
                    )

                    if to_currency is None:
                        return rates
                    rate = rates.get(to_currency)
                    if rate:
                        rate_decimal = Decimal(str(rate))
                        logger.info(
                            f"Fetched rate from API {endpoint}: 1 {from_currency} = {rate_decimal} {to_currency}"
                        )
                        return rate_decimal

                except Exception as e:
                    logger.warning(
                        f"Failed to fetch from {endpoint} ({param_name}={from_currency}): {e}"
                    )
                    continue

        return None

    @classmethod
    def get_rate_from_db(cls, from_currency: Currency, to_currency: Currency, date=None) -> Decimal | None:
        """Get exchange rate from database."""
        if date is None:
            date = timezone.now().date()

        exchange_rate = (
            ExchangeRate.objects.filter(
                from_currency=from_currency,
                to_currency=to_currency,
                date__lte=date,
            )
            .order_by("-date")
            .first()
        )

        if exchange_rate:
            return exchange_rate.rate

        # Try reverse rate
        reverse_rate = (
            ExchangeRate.objects.filter(
                from_currency=to_currency,
                to_currency=from_currency,
                date__lte=date,
            )
            .order_by("-date")
            .first()
        )

        if reverse_rate and reverse_rate.rate != 0:
            return Decimal("1.0") / reverse_rate.rate

        return None

    @classmethod
    def get_exchange_rate(cls, from_currency: Currency, to_currency: Currency, date=None) -> Decimal:
        """Get exchange rate with DB first (fast), then API fallback,
        with a cross-rate fallback via USD when direct rates are unavailable."""
        if from_currency == to_currency:
            return Decimal("1.0")

        db_rate = cls.get_rate_from_db(from_currency, to_currency, date)
        if db_rate:
            return db_rate

        api_rate = cls.get_rate_from_api(from_currency.name, to_currency.name)
        if api_rate:
            return api_rate

        # Cross-rate fallback: compute from_currency → USD → to_currency
        usd = Currency.objects.filter(name="USD", is_active=True).first()
        if usd and from_currency != usd and to_currency != usd:
            rates_from_usd = cls.get_rate_from_api(usd.name)
            if rates_from_usd:
                from_str = from_currency.name.upper()
                to_str = to_currency.name.upper()
                from_rate = rates_from_usd.get(from_str)
                to_rate = rates_from_usd.get(to_str)
                if from_rate and to_rate and float(from_rate) != 0:
                    cross = Decimal(str(to_rate)) / Decimal(str(from_rate))
                    logger.info(
                        f"Cross-rate: 1 {from_currency.name} = {cross} {to_currency.name} (via USD)"
                    )
                    return cross

        # Ultimate fallback
        logger.warning(
            f"No exchange rate found for {from_currency.name} to {to_currency.name}, using 1.0"
        )
        return Decimal("1.0")

    @classmethod
    def convert_amount(cls, amount: Decimal, from_currency: Currency, to_currency: Currency, date=None) -> Decimal:
        """Convert amount from one currency to another."""
        if from_currency == to_currency:
            return amount
        rate = cls.get_exchange_rate(from_currency, to_currency, date)
        return amount * rate

    @classmethod
    def update_rates_from_api(cls, base_currency: str = "USD") -> dict:
        """Fetch and store latest rates from API to database."""
        results = {"success": [], "failed": []}

        for endpoint in cls.API_ENDPOINTS:
            for param_name in ("base", "from"):
                try:
                    params = {param_name: base_currency}
                    response = requests.get(endpoint, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()

                    rates = data.get("rates", data.get("data", {}))
                    if not rates:
                        continue

                    response_base = data.get("base")
                    if response_base and response_base.upper() != base_currency.upper():
                        continue

                    date = timezone.now().date()

                    for currency_code, rate in rates.items():
                        try:
                            from_curr = Currency.objects.get(name=base_currency)
                            to_curr = Currency.objects.get(name=currency_code)

                            exchange_rate, created = ExchangeRate.objects.update_or_create(
                                from_currency=from_curr,
                                to_currency=to_curr,
                                date=date,
                                defaults={"rate": Decimal(str(rate)), "is_active": True},
                            )
                            results["success"].append(f"{base_currency} -> {currency_code}: {rate}")
                        except Currency.DoesNotExist:
                            results["failed"].append(f"Currency {currency_code} not in database")

                    logger.info(f"Updated {len(results['success'])} exchange rates from {endpoint}")
                    return results  # Success, don't try other endpoints/params

                except Exception as e:
                    logger.error(f"Failed to update rates from {endpoint} ({param_name}={base_currency}): {e}")
                    results["failed"].append(str(e))
                    continue

        return results
