import yaml
import pandas as pd


def load_method_config(filename):

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as f:

        return yaml.safe_load(f)


def load_sample_parameters(
    filename="src/config/sample_parameters.csv"
):

    return pd.read_csv(filename)