from django.db import models
from django.conf import settings
import uuid

from helpers.models.basemodel import BaseModel
# Create your models here.
class Category(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                condition=models.Q(is_active=True),
                name="unique_category_name_per_user",
            ),
            models.UniqueConstraint(
                fields=["user", "slug"],
                condition=models.Q(is_active=True),
                name="unique_category_slug_per_user",
            ),
        ]
