import pandas as pd

from config.profile_loader import (
    load_profile
)


def build_pvgc2_report(results_df):

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

        # ---------------------------------
        # Identificación muestra
        # ---------------------------------

        row["sample_id"] = sample_id

        row["sample_weight_g"] = round(
            float(
                first_row[
                    "sample_weight_g"
                ]
            ),
            6
        )

        row["mass_c23_added_g"] = round(
            float(
                first_row[
                    "mass_c23_added_g"
                ]
            ),
            12
        )

        # ---------------------------------
        # Analitos
        # ---------------------------------

        for compound in compounds:

            compound_row = sample.loc[
                sample["compound"] == compound
            ]

            pct_col = (
                f"{compound}_%Area"
            )

            area_col = (
                f"{compound}_Area"
            )

            if compound_row.empty:

                row[pct_col] = 0.0
                row[area_col] = 0.0

                continue

            compound_row = (
                compound_row.iloc[0]
            )

            pct_value = float(
                compound_row[
                    "fame_percent"
                ]
            )

            area_value = float(
                compound_row[
                    "area"
                ]
            )

            # Regla especial C23

            if compound == "C23:0":

                pct_value = 0.0

            row[pct_col] = round(
                pct_value,
                2
            )

            row[area_col] = round(
                area_value,
                6
            )

        output_rows.append(
            row
        )

    report = pd.DataFrame(
        output_rows
    )

    return report