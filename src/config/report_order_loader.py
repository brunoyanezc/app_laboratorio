import pandas as pd


def load_report_order():

    return pd.read_csv(
        "src/config/report_order.csv"
    )