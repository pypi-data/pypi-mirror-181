from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django_twilio_2fa.session import TwoFASession
from django_twilio_2fa.app_settings import conf
from users.models import UserProfile


User = get_user_model()


class SessionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            email="test@example.com"
        )

        UserProfile.objects.create(
            user=self.user,
            phone_number="+12055551234",
            phone_carrier_type="mobile"
        )

        self.client = Client()

    def test_defaults(self):
        session = TwoFASession()

        self.assertTrue(
            session.has("verification_sid")
        )

        self.assertIsNone(
            session.get("verification_sid")
        )

    def test_set_with_no_request(self):
        session = TwoFASession()

        session["verification_sid"] = "abc123"

        self.assertEqual(
            session["verification_sid"],
            "abc123"
        )

        self.assertTrue(
            "verification_sid" in session.dump()
        )

    def test_set_with_request(self):
        self.client.force_login(self.user)

        r = self.client.get("/")

        session = TwoFASession(
            request=r.wsgi_request
        )

        session["verification_sid"] = "abc123"

        self.assertEqual(
            r.wsgi_request.session[conf.session_data_key()].get("verification_sid"),
            "abc123"
        )

    def test_int(self):
        session = TwoFASession()

        session["attempts"] = "3"

        self.assertEqual(
            session["attempts"],
            3
        )
