import os
import sys
import re
from pathlib import Path

os.environ["DJANGO_SETTINGS_MODULE"] = "test_app.settings"
sys.path.append(f"{Path(__file__).parent.parent.resolve() / 'test_app'}")

import django
django.setup()

from django_twilio_2fa.errors import get_error_details

filename = "docs/errors.md"

with open(filename, "w") as fh:
    fh.write("# Errors\n\n")

    fh.write("""
Error classes are located in `django_twilio_2fa.errors` and are `Exception` subclasses. 

When using the API endpoints, errors are returned as a JSON object:
```json
{
    "success": false,
    "error_code": "<error_code>",
    "display": "<user_display>",
    "data": "<obj>",
    "blocking": <true or false>
}
```
\n\n""")

    errors = get_error_details()

    sorted(errors)

    for error in errors.values():
        fh.write(f"## `{error['name']}`\n\n")

        docstring = error["obj"].__doc__

        if docstring:
            fh.write(re.sub(r" {2,}", "", docstring.strip()) + "\n\n")

        fh.write(f"* **Error code:** `{error['code']}`\n")
        fh.write(f"* **Display for user:** `{error['display']}`\n")
        fh.write(f"* **Status Code:** `{error['status_code']}`\n")
        fh.write(f"* **Should block further attempts?** {'Yes' if error['blocking'] else 'No'}\n")

        fh.write("\n\n")
