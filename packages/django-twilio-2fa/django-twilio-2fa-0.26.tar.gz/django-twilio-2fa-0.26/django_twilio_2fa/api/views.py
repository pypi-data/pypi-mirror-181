from rest_framework.views import APIView
from rest_framework.response import Response
from ..app_settings import conf
from ..client import TwoFAClient
from ..errors import *
from .serializers import VerificationSerializer, CheckSerializer


class BaseView(APIView):
    serializer_class = None

    def _get_response(self, data, status_code=200):
        data["_debug"] = {
            "session": self.twofa_client.session._to_dict()
        }

        return Response(
            data,
            status=status_code
        )

    def _get_classes(self, key):
        return conf.api_classes().get(key)

    def get_throttles(self):
        return self._get_classes("throttle") or super().get_throttles()

    def get_permissions(self):
        return self._get_classes("permission") or super().get_permissions()

    def get_authenticators(self):
        return self._get_classes("authentication") or super().get_authenticators()

    def get_serialized_response(self, **data):
        data.update({
            "can_resend_in": self.twofa_client.can_resend_verification_in(),
            "expires_in": self.twofa_client.verification_expires_in(),
            "attempts": self.twofa_client.session["attempts"],
            "sends": self.twofa_client.session["sends"]
        })

        payload = data

        if self.serializer_class:
            s = self.serializer_class(data=data)
            s.is_valid()
            payload = s.data

        return self._get_response(payload)

    def post(self, request, *args, **kwargs):
        self.twofa_client = TwoFAClient(request=self.request)

        try:
            return self.do_post()
        except Error as e:
            return self._get_response(
                e.get_json(),
                status_code=e.status_code
            )


class SetPhoneNumberView(BaseView):
    def do_post(self):
        self.twofa_client.set_user_data(
            "phone_number",
            phone_number=self.request.data.get("phone_number"),
            country_code=self.request.data.get("country_code")
        )
        return Response({
            "success": True
        })


class SetEmailView(BaseView):
    def do_post(self):
        self.twofa_client.set_user_data(
            "email",
            email=self.request.data.get("email")
        )
        return Response({
            "success": True
        })


class SendView(BaseView):
    serializer_class = VerificationSerializer

    def do_post(self):
        method = self.request.data.get("method", "sms")

        phone_number = self.request.data.get("phone_number")
        phone_country = self.request.data.get("phone_country")
        email = self.request.data.get("email")

        if self.twofa_client.get_user() and not self.twofa_client.get_phone_number() and conf.user_must_have_phone():
            raise PhoneNumberNotSet()

        if not self.twofa_client.get_user():
            if phone_number or phone_country:
                self.twofa_client.set_phone_number(
                    phone_number=phone_number,
                    country_code=phone_country
                )

            if email:
                self.twofa_client.set_email(
                    email=email
                )

        verification_sid = self.twofa_client.send_verification(
            method
        )

        return self.get_serialized_response(
            verification_id=verification_sid
        )


class VerifyView(BaseView):
    serializer_class = CheckSerializer

    def do_post(self):
        verification_id = self.request.data.get("verification_id")
        code = self.request.data.get("code")

        if not code:
            raise MalformedRequest(
                missing_field="code"
            )

        verified = self.twofa_client.check_verification(
            verification_sid=verification_id,
            code=code
        )

        return self.get_serialized_response(
            verified=verified
        )


class CancelView(BaseView):
    def do_post(self):
        self.twofa_client.cancel_verification(
            verification_sid=self.request.data.get("verification_id")
        )

        return self.get_serialized_response(
            success=True
        )


class MethodsView(BaseView):
    def do_post(self):
        methods = self.twofa_client.get_verification_methods()

        for key in ["sms", "call"]:
            if key not in methods:
                continue

            methods[key]["obfuscated"] = self.twofa_client.get_phone_number().obfuscated

        if "email" in methods:
            methods["email"]["obfuscated"] = self.twofa_client.get_email().obfuscated

        return Response({
            "verification_methods": methods
        })
