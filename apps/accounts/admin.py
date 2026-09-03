from django.contrib import admin

from apps.accounts.models import Account

# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'slug', 'balance', 'account_type', 'currency', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'user', 'slug', 'balance', 'currency')
    prepopulated_fields = {'slug':('name',)}
    ordering = ('name',)