from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class PersianAdminSite(AdminSite):
    site_header = _("پنل مدیریت دفتر مالی")
    site_title = _("مدیریت دفتر مالی")
    index_title = _("خوش آمدید به پنل مدیریت")
    site_url = "/"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        persian_names = {
            "Users": "کاربران",
            "Accounts": "حساب‌ها",
            "Categories": "کتگوری‌ها",
            "Transactions": "تراکنش‌ها",
            "Common": "پایه",
            "Dashboard": "داشبورد",
        }
        for app in app_list:
            if app["name"] in persian_names:
                app["name"] = persian_names[app["name"]]
            for model in app["models"]:
                if model["object_name"] in persian_names:
                    model["name"] = persian_names[model["object_name"]]
        return app_list


persian_admin_site = PersianAdminSite(name="persian_admin")

# Register models with the custom admin site
from apps.users.models import User, UserProfile
from apps.accounts.models import Account, AccountType
from apps.categories.models import Category
from apps.transactions.models import Transaction
from apps.common.models import Currency, ExchangeRate
from apps.users.admin import UserAdmin, UserProfileAdmin
from apps.accounts.admin import AccountAdmin, AccountTypeAdmin
from apps.categories.admin import CategoryAdmin
from apps.transactions.admin import TransactionAdmin
from apps.common.admin import CurrencyAdmin, ExchangeRateAdmin

persian_admin_site.register(User, UserAdmin)
persian_admin_site.register(UserProfile, UserProfileAdmin)
persian_admin_site.register(Account, AccountAdmin)
persian_admin_site.register(AccountType, AccountTypeAdmin)
persian_admin_site.register(Category, CategoryAdmin)
persian_admin_site.register(Transaction, TransactionAdmin)
persian_admin_site.register(Currency, CurrencyAdmin)
persian_admin_site.register(ExchangeRate, ExchangeRateAdmin)