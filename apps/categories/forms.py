from django import forms
from django.utils.text import slugify
from unidecode import unidecode

from apps.categories.models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def save(self, commit = True):
        category = super().save(commit = False)

        base_name = category.name
        name = base_name
        counter = 2

        while Category.objects.filter(
            user = category.user,
            name = name
        ).exclude(pk=category.pk).exists():
            name = f"{base_name}-{counter}"
            counter += 1

        category.name = name
        category.slug = slugify(unidecode(name))

        if commit:
            category.save()

        return category