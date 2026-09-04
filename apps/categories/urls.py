from django.urls import path

from apps.categories.views import CategoriesView, CategoryView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

app_name = "apps.categories"

urlpatterns = [
    path("", CategoriesView.as_view(), name="list"),
    path("create/", CategoryCreateView.as_view(), name="create"),
    path("<slug:slug>/", CategoryView.as_view(), name="detail"),
    path("<slug:slug>/edit", CategoryUpdateView.as_view(), name="edit"),
    path("<slug:slug>/delete", CategoryDeleteView.as_view(), name="delete"),
]
