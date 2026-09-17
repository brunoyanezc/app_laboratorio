from calculations.build_results import (
    build_results
)


def audit_sample(sample_id, compound):

    df = build_results(
        "data/examples"
    )

    row = df.loc[
        (df["sample_id"] == sample_id)
        &
        (df["compound"] == compound)
    ]

    if row.empty:

        print(
            f"No se encontró {compound} en {sample_id}"
        )
        return

    row = row.iloc[0]

    print()
    print("=" * 60)
    print("AUDITORIA")
    print("=" * 60)

    print("Muestra:", row["sample_id"])
    print("Compuesto:", row["compound"])

    print()

    print("AREA X:", row["area"])
    print("AREA C23:", row["area_c23"])

    print()

    print(
        "C23 CONCENTRACION:",
        row["c23_concentration_g_g"]
    )

    print(
        "MASA C23 AGREGADA:",
        row["mass_c23_added_g"]
    )

    print()

    print("TCF:", row["tcf"])
    print("FFAx:", row["ffax"])

    print()

    print("WFAMEx:", row["wfamex"])
    print("Wx:", row["wx"])

    print()

    print("g/100g:", row["g100g"])

    print()

    print(
        "FAME DENOMINADOR:",
        row["fame_denominator"]
    )

    print(
        "%FAME:",
        row["fame_percent"]
    )

    print("=" * 60)


if __name__ == "__main__":

    audit_sample(
        sample_id="VIT25-7248",
        compound="C16:0"
    )