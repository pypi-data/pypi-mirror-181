from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django_twilio_2fa.client import TwoFAClient
from users.models import UserProfile


User = get_user_model()


class ClientTestCase(TestCase):
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

    def test_user_explicit(self):
        twofa_client = TwoFAClient(
            user=self.user
        )

        self.assertEqual(
            twofa_client.get_user(),
            self.user
        )

        self.assertEqual(
            str(twofa_client.get_phone_number()),
            self.user.profile.phone_number
        )

        self.assertEqual(
            str(twofa_client.get_email()),
            self.user.email
        )


    def test_user_authenticated(self):
        self.client.force_login(self.user)

        r = self.client.get("/")

        twofa_client = TwoFAClient(
            request=r.wsgi_request
        )

        self.assertEqual(
            twofa_client.get_user(),
            self.user
        )

        self.assertEqual(
            str(twofa_client.get_phone_number()),
            self.user.profile.phone_number
        )

        self.assertEqual(
            str(twofa_client.get_email()),
            self.user.email
        )

    def test_user_from_query_param(self):
        r = self.client.get(f"/?user_id={self.user.pk}")

        twofa_client = TwoFAClient(
            request=r.wsgi_request
        )

        self.assertEqual(
            twofa_client.get_user(),
            self.user
        )

        self.assertEqual(
            str(twofa_client.get_phone_number()),
            self.user.profile.phone_number
        )

        self.assertEqual(
            str(twofa_client.get_email()),
            self.user.email
        )

