from django import forms
from django.utils.text import slugify
from unidecode import unidecode

from apps.accounts.models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "account_type", "currency", "balance"]

    def save(self, commit = True):
        account = super().save(commit=False)

        base_name = account.name
        name = base_name
        counter = 2

        while Account.objects.filter(
            user = account.user,
            name = name
        ).exclude(pk=account.pk).exists():
            name = f"{base_name}-{counter}"
            counter += 1


        account.name = name
        account.slug = slugify(unidecode(name))

        if commit:
            account.save()

        return account    