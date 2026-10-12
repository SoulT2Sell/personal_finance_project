from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User, UserProfile
from apps.common.models import Currency


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")
        labels = {
            "email": "ایمیل",
            "username": "نام کاربری",
            "password1": "رمز عبور",
            "password2": "تکرار رمز عبور",
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")
        labels = {
            "first_name": "نام",
            "last_name": "نام خانوادگی",
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone_number", "preferred_currency", "timezone")
        labels = {
            "phone_number": "شماره تلفن",
            "preferred_currency": "ارز ترجیحی",
            "timezone": "منطقه زمانی",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["preferred_currency"].queryset = Currency.objects.filter(is_active=True)
        self.fields["preferred_currency"].required = False
        self.fields["preferred_currency"].label_from_instance = lambda obj: obj.display_name
