import pandas as pd


def calculate_fame(
    df: pd.DataFrame,
    exclude_ni: bool = False
):

    work = df.copy()

    denominator = work.loc[
        work["compound"] != "C23:0",
        "area"
    ].sum()

    if exclude_ni:

        denominator -= work.loc[
            work["compound"].str.lower().isin(
                ["unknown", "unknow", "-"]
            ),
            "area"
        ].sum()

    work["fame_percent"] = (
        work["area"] / denominator * 100
    )

    work.loc[
        work["compound"] == "C23:0",
        "fame_percent"
    ] = 0

    return work
