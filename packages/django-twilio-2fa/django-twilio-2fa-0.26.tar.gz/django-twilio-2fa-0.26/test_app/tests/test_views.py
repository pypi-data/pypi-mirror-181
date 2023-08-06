from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
import requests_mock
from django_twilio_2fa.client import TwoFAClient
from users.models import UserProfile
from .utils import *


@requests_mock.Mocker()
class ViewTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.client = Client()

        self.user = get_user_model().objects.create(
            username="testuser"
        )

        UserProfile.objects.create(
            user=self.user
        )

        self.client.force_login(self.user)

    @override_settings(
        TWILIO_2FA_ALLOW_REGISTER=True
    )
    def test_register(self, m):
        mock_twilio_lookup(m)
        mock_twilio_happy_verification(m)

        r = self.client.get(
            reverse("twilio_2fa:register")
        )

        self.assertIn(
            "For the safety and security of your account, we require you to",
            r.content.decode(),
        )

        r = self.client.post(
            reverse("twilio_2fa:register"),
            follow=True,
            data={
                "phone_number": "205-555-1234",
                "country_code": "US"
            }
        )

        twofa_client = TwoFAClient(request=r.wsgi_request)

        self.assertEqual(
            str(twofa_client.get_phone_number()),
            "+12055551234"
        )

        self.assertEqual(
            r.wsgi_request.path,
            reverse("twilio_2fa:start")
        )

    @override_settings(
        TWILIO_2FA_ALLOW_REGISTER=False
    )
    def test_change_not_allowed(self, m):
        r = self.client.get(
            reverse("twilio_2fa:register"),
            follow=True
        )

        self.assertEqual(
            r.wsgi_request.path,
            reverse("twilio_2fa:failed")
        )

    @override_settings(
        TWILIO_2FA_ALLOW_CHANGE=False
    )
    def test_change_not_allowed(self, m):
        self.user.profile.phone_number = "+12055551234"
        self.user.profile.save()

        r = self.client.get(
            reverse("twilio_2fa:change"),
            follow=True
        )

        self.assertEqual(
            r.wsgi_request.path,
            reverse("twilio_2fa:failed")
        )

    @override_settings(
        TWILIO_2FA_ALLOW_CHANGE=True
    )
    def test_change(self, m):
        mock_twilio_lookup(m)
        mock_twilio_happy_verification(m)

        self.user.profile.phone_number = "+12055551234"
        self.user.profile.save()

        r = self.client.get(
            reverse("twilio_2fa:change"),
            follow=True
        )

        self.assertEqual(
            r.wsgi_request.path,
            reverse("twilio_2fa:change")
        )

        r = self.client.post(
            reverse("twilio_2fa:change"),
            follow=True,
            data={
                "phone_number": "205-555-1234",
                "country_code": "US"
            }
        )

        self.assertEqual(
            r.wsgi_request.path,
            reverse("twilio_2fa:start")
        )

    def test_no_phone(self, m):
        mock_twilio_lookup(m)

        r = self.client.get(
            reverse("twilio_2fa:start"),
            follow=True
        )

        self.assertEqual(
            r.wsgi_request.path,
            reverse("twilio_2fa:register")
        )

    def test_start(self, m):
        mock_twilio_happy_verification(m)

        self.user.profile.phone_number = "+12055551234"
        self.user.profile.phone_carrier_type = "mobile"
        self.user.profile.save()

        r = self.client.get(
            reverse("twilio_2fa:start")
        )

        self.assertEqual(
            r.wsgi_request.path,
            reverse("twilio_2fa:start")
        )

        r = self.client.post(
            reverse("twilio_2fa:start"),
            follow=True,
            data={
                "method": "sms"
            }
        )

        self.assertEqual(
            r.wsgi_request.path,
            reverse("twilio_2fa:verify")
        )

    def test_verify_happy(self, m):
        mock_twilio_check(m)

        self.user.profile.phone_number = "+12055551234"
        self.user.profile.phone_carrier_type = "mobile"
        self.user.profile.save()

        r = self.client.post(
            reverse("twilio_2fa:start"),
            follow=True,
            data={
                "method": "sms"
            }
        )

        r = self.client.post(
            reverse("twilio_2fa:verify"),
            follow=True,
            data={
                "token": "1234"
            }
        )

        self.assertEqual(
            r.wsgi_request.path,
            reverse("twilio_2fa:success")
        )

    def test_verify_sad(self, m):
        mock_twilio_check(m, False)

        self.user.profile.phone_number = "+12055551234"
        self.user.profile.phone_carrier_type = "mobile"
        self.user.profile.save()

        r = self.client.post(
            reverse("twilio_2fa:start"),
            follow=True,
            data={
                "method": "sms"
            }
        )

        r = self.client.post(
            reverse("twilio_2fa:verify"),
            follow=True,
            data={
                "token": "1234"
            }
        )

        self.assertIn(
            "Your verification code is not correct",
            r.content.decode()
        )
