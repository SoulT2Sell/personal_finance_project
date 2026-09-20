from django import forms

from apps.transactions.models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["account", "category", "transaction_type", "amount", "description", "transaction_date"]

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["account"].queryset = user.accounts.filter(is_active=True)
        self.fields["category"].queryset = user.categories.filter(is_active=True)

