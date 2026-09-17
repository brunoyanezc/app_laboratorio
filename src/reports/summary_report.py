import yaml
import pandas as pd


def load_groups():

    with open(
        "src/config/groups.yaml",
        "r",
        encoding="utf-8"
    ) as f:

        return yaml.safe_load(f)


def build_summary_report(df):

    groups = load_groups()

    summaries = []

    for sample_id in df["sample_id"].unique():

        sample = df.loc[
            df["sample_id"] == sample_id
        ]

        sat = sample.loc[
            sample["compound"].isin(
                groups["sat"]
            ),
            "g100g"
        ].sum()

        mufa = sample.loc[
            sample["compound"].isin(
                groups["mufa"]
            ),
            "g100g"
        ].sum()

        omega3 = sample.loc[
            sample["compound"].isin(
                groups["omega3"]
            ),
            "g100g"
        ].sum()

        omega6 = sample.loc[
            sample["compound"].isin(
                groups["omega6"]
            ),
            "g100g"
        ].sum()

        pufa = omega3 + omega6

        epa = sample.loc[
            sample["compound"] == "C20:5n3",
            "g100g"
        ].sum()

        dha = sample.loc[
            sample["compound"] == "C22:6n3",
            "g100g"
        ].sum()

        total_fatty_acids = (
            sample["g100g"].sum()
        )

        omega6_omega3 = None

        if omega3 > 0:

            omega6_omega3 = (
                omega6 / omega3
            )

        summaries.append(
            {
                "sample_id": sample_id,
                "total_fatty_acids": total_fatty_acids,
                "saturated": sat,
                "mufa": mufa,
                "pufa": pufa,
                "omega3": omega3,
                "omega6": omega6,
                "omega6_omega3": omega6_omega3,
                "epa": epa,
                "dha": dha,
            }
        )

    return pd.DataFrame(
        summaries
    )