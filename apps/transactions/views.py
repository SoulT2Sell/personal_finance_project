from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.urls import reverse_lazy

from apps.transactions.models import Transaction
from apps.transactions.forms import TransactionForm
from apps.transactions.choices import TransactionType
from apps.common.models import Currency

from services.transaction_service import TransactionService

# Create your views here.
# Transaction Views
class TransactionsView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transactions/transactions.html"
    context_object_name = "transactions"
    login_url = "users:login"

    def get_queryset(self):
        queryset = self.request.user.transactions.filter(is_active=True)

        account = self.request.GET.get("account")
        category = self.request.GET.get("category")
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        amount_min = self.request.GET.get("amount_min")
        amount_max = self.request.GET.get("amount_max")
        transaction_type = self.request.GET.get("transaction_type")
        currency = self.request.GET.get("currency")

        if account:
            queryset = queryset.filter(account=account)

        if category:
            queryset = queryset.filter(category=category)

        if date_from:
            queryset = queryset.filter(transaction_date__gte=date_from)

        if date_to:
            queryset = queryset.filter(transaction_date__lte=date_to)

        if amount_min:
            queryset = queryset.filter(amount__gte=amount_min)

        if amount_max:
            queryset = queryset.filter(amount__lte=amount_max)

        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        if currency:
            queryset = queryset.filter(account__currency=currency)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["accounts"] = self.request.user.accounts.filter(is_active=True)
        context["categories"] = self.request.user.categories.filter(is_active=True)
        context["currencies"] = Currency.objects.filter(is_active=True)
        context["transaction_types"] = TransactionType.choices

        return context

class TransactionView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "transactions/transaction.html"
    context_object_name = "transaction"
    login_url = "users:login"

    def get_queryset(self):
        return self.request.user.transactions.all()

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = "transactions/create.html"
    form_class = TransactionForm
    login_url = "users:login"
    success_url = reverse_lazy("transactions:list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user

        try:
            self.object = TransactionService.create(
                transaction_obj=form.instance
            )
            messages.success(self.request, "گردش حساب با موفقیت ساخته شد")
            return redirect("transactions:list")
        except Exception as ex:
            form.add_error(None, f"خطا در ساخت گردش حساب : {str(ex)}")
            return self.form_invalid(form)

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    template_name = "transactions/update.html"
    form_class = TransactionForm
    login_url = "users;login"
    success_url = reverse_lazy("transactions:detail")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        return self.request.user.transactions.filter(is_active=True)

    def form_valid(self, form):
        try:
            self.object = TransactionService.update(transaction_obj=form.instance)
            messages.success(self.request, "تراکنش با موفقیت ویرایش شد")
            return redirect("transactions:detail", self.object.pk)
        except Exception as ex:
            form.add_error(None, f"خطا در ویرایش تراکنش : {str(ex)}")
            return self.form_invalid(form)

class TransactionDeleteView(LoginRequiredMixin, View):
    template_name = "transactions/confirm_delete.html"

    def get(self, request, *args, **kwargs):
        transaction = get_object_or_404(Transaction, user=request.user, id=kwargs["pk"])
        context = {"transaction": transaction}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        transaction = get_object_or_404(Transaction, user=request.user, id=kwargs["pk"])
        context = {"transaction": transaction}

        try:      
            TransactionService.deactivate(transaction_obj=transaction)
            messages.success(request, "تراکنش با موفقیت حذف شد")
            return redirect("transactions:list")
        except Exception as ex:
            messages.error(request, str(ex))
            return render(request, self.template_name, context)