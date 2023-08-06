import re


TWILIO_VERIFY_URL = re.compile(r"https://verify.twilio.com/v2/.*")
TWILIO_LOOKUP_URL = re.compile(r"https://lookups.twilio.com/v1/.*")


def register_twilio_url(m, json, method="POST", status_code=200, verify=True):
    m.register_uri(
        method,
        TWILIO_VERIFY_URL if verify else TWILIO_LOOKUP_URL,
        json=json,
        status_code=status_code
    )


def mock_twilio_lookup(m, phone_number="+12055551234", country_code="US", carrier_type="mobile"):
    register_twilio_url(m, method="GET", verify=False, json={
        "caller_name": None,
        "carrier": {
            "error_code": None,
            "mobile_country_code": "310",
            "mobile_network_code": "456",
            "name": "verizon",
            "type": "mobile"
        },
        "country_code": "US",
        "national_format": "(205) 555-1234",
        "phone_number": phone_number,
        "add_ons": None,
        "url": "https://lookups.twilio.com/v1/PhoneNumbers/+15108675310"
    })


def mock_twilio_happy_verification(m):
    sid = "VE123456789"

    register_twilio_url(m, json={
        "sid": sid,
        "service_sid": "VA123456789",
        "account_sid": "AC123456789",
        "to": "+12055551234",
        "channel": "sms",
        "status": "pending",
        "valid": False,
        "date_created": "2015-07-30T20:00:00Z",
        "date_updated": "2015-07-30T20:00:00Z",
        "lookup": {},
        "amount": None,
        "payee": None,
        "sna": None,
        "url": "https://verify.twilio.com/v2/Services/VA123456789/Verifications/VE123456789"
    })

    return sid


def mock_twilio_check(m, approved=True):
    register_twilio_url(m, json={
        "sid": "VEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "service_sid": "VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "to": "+15017122661",
        "channel": "sms",
        "status": "approved" if approved else "pending",
        "valid": True,
        "amount": None,
        "payee": None,
        "sna_attempts_error_codes": [],
        "date_created": "2015-07-30T20:00:00Z",
        "date_updated": "2015-07-30T20:00:00Z"
    })
