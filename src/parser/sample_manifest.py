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
                "JOB": report[
                    "sample_id"
                ],
                "Peso muestra [g]": None,
                "Peso C23 ISTD [g]": None
            }
        )

    return pd.DataFrame(rows)