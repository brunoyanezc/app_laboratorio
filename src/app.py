import streamlit as st
from pathlib import Path

from parser.zip_loader import (
    extract_zip
)

from parser.sample_manifest import (
    create_manifest
)

from config.runtime_parameters import (
    save_runtime_parameters
)

from calculations.build_results import (
    build_results
)

from reports.excel_export import (
    export_excel
)

from config.settings_manager import (
load_settings,
save_settings
)

from config.runtime_method import (
    create_runtime_method_file
)

from reports.pvgc2_report import (
    build_pvgc2_report
)

from reports.pvgc2_100g_report import (
    build_pvgc2_100g_report
)

from pipeline import (
    run_pipeline
)

from config.profile_loader import (
    load_profile
)

from pipeline_nutri import (
    run_nutri_pipeline
)

from reports.nutri_excel_export import (
    export_nutri_excel
)

from reports.nutri_excel_export import (
    export_nutri_excel
)

st.set_page_config(
    page_title="Planilla PAG [g/100g]",
    layout="wide"
)

settings = load_settings()

profile_name = st.sidebar.selectbox(
    "Perfil",
    [
        "PVGC2",
        "PVGC1",
        "VitaproGC1",
        "TerramarGC1"
    ]
)

profile = load_profile(
    profile_name
)

with st.sidebar.expander(
    "⚙ Opciones Avanzadas",
    expanded=False
):

    purity = st.number_input(
        "Pureza",
        value=float(
            settings.get(
                "purity",
                0.99
            )
        ),
        format="%.5f"
    )

    flask_volume_ml = st.number_input(
        "Aforo (mL)",
        value=float(
            settings.get(
                "flask_volume_ml",
                10
            )
        )
    )

    stock_mass_g = st.number_input(
        "Peso C23 (g)",
        value=float(
            settings.get(
                "stock_mass_g",
                0.1035
            )
        ),
        format="%.7f"
    )

st.sidebar.divider()
st.sidebar.caption(
"Versión 0.1.0"
)
st.sidebar.markdown("---")

if st.sidebar.button(
    "Guardar configuración"
):

    save_settings(
    {
        "profile": profile_name,
        "purity": purity,
        "flask_volume_ml": flask_volume_ml,
        "stock_mass_g": stock_mass_g
    }
)

    st.sidebar.success(
        "Configuración guardada"
    )

st.title("Planilla PAG [g/100g]")

st.markdown(
    """
    <div style="
        position:absolute;
        top:0px;
        right:25px;
        text-align:right;
        font-size:11px;
        line-height:1.1;
    ">
    <b>Bruno Yáñez C.</b><br>
    Ingeniero de Investigación y Desarrollo, MSc<br>
    R&D Projects
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Cargar ZIP de muestras",
    type=["zip"]
)

if uploaded_file:

    temp_folder = extract_zip(
        uploaded_file
    )

    manifest = create_manifest(
        temp_folder
    )

    st.subheader(
        "Muestras detectadas"
    )

    edited = st.data_editor(
        manifest.rename(
            columns={
                "order": "Orden",
                "sample_id": "JOB",
                "sample_weight_g": "Peso muestra [g]",
                "c23_solution_weight_g": "Peso alícuota C23 [g]"
            }
        ),
        column_config={
            "Orden": st.column_config.NumberColumn(
                "Orden",
                min_value=1,
                step=1
            )
        },
        hide_index=True,
        use_container_width=True,
        num_rows="fixed"
    )

    if st.button(
        "Procesar"
    ):

        parameter_file = (
            Path(temp_folder)
            / "sample_parameters.csv"
        )

        edited = edited.rename(
            columns={
                "Orden": "order",
                "JOB": "sample_id",
                "Peso muestra [g]": "sample_weight_g",
                "Peso alícuota C23 [g]": "c23_solution_weight_g"
                }
        )

        edited["order"] = (
            edited["order"]
            .astype(int)
        )

        edited = edited.sort_values(
            "order"
        ).reset_index(
            drop=True
        )

        save_runtime_parameters(
            edited,
            parameter_file
        )

        method_file = (
            Path(temp_folder)
            / "method_runtime.yaml"
        )

        create_runtime_method_file(
            density=profile["density"],
            purity=purity,
            flask_volume_ml=flask_volume_ml,
            stock_mass_g=stock_mass_g,
            c23_tag_factor=profile["c23_tag_factor"],
            filename=str(method_file)
        )

        report_file = (
            Path(temp_folder)
            / f"{Path(uploaded_file.name).stem}.xlsx"
        )

        has_weights = (
            edited["sample_weight_g"]
            .astype(str)
            .str.strip()
            .ne("")
            .all()
            and
            edited["c23_solution_weight_g"]
            .astype(str)
            .str.strip()
            .ne("")
            .all()
        )

        if has_weights:

            pipeline_result = run_pipeline(
                temp_folder,
                str(parameter_file),
                str(method_file),
                str(report_file),
                profile_name
            )

            results = pipeline_result[
                "results"
            ]

            area_report = pipeline_result[
                "area_report"
            ]

            report_100g = pipeline_result[
                "report_100g"
            ]

            nutri_report = pipeline_result[
                "nutri_report"
            ]

            st.subheader(
                "AFOCR_AC_GRASOS_A"
            )

            st.data_editor(
                area_report,
                hide_index=True,
                use_container_width=True
            )

            st.subheader(
                "AFOCR_AC_GRASOS_100G"
            )

            st.data_editor(
                report_100g,
                hide_index=True,
                use_container_width=True
            )

        else:

            st.info(
                "No se ingresaron pesos. "
                "Se generará únicamente INS_PERFMIX37_NUTRI."
            )

            pipeline_result = run_nutri_pipeline(
                temp_folder,
                profile_name,
                str(parameter_file),
                str(method_file)
            )

            nutri_report = pipeline_result[
                "nutri_report"
            ]

            report_file = (
                Path(temp_folder)
                / f"{Path(uploaded_file.name).stem}_NUTRI.xlsx"
            )

            export_nutri_excel(
                nutri_report,
                str(report_file)
            )

        st.subheader(
            "INS_PERFMIX37_NUTRI"
        )

        st.data_editor(
            nutri_report,
            hide_index=True,
            use_container_width=True
        )

        with open(
            report_file,
            "rb"
        ) as f:

            report_bytes = f.read()

        st.download_button(
            "Descargar Excel",
            data=report_bytes,
            file_name=report_file.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success(
            "Proceso finalizado"
        )