from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    can_resend_in = serializers.IntegerField()
    expires_in = serializers.IntegerField()
    attempts = serializers.IntegerField()
    sends = serializers.IntegerField()


class VerificationSerializer(BaseSerializer):
    verification_id = serializers.CharField()


class CheckSerializer(BaseSerializer):
    verified = serializers.BooleanField()
