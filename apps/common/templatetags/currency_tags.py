from django import template
from django.utils.safestring import mark_safe
import re

from apps.common.models import Currency

register = template.Library()

# Currencies that don't use decimal places (like IRR)
ZERO_DECIMAL_CURRENCIES = {'IRR', 'VND', 'JPY', 'KRW', 'CLP', 'PYG', 'UGX', 'BIF', 'DJF', 'GNF', 'KMF', 'MGA', 'RWF', 'XAF', 'XOF', 'XPF'}

# Currencies that use 3 decimal places
THREE_DECIMAL_CURRENCIES = {'BHD', 'JOD', 'KWD', 'OMR', 'TND'}

# Default decimal places for most currencies
DEFAULT_DECIMAL_PLACES = 2

# Persian display names for common English account type names
ACCOUNT_TYPE_DISPLAY_NAMES = {
    'bank': 'بانکی',
    'bank account': 'حساب بانکی',
    'checking': 'جاری',
    'savings': 'پس‌انداز',
    'cash': 'نقد',
    'credit card': 'کارت اعتباری',
    'debit card': 'کارت نقدی',
    'investment': 'سرمایه‌گذاری',
    'loan': 'وام',
    'credit': 'اعتباری',
    'wallet': 'کیف پول',
    'ewallet': 'کیف پول الکترونیک',
    'mobile wallet': 'کیف پول موبایلی',
    'crypto': 'ارز دیجیتال',
    'cryptocurrency': 'ارز دیجیتال',
}


@register.simple_tag
def get_decimal_places(currency_code):
    """Get the number of decimal places for a currency."""
    currency_code = currency_code.upper() if currency_code else ''
    if currency_code in ZERO_DECIMAL_CURRENCIES:
        return 0
    elif currency_code in THREE_DECIMAL_CURRENCIES:
        return 3
    return DEFAULT_DECIMAL_PLACES


@register.simple_tag
def format_currency(amount, currency_code=None):
    """
    Format a currency amount according to the currency's conventions.
    For IRR and similar: no decimals, thousands separator
    For most currencies: 2 decimals, thousands separator
    For some: 3 decimals
    """
    if amount is None:
        return ''

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return str(amount)

    currency_code = currency_code.upper() if currency_code else ''
    decimal_places = get_decimal_places(currency_code)

    # Format with appropriate decimal places
    if decimal_places == 0:
        formatted = f"{amount:,.0f}"
    else:
        formatted = f"{amount:,.{decimal_places}f}"

    # Replace comma with Persian thousands separator
    formatted = formatted.replace(',', '٬')

    return mark_safe(formatted)


@register.filter
def format_currency_with_symbol(amount, currency_code=None):
    """Format currency amount with the currency code."""
    formatted = format_currency(amount, currency_code)
    if currency_code:
        return mark_safe(f"{formatted} {currency_code}")
    return formatted


@register.filter
def format_currency_rtl(amount, currency_code=None):
    """Format currency for RTL display (Persian/Arabic)."""
    formatted = format_currency(amount, currency_code)
    if currency_code:
        return mark_safe(f"{currency_code} {formatted}")
    return formatted


@register.filter(name="currency_name")
def currency_name(currency_code):
    """Return the Persian display name for a currency code."""
    if not currency_code:
        return ''
    if hasattr(currency_code, "name"):
        currency_code = currency_code.name
    code = currency_code.upper()
    return Currency.CURRENCY_NAMES.get(code, currency_code)


@register.filter(name="account_type_name")
def account_type_name(account_type_value):
    """Return the Persian display name for an account type.

    Falls back to the original value if no mapping is found.
    """
    if not account_type_value:
        return ''
    if account_type_value in ACCOUNT_TYPE_DISPLAY_NAMES:
        return ACCOUNT_TYPE_DISPLAY_NAMES[account_type_value]
    key = account_type_value.strip().lower()
    if key in ACCOUNT_TYPE_DISPLAY_NAMES:
        return ACCOUNT_TYPE_DISPLAY_NAMES[key]
    return account_type_value
