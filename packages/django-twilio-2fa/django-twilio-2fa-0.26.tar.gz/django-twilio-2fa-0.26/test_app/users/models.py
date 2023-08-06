from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    phone_number = models.CharField(
        max_length=15,
        null=True, blank=True
    )
    phone_carrier_type = models.CharField(
        max_length=25,
        null=True, blank=True
    )
    last_2fa_attempt = models.DateTimeField(
        null=True, blank=True
    )
    timeout_for_2fa = models.DateTimeField(
        null=True, blank=True
    )
