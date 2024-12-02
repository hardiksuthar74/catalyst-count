from django.contrib import admin
from django.urls import path, include

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def goToLogin(request):
    return redirect('/app/company')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("app/", include("app.urls")),
    path("accounts/", include("allauth.urls")),
    path("", goToLogin),
]
