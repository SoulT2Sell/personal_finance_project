from django.db import transaction

from apps.transactions.models import Transaction
from apps.transactions.choices import TransactionType

class TransactionService:

    @staticmethod
    @transaction.atomic
    def create(*, transaction_obj: Transaction) -> Transaction:

        account = transaction_obj.account
        amount = transaction_obj.amount

        if amount <= 0:
            raise ValueError(
                "مبلغ تراکنش باید بیشتر از 0 باشد"
            )

        if transaction_obj.transaction_type == TransactionType.EXPENSE:
            if amount > account.balance:
                raise ValueError(
                    "موجودی حساب کافی نیست"
                )

            account.balance -= amount
        elif transaction_obj.transaction_type == TransactionType.INCOME:
            account.balance += amount


        account.save(update_fields=["balance"])
        
        transaction_obj.save()

        return transaction_obj

    @staticmethod
    @transaction.atomic
    def update(*, transaction_obj: Transaction) -> Transaction:

        old_transaction = Transaction.objects.filter(id = transaction_obj.id).first()
        old_account = old_transaction.account
        old_amount = old_transaction.amount
        old_type = old_transaction.transaction_type

        if old_type == TransactionType.EXPENSE:
            old_account.balance += old_amount 
        elif old_type == TransactionType.INCOME:
            if old_amount > old_account.balance:
                raise ValueError(
                    "موجودی حساب قبلی برای اعمال تغییرات کافی نیست"
                )
            
            old_account.balance -= old_amount

        new_account = transaction_obj.account
        new_amount = transaction_obj.amount
        new_type = transaction_obj.transaction_type       

        if new_amount <= 0: 
            raise ValueError(
                "مبلغ تراکنش باید بیشتر از 0 باشد"
            )

        if new_type == TransactionType.EXPENSE:
            if new_amount > new_account.balance:
                raise ValueError(
                    "موجودی حساب کافی نیست"
                )

            new_account.balance -= new_amount
        elif new_type == TransactionType.INCOME:
            new_account.balance += new_amount

        old_account.save(update_fields=["balance"])
        new_account.save(update_fields=["balance"])
        transaction_obj.save()

        return transaction_obj

    @staticmethod
    @transaction.atomic
    def deactivate(*, transaction_obj:Transaction):
        account = transaction_obj.account
        amount = transaction_obj.amount

        if transaction_obj.transaction_type == TransactionType.EXPENSE:
            account.balance += amount
        elif transaction_obj.transaction_type == TransactionType.INCOME:
            if amount > account.balance:
                raise ValueError(
                    "موجودی حساب قبلی برای اعمال تغییرات کافی نیست"
                )

            account.balance -= amount

        account.save(update_fields=["balance"])

        transaction_obj.is_active = False
        transaction_obj.save()