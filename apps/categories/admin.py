from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
        "slug",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "user__username", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
    list_filter = ("is_active",)
    verbose_name = _("کتگوری")
    verbose_name_plural = _("کتگوری‌ها")
