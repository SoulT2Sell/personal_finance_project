from django import forms
from django.utils import timezone

from apps.transactions.models import Transaction
from apps.transactions.choices import TransactionType


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["account", "category", "transaction_type", "amount", "description", "transaction_date"]
        labels = {
            "account": "حساب",
            "category": "دسته‌بندی",
            "transaction_type": "نوع تراکنش",
            "amount": "مبلغ",
            "description": "توضیحات",
            "transaction_date": "تاریخ تراکنش",
        }
        widgets = {
            "transaction_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-input",
                },
                format="%Y-%m-%d",
            ),
            "description": forms.Textarea(attrs={"rows": 3}),
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["account"].queryset = user.accounts.filter(is_active=True)
        self.fields["category"].queryset = user.categories.filter(is_active=True)
        self.fields["transaction_type"].choices = TransactionType.choices
        
        # Set default date to today
        if not self.instance.pk:
            self.fields["transaction_date"].initial = timezone.now().date()