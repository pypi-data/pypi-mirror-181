import re

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

from .errors import *


class PhoneNumber(object):
    def __init__(self, phone_number, country_code, verified=False, carrier_type=None):
        self.phone_number = phone_number
        self.country_code = country_code
        self.carrier_type = carrier_type
        self.verified = verified

    def __str__(self):
        return self.e164_format

    def get_phone_number(self):
        if not self.phone_number:
            return

        if not isinstance(self.phone_number, phonenumbers.PhoneNumber):
            self.parse_phone_number()

        return self.phone_number

    def parse_phone_number(self):
        if not self.phone_number:
            return

        if isinstance(self.phone_number, phonenumbers.PhoneNumber):
            return self.phone_number

        # Cleanup phone number
        transtab = str.maketrans("", "", "()-. _")
        self.phone_number.translate(transtab)

        try:
            self.phone_number = phonenumbers.parse(
                self.phone_number,
                self.country_code
            )
        except NumberParseException as e:
            raise InvalidPhoneNumber(
                country_code=self.country_code,
                phone_number=self.phone_number,
                reason=str(e)
            )

        return self.phone_number

    @property
    def is_valid(self):
        try:
            return phonenumbers.is_valid_number(self.get_phone_number())
        except InvalidPhoneNumber:
            return False

    @property
    def e164_format(self):
        if not self.phone_number:
            return ""

        return phonenumbers.format_number(
            self.get_phone_number(),
            phonenumbers.PhoneNumberFormat.E164
        )

    @property
    def national_format(self):
        if not self.phone_number:
            return ""

        return phonenumbers.format_number(
            self.get_phone_number(),
            phonenumbers.PhoneNumberFormat.NATIONAL
        )

    @property
    def international_format(self):
        if not self.phone_number:
            return ""

        return phonenumbers.format_number(
            self.get_phone_number(),
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

    @property
    def obfuscated(self):
        if not self.phone_number:
            return ""

        n = ""

        for c in self.national_format:
            if c.isdigit():
                n += "X"
            else:
                n += c

        return n[:-4] + self.national_format[-4:]


class Email(object):
    def __init__(self, email, verified=False):
        self.email = email
        self.verified = verified

    def __str__(self):
        return self.email

    @property
    def obfuscated(self):
        if not self.email:
            return ""

        if not re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email):
            return ""

        email_parts = self.email.split("@")
        u = email_parts[0]
        d = email_parts[1]
        dl = len(d) - len(d.split(".")[-1]) - 2
        e = ""
        for x, c in enumerate(u):
            if x < 1:
                e += c
            else:
                if c.isalnum():
                    e += "X"
                else:
                    e += c
        e += "@"
        for x, c in enumerate(d):
            if x < 1 or x > dl:
                e += c
            else:
                if c.isalnum():
                    e += "X"
                else:
                    e += c
        return e
