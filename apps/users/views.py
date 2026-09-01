from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic import FormView, TemplateView
from django.views import View
from django.urls import reverse_lazy

from apps.users.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
class UserSignupView(FormView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = 'users:profile'

class UserLogoutView(LogoutView):
    next_page = 'users:login'

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = 'users:login'

class UserProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'users/profile_edit.html'
    login_url = 'users:login'

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile')

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, self.template_name, context)

