from django.db import models

from helpers.models.basemodel import BaseModel

# Create your models here.
class Currency(BaseModel):
    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name

