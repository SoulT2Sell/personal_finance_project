from django.urls import path

from apps.dashboard.views import DashboardView

app_name = "apps.dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="home")
]
