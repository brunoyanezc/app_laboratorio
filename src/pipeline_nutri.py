from calculations.build_results import (
    build_results
)

from reports.pvgc2_nutri_report import (
    build_pvgc2_nutri_report
)


def run_nutri_pipeline(
    data_folder,
    profile_name,
    sample_parameters_file,
    method_file
):

    results = build_results(
        data_folder,
        sample_parameters_file,
        method_file
    )

    nutri_report = (
        build_pvgc2_nutri_report(
            results,
            profile_name
        )
    )

    return {
        "results": results,
        "nutri_report": nutri_report
    }