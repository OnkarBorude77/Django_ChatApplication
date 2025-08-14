from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),               # logged-in landing
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("public/", views.home_public, name="home_public"),
]
