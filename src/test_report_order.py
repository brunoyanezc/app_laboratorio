from config.report_order_loader import (
    load_report_order
)


def main():

    df = load_report_order()

    print()

    print(df.head())

    print()

    print(
        "Numero compuestos:",
        len(df)
    )


if __name__ == "__main__":
    main()