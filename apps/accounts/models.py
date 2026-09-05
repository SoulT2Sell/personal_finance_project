from django.db import models
from django.conf import settings
import uuid

from django.db.models import ForeignKey


from apps.common.models import Currency


# Create your models here.
class AccountType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
