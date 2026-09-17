import pandas as pd

from config.report_order_loader import (
    load_report_order
)


def build_client_report(df):

    report_order = load_report_order()

    report = df.copy()

    # -------------------------
    # Merge orden oficial
    # -------------------------

    report = report.merge(
        report_order,
        on="compound",
        how="left"
    )

    # -------------------------
    # Ordenar según plantilla
    # -------------------------

    report = report.sort_values(
        [
            "sample_id",
            "report_order"
        ]
    )

    # -------------------------
    # Redondeos cliente
    # -------------------------

    report["fame_percent"] = (
        report["fame_percent"]
        .fillna(0)
        .round(2)
    )

    report["g100g"] = (
        report["g100g"]
        .fillna(0)
        .round(3)
    )

    # -------------------------
    # Selección final
    # -------------------------

    report = report[
        [
            "sample_id",
            "compound",
            "fame_percent",
            "g100g"
        ]
    ].copy()

    return report