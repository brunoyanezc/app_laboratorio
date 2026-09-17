from calculations.build_results import (
    build_results
)

from reports.excel_export import (
    export_excel
)


def main():

    results = build_results(
        "data/examples",
        "src/config/sample_parameters.csv",
        "src/config/method.yaml"
    )

    filename = export_excel(
        results,
        "Reporte_GCFID.xlsx"
    )

    print()

    print(
        f"Reporte generado: {filename}"
    )


if __name__ == "__main__":
    main()