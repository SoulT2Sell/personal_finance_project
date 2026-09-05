from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from apps.users.models import User, UserProfile


# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)


admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_diplay = ("user", "mobile_number")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "mobile_number",
    )
