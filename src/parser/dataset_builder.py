import pandas as pd

from*discover import discover_reports
f*om report_reader import read_repor*


def build_dataset(root_folder: *tr):

    reports = discover_repor*s(root_folder)

    all_rows = []
*    for report in reports:

      * sample_id = report["sample_id"]

*       result = read_report(
     *      report["report_file"]
      * )

        df = result["data"]

 *      df["sample_id"] = sample_id
*        df["total_peak_response"] * result[
            "total_peak_r*sponse"
        ]

        all_row*.append(df)

    dataset = pd.conc*t(
        all_rows,
        ignor*_index=True
    )

    return data*et
