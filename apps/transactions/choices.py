from django.db import models

class TransactionType(models.TextChoices):
    INCOME = "income", "درآمد"
    EXPENSE = "expense", "هزینه"
    TRANSFER = "transfer", "انتقال"
    REFUND = "refund", "بازپرداخت"
    FEE = "fee", "کارکرد"
    ADJUSTMENT = "adjustment", "تنظیم"