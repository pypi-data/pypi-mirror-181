from django.test import TestCase
from django_twilio_2fa.options import PhoneNumber, Email


class PhoneNumberTestCase(TestCase):
    def test_invalid_number(self):
        phone_number = PhoneNumber(
            "000000000",
            "US"
        )

        self.assertFalse(
            phone_number.is_valid
        )

    def test_valid_number(self):
        phone_number = PhoneNumber(
            "2055551234",
            "US",
            "mobile"
        )

        self.assertTrue(
            phone_number.is_valid
        )

    def test_e164_format(self):
        phone_number = PhoneNumber(
            "2055551234",
            "US",
            "mobile"
        )

        self.assertEqual(
            phone_number.e164_format,
            "+12055551234"
        )

    def test_obfuscated(self):
        phone_number = PhoneNumber(
            "2055551234",
            "US",
            "mobile"
        )

        self.assertEqual(
            phone_number.obfuscated,
            "(XXX) XXX-1234"
        )


class EmailTestCase(TestCase):
    def test_email(self):
        email = Email(
            "test@example.com"
        )

        self.assertEqual(
            str(email),
            "test@example.com"
        )

    def test_obfuscated(self):
        email = Email(
            "test@example.com"
        )

        self.assertEqual(
            email.obfuscated,
            "tXXX@eXXXXXX.com"
        )
