import pandas as pd

from parser.dataset_builder import (
    build_dataset
)

from config.factor_loader import (
    load_factors
)

from config.config_loader import (
    load_method_config,
    load_sample_parameters,
)

from calculations.c23 import (
    calculate_c23_concentration,
)

from calculations.quantification import (
    calculate_wfamex,
    calculate_wx,
    calculate_g100g,
)


def build_results(
    data_folder,
    sample_parameters_file,
    method_file
):

    # ----------------------------------
    # Datos cromatográficos
    # ----------------------------------

    dataset = build_dataset(
        data_folder
    )

    # ----------------------------------
    # Factores TCF / FFAx
    # ----------------------------------

    factors = load_factors()

    dataset = dataset.merge(
        factors,
        on="compound",
        how="left"
    )

    # ----------------------------------
    # Configuración método
    # ----------------------------------

    method = load_method_config(
        method_file
    )

    samples = load_sample_parameters(
        sample_parameters_file
    )

    c23_cfg = method["c23"]

    # ----------------------------------
    # Concentración C23
    # ----------------------------------

    c23_result = calculate_c23_concentration(
        stock_mass_g=c23_cfg["stock_mass_g"],
        flask_volume_ml=c23_cfg["flask_volume_ml"],
        density_g_ml=c23_cfg["density"],
        purity=c23_cfg["purity"],
    )

    concentration_g_g = (
        c23_result["concentration_g_g"]
    )

    solvent_mass_g = (
        c23_result["solvent_mass_g"]
    )

    # ----------------------------------
    # Parámetros método
    # ----------------------------------

    dataset["c23_density"] = (
        c23_cfg["density"]
    )

    dataset["c23_purity"] = (
        c23_cfg["purity"]
    )

    dataset["c23_flask_volume_ml"] = (
        c23_cfg["flask_volume_ml"]
    )

    dataset["c23_stock_mass_g"] = (
        c23_cfg["stock_mass_g"]
    )

    dataset["c23_solvent_mass_g"] = (
        solvent_mass_g
    )

    dataset["c23_concentration_g_g"] = (
        concentration_g_g
    )

    # ----------------------------------
    # Parámetros muestra
    # ----------------------------------

    dataset = dataset.merge(
        samples,
        on="sample_id",
        how="left"
    )

    # ----------------------------------
    # Masa C23 agregada
    # ----------------------------------

    dataset["mass_c23_added_g"] = (
        dataset["c23_solution_weight_g"]
        * dataset["c23_concentration_g_g"]
    )

    # ----------------------------------
    # Área C23 por muestra
    # ----------------------------------

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

    # ----------------------------------
    # WFAMEx
    # ----------------------------------

    dataset["wfamex"] = dataset.apply(
        lambda r: calculate_wfamex(
            area_x=r["area"],
            area_c23=r["area_c23"],
            mass_c23_added=r["mass_c23_added_g"],
            tcf=r["tcf"],
        ),
        axis=1
    )

    # ----------------------------------
    # Wx
    # ----------------------------------

    dataset["wx"] = dataset.apply(
        lambda r: calculate_wx(
            wfamex=r["wfamex"],
            ffax=r["ffax"],
        ),
        axis=1
    )

    # ----------------------------------
    # g/100g
    # ----------------------------------

    dataset["g100g"] = dataset.apply(
        lambda r: calculate_g100g(
            wx=r["wx"],
            sample_weight_g=r["sample_weight_g"],
        ),
        axis=1
    )

    # ----------------------------------
    # %FAME
    # Excluye C23 del denominador
    # ----------------------------------

    dataset["fame_denominator"] = None
    dataset["fame_percent"] = None

    for sample_id in dataset["sample_id"].unique():

        sample_mask = (
            dataset["sample_id"] == sample_id
        )

        sample_df = dataset.loc[
            sample_mask
        ]

        denominator = (
            sample_df.loc[
                sample_df["compound"] != "C23:0",
                "area"
            ].sum()
        )

        dataset.loc[
            sample_mask,
            "fame_denominator"
        ] = denominator

        dataset.loc[
            sample_mask,
            "fame_percent"
        ] = (
            dataset.loc[
                sample_mask,
                "area"
            ]
            / denominator
            * 100
        )

        dataset.loc[
            sample_mask
            &
            (dataset["compound"] == "C23:0"),
            "fame_percent"
        ] = 0

    # ----------------------------------
    # Flags
    # ----------------------------------

    dataset["is_internal_standard"] = (
        dataset["compound"] == "C23:0"
    )

    dataset["is_unknown"] = (
        dataset["compound"]
        .astype(str)
        .str.lower()
        .isin(
            [
                "unknown",
                "unknow",
                "-"
            ]
        )
    )

    return dataset