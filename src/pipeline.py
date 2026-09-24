from calculations.build_results import (
    build_results
)

from reports.excel_export import (
    export_excel
)

from reports.pvgc2_report import (
    build_pvgc2_report
)

from reports.pvgc2_100g_report import (
    build_pvgc2_100g_report
)

from reports.pvgc2_nutri_report import (
    build_pvgc2_nutri_report
)


def run_pipeline(
    data_folder,
    sample_parameters_file,
    method_file,
    output_file,
    profile_name
):

    # -----------------------------
    # Motor de cálculo
    # -----------------------------

    results = build_results(
        data_folder,
        sample_parameters_file,
        method_file
    )

    # -----------------------------
    # Reportes
    # -----------------------------

    area_report = build_pvgc2_report(
        results,
        profile_name
    )

    report_100g = build_pvgc2_100g_report(
        results,
        profile_name
    )

    nutri_report = build_pvgc2_nutri_report(
        results,
        profile_name
    )

    # -----------------------------
    # Exportación Excel
    # -----------------------------

    export_excel(
        results,
        output_file,
        profile_name
    )

    # -----------------------------
    # Resultado pipeline
    # -----------------------------

    return {
        "results": results,
        "area_report": area_report,
        "report_100g": report_100g,
        "nutri_report": nutri_report,
        "output_file": output_file
    }