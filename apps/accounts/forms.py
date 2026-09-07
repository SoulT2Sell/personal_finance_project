from django import forms
from django.utils.text import slugify
from unidecode import unidecode

from apps.accounts.models import Account, AccountType
from apps.common.models import Currency


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "account_type", "currency", "balance"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["account_type"].queryset = AccountType.objects.filter(is_active=True)
        self.fields["currency"].queryset = Currency.objects.filter(is_active=True)

    def save(self, commit=True):
        account = super().save(commit=False)

        base_name = account.name
        name = base_name
        counter = 2

        while (
            Account.objects.filter(user=account.user, name=name, is_active=True)
            .exclude(pk=account.pk)
            .exists()
        ):
            name = f"{base_name}-{counter}"
            counter += 1

        account.name = name
        account.slug = slugify(unidecode(name))

        if commit:
            account.save()

        return account
