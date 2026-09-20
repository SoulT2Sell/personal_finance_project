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
        "description",
        "transaction_date", 
        "created_at", 
        "updated_at", 
        "is_active"
    )
    search_fields = ("id", "category", "account", "transaction_date", "amount", "created_at", "update_at", 'is-active')
    ordering = ("transaction_date",)

# @admin.register(Transfer)
# class TransferAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "from_account",
#         "to_account",
#         "amount",
#         "description",
#         "transfer_date",
#         "created_at", 
#         "updated_at", 
#         "is_active"
#     )

#     search_fields = ("id", "from_account", "to_account", "transfer_date", "amount", "created_at", "updated_at", "is_active")
#     ordering = ("transfer_date",)
