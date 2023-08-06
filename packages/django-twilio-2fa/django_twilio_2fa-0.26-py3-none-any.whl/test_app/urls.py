"""test_app URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from .users.views import index_view


# Utility views

def utility_clear_session(request, *args, **kwargs):
    request.session["twilio_2fa_verification"] = False
    return HttpResponse("Session cleared!")


def utility_clear_mfa(request, *args, **kwargs):
    request.user.profile.phone_number = None
    request.user.profile.last_2fa_attempt = None
    request.user.profile.timeout_for_2fa = None
    request.user.profile.save()

    return HttpResponse("MFA cleared!")


urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),
    path(
        "2fa/",
        include("django_twilio_2fa.urls")
    ),
    path(
        "api/",
        include("django_twilio_2fa.api.urls")
    ),
    path(
        "utility/clear_session",
        utility_clear_session
    ),
    path(
        "utility/clear_mfa",
        utility_clear_mfa
    ),
    path(
        "",
        index_view,
        name="index"
    )
]
