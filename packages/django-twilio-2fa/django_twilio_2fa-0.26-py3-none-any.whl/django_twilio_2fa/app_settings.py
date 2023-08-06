from django.conf import settings
from django.utils.translation import gettext_lazy as _


class SettingError(Exception):
    def __init__(self, key):
        self.key = key


class MustBeCallable(SettingError):
    def __str__(self):
        return f"{self.key}: Must be callable"


class EagerCallable(SettingError):
    def __str__(self):
        return f"{self.key}: Cannot make a callable eager loading"


class MissingRequiredCallbackArgument(SettingError):
    def __str__(self):
        return f"Missing required callback argument: {self.key}"


class MissingRequiredSetting(SettingError):
    def __str__(self):
        return f"Missing required setting: {self.key}"


DJ_SETTING_PREFIX = "TWILIO_2FA"


class Constant(object):
    def __init__(self, value, description=None):
        self.value = value
        self.description = description or ""

    def __call__(self):
        return self.value


class Setting(object):
    def __init__(
            self,
            key,
            required=False,
            default=None,
            must_be_callable=False,
            cb_kwargs_required=None,
            description=None
    ):
        self.key = key.upper()
        self.required = required
        self.default = default
        self.cb_kwargs_required = cb_kwargs_required
        self.has_attr = False
        self.must_be_callable = must_be_callable
        self.description = description or ""

        if not self.key.startswith(DJ_SETTING_PREFIX):
            self.key = f"{DJ_SETTING_PREFIX}_{self.key}"

        if must_be_callable and not self.key.endswith("_CB"):
            self.key += "_CB"

        if required and not hasattr(settings, self.key):
            raise AttributeError(f"Cannot find setting {self.key}")

        if not hasattr(settings, self.key):
            return

        if must_be_callable and not callable(getattr(settings, self.key)):
            raise MustBeCallable(self.key)

    def __call__(self, default=None, **cb_kwargs):
        if not default and callable(self.default):
            default = self.default()
        elif not default:
            default = self.default

        if not hasattr(settings, self.key):
            return default

        getter = getattr(settings, self.key)

        if callable(getter):
            for arg in self.cb_kwargs_required or []:
                if arg in cb_kwargs:
                    continue
                raise MissingRequiredCallbackArgument(arg)

            value = getter(**cb_kwargs)
        else:
            value = getter

        if value is None:
            return default

        return value


