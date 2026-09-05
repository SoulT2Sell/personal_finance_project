from django.contrib import admin

from apps.accounts.models import Account, AccountType


# Register your models here.
@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)


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
    search_fields = ("name", "user", "slug", "balance", "currency")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
