import sys
import inspect
from django.utils.translation import gettext_lazy as _
from .app_settings import conf


def get_error_details():
    details = {}

    for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if name == "Error" or not issubclass(obj, Error):
            continue

        details[obj.code] = {
            "obj": obj,
            "name": name,
            "code": obj().get_code(),
            "display": obj().get_display(),
            "status_code": obj.status_code,
            "blocking": obj.blocking
        }

    return details


class Error(Exception):
    code = None
    display = None
    status_code = 500
    blocking = False

    def __init__(self, display=None, **data):
        self.data = data

        if display:
            self.display = display
        else:
            display = conf.error_displays().get(self.code)

            if display:
                self.display = display

        if not self.display:
            self.display = conf.default_error_display()

    def get_code(self):
        try:
            return self.code.format(**self.data)
        except KeyError:
            return self.code

    def get_display(self):
        try:
            return self.display.format(**self.data)
        except KeyError:
            return self.display

    def get_json(self):
        return {
            "success": False,
            "error_code": self.get_code(),
            "display": self.get_display(),
            "data": self.data,
            "blocking": self.blocking
        }


class UserNotAllowed(Error):
    code = "user_not_allowed"
    display = _("You are not allowed to verify at this time")
    status_code = 403


class MethodNotAllowed(Error):
    code = "method_not_allowed"
    display = _("The method {method} selected cannot be used at this time")
    status_code = 400


class PhoneCountryNotAllowed(Error):
    code = "phone_country_not_allowed"
    display = _("We do not allow phone numbers originating from {country_code}")
    status_code = 400


class InvalidPhoneNumber(Error):
    code = "invalid_phone_number"
    display = _("Invalid phone number")
    status_code = 400


class InvalidCarrierType(Error):
    code = "invalid_carrier_type"
    display = _("{carrier_type} phone numbers are not allowed")
    status_code = 400


class VerificationNotFound(Error):
    code = "verification_not_found"
    status_code = 404


class TwilioRateLimited(Error):
    code = "twilio_rate_limited"


class GenericTwilioError(Error):
    code = "twilio_error_{twilio_error}"


class UserUnauthenticated(Error):
    code = "user_unauthenticated"
    display = _("You must be logged in")
    status_code = 401


class UnauthenticatedUserFieldMissing(Error):
    code = "unauthenticated_user_field_missing"


class UnauthenticatedUserParamMissing(Error):
    code = "unauthenticated_user_param_missing"
    status_code = 400


class UserNotFound(Error):
    code = "user_not_found"
    status_code = 404


class BadUserData(Error):
    code = "bad_user_data"
    status_code = 400


class MissingUserData(Error):
    code = "missing_user_data"
    status_code = 404


class MaxAttemptsReached(Error):
    code = "max_attempts_reached"
    status_code = 400


class MaxSendsReached(Error):
    code = "max_sends_reached"
    status_code = 400


class MobileNumberRequired(Error):
    code = "mobile_number_required"
    display = _("To use {method_label}, you must have a mobile number")
    status_code = 400


class SendCooldown(Error):
    code = "resend_cooldown"
    display = _("Please wait before resending your verification")


class EmailNotSet(Error):
    code = "email_not_set"
    display = _("An e-mail address is not set for your account.")


class PhoneNumberNotSet(Error):
    code = "phone_not_set"
    display = _("A phone number is not set for your account.")


class MalformedRequest(Error):
    code = "malformed_request"
    status_code = 400


class UserCannotVerify(Error):
    code = "user_cannot_verify"
    status_code = 401
    display = _("You cannot verify at this time.")
    blocking = True


class NoMethodAvailable(Error):
    code = "no_method_available"
    display = _("No method available for verification")
    blocking = True


class UserRequired(Error):
    code = "user_required"
    display = _("A user is required for 2FA")
    blocking = True


class ChangeNotAllowed(Error):
    code = "change_not_allowed"
    display = _("You cannot change your {field_display}")


class RegistrationNotAllowed(Error):
    code = "registration_not_allowed"
    display = _("You cannot set your 2FA {field_display}")


class TwilioInvalidParameter(Error):
    code = "twilio_invalid_parameter_{parameter}"
    status_code = 400
    blocking = False


class InvalidVerificationCode(TwilioInvalidParameter):
    code = "invalid_verification_code"
    display = _("Verification code is invalid")
