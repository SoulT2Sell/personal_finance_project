from django.db import models
from django.conf import settings

from helpers.models.basemodel import BaseModel
from apps.accounts.models import Account
from apps.categories.models import Category
from apps.transactions.choices import TransactionType
# Create your models here.
class Transaction(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TransactionType)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    transaction_date = models.DateField()