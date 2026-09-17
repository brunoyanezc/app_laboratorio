from calculations.build_results import (
    build_results
)


def main():

    df = build_results(
        "data/examples"
    )

    print(df.columns)

    print()
    print(df.head())

    df.to_excel(
        "resultado_completo.xlsx",
        index=False
    )

    print()
    print("Archivo exportado:")
    print("resultado_completo.xlsx")


if __name__ == "__main__":
    main()