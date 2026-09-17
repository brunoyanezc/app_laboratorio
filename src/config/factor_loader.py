import pandas as pd


def load_tcf():

    return pd.read_csv(
        "src/config/tcf.csv"
    )


def load_ffax():

    return pd.read_csv(
        "src/config/ffax.csv"
    )


def load_factors():

    tcf = load_tcf()

    ffax = load_ffax()

    return tcf.merge(
        ffax,
        on="compound",
        how="inner"
    )