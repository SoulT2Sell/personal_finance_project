from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.users.models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    verbose_name = _("پروفایل کاربر")
    verbose_name_plural = _("پروفایل کاربر")


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ("id", "email", "username", "first_name", "last_name", "is_staff", "is_active", "date_joined")
    search_fields = ("email", "username", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser")
    ordering = ("-date_joined",)
    verbose_name = _("کاربر")
    verbose_name_plural = _("کاربران")


admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "preferred_currency", "timezone", "admin_link")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "phone_number",
    )
    list_filter = ("preferred_currency", "timezone")
    verbose_name = _("پروفایل")
    verbose_name_plural = _("پروفایل‌ها")

    def admin_link(self, obj):
        url = reverse("admin:users_userprofile_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, _("ویرایش پروفایل"))
    admin_link.short_description = _("عملیات")
