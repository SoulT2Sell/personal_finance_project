from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.transactions.models import Transaction
from apps.transactions.choices import TransactionType


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "account",
        "category",
        "transaction_type",
        "amount",
        "description",
        "transaction_date",
        "created_at",
        "updated_at",
        "is_active",
    )
    search_fields = (
        "id",
        "category__name",
        "account__name",
        "transaction_date",
        "amount",
        "created_at",
        "updated_at",
    )
    list_filter = ("transaction_type", "is_active", "account__currency", "category")
    ordering = ("-transaction_date",)
    verbose_name = _("تراکنش")
    verbose_name_plural = _("تراکنش‌ها")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user", "account", "category", "account__currency")
