from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),         
    path("", include("users.urls")),         
    path("", include("chat.urls")),          
    path("", RedirectView.as_view(pattern_name="home", permanent=False)),
]
 