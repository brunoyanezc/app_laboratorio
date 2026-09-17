import json
from pathlib import Path


SETTINGS_FILE = (
    "src/config/user_settings.json"
)


def load_settings():

    file = Path(
        SETTINGS_FILE
    )

    if not file.exists():

        return {}

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def save_settings(settings):

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            settings,
            f,
            indent=4
        )