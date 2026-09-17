import pandas as pd


def calculate_fame(df, exclude_ni=False):

    result = df.copy()

    for sample_id in result["sample_id"].unique():

        mask = result["sample_id"] == sample_id

        sample = result.loc[mask]

        denominator = sample.loc[
            sample["compound"] != "C23:0",
            "area"
        ].sum()

        if exclude_ni:

            denominator -= sample.loc[
                sample["compound"].str.lower().isin(
                    ["unknown", "unknow", "-"]
                ),
                "area"
            ].sum()

        result.loc[
            mask,
            "fame_percent"
        ] = (
            sample["area"]
            / denominator
            * 100
        )

        result.loc[
            mask
            & (result["compound"] == "C23:0"),
            "fame_percent"
        ] = 0

    return result