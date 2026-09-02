from django.db import models

class AccountType(models.TextChoices):
    CASH = "cash", "Cash"
    BANK = "bank", "Bank Account"
    SAVINGS = "savings", "Savings Account"
    CREDIT_CARD = "credit_card", "Credit Card"
    INVESTMENT = "investment", "Investment Acount"