import pandas as pd

from config.profile_loader import (
    load_profile
)


def build_pvgc2_100g_report(results_df):

    profile = load_profile(
        "PVGC2"
    )

    compounds = profile[
        "report_order"
    ]

    output_rows = []

    for sample_id in sorted(
        results_df["sample_id"].unique()
    ):

        sample = results_df.loc[
            results_df["sample_id"] == sample_id
        ]

        first_row = sample.iloc[0]

        row = {}

        row["sample_id"] = sample_id

        row["total_g100g"] = round(
    float(
        sample["g100g"].sum()
    ),
    3
)
        
        for compound in compounds:

            compound_row = sample.loc[
                sample["compound"] == compound
            ]

            if compound_row.empty:

                row[compound] = 0.0

                continue

            row[compound] = round(
                float(
                    compound_row.iloc[0]["g100g"]
                ),
                3
            )

        output_rows.append(
            row
        )

    return pd.DataFrame(
        output_rows
    )