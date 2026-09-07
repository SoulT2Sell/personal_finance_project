from django.contrib import admin

from apps.transactions.models import Transaction

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "user", 
        "account", 
        "category",
        "transaction_type", 
        "amount", 
        "transaction_date", 
        "created_at", 
        "updated_at", 
        "is_active"
    )
    search_fields = ("category", "account", "transaction_date", "amount")
    ordering = ("transaction_date",)
