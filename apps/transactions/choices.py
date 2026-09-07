from django.db import models

class TransactionType(models.TextChoices):
    INCOME = "income", "Income"
    EXPENSE = "expense", "Expense"
    TRANSFER = "transfer", "Transfer"
    REFUND = "refund", "Refund"
    FEE = "fee", "Fee"
    ADJUSTMENT = "adjustment", "Adjustment"