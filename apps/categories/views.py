from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from apps.categories.models import Category
from apps.categories.forms import CategoryForm


# Create your views here.
class CategoriesView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "categories/categories.html"
    context_object_name = "categories"
    login_url = "users:login"

    def get_queryset(self):
        queryset = self.request.user.categories.filter(is_active=True)
        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class CategoryView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "categories/category.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    login_url = "users:login"

    def get_queryset(self):
        return self.request.user.categories.all()


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "categories/create.html"
    form_class = CategoryForm
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("categories:list")
    login_url = "users;login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "categories/update.html"
    form_class = CategoryForm
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("categories:list")
    login_url = "users:login"

    def get_queryset(self):
        return self.request.user.categories.all()


class CategoryDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, user=request.user, slug=kwargs["slug"])
        template_name = "categories/confirm_delete.html"
        context = {"category": category}

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        category = get_object_or_404(Category, user=request.user, slug=kwargs["slug"])

        category.is_active = False
        category.save(update_fields=["is_active"])

        return redirect("categories:list")
