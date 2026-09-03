from django import forms
from django.utils.text import slugify
from unidecode import unidecode

from apps.accounts.models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "account_type", "currency", "balance"]

    def save(self, commit = True):
        account = super().save(commit)

        base_slug = slugify(unidecode(account.name))
        slug = base_slug
        counter = 2

        while Account.objects.filter(
            user = account.user,
            slug = slug,
        ).exclude(pk=account.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        account.slug = slug

        if commit:
            account.save()

        return account    