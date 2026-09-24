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

        row = {}

        row["sample_id"] = sample_id

        # ----------------------------------
        # Total g/100g reportado
        # Excluye:
        # - C23:0
        # - Unknow
        # ----------------------------------

        reported_sample = sample.loc[
            sample["compound"].isin(
                compounds
            )
        ]

        reported_sample = reported_sample.loc[
            reported_sample["compound"] != "C23:0"
        ]

        reported_sample = reported_sample.loc[
            reported_sample["compound"] != "Unknow"
        ]

        row["total_g100g"] = round(
            float(
                reported_sample[
                    "g100g"
                ].sum()
            ),
            3
        )

        # ----------------------------------
        # Analitos individuales
        # ----------------------------------

        for compound in compounds:

            compound_row = sample.loc[
                sample["compound"] == compound
            ]

            if compound_row.empty:

                row[compound] = 0.0

                continue

            value = float(
                compound_row.iloc[0]["g100g"]
            )

            # C23 no se reporta

            if compound == "C23:0":

                value = 0.0

            row[compound] = round(
                value,
                3
            )

        output_rows.append(
            row
        )

    return pd.DataFrame(
        output_rows
    )