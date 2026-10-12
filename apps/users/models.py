from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid

from apps.common.models import Currency

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.email}:{self.username}"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userprofile"
    )
    phone_number = models.CharField(max_length=20, blank=True)
    preferred_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="preferred_currency",
        null=True,
        blank=True,
    )
    timezone = models.CharField(max_length=50, default="UTC")

    def __str__(self):
        return f"{self.user.email}'s profile"

    def get_preferred_currency(self):
        if self.preferred_currency:
            return self.preferred_currency
        return Currency.objects.filter(is_active=True).first()