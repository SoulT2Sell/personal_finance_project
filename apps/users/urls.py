from django.contrib import admin
from django.urls import path

from apps.users.views import UserSignupView, UserLoginView, UserLogoutView, UserProfileView, UserProfileUpdateView

app_name = "apps.users"

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile", UserProfileView.as_view(), name="profile"),
    path("profile/edit", UserProfileUpdateView.as_view(), name="profile_edit") 
]
