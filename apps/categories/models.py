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

# class ProgressableCategory(Category):
#     target_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     deadline = models.DateField(null=True, blank=True)
#     monthly_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
#     @property
#     def progress(self):
#         if self.target_amount == 0: 
#             return 0

#         return (self.target_amount/self.current_amount) * 100
