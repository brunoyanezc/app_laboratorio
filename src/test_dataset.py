from parser.dataset_builder import build_dataset


def main():

    df = build_dataset(
        "data/examples"
    )

    print()
    print(df.head())
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
