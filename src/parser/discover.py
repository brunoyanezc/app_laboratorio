from pathlib import Path


def discover_reports(root_folder: str):

    root = Path(root_folder)

    reports = []

    for folder in root.rglob("*.D"):

        report_file = folde* / "Report01.xls"

        if repo*t_file.exists():

            repo*ts.append(
                {
     *              "sample_id": folder.*tem,
                    "report_f*le": str(report_file)
            *   }
            )

    reports.so*t(key=lambda x: x["sample_id"])

 *  return reports
