from openpyxl import Workbook

from reports.pvgc2_nutri_report import (
    build_pvgc2_nutri_report
)


def export_nutri_excel(
    nutri_report,
    filename
):

    wb = Workbook()

    ws = wb.active

    ws.title = (
        "INS_PERFMIX37_NUTRI"
    )

    ws.append(
        list(nutri_report.columns)
    )

    for _, row in nutri_report.iterrows():

        ws.append(
            list(row)
        )

    wb.save(filename)

    return filename