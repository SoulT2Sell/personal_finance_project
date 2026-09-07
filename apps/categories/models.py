from django.db import models
from django.conf import settings

from helpers.models.basemodel import BaseModel
# Create your models here.
class Category(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name
    
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

