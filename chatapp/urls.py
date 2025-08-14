from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),         # keep Django's admin login for superusers
    path("", include("users.urls")),         # signup/login/logout + home routes
    path("", include("chat.urls")),          # chat routes
    path("", RedirectView.as_view(pattern_name="home", permanent=False)),
]
