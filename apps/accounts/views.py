from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, CreateView, UpdateView, DetailView
from django.views import View

from apps.accounts.forms import AccountForm
from apps.accounts.models import Account

# Create your views here.
class AccountsView(LoginRequiredMixin, ListView):
    model = Account
    template_name = "accounts/accounts.html"
    context_object_name = "accounts"

    def get_queryset(self):
        return self.request.user.accounts.all()

class AccountView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = "accounts/account.html"
    context_object_name = "account"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return self.request.user.accounts.all()

