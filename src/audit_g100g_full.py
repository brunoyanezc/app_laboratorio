from calculations.build_results import (
    build_results
)

SAMPLE_ID = "CI26-00450-001"


df = build_results(
    "data/examples",
    "src/config/sample_parameters.csv",
    "src/config/method.yaml"
)

sample = df.loc[
    df["sample_id"] == SAMPLE_ID
].copy()

sample = sample[
    [
        "compound",
        "area",
        "tcf",
        "ffax",
        "wfamex",
        "wx",
        "g100g",
        "fame_percent"
    ]
]

sample = sample.sort_values(
    "g100g",
    ascending=False
)

print()
print("=" * 120)
print(SAMPLE_ID)
print("=" * 120)

print(
    sample.to_string(
        index=False
    )
)

print()
print("TOTAL G100G")
print(sample["g100g"].sum())

print()
print("TOTAL SIN C23")

print(
    sample.loc[
        sample["compound"] != "C23:0",
        "g100g"
    ].sum()
)

print()
print("TOTAL SIN C23 NI")

print(
    sample.loc[
        ~sample["compound"].isin(
            [
                "C23:0",
                "Unknow"
            ]
        ),
        "g100g"
    ].sum()
)