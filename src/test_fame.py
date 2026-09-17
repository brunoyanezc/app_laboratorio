from parser.discover import discover_reports
from parser.report_reader import read_report

from calculations.calculate_fame import (
    calculate_fame
)


def main():

    reports = discover_reports(
        "data/examples"
    )

    sample = reports[0]

    result = read_report(
        sample["report_file"]
    )

    df = result["data"]

    fame = calculate_fame(
        df,
        exclude_ni=False
    )

    print()
    print(sample["sample_id"])
    print()

    print(
        fame[
            ["compound",
             "area",
             "fame_percent"]
        ].head(20)
    )

    print()
    print(
        "SUMA:",
        fame["fame_percent"].sum()
    )


if __name__ == "__main__":
    main()
