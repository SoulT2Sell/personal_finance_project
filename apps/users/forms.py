from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User, UserProfile
from apps.common.models import Currency


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=commit)
        UserProfile.objects.create(user=user)
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone_number", "preferred_currency", "timezone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["preferred_currency"].queryset = Currency.objects.filter(is_active=True)
