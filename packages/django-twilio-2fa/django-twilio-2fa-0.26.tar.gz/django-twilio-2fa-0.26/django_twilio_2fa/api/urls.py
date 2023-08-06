from django.urls import path
from .views import SendView, VerifyView, CancelView, MethodsView, SetEmailView, SetPhoneNumberView


app_name = "twilio_2fa_api"


urlpatterns = [
    path(
        "send",
        SendView.as_view(),
        name="send"
    ),
    path(
        "verify",
        VerifyView.as_view(),
        name="verify"
    ),
    path(
        "cancel",
        CancelView.as_view(),
        name="cancel"
    ),
    path(
        "verification-methods",
        MethodsView.as_view(),
        name="methods"
    ),
    path(
        "set-email",
        SetEmailView.as_view(),
        name="set_email"
    ),
    path(
        "set-phone-number",
        SetPhoneNumberView.as_view(),
        name="set_phone_number"
    ),
]
