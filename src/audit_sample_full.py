from calculations.build_results import (
    build_results
)


SAMPLE_ID = "CI26-00450-001"

print("INICIANDO AUDITORIA")

def main():

    df = build_results(
        "data/examples",
        "src/config/sample_parameters.csv",
        "src/config/method.yaml"
    )

    sample = df.loc[
        df["sample_id"] == SAMPLE_ID
    ].copy()

    print()
    print("=" * 80)
    print("MUESTRA")
    print("=" * 80)

    print(SAMPLE_ID)

    print()
    print("PARAMETROS")
    print("=" * 80)

    print(
        "sample_weight_g =",
        sample["sample_weight_g"].iloc[0]
    )

    print(
        "mass_c23_added_g =",
        sample["mass_c23_added_g"].iloc[0]
    )

    print(
        "total_peak_response =",
        sample["total_peak_response"].iloc[0]
    )

    print()

    print("AREA C23")
    print("=" * 80)

    c23 = sample.loc[
        sample["compound"] == "C23:0"
    ]

    print(
        c23[
            [
                "area",
                "fame_percent"
            ]
        ]
    )

    print()

    print("SUMATORIAS")
    print("=" * 80)

    print(
        "SUMA AREA =",
        sample["area"].sum()
    )

    print(
        "SUMA PPM =",
        sample["ppm"].sum()
    )

    print(
        "SUMA G100G =",
        sample["g100g"].sum()
    )

    print()

    print("COMPUESTOS SIN TCF")
    print("=" * 80)

    missing_tcf = sample[
        sample["tcf"].isna()
    ]

    if missing_tcf.empty:

        print("NINGUNO")

    else:

        print(
            missing_tcf[
                [
                    "compound"
                ]
            ]
        )

    print()

    print("COMPUESTOS SIN FFAx")
    print("=" * 80)

    missing_ffax = sample[
        sample["ffax"].isna()
    ]

    if missing_ffax.empty:

        print("NINGUNO")

    else:

        print(
            missing_ffax[
                [
                    "compound"
                ]
            ]
        )

    print()

    print("TOP 20 g/100g")
    print("=" * 80)

    top = (
        sample[
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
        .sort_values(
            "g100g",
            ascending=False
        )
        .head(20)
    )

    print(top)

    print()

    print("TOP 20 %AREA")
    print("=" * 80)

    top_area = (
        sample[
            [
                "compound",
                "area",
                "fame_percent"
            ]
        ]
        .sort_values(
            "fame_percent",
            ascending=False
        )
        .head(20)
    )

    print(top_area)

    print()

    print("UNKNOWN")
    print("=" * 80)

    unknown = sample.loc