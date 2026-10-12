from django.db import models

from helpers.models.basemodel import BaseModel

# Create your models here.
class Currency(BaseModel):
    name = models.CharField(max_length=3, unique=True)

    CURRENCY_NAMES = {
        'USD': 'دلار آمریکا',
        'EUR': 'یورو',
        'GBP': 'پوند بریتانیا',
        'JPY': 'ین ژاپن',
        'IRR': 'ریال ایران',
        'TRY': 'لیر ترکیه',
        'RUB': 'روبل روسیه',
        'CNY': 'یوآن چین',
        'AED': 'درهم امارات',
        'CAD': 'دلار کانادا',
        'AUD': 'دلار استرالیا',
        'CHF': 'فرانک سوئیس',
        'INR': 'روپیه هند',
        'BRL': 'رئال برزیل',
        'KRW': 'وون کره جنوبی',
        'SEK': 'کرونه سوئد',
        'NOK': 'کرونه نروژ',
        'DKK': 'کرونه دانمارک',
        'BTC': 'بیت‌کوین',
        'TRL': 'لیر ترکیه',
    }

    @property
    def display_name(self):
        return self.CURRENCY_NAMES.get(self.name.upper(), self.name)

    def __str__(self):
        return self.name


class ExchangeRate(BaseModel):
    from_currency = models.ForeignKey(
        Currency, on_delete=models.PROTECT, related_name="exchange_rates_from"
    )
    to_currency = models.ForeignKey(
        Currency, on_delete=models.PROTECT, related_name="exchange_rates_to"
    )
    rate = models.DecimalField(max_digits=15, decimal_places=6)
    date = models.DateField()

    def __str__(self):
        return f"1 {self.from_currency} = {self.rate} {self.to_currency} ({self.date})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_currency", "to_currency", "date"],
                name="unique_exchange_rate_per_date",
            )
        ]

