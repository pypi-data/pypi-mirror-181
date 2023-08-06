from django import forms
import pycountry
from .client import TwoFAClient
from .app_settings import conf


__all__ = [
    "Twilio2FARegistrationForm", "Twilio2FAVerifyForm", "CountryCodeField",
]


class CountryCodeField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs["choices"] = [
            ("", "--"),
        ]

        country_codes = list(set(conf.allowed_countries()) - set(conf.disallowed_countries()))
        country_codes.sort()

        for c in country_codes:
            country = pycountry.countries.get(alpha_2=c)

            if country:
                kwargs["choices"].append((c, country.name))
            else:
                raise ValueError(f"{c} is not a valid alpha_2 country code")

        super().__init__(*args, **kwargs)


class Twilio2FARegistrationForm(forms.Form):
    country_code = CountryCodeField()
    phone_number = forms.CharField()


class Twilio2FAVerifyForm(forms.Form):
    token = forms.CharField(
        required=True
    )
