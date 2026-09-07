from django.db import models
from django.conf import settings

from helpers.models.basemodel import BaseModel
from apps.common.models import Currency


# Create your models here.
class AccountType(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Account(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    account_type = models.ForeignKey(
        AccountType, on_delete=models.PROTECT, related_name="accoun_type"
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.PROTECT, related_name="currency"
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                condition=models.Q(is_active=True),
                name="unique_account_name_per_user",
            ),
            models.UniqueConstraint(
                fields=["user", "slug"],
                condition=models.Q(is_active=True),
                name="unique_account_slug_per_user",
            ),
        ]
