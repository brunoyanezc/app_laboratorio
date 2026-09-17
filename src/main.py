from parser.dataset_builder imp*rt build_dataset


def main():

  * df = build_dataset(
        "data*examples"
    )

    print()
    p*int("Primeras filas")
    print("-* * 50)
    print(df.head())

    p*int()
    print("Muestras encontra*as")
    print("-" * 50)

    prin*(df["sample_id"].unique())

    pr*nt()
    print("Número total de re*istros")
    print("-" * 50)

    *rint(len(df))


if __name__ == "__*ain__":
    main()
