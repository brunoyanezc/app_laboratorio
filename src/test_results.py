from calculations.build_results import (
    build_results
)


def main():

    df = build_results(
        "data/examples"
    )

    print()

    print(
        df[
            [
                "sample_id",
                "compound",
                "area",
                "tcf",
                "ffax",
                "wfamex",
                "wx",
                "g100g"
            ]
        ].head(20)
    )

    print()

    print(
        "Muestras:",
        df["sample_id"].nunique()
    )

    print(
        "Filas:",
        len(df)
    )


if __name__ == "__main__":
    main()