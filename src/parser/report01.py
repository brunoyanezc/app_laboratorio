import xlrd

from models.sample import Peak, Sample


class Report01Parser:

    SHEET_NAME = "PeakSumCalcT1"

    def __init__(self, filename: str):
        self.filename = filename

    def parse(self) -> Sample:

        wb = xlrd.open_workbook(self.filename)

        sheet = wb.sheet_by_name(self.SHEET_NAME)

        peaks = []
        total_peak_response = 0.0
        area_c23 = None

        for row in range(sheet.nrows):

            values = [
                sheet.cell_value(row, col)
                for col in range(sheet.ncols)
            ]

            # TotPeakResponse
            if row >= 0:

                label = str(values[0]).strip()

                if label == "TotPeakResponse":
                    total_peak_response = float(values[1])

            seg_name = str(values[2]).strip()

            if not seg_name:
                continue

            try:
                area = float(values[6])
            except Exception:
                area = 0.0

            try:
                ppm = float(values[7])
            except Exception:
                ppm = 0.0

            peaks.append(
                Peak(
                    compound=seg_name,
                    area=area,
                    ppm=ppm
                )
            )

            if seg_name == "C23:0":
                area_c23 = area

        return Sample(
            sample_id="UNKNOWN",
            total_peak_response=total_peak_response,
            area_c23=area_c23,
            peaks=peaks
        )
