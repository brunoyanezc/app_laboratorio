import pandas as pd

from parser.dataset_builder import build_dataset

from config.factor_loader import (
    load_factors
)

from config.config_loader import (
    load_method_config,
    load_sample_parameters,
)

from calculations.c23 import (
    calculate_c23_concentration,
    calculate_added_c23_mass,
)

from calculations.quantification import (
    calculate_wfamex,
    calculate_wx,
    calculate_g100g,
)


def build_results(data_folder):

    # -------------------------
    # Datos cromatográficos
    # -------------------------

    dataset = build_dataset(data_folder)

    # -------------------------
    # Factores
    # -------------------------

    factors = load_factors()

    dataset = dataset.merge(
        factors,
        on="compound",
        how="left"
    )

    # -------------------------
    # Parámetros método
    # -------------------------

    method = load_method_config(
        "src/config/method.yaml"
    )

    samples = load_sample_parameters(
        "src/config/sample_parameters.csv"
    )

    # -------------------------
    # Concentración C23
    # -------------------------

    c23_cfg = method["c23"]

    c23_result = calculate_c23_concentration(
        stock_mass_g=c23_cfg["stock_mass_g"],
        flask_volume_ml=c23_cfg["flask_volume_ml"],
        density_g_ml=c23_cfg["density"],
        purity=c23_cfg["purity"],
    )

    concentration_g_g = (
        c23_result["concentration_g_g"]
    )

    # -------------------------
    # Agregar parámetros muestra
    # -------------------------

    dataset = dataset.merge(
        samples,
        on="sample_id",
        how="left"
    )

    dataset["mass_c23_added_g"] = (
        dataset["c23_solution_weight_g"]
        * concentration_g_g
    )

    # -------------------------
    # Área C23 por muestra
    # -------------------------

    c23_areas = (
        dataset.loc[
            dataset["compound"] == "C23:0",
            ["sample_id", "area"]
        ]
        .rename(
            columns={
                "area": "area_c23"
            }
        )
    )

    dataset = dataset.merge(
        c23_areas,
        on="sample_id",
        how="left"
    )

    # -------------------------
    # Cálculos
    # -------------------------

    dataset["wfamex"] = dataset.apply(
        lambda r: calculate_wfamex(
            area_x=r["area"],
            area_c23=r["area_c23"],
            mass_c23_added=r["mass_c23_added_g"],
            tcf=r["tcf"],
        ),
        axis=1
    )

    dataset["wx"] = dataset.apply(
        lambda r: calculate_wx(
            wfamex=r["wfamex"],
            ffax=r["ffax"],
        ),
        axis=1
    )

    dataset["g100g"] = dataset.apply(
        lambda r: calculate_g100g(
            wx=r["wx"],
            sample_weight_g=r["sample_weight_g"],
        ),
        axis=1
    )

    return dataset