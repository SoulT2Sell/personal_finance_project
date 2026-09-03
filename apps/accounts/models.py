from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid
from unidecode import unidecode

from apps.accounts.choices import AccountType

# Create your models here.
class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    currency = models.CharField(max_length=3, default="USD")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_account_name_per_user"
            ),
            models.UniqueConstraint(
                fields=["user", "slug"],
                name="unique_account_slug_per_user"
            ),
        ]
