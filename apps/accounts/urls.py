from django.urls import path

from apps.accounts.views import AccountsView, AccountView, AccountCreateView, AccountUpdateView, AccountDeleteView

app_name = "apps.accounts"

urlpatterns = [
    path("", AccountsView.as_view(), name="list"),
    path("create/", AccountCreateView.as_view(), name="create"),
    path("<slug:slug>/", AccountView.as_view(), name="detail"),
    path("<slug:slug>/edit", AccountUpdateView.as_view(), name="edit"),
    path("<slug:slug>/delete", AccountDeleteView.as_view(), name="delete")
]
