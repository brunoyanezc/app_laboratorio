import xlrd
import pandas as pd


PEAKSUM_SHEET = "PeakSumCalcT1"


def read_report(report_file: str):

    workbook = xlrd.open_workbook(report_file)

    sheet = workbook.sheet_by_name(PEAKSUM_SHEET)

    rows = []

    total_peak_response = None

    for row_idx in range(sheet.nrows):

        values = [
            sheet.cell_value(row_idx, col_idx)
            for col_idx in range(sheet.ncols)
        ]

        header_name = str(values[0]).strip()

        if header_name == "TotPeakResponse":
            total_peak_response = float(values[1])

        compound = str(values[2]).strip()

        if not compound:
            continue

        if compound == "segName":
            continue

        try:
            area = float(values[6])
        except Exception:
            area = 0.0

        try:
            ppm = float(values[7])
        except Exception:
            ppm = 0.0

        rows.append(
            {
                "compound": compound,
                "area": area,
                "ppm": ppm,
                "is_internal_standard": compound == "C23:0"
            }
        )

    df = pd.DataFrame(rows)

    return {
        "total_peak_response": total_peak_response,
        "data": df
    }
