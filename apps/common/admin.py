from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.common.models import Currency, ExchangeRate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)
    verbose_name = _("ارز")
    verbose_name_plural = _("ارزها")


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("id", "from_currency", "to_currency", "rate", "date", "is_active", "created_at")
    list_filter = ("from_currency", "to_currency", "date", "is_active")
    search_fields = ("from_currency__name", "to_currency__name")
    ordering = ("-date",)
    date_hierarchy = "date"
    verbose_name = _("نرخ ارز")
    verbose_name_plural = _("نرخ‌های ارز")
