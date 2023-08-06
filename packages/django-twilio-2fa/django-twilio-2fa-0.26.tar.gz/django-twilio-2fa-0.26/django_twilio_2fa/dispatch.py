import django.dispatch


__all__ = [
    "twilio_2fa_verification_sent", "twilio_2fa_verification_success", "twilio_2fa_verification_status_changed",
    "twilio_2fa_verification_failed", "twilio_2fa_set_user_data", "twilio_2fa_twilio_error",
]


twilio_2fa_verification_sent = django.dispatch.Signal()

twilio_2fa_verification_success = django.dispatch.Signal()

twilio_2fa_verification_status_changed = django.dispatch.Signal()

twilio_2fa_verification_failed = django.dispatch.Signal()

twilio_2fa_set_user_data = django.dispatch.Signal()

twilio_2fa_twilio_error = django.dispatch.Signal()
