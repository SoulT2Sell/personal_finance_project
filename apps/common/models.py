from django.db import models
import uuid

from helpers.models.basemodel import BaseModel

# Create your models here.
class Currency(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name

