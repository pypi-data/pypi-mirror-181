from datetime import datetime, timedelta, timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_twilio_2fa.utils import *
from django.contrib import messages


class Require2faMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def is_2fa_required(self, request):
        if not request.user.is_authenticated:
            return False

        if request.session.get("twilio_2fa_verification", False):
            return False

        if request.user.is_superuser:
            return False

        return True

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (
            "static" in request.path or
            (request.resolver_match and URL_PREFIX in request.resolver_match.view_name) or
            "utility" in request.path
        ):
            return

        if self.is_2fa_required(request):
            next_url = reverse(
                request.resolver_match.view_name,
                kwargs=view_kwargs,
                args=view_args
            )
            return HttpResponseRedirect(
                f"{reverse(f'{URL_PREFIX}:start')}?next={next_url}"
            )
