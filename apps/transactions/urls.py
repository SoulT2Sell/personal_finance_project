from django.urls import path

from apps.transactions.views import TransactionsView, TransactionView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView

app_name = "apps.transactions"

urlpatterns = [
    path("", TransactionsView.as_view(), name="list"),
    path("create/", TransactionCreateView.as_view(), name="create"),
    path("<uuid:pk>/", TransactionView.as_view(), name="detail"),
    path("<uuid:pk>/update", TransactionUpdateView.as_view(), name="edit"),
    path("<uuid:pk>/delete", TransactionDeleteView.as_view(), name="delete"),
]
