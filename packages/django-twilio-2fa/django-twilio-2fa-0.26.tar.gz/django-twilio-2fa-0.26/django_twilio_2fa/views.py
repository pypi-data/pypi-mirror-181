import logging
import json
from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
import phonenumbers
from .forms import *
from .utils import *

from .client import TwoFAClient
from .errors import *


__all__ = [
    "Twilio2FARegisterView", "Twilio2FAChangeView", "Twilio2FAStartView", "Twilio2FAVerifyView",
    "Twilio2FASuccessView", "Twilio2FAFailedView",
]


logger = logging.getLogger("django_twilio_2fa")


class Twilio2FAMixin(object):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.twofa_client = TwoFAClient(
            request=request
        )

        if request.GET.get("next"):
            request.session[conf.next_session_key()] = request.GET.get("next")

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Error as e:
            error = e.get_json()
            del error["data"]  # Remove data for security
            error = json.dumps(error)

            return HttpResponseRedirect(
                f"{reverse('twilio_2fa:failed')}?e={urlsafe_b64encode(error.encode()).decode()}"
            )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if settings.DEBUG:
            ctx["debug"] = self.twofa_client.session._to_dict()
            ctx["debug"].update({
                "resend_in": self.twofa_client.can_resend_verification_in(),
                "expires_in": self.twofa_client.verification_expires_in()
            })

        return ctx

    def get_redirect(self, view_name, *args, **kwargs):
        logger.debug(f"Redirecting to: {view_name}")
        return HttpResponseRedirect(
            reverse(f"{URL_PREFIX}:{view_name}", args=args, kwargs=kwargs)
        )


class Twilio2FARegistrationFormView(Twilio2FAMixin, FormView):
    form_class = Twilio2FARegistrationForm
    success_url = reverse_lazy("twilio_2fa:start")
    template_name = "twilio_2fa/register.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["is_optional"] = get_setting(
            "REGISTER_OPTIONAL",
            default=False
        )
        ctx["skip_href"] = get_setting(
            "REGISTER_OPTIONAL_URL",
            default="javascript:history.back()"
        )

        return ctx

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        self.twofa_client.set_user_data(
            "phone_number",
            phone_number=cleaned_data["phone_number"],
            country_code=cleaned_data["country_code"]
        )

        return super().form_valid(form)


class Twilio2FARegisterView(Twilio2FARegistrationFormView):
    template_name = "twilio_2fa/register.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["is_optional"] = get_setting(
            "REGISTER_OPTIONAL",
            default=False
        )
        ctx["skip_href"] = get_setting(
            "REGISTER_OPTIONAL_URL",
            default="javascript:history.back()"
        )

        return ctx

    def get(self, request, *args, **kwargs):
        if self.twofa_client.get_phone_number() is not None:
            return self.get_redirect(
                "change"
            )

        return super().get(request, *args, **kwargs)


class Twilio2FAChangeView(Twilio2FARegistrationFormView):
    template_name = "twilio_2fa/change.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        self.twofa_client.is_set_data_allowed("phone_number")

        ctx["is_optional"] = False
        ctx["skip_href"] = None

        return ctx


class Twilio2FAStartView(Twilio2FAMixin, TemplateView):
    success_url = reverse_lazy("twilio_2fa:verify")
    template_name = "twilio_2fa/start.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.user_methods = self.twofa_client.get_verification_methods()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["methods"] = self.user_methods
        ctx["phone_number"] = self.twofa_client.get_phone_number().obfuscated if self.twofa_client.get_phone_number() else ""
        ctx["email"] = self.twofa_client.get_email().obfuscated if self.twofa_client.get_email() else ""

        return ctx

    def get(self, request, *args, **kwargs):
        if not self.twofa_client.get_phone_number() and (
                not self.twofa_client.is_method_allowed("email") or conf.user_must_have_phone()
        ):
            return self.get_redirect(
                "register"
            )

        if not len(self.user_methods):
            raise NoMethodAvailable()

        clear_session = request.GET.get("c")

        if clear_session:
            self.twofa_client.session.clear()

        if self.twofa_client.verification_expires_in() > 0:
            # Verification hasn't expired
            if self.twofa_client.can_resend_verification_in() <= 0:
                # Resend verification
                self.twofa_client.send_verification(
                    self.twofa_client.session["verification_method"]
                )
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Verification has been resent")
                )
            else:
                # Cooldown not met
                messages.add_message(
                    request,
                    messages.WARNING,
                    _("Please wait before resending verification")
                )

            return HttpResponseRedirect(
                self.success_url
            )


        if len(self.user_methods) == 1 and conf.send_immediately_on_single():
            # If only one option exists, we start the verification and send the user on
            self.twofa_client.send_verification(
                list(self.user_methods.keys())[0]
            )
            return HttpResponseRedirect(
                self.success_url
            )

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        method = request.POST.get("method")

        self.twofa_client.send_verification(method)

        return HttpResponseRedirect(
            self.success_url
        )


class Twilio2FAVerifyView(Twilio2FAMixin, FormView):
    form_class = Twilio2FAVerifyForm
    success_url = reverse_lazy("twilio_2fa:success")
    template_name = "twilio_2fa/verify.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["method"] = self.twofa_client.session["verification_method"]
        ctx["obfuscated_value"] = self.twofa_client.session["send_to_display"]

        return ctx

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        verified = self.twofa_client.check_verification(
            code=cleaned_data["token"]
        )

        if not verified:
            form.add_error(
                None,
                _("Your verification code is not correct")
            )
            return super().form_invalid(form)

        return super().form_valid(form)


class Twilio2FASuccessView(Twilio2FAMixin, TemplateView):
    template_name = "twilio_2fa/success.html"

    def get(self, request, *args, **kwargs):
        success_redirect_url = request.session.get(
            conf.next_session_key(),
            conf.success_redirect_url(
                user=self.twofa_client.get_user()
            )
        )

        if success_redirect_url:
            return HttpResponseRedirect(
                success_redirect_url
            )

        return super().get(request, *args, **kwargs)


class Twilio2FAFailedView(TemplateView):
    template_name = "twilio_2fa/failed.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        error = json.loads(urlsafe_b64decode(request.GET.get("e")).decode())

        self.error_code = error.get("error_code", "")
        self.error_display = error.get("display", conf.default_error_display())
        self.verification_id = request.GET.get("v")

        self.error_blocking = error.get("blocking", False)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx.update({
            "error_code": self.error_code,
            "error_display": self.error_display,
            "is_blocking": self.error_blocking,
            "verification_id": self.verification_id
        })

        return ctx
