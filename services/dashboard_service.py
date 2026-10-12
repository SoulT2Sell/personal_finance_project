from decimal import Decimal

from django.db.models import Sum, F
from django.utils import timezone

from apps.common.models import Currency
from apps.transactions.choices import TransactionType
from services.exchange_rate_service import ExchangeRateService


class DashboardService:
    @staticmethod
    def get_exchange_rate(from_currency: Currency, to_currency: Currency, date=None) -> Decimal:
        return ExchangeRateService.get_exchange_rate(from_currency, to_currency, date)

    @staticmethod
    def convert_amount(amount: Decimal, from_currency: Currency, to_currency: Currency, date=None) -> Decimal:
        return ExchangeRateService.convert_amount(amount, from_currency, to_currency, date)

    @staticmethod
    def _pre_fetch_rates(user, preferred_currency):
        """Pre-fetch exchange rates for every unique currency pair used by this
        user's accounts and transactions.  This replaces the per-transaction
        API round-trip that was the primary cause of dashboard slowness."""
        rate_cache = {}

        accounts = user.accounts.filter(is_active=True).select_related("currency")
        for account in accounts:
            key = (account.currency_id, preferred_currency.id)
            if key not in rate_cache:
                rate_cache[key] = DashboardService.get_exchange_rate(
                    account.currency, preferred_currency
                )

        return rate_cache

    @staticmethod
    def _apply_rate(amount, from_currency, preferred_currency, rate_cache):
        key = (from_currency.id, preferred_currency.id)
        rate = rate_cache.get(key)
        if rate is None:
            rate = DashboardService.get_exchange_rate(from_currency, preferred_currency)
            rate_cache[key] = rate
        return amount * rate

    @staticmethod
    def get_user_total_balance(user, preferred_currency: Currency = None, rate_cache=None) -> Decimal:
        if preferred_currency is None:
            preferred_currency = user.userprofile.get_preferred_currency()
        if rate_cache is None:
            rate_cache = {}

        accounts = user.accounts.filter(is_active=True).select_related("currency")
        total = Decimal("0.0")

        for account in accounts:
            converted = DashboardService._apply_rate(
                account.balance, account.currency, preferred_currency, rate_cache
            )
            total += converted

        return total

    @staticmethod
    def get_user_transactions_summary(user, preferred_currency: Currency = None, rate_cache=None):
        if preferred_currency is None:
            preferred_currency = user.userprofile.get_preferred_currency()
        if rate_cache is None:
            rate_cache = {}

        transactions = user.transactions.filter(is_active=True)

        income_transactions = transactions.filter(transaction_type=TransactionType.INCOME)
        expense_transactions = transactions.filter(transaction_type=TransactionType.EXPENSE)

        total_income = Decimal("0.0")
        total_expense = Decimal("0.0")

        for transaction in income_transactions:
            converted = DashboardService._apply_rate(
                transaction.amount, transaction.account.currency, preferred_currency, rate_cache
            )
            total_income += converted

        for transaction in expense_transactions:
            converted = DashboardService._apply_rate(
                transaction.amount, transaction.account.currency, preferred_currency, rate_cache
            )
            total_expense += converted

        return {
            "income": total_income,
            "expense": total_expense,
            "net": total_income - total_expense,
        }

    @staticmethod
    def get_monthly_transactions_summary(user, preferred_currency: Currency = None, rate_cache=None):
        if preferred_currency is None:
            preferred_currency = user.userprofile.get_preferred_currency()
        if rate_cache is None:
            rate_cache = {}

        month_start = timezone.now().date().replace(day=1)
        transactions = user.transactions.filter(is_active=True, transaction_date__gte=month_start)

        income_transactions = transactions.filter(transaction_type=TransactionType.INCOME)
        expense_transactions = transactions.filter(transaction_type=TransactionType.EXPENSE)

        month_income = Decimal("0.0")
        month_expense = Decimal("0.0")

        for transaction in income_transactions:
            converted = DashboardService._apply_rate(
                transaction.amount, transaction.account.currency, preferred_currency, rate_cache
            )
            month_income += converted

        for transaction in expense_transactions:
            converted = DashboardService._apply_rate(
                transaction.amount, transaction.account.currency, preferred_currency, rate_cache
            )
            month_expense += converted

        return {
            "income": month_income,
            "expense": month_expense,
            "net": month_income - month_expense,
        }

    @staticmethod
    def get_top_categories(user, preferred_currency: Currency = None, rate_cache=None, limit=5):
        if preferred_currency is None:
            preferred_currency = user.userprofile.get_preferred_currency()
        if rate_cache is None:
            rate_cache = {}

        month_start = timezone.now().date().replace(day=1)
        transactions = user.transactions.select_related("account__currency").filter(
            is_active=True, transaction_type=TransactionType.EXPENSE, transaction_date__gte=month_start
        )

        category_totals = {}
        for transaction in transactions:
            category_name = transaction.category.name
            converted = DashboardService._apply_rate(
                transaction.amount, transaction.account.currency, preferred_currency, rate_cache
            )
            if category_name in category_totals:
                category_totals[category_name] += converted
            else:
                category_totals[category_name] = converted

        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:limit]
        return [{"name": name, "total": total} for name, total in sorted_categories]

    @staticmethod
    def get_dashboard_context(user):
        preferred_currency = user.userprofile.get_preferred_currency()

        rate_cache = DashboardService._pre_fetch_rates(user, preferred_currency)

        total_balance = DashboardService.get_user_total_balance(
            user, preferred_currency, rate_cache
        )
        all_time = DashboardService.get_user_transactions_summary(
            user, preferred_currency, rate_cache
        )
        monthly = DashboardService.get_monthly_transactions_summary(
            user, preferred_currency, rate_cache
        )
        top_categories = DashboardService.get_top_categories(
            user, preferred_currency, rate_cache
        )
        max_category_total = top_categories[0]["total"] if top_categories else Decimal("0.0")
        accounts = user.accounts.filter(is_active=True).select_related("currency")
        recent_transactions = user.transactions.filter(is_active=True).select_related(
            "account__currency", "category"
        ).order_by("-created_at")[:10]

        return {
            "total_balance": total_balance,
            "income": all_time["income"],
            "expense": all_time["expense"],
            "net": all_time["net"],
            "month_income": monthly["income"],
            "month_expense": monthly["expense"],
            "month_net": monthly["net"],
            "accounts": accounts,
            "recent_transactions": recent_transactions,
            "top_categories": top_categories,
            "max_category_total": max_category_total,
            "preferred_currency": preferred_currency,
        }
