import pandas as pd

from config.profile_loader import (
    load_profile
)


def build_pvgc2_nutri_report(
    results_df,
    profile_name
):

    profile = load_profile(
        profile_name
    )

    compounds = profile[
        "nutri_order"
    ]

    output_rows = []

    sample_order = (
        results_df[
            ["sample_id", "order"]
        ]
        .drop_duplicates()
        .sort_values("order")
    )

    for sample_id in sample_order["sample_id"]:

        sample = results_df.loc[
            results_df["sample_id"] == sample_id
        ]

        row = {}

        row["sample_id"] = sample_id

        for compound in compounds:

            # columnas en blanco
            if compound == "":

                blank_col = (
                    f"BLANK_{len(row)}"
                )

                row[blank_col] = ""

                continue

            compound_row = sample.loc[
                sample["compound"] == compound
            ]

            if compound_row.empty:

                row[compound] = 0.0

                continue

            value = float(
                compound_row.iloc[0][
                    "fame_percent"
                ]
            )

            if compound == "C23:0":

                value = 0.0

            row[compound] = round(
                value,
                2
            )

        output_rows.append(
            row
        )

    report = pd.DataFrame(
        output_rows
    )

    return report