class Conf(object):
    available_methods = Constant({
        "sms": {
            "value": "sms",
            "label": _("Text Message"),
            "icon": "fas fa-sms",
            "data_required": "phone_number",
            "carrier_required": "mobile"
        },
        "call": {
            "value": "call",
            "label": _("Phone Call"),
            "icon": "fas fa-phone",
            "data_required": "phone_number"
        },
        "email": {
            "value": "email",
            "label": _("E-mail"),
            "icon": "fas fa-envelope",
            "data_required": "email"
        },
        "whatsapp": {
            "value": "whatsapp",
            "label": _("WhatsApp"),
            "icon": "fab fa-whatsapp",
            "data_required": "phone_number"
        }
    })
    session_data_key = Constant(
        "twilio_2fa_data"
    )
    allowed_methods = Setting(
        "allowed_methods",
        default=list,
        description="""
        List of methods setup in your Verify service. The method must be enabled in the Verify service you setup in the Twilio Console.
        
        Available methods: `sms`, `call`, `email` and `whatsapp`. 
        _Note: `email` requires a Sendgrid integration.  Details can be found [here](https://www.twilio.com/docs/verify/email#create-an-email-template)._
        
        If this setting is `None` or not set, all available methods will be presented to the end user.
        """
    )
    method_details = Setting(
        "method_details",
        default=dict,
        description="""
        Allows overriding a verification method's details like icon and display text.
        
        This setting should return a dictionary with one or more methods and the overrides in a nested dictionary.
        
        Each method can define one or both of the following:
         * `label` - Method name displayed to user
         * `icon` - Icon class (from places like [FontAwesome](https://fontawesome.com/))
        """
    )
    default_error_code = Setting(
        "default_error_code",
        default="2fa_error",
        description="Default error code when an unknown error is thrown"
    )
    default_error_display = Setting(
        "default_error_display",
        default=_("Unable to verify at this time"),
        description="Default error message displayed to user"
    )
    error_displays = Setting(
        "error_display",
        default=dict,
        must_be_callable=True,
        cb_kwargs_required=["code"],
        description="""
        Allows overriding of error messages displayed to user.
        
        The [error code](errors.md) is sent and the string or gettext_lazy 
        """
    )
    allow_userless = Setting(
        "allow_userless",
        default=False,
        description="Allow verification without any user"
    )
    #
    # Unauthenticated Requests
    allow_unauthenticated_users = Setting(
        "allow_unauthenticated_users",
        default=False,
        description="Allow verification outside of an authenticated user session"
    )
    unauthenticated_query_param = Setting(
        "unauthenticated_query_param",
        default="user_id",
        description="URL query parameter used to specify the field on the user model"
    )
    unauthenticated_user_field = Setting(
        "unauthenticated_user_field",
        default="pk",
        description="User model field to compare value of query parameter"
    )
    #
    # Twilio
    twilio_account_sid = Setting(
        "account_sid",
        required=True,
        description="""
        Your Twilio account SID from the Twilio Console.
        
        _Note: You cannot use test credentials with Verify._
        """
    )
    twilio_auth_token = Setting(
        "auth_token",
        required=True,
        description="""
        Your Twilio account token from the Twilio Console.
        
        _Note: You cannot use test credentials with Verify._
        """
    )
    twilio_service_id = Setting(
        "service_id",
        required=True,
        description="Your Twilio Verify service SID from the Twilio Console."
    )
    twilio_service_name = Setting(
        "service_name",
        cb_kwargs_required=["request"],
        description="Overrides the Verify service's friendly name set in the Twilio Console."
    )
    has_clnpc_permission = Setting(
        "has_clnpc_permission",
        default=False,
        description="""
        To perform a lookup on a Canadian number, you must have permission from the CLNPC and you account must be updated by Twilio support.
        
        See [this Twilio support article](https://support.twilio.com/hc/en-us/articles/360004563433).
        """
    )
    #
    # Twilio 2FA
    verification_expiration = Setting(
        "verification_expiration",
        default=10,  # minutes
        description="Verification expiration in minutes (contact Twilio support to change)"
    )
    send_cooldown = Setting(
        "send_cooldown",
        default=30,  # seconds
        description="""
        Seconds after the last delivery attempt to allow the user to reattempt delivery of the verification.
        
        Twilio does not have a limit on the amount of time between retries.
        """
    )
    max_attempts = Setting(
        "max_attempts",
        default=5,
        description="Maximum attempts allowed (configurable through Twilio)"
    )
    max_sends = Setting(
        "max_sends",
        default=5,
        description="Maximum number of sends (configurable through Twilio)"
    )
    cancel_on_max_retries = Setting(
        "cancel_on_max_retries",
        default=False,
        description="If a user reaches max attempts, cancel verification -- user will be unable to verify again until "
                    "the current verification has expired or been canceled"
    )
    #
    # Phone numbers
    do_carrier_lookup = Setting(
        "phone_number_carrier_lookup",
        default=True,
        description="Perform a carrier lookup using Twilio Lookup service"
    )
    allowed_countries = Setting(
        "phone_number_allowed_countries",
        default=["US"],
        description="List of country codes from which phone numbers are allowed to originate."
    )
    disallowed_countries = Setting(
        "phone_number_disallowed_countries",
        default=list,
        description="""
        List of country codes from which phone numbers *are not* allowed to originate. 
        
        These countries are *removed* from the allowed countries list.
        """
    )
    default_country_code = Setting(
        "phone_number_default_region",
        default="US",
        description="""
        Default ISO country code for phone numbers.
        
        The default region for [`phonenumbers`](https://github.com/daviddrysdale/python-phonenumbers) library. Typically, this is the country code, but the entire list can be found [here](https://github.com/daviddrysdale/python-phonenumbers/tree/dev/python/phonenumbers/data).
        
        Setting this allows users to not need to enter a country code with their phone number. 

        You can set this to `None` to not have a default region. 
        """
    )
    allowed_carrier_types = Setting(
        "phone_number_allowed_carrier_types",
        default=["mobile"],
        description="""
        A list of allowed carrier types.

        Available types: `voip`, `landline`, and `mobile`.
        
        _Note: not all countries provide this information._
        """
    )
    bypass_carrier_on_empty = Setting(
        "phone_number_bypass_carrier_on_empty",
        default=True,
        description="Allow bypassing if the carrier information is empty on lookup"
    )
    #
    # User
    allow_user_to_verify = Setting(
        "allow_user",
        must_be_callable=True,
        default=True,
        cb_kwargs_required=["user"],
        description="""
        Indicates if a user is allowed to use 2FA verification.
        
        This setting is useful if you have users that are verified outside of the normal flow (such as SSO).
        """
    )
    allow_registration = Setting(
        "allow_registration",
        default=True,
        cb_kwargs_required=["user"],
        description="Indicates if a user is allowed to register a phone number for 2FA"
    )
    allow_change = Setting(
        "allow_change",
        default=True,
        cb_kwargs_required=["user"],
        description="Indicates if a user is allowed to change 2FA phone number"
    )
    user_methods = Setting(
        "user_methods",
        must_be_callable=True,
        cb_kwargs_required=["user"],
        description="""
        List of methods a user is allowed to verify with.
        
        By default, the methods allowed for a user is determined based on data available.
        For example, a user with a phone number but no carrier type wouldn't be able to use the `sms` method.
        """
    )
    user_phone_number = Setting(
        "user_phone_number",
        required=True,
        must_be_callable=True,
        cb_kwargs_required=["user"],
        description="Return a user's phone number as a `django_twilio_2fa.options.PhoneNumber` instance"
    )
    user_email = Setting(
        "user_email",
        required=True,
        must_be_callable=True,
        cb_kwargs_required=["user"],
        description="Return a user's e-mail address as an `django_twilio_2fa.options.Email` instance"
    )
    user_must_have_phone = Setting(
        "user_must_have_phone",
        default=False,
        description="If a user does not have a phone number, they must register one to verify."
    )
    #
    # View-based settings
    next_session_key = Constant(
        "twilio_2fa_next"
    )
    disallowed_redirect_url = Setting(
        "disallowed_redirect_url",
        default="/",
        cb_kwargs_required=["user"],
        description="""
        Redirect URL when a user is not allowed to verify.
        
        (Applicable only to view-based 2FA.)
        """
    )
    success_redirect_url = Setting(
        "success_redirect_url",
        cb_kwargs_required=["user"],
        description="""
        The URL to redirect users to after a successful verification. This _should not_ return a `Response` (like `HttpResponseRedirect`) and should only return the URL as a string.

        (Only applicable to view-based 2FA.)
        """
    )
    send_immediately_on_single = Setting(
        "send_immediately_on_single",
        default=True,
        description="""
        If only one verification method is available, skip method selection and send immediately.
        
        (Only applicable to view-based 2FA.)
        """
    )
    #
    # API settings
    api_classes = Setting(
        "api_classes",
        default=dict,
        description="""
        Dictionary of classes list to apply to API views.
        
        Accepted keys:
         * `permission`
         * `authentication`
         * `throttle`
        
        (Only applicable to API-based 2FA.)
        """
    )


conf = Conf()
