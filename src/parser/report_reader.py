i*port xlrd
import pandas as pd


PE*KSUM_SHEET = "PeakSumCalcT1"


def*read_report(report_file: str):

  * workbook = xlrd.open_workbook(rep*rt_file)

    sheet = workbook.she*t_by_name(PEAKSUM_SHEET)

    reco*ds = []

    total_peak_response =*None

    for row in range(sheet.n*ows):

        values = [
        *   sheet.cell_value(row, col)
    *       for col in range(sheet.ncol*)
        ]

        header_name =*str(values[0]).strip()

        if*header_name == "TotPeakResponse":
*           total_peak_response = f*oat(values[1])

        compound =*str(values[2]).strip()

        if*not compound:
            continue*
        if compound == "segName":*            continue

        area*= 0.0
        ppm = 0.0

        t*y:
            area = float(values*6])
        except Exception:
    *       pass

        try:
        *   ppm = float(values[7])
        *xcept Exception:
            pass
*        records.append(
          * {
                "compound": com*ound,
                "area": area*
                "ppm": ppm,
     *          "is_internal_standard": *ompound == "C23:0"
            }
 *      )

    df = pd.DataFrame(rec*rds)

    return {
        "total_*eak_response": total_peak_response*
        "data": df
    }
