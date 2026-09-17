from pathlib import Path


def discover_reports(root_folder: str):

    root = Path(root_folder)

    reports = []

    for folder in root.rglob("*.D"):

        report_file = folder / "Report01.xls"

        if report_file.exists():

            reports.append(
                {
                    "sample_id": folder.stem,
                    "report_file": str(report_file)
                }
            )

    reports.sort(
        key=lambda x: x["sample_id"]
    )

    return reports
