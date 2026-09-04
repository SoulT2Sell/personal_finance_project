from django.contrib import admin

from apps.categories.models import Category

# Register your models here.
@admin.register(Category)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'slug','is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'user', 'slug')
    prepopulated_fields = {'slug':('name',)}
    ordering = ('name',)