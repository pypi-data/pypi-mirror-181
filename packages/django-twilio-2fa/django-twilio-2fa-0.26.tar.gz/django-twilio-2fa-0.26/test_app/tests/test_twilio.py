import os
import re
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
import requests_mock
from django_twilio_2fa.client import TwoFAClient
from django_twilio_2fa.options import PhoneNumber
from django_twilio_2fa.app_settings import conf
from users.models import UserProfile
from .utils import *


class BaseTwilioTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.user = get_user_model().objects.create(
            username="testuser"
        )

        UserProfile.objects.create(
            user=self.user,
            phone_number="+12055551234",
            phone_carrier_type="mobile"
        )

        self.twofa_client = TwoFAClient(
            user=self.user
        )


class LiveTwilioTestCase(BaseTwilioTestCase):
    def setUp(self):
        super().setUp()

        self.test_phone_number = PhoneNumber(
            phone_number=os.environ["TEST_PHONE_NUMBER"],
            country_code="US"
        )

    def test_carrier_type(self):
        country_code, carrier_type = self.twofa_client.do_carrier_lookup(self.test_phone_number)

        self.assertEqual(
            country_code,
            "US"
        )

        self.assertEqual(
            carrier_type,
            "mobile"
        )


@requests_mock.Mocker()
class MockTwilioTestCase(BaseTwilioTestCase):
    def setUp(self):
        super().setUp()

        self.twofa_client.send_signals = False

    def test_send_verification(self, m):
        sid = mock_twilio_happy_verification(m)

        self.assertEqual(
            self.twofa_client.send_verification(
                "sms",
                "+12055551234"
            ),
            sid
        )

        self.assertGreaterEqual(
            self.twofa_client.verification_expires_in(),
            (60 * 10) - 10
        )

        self.assertGreaterEqual(
            self.twofa_client.can_resend_verification_in(),
            conf.send_cooldown() - 10
        )

    def test_happy_check(self, m):
        mock_twilio_check(m, )

        self.assertTrue(
            self.twofa_client.check_verification(
                code="1234",
                verification_sid="VE1234"
            )
        )

    def test_sad_check(self, m):
        mock_twilio_check(m, False)

        self.assertFalse(
            self.twofa_client.check_verification(
                code="1234",
                verification_sid="VE1234"
            )
        )
