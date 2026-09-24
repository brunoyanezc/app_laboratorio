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

    print()
    print("SAMPLES COLUMNS:")
    print(samples.columns.tolist())
    print()

    c23_cfg = method["c23"]

    from config.profile_loader import (
    load_profile
    )

    profile = load_profile(
    "PVGC2"
    )

    c23_tag_factor = profile.get(
        "c23_tag_factor",
        1.0
    )
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
        c23_tag_factor=c23_tag_factor,
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
    # Base Excel:
    #
    # At sin NI = suma áreas identificadas
    #             incluyendo C23
    #
    # %AG       = suma ppm identificados
    #
    # At con NI = 100 * At sin NI / %AG
    #
    # Denominador %Area reportado =
    # At con NI - Área C23
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

        c23_area = (
            sample_df.loc[
                sample_df["compound"] == "C23:0",
                "area"
            ].sum()
        )

        # -----------------------------
        # At sin NI
        # Incluye C23
        # -----------------------------


        at_sin_ni = (
            sample_df["area"].sum()
        )

        # -----------------------------
        # %AG
        # Suma %Area GC identificados
        # -----------------------------

        percent_ag = (
            sample_df["ppm"].sum()
        )

        # -----------------------------
        # At con NI
        # -----------------------------

        at_con_ni = (
            100
            * at_sin_ni
            / percent_ag
        )

        # -----------------------------
        # Área NI
        # -----------------------------

        unknown_area = (
            at_con_ni
            - at_sin_ni
        )

        # -----------------------------
        # % NI
        # -----------------------------

        unknown_percent = (
            100
            - percent_ag
        )

        # -----------------------------
        # Denominador reportado
        # Excluye C23
        # -----------------------------

        denominator = (
            at_con_ni
            - c23_area
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

        # C23 siempre reporta 0 %

        dataset.loc[
            sample_mask
            &
            (dataset["compound"] == "C23:0"),
            "fame_percent"
        ] = 0

        # Si la fila Unknow ya existe

        dataset.loc[
            sample_mask
            &
            (
                dataset["compound"]
                .astype(str)
                .str.lower()
                == "unknow"
            ),
            "area"
        ] = unknown_area


        dataset.loc[
            sample_mask
            &
            (
                dataset["compound"]
                .astype(str)
                .str.lower()
                == "unknow"
            ),
            "fame_percent"
        ] = unknown_percent

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

    unknown_rows = []

    for sample_id in dataset["sample_id"].unique():

        sample_df = dataset.loc[
            dataset["sample_id"] == sample_id
        ]

        c23_area = (
            sample_df.loc[
                sample_df["compound"] == "C23:0",
                "area"
            ].sum()
        )

        at_sin_ni = (
            sample_df["area"].sum()
        )

        percent_ag = (
            sample_df["ppm"].sum()
        )

        at_con_ni = (
            100
            * at_sin_ni
            / percent_ag
        )

        unknown_area = (
            at_con_ni
            - at_sin_ni
        )

        unknown_percent = (
            100
            - percent_ag
        )

        template = (
            sample_df.iloc[0]
            .copy()
        )

        template["compound"] = "Unknow"

        template["area"] = unknown_area

        template["fame_percent"] = (
            unknown_percent
        )

        template["wfamex"] = 0

        template["wx"] = 0

        template["g100g"] = 0

        unknown_rows.append(
            template
        )

    dataset = pd.concat(
        [
            dataset,
            pd.DataFrame(
                unknown_rows
            )
        ],
        ignore_index=True
    )

    return dataset