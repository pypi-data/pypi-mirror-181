import os
import sys
import re
from pathlib import Path

os.environ["DJANGO_SETTINGS_MODULE"] = "test_app.settings"
sys.path.append(f"{Path(__file__).parent.parent.resolve() / 'test_app'}")

import django
django.setup()

from django_twilio_2fa.app_settings import conf, Constant

filename = "docs/settings.md"

with open(filename, "w") as fh:
    fh.write("# Available Settings\n\n")

    fh.write("All settings must be prefixed with `TWILIO_2FA_`.\n\n")

    settings = []

    for setting_name in dir(conf):
        if setting_name.startswith("__"):
            continue

        setting = getattr(conf, setting_name)

        if isinstance(setting, Constant):
            settings.append((
                setting_name, setting
            ))
        else:
            settings.append((
                setting.key.replace("TWILIO_2FA_", ""), setting
            ))

    settings.sort(key=lambda n: n[0])

    for setting_name, setting in settings:
        description = re.sub(r" {2,}", "", setting.description.strip())

        if isinstance(setting, Constant):
            # fh.write(f"### `{setting_name}`\n")
            # fh.write("_This is a constant that cannot be changed._\n")
            #
            # if description:
            #     fh.write(f"\n{description}\n\n")
            #
            # fh.write("\n\n")

            continue

        fh.write(f"### `{setting_name}`\n")

        if setting.must_be_callable:
            fh.write("_This setting must be a callable._\n")

        if description:
            fh.write(f"\n{description}\n\n")

        default = setting.default

        if default in [list, dict]:
            default = default()

        fh.write(f"Defaults to: `{default}`\n")

        if setting.cb_kwargs_required:
            fh.write("\nIf callable, the following kwargs are sent:\n")
            for kwarg in setting.cb_kwargs_required:
                fh.write(f" * `{kwarg}`\n")

        fh.write("\n\n")
