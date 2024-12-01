from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app/", include("app.urls")),
    path("accounts/", include("allauth.urls")),
]


handler404 = "app.views.redirect_to_login"
