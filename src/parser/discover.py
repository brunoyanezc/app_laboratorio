from pathlib import Path


def discover_reports(root_folder: str):
    """
    Busca recursivamente carpetas *.D que contengan Report01.xls
    """

    root = Path(root_folder)

    samples = []

    for folder in root.rglob("*.D"):

        report_file = folder / "Report01.xls"

        if report_file.exists():

            samples.append(
                {
                    "sample_id": folder.stem,
                    "folder": str(folder),
                    "report_file": str(report_file)
                }
            )

    return sorted(samples, key=lambda x: x["sample_id"])
