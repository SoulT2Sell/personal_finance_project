from django.views.generic import TemplateView
from django.shortcuts import render, redirect

# Create your views here.

class HomeView(TemplateView):
    template_name = "common/home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:home")
        return super().get(request, *args, **kwargs)
