import xlrd
import pandas as pd


def read_peaksumcalc(report_file):

    workbook = xlrd.open_workbook(report_file)

    sheet = workbook.sheet_by_name("PeakSumCalcT1")

    data = []
    total_peak_response = None

    for row in range(sheet.nrows):

        values = [
            sheet.cell_value(row, col)
            for col in range(sheet.ncols)
        ]

        if str(values[0]).strip() == "TotPeakResponse":
            total_peak_response = float(values[1])

        compound = str(values[2]).strip()

        if not compound:
            continue

        try:
            area = float(values[6])
        except Exception:
            area = 0.0

        try:
            ppm = float(values[7])
        except Exception:
            ppm = 0.0

        data.append(
            {
                "compound": compound,
                "area": area,
                "ppm": ppm
            }
        )

    df = pd.DataFrame(data)

    return df, total_peak_response
