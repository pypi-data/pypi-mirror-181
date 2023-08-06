import logging
from datetime import datetime, timedelta
from django.dispatch import receiver
from django_twilio_2fa.dispatch import *
from django.contrib.auth.signals import user_logged_in


logger = logging.getLogger("django_twilio_2fa")


@receiver(twilio_2fa_verification_success, sender=None)
def handle_2fa_success(signal, request, user, **kwargs):
    logger.debug("twilio_2fa_verification_success signal received")

    if not user:
        return

    user.profile.last_2fa_attempt = datetime.now()
    user.profile.save()

    request.session["twilio_2fa_verification"] = True



@receiver(twilio_2fa_set_user_data, sender=None)
def handle_2fa_data_set(signal, request, user, field, value, **kwargs):
    logger.debug("twilio_2fa_set_user_data signal received")

    if field == "phone_number":
        user.profile.phone_number = value.e164_format
        user.profile.phone_carrier_type = value.carrier_type
        user.profile.save()
    else:
        user.email = str(value)
        user.save()


@receiver(twilio_2fa_twilio_error, sender=None)
def twilio_error_log(sender, *args, **kwargs):
    logger.debug("twilio_2fa_twilio_error signal received")


@receiver(twilio_2fa_verification_failed, sender=None)
def twilio_error_log(sender, *args, **kwargs):
    logger.debug("twilio_2fa_verification_failed signal received")


@receiver(twilio_2fa_verification_status_changed, sender=None)
def twilio_error_log(sender, *args, **kwargs):
    logger.debug("twilio_2fa_status_changed signal received")


@receiver(twilio_2fa_verification_sent, sender=None)
def twilio_error_log(sender, *args, **kwargs):
    logger.debug("twilio_2fa_verification_sent signal received")
