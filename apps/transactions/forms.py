from django import forms

from apps.transactions.models import Transaction, TransactionType

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["account", "category", "transaction_type", "amount", "description", "transaction_date"]

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["account"].queryset = user.accounts.filter(is_active=True)
        self.fields["category"].queryset = user.categories.filter(is_active=True)

    def clean(self):
        cleaned_data = super().clean()

        account = cleaned_data.get("account")
        amount = cleaned_data.get("amount")
        transaction_type = cleaned_data.get("transaction_type")

        # this comment lines just was for test
        # print("ACCOUNT:", account)
        # print("BALANCE:", account.balance if account else None)
        # print("AMOUNT:", amount)
        # print("TYPE:", transaction_type)
        # print("PK:", self.instance.pk)

        if not account or not amount or not transaction_type:
            return cleaned_data

        if amount <= 0:
            raise forms.ValidationError( "مبلغ تراکنش باید بیشتر از صفر باشد." )

        if (transaction_type == TransactionType.EXPENSE and self.instance._state.adding and amount > account.balance):
            raise forms.ValidationError("مبلغ تراکنش بیشتر از موجودی حساب است.")

        return cleaned_data
