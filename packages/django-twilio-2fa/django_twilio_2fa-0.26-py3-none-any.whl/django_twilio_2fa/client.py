import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException
import phonenumbers
import pycountry

from .app_settings import conf
from .errors import *
from .options import Email, PhoneNumber
from .session import TwoFASession
from .utils import get_twilio_client
from .dispatch import *


logger = logging.getLogger("django_twilio_2fa")

User = get_user_model()


class TwoFAClient(object):
    send_signals = True

    def __init__(
            self,
            request=None,
            user=None,
            email=None,
            phone_number=None
    ):
        self.request = request
        self.user = self.get_user(user)
        self.email = self.get_email(email)
        self.phone_number = self.get_phone_number(phone_number)

        self.session = TwoFASession(self.request)

    @classmethod
    def get_twilio_client(cls, account_sid, auth_token, **kwargs):
        """
        Return an instance of TwilioClient
        """
        if not account_sid:
            account_sid = conf.twilio_account_sid

        if not auth_token:
            auth_token = conf.twilio_auth_token

        return TwilioClient(account_sid, auth_token, **kwargs)

    def get_user(self, user=None):
        """
        Returns a User instance
        """
        if hasattr(self, "user"):
            return self.user

        if user:
            self.user = user
        elif self.request.user.is_authenticated:
            self.user = self.request.user
        elif not conf.allow_unauthenticated_users():
            raise UserUnauthenticated()
        else:
            if not hasattr(self.request, "user"):
                if not conf.allow_userless():
                    raise UserRequired()
                else:
                    self.user = None
                    return
            
            query_param = conf.unauthenticated_query_param()
            user_id = self.request.data.get(query_param)
            user_field = conf.unauthenticated_user_field()

            if not user_id:
                if not conf.allow_userless():
                    raise UnauthenticatedUserParamMissing(
                        query_param=query_param
                    )
                else:
                    self.user = None
                    return

            if not hasattr(User, user_field):
                raise UnauthenticatedUserFieldMissing()

            try:
                self.user = User.objects.get(**{
                    user_field: user_id
                })
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                raise UserNotFound(
                    user_id=user_id,
                    user_field=user_field,
                    query_param=query_param
                )

        return self.user

    def get_phone_number(self, phone_number=None):
        if hasattr(self, "phone_number"):
            return self.phone_number

        if phone_number:
            self.phone_number = phone_number
        elif self.user:
            self.phone_number = conf.user_phone_number(
                user=self.user
            )

        if not hasattr(self, "phone_number") or self.phone_number is None:
            self.phone_number = None
            return

        if self.phone_number:
            if not isinstance(self.phone_number, PhoneNumber):
                raise BadUserData(
                    data="phone_number",
                    additional_info="UserPhoneNumber instance must be passed for user_phone_number"
                )

            if not isinstance(self.phone_number.phone_number, phonenumbers.PhoneNumber):
                self.phone_number.parse_phone_number()

        return self.phone_number

    def get_email(self, email=None):
        if hasattr(self, "email"):
            return self.email

        if email:
            self.email = email
        elif self.user:
            self.email = conf.user_email(
                user=self.user
            )

        if not hasattr(self, "email"):
            self.email = None
            return

        if self.email and not isinstance(self.email, Email):
            raise BadUserData(
                data="email",
                additional_info="Email instance must be passed"
            )

        return self.email

    def get_method_details(self, method):
        details = conf.available_methods().get(method, {})
        override = conf.method_details().get(method, {})

        for key in ["icon", "label"]:
            if key not in override:
                continue

            details[key] = override[key]

        return details

    @classmethod
    def allowed_country_codes(cls):
        return list(set(conf.allowed_countries()) - set(conf.disallowed_countries()))

    @classmethod
    def is_country_allowed(cls, country_code):
        return country_code in cls.allowed_country_codes()

    def get_verification_sid(self, verification_sid=None):
        verification_sid = verification_sid or self.session["verification_sid"]

        if not verification_sid:
            raise VerificationNotFound()

        return verification_sid

    def set_email(self, email):
        if not email:
            raise MissingUserData(
                field="email"
            )

        self.email = Email(
            email=email
        )
        return self.email

    def set_phone_number(self, phone_number, country_code):
        self.phone_number = self.check_phone_number(phone_number, country_code)
        return self.phone_number

    @classmethod
    def check_phone_number(cls, phone_number, country_code):
        """
        Check a phone number and return UserPhoneNumber object
        """
        if not phone_number:
            raise MissingUserData(
                field="phone_number"
            )

        if not country_code:
            raise MissingUserData(
                field="country_code"
            )

        if not cls.is_country_allowed(country_code):
            raise PhoneCountryNotAllowed(
                country_code=country_code
            )

        obj = PhoneNumber(
            phone_number=phone_number,
            country_code=country_code
        )

        obj.parse_phone_number()

        if conf.do_carrier_lookup() and (
            # Canada requires permission from CLNPC for carrier lookups
            # See https://support.twilio.com/hc/en-us/articles/360004563433
            country_code != "CA" or
            (country_code == "CA" and conf.has_clnpc_permission())
        ):
            obj.country_code, obj.carrier_type = cls.do_carrier_lookup(obj)

            if not cls.is_country_allowed(obj.country_code):
                raise PhoneCountryNotAllowed(
                    country_code=obj.country_code
                )

            # FIXME: Make sure this is the right response for no carrier type
            if not obj.carrier_type and not conf.bypass_carrier_on_empty():
                raise InvalidCarrierType(
                    carrier_type=obj.carrier_type
                )

        return obj

    def send_signal(self, signal, **data):
        data.update({
            "request": self.request,
            "user": self.get_user(),
        })

        if not self.send_signals:
            return

        signal.send(None, **data)

    def verification_expires_in(self):
        """
        Returns seconds before verification expires
        """
        if not self.session["start_timestamp"]:
            return 0

        expiration = self.session["start_timestamp"] + timedelta(minutes=conf.verification_expiration())

        return int((expiration - timezone.now()).total_seconds())

    def can_resend_verification_in(self):
        """
        Returns seconds before a verification can be resent
        """
        if not self.session["last_send_timestamp"]:
            return -1

        return int(conf.send_cooldown() - (timezone.now() - self.session["last_send_timestamp"]).total_seconds())

    def can_user_verify(self):
        return conf.allow_user_to_verify(
            user=self.get_user()
        )

    def is_method_allowed(self, method):
        return method in conf.allowed_methods()

    def get_verification_methods(self):
        methods = {}

        methods_allowed_for_user = conf.user_methods(
            user=self.get_user()
        )

        for method_name in conf.allowed_methods():
            method_details = self.get_method_details(method_name)

            if method_name not in conf.available_methods():
                continue

            if methods_allowed_for_user and method_name not in methods_allowed_for_user:
                continue

            if method_details.get("data_required") == "phone_number":
                if not self.get_phone_number():
                    continue

                if (
                        method_details.get("carrier_required") and
                        self.get_phone_number().carrier_type != method_details.get("carrier_required", "")
                ):
                    continue
            elif method_details.get("data_required") == "email" and not self.get_email():
                continue

            methods[method_name] = method_details

        return methods

    def get_success_redirect_url(self, url=None):
        return url or self.session["success_redirect_url"] or conf.success_redirect_url(user=self.get_user())

    def is_set_data_allowed(self, field, raise_exc=True):
        if field == "email":
            field_display = _("e-mail address")
        else:
            field_display = _("phone number")

        if getattr(self, f"get_{field}")() is not None and not conf.allow_change(field=field, user=self.get_user()):
            if raise_exc:
                raise ChangeNotAllowed(
                    field=field,
                    field_display=field_display
                )
            return False
        elif not conf.allow_registration(field=field, user=self.get_user()):
            if raise_exc:
                raise RegistrationNotAllowed(
                    field=field,
                    field_display=field_display
                )
            return False

        return True

    def set_user_data(self, field, **values):
        if field not in ["email", "phone_number"]:
            raise KeyError(f"User data field must be email or phone_number, not {field}")

        if not self.get_user():
            raise UserNotFound()

        self.is_set_data_allowed(field)

        value = getattr(self, f"set_{field}")(**values)

        self.send_signal(
            twilio_2fa_set_user_data,
            field=field,
            value=value
        )

    #
    # Twilio calls

    @classmethod
    def handle_twilio_error(cls, exc):
        twilio_2fa_twilio_error.send(
            None,
            exc=exc
        )

        if exc.code == 20404:
            # Verification not found
            raise VerificationNotFound()
        elif exc.code == 20429:
            # Rate limited by Twilio
            raise TwilioRateLimited()
        elif exc.code == 60202:
            # Max retries
            raise MaxAttemptsReached()
        elif exc.code == 60203:
            # Max resends
            raise MaxSendsReached()
        elif exc.code == 60223:
            # Method not allowed
            raise MethodNotAllowed()
        elif exc.code == 60200:
            # Invalid Parameter
            if "Code" in exc.msg:
                raise InvalidVerificationCode()
            else:
                raise TwilioInvalidParameter(parameter=exc.msg.split(": ")[1])
        else:
            logger.exception(exc)
            raise GenericTwilioError(
                twilio_error=exc.code
            )

    @classmethod
    def do_carrier_lookup(cls, phone_number):
        try:
            response = (
                get_twilio_client().lookups
                    .phone_numbers(phone_number.e164_format)
                    .fetch(type=["carrier"])
            )
        except TwilioRestException as e:
            raise cls.handle_twilio_error(e)

        return response.country_code, response.carrier.get("type")

    def send_verification(self, method, send_to=None, **kwargs):
        self.get_user()

        if not send_to:
            method_details = self.get_method_details(method)

            if method_details.get("data_required") == "phone_number":
                phone_number = self.get_phone_number()

                if not phone_number:
                    raise PhoneNumberNotSet()

                if (
                        method_details.get("carrier_required") and
                        self.get_phone_number().carrier_type != method_details.get("carrier_required", "")
                ):
                    raise MobileNumberRequired(
                        method=method,
                        method_label=self.get_method_details(method).get("label", _("this method"))
                    )

                send_to = str(phone_number)
            elif method_details.get("data_required") == "email":
                email = self.get_email()
                if not email:
                    raise EmailNotSet()
                send_to = str(email)

        if method not in self.get_verification_methods():
            raise MethodNotAllowed(
                method=method
            )

        if self.verification_expires_in() > 0 < self.can_resend_verification_in():
            # Resend verification attempt before cooldown ends
            raise SendCooldown()

        try:
            verification = (get_twilio_client().verify
                .services(conf.twilio_service_id())
                .verifications
                .create(
                    to=send_to,
                    channel=method,
                    custom_friendly_name=conf.twilio_service_name(
                        request=self.request
                    )
                )
            )

            if self.session["verification_sid"] != verification.sid:
                # New verification
                self.session.clear()
                self.session["verification_sid"] = verification.sid
                self.session["verification_method"] = method
                self.session["start_timestamp"] = timezone.now()
                self.session["last_send_timestamp"] = timezone.now()
                self.session["sends"] = 1
            else:
                # Resend
                self.session["last_send_timestamp"] = timezone.now()
                self.session["sends"] += 1

            self.session["send_to_value"] = send_to

            if method == "email":
                self.session["send_to_display"] = self.get_email().obfuscated
            else:
                self.session["send_to_display"] = self.get_phone_number().obfuscated

            self.send_signal(
                twilio_2fa_verification_sent,
                method=method,
                verification_sid=self.session["verification_sid"],
                start_timestamp=self.session["start_timestamp"],
                last_send_timestamp=self.session["last_send_timestamp"]
            )

            return verification.sid
        except TwilioRestException as e:
            raise self.handle_twilio_error(e)

    def check_verification(self, code, verification_sid=None):
        verification_sid = self.get_verification_sid(verification_sid)

        try:
            verification = (get_twilio_client().verify
                .services(conf.twilio_service_id())
                .verification_checks
                .create(
                    verification_sid=verification_sid,
                    code=code
                )
            )
        except TwilioRestException as e:
            raise self.handle_twilio_error(e)

        verified = verification.status == "approved"

        if verified:
            # Send this signal manually
            self.send_signal(
                twilio_2fa_verification_status_changed,
                status="approved",
                verification_sid=verification_sid
            )

            self.send_signal(
                twilio_2fa_verification_success,
                verification_sid=verification_sid
            )

            self.session.clear()

            return True

        self.send_signal(
            twilio_2fa_verification_failed,
            verification_sid=verification_sid
        )

        self.session["attempts"] += 1
        self.session["last_check_timestamp"] = timezone.now()

        return False

    def approve_verification(self, verification_sid=None):
        return self.update_verification_status(
            status="approved",
            verification_sid=verification_sid
        )

    def cancel_verification(self, verification_sid=None):
        ret = self.update_verification_status(
            status="canceled",
            verification_sid=verification_sid
        )

        if ret:
            self.session.clear()

        return ret

    def update_verification_status(self, status, verification_sid=None):
        verification_sid = self.get_verification_sid(verification_sid)

        if not verification_sid:
            raise VerificationNotFound()

        try:
            (get_twilio_client().verify
                .services(conf.twilio_service_id())
                .verifications(verification_sid)
                .update(status=status)
             )

            self.send_signal(
                twilio_2fa_verification_status_changed,
                status=status,
                verification_sid=verification_sid
            )

            return True
        except TwilioRestException as e:
            raise self.handle_twilio_error(e)
