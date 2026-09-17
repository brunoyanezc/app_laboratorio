import pandas as pd


def save_runtime_parameters(
    dataframe,
    filename
):

    dataframe.to_csv(
        filename,
        index=False
    )


def load_runtime_parameters(
    filename
):

    return pd.read_csv(
        filename
    )