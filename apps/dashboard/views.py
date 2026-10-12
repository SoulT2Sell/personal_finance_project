from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from services.dashboard_service import DashboardService


# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"
    login_url = "users:login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        dashboard_context = DashboardService.get_dashboard_context(user)
        context.update(dashboard_context)
        return context
