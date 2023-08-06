from django.test import TestCase
from django_twilio_2fa.errors import UserNotAllowed


class ErrorsTestCase(TestCase):
    def test_user_not_allowed(self):
        error = UserNotAllowed()

        self.assertDictEqual(
            error.get_json(),
            {
                "success": False,
                "error_code": "user_not_allowed",
                "display": "You are not allowed to verify at this time",
                "blocking": False,
                "data": {}
            }
        )
