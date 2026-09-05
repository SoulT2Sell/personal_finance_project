from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from apps.accounts.forms import AccountForm
from apps.accounts.models import Account, AccountType


# Create your views here.
class AccountsView(LoginRequiredMixin, ListView):
    model = Account
    template_name = "accounts/accounts.html"
    context_object_name = "accounts"
    login_url = "users:login"

    def get_queryset(self):
        queryset = self.request.user.accounts.filter(is_active=True)
        search = self.request.GET.get("search")
        account_type = self.request.GET.get("account_type")
        currency = self.request.GET.get("currency")

        if search:
            queryset = queryset.filter(name__icontains=search)

        if account_type:
            queryset = queryset.filter(account_type=account_type)

        if currency:
            queryset = queryset.filter(currency=currency)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["account_types"] = AccountType.objects.all()
        context["currencies"] = self.request.user.accounts.values_list(
            "currency", flat=True
        ).distinct()

        return context


class AccountView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = "accounts/account.html"
    context_object_name = "account"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    login_url = "users:login"

    def get_queryset(self):
        return self.request.user.accounts.all()


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    template_name = "accounts/create.html"
    form_class = AccountForm
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("accounts:list")
    login_url = "users:login"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = "accounts/update.html"
    form_class = AccountForm
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("accounts:list")
    login_url = "users:login"

    def get_queryset(self):
        return self.request.user.accounts.all()


class AccountDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        account = get_object_or_404(Account, user=request.user, slug=kwargs["slug"])
        template_name = "accounts/confirm_delete.html"
        context = {"account": account}
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        account = get_object_or_404(Account, user=request.user, slug=kwargs["slug"])

        account.is_active = False
        account.save(update_fields=["is_active"])

        return redirect("accounts:list")
