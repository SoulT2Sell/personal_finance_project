from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Account, AccountType


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)
    verbose_name = _("نوع حساب")
    verbose_name_plural = _("انواع حساب")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
        "slug",
        "balance",
        "account_type",
        "currency",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "user__username", "slug", "balance", "currency__name")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
    list_filter = ("account_type", "currency", "is_active")
    verbose_name = _("حساب")
    verbose_name_plural = _("حساب‌ها")
