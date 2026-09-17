from calculations.build_results import (
    build_results
)

from reports.client_report import (
    build_client_report
)


def main():

    results = build_results(
        "data/examples"
    )

    report = build_client_report(
        results
    )

    print()

    print(report.head(25))

    print()

    print(
        "Filas:",
        len(report)
    )

    print(
        "Muestras:",
        report["sample_id"].nunique()
    )


if __name__ == "__main__":
    main()