import pandas as pd

from parser.discover import discover_reports
from parser.report_reader import read_report


def build_dataset(root_folder):

    reports = discover_reports(root_folder)

    all_rows = []

    for report in reports:

        sample_id = report["sample_id"]

        result = read_report(
            report["report_file"]
        )

        df = result["data"].copy()

        df["sample_id"] = sample_id

        df["total_peak_response"] = (
            result["total_peak_response"]
        )

        all_rows.append(df)

    return pd.concat(
        all_rows,
        ignore_index=True
    )
