from discover import discover_reports
from report01 import read_peaksumcalc


def main():

    reports = discover_reports("data/examples")

    sample = reports[0]

    print()
    print("Muestra:", sample["sample_id"])
    print()

    df, total = read_peaksumcalc(
        sample["report_file"]
    )

    print("TotPeakResponse")
    print(total)

    print()
    print(df.head())

    print()
    print("Numero de compuestos:")
    print(len(df))


if __name__ == "__main__":
    main()
