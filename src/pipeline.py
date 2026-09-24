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


def run_pipeline(
    data_folder,
    sample_parameters_file,
    method_file,
    output_file,
    profile_name
):

    results = build_results(
        data_folder,
        sample_parameters_file,
        method_file
    )

    pvgc2_report = build_pvgc2_report(
        results,
        profile_name
    )

    report_100g = build_pvgc2_100g_report(
        results,
        profile_name
    )

    export_excel(
    results,
    output_file,
    profile_name
)

    return {
        "results": results,
        "pvgc2_report": pvgc2_report,
        "report_100g": report_100g,
        "output_file": output_file
    }