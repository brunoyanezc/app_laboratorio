from parser.report01 import Report01Parser

REPORT_FILE = "Report01.xls"


def main():

    parser = Report01Parser(REPORT_FILE)

    sample = parser.parse()

    print()
    print("===== RESUMEN =====")
    print()

    print("TotalPeakResponse:", sample.total_peak_response)
    print("Area C23:", sample.area_c23)

    print()
    print("Primeros compuestos:")
    print()

    for peak in sample.peaks[:10]:

        print(
            peak.compound,
            peak.area,
            peak.ppm
        )


if __name__ == "__main__":
    main()
