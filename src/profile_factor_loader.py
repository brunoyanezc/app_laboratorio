import pandas as pd

from config.profile_loader import (
    load_profile
)


def build_factor_table(
    profile_name
):

    profile = load_profile(
        profile_name
    )

    rows = []

    for compound, values in (
        profile["factors"].items()
    ):

        rows.append(
            {
                "compound": compound,
                "tcf": values["tcf"],
                "ffax": values["ffax"]
            }
        )

    return pd.DataFrame(rows)