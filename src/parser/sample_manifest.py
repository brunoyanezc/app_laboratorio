import pandas as pd

from parser.discover import (
    discover_reports
)


def create_manifest(root_folder):

    reports = discover_reports(
        root_folder
    )

    rows = []

    for report in reports:

        rows.append(
            {
                "sample_id": report[
                    "sample_id"
                ],
                "sample_weight_g": None,
                "c23_solution_weight_g": None
            }
        )

    return pd.DataFrame(rows)