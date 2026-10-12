from django import forms
from django.utils.text import slugify
from unidecode import unidecode

from apps.accounts.models import Account, AccountType
from apps.common.models import Currency
from apps.common.templatetags.currency_tags import ACCOUNT_TYPE_DISPLAY_NAMES


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["name", "account_type", "currency", "balance"]
        labels = {
            "name": "نام حساب",
            "account_type": "نوع حساب",
            "currency": "ارز",
            "balance": "موجودی اولیه",
        }
        widgets = {
            "balance": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["account_type"].queryset = AccountType.objects.filter(is_active=True)
        self.fields["currency"].queryset = Currency.objects.filter(is_active=True)

        self.fields["currency"].label_from_instance = lambda obj: obj.display_name
        self.fields["account_type"].label_from_instance = lambda obj: ACCOUNT_TYPE_DISPLAY_NAMES.get(
            obj.name.strip().lower(), obj.name
        ) or obj.name

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
