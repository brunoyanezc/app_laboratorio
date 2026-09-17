import yaml


def load_profile(profile_name):

    filename = (
        f"src/config/profiles/{profile_name}.yaml"
    )

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as f:

        return yaml.safe_load(f)