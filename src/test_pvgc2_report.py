from calculations.build_results import (
    build_results
)

from reports.pvgc2_report import (
    build_pvgc2_report
)


def main():

    results = build_results(
        "data/examples"
    )

    report = build_pvgc2_report(
        results
    )

    print()

    print(
        report.iloc[:, 0:15]
    )

    print()

    print(
        "Filas:",
        len(report)
    )

    print(
        "Columnas:",
        len(report.columns)
    )

    report.to_excel(
        "PVGC2_Report.xlsx",
        index=False
    )

    print()

    print(
        "PVGC2_Report.xlsx generado"
    )


if __name__ == "__main__":
    main()