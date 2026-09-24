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

    density = st.number_input(
        "Densidad",
        value=float(
            settings.get(
                "density",
                0.69663
            )
        ),
        format="%.5f"
    )

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

    c23_tag_factor = st.number_input(
        "Factor TAG→FAME C23",
        value=float(
            settings.get(
                "c23_tag_factor",
                1.0037
            )
        ),
        format="%.6f"
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
        "density": density,
        "purity": purity,
        "flask_volume_ml": flask_volume_ml,
        "stock_mass_g": stock_mass_g,
        "c23_tag_factor": c23_tag_factor
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
            "sample_id": "JOB",
            "sample_weight_g": "Peso muestra [g]",
            "c23_solution_weight_g": "Peso alícuota C23 [g]"
        }
    ),
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
                "JOB": "sample_id",
                "Peso muestra [g]":
                    "sample_weight_g",
                "Peso alícuota C23 [g]":
                    "c23_solution_weight_g"
            }
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
            density=density,
            purity=purity,
            flask_volume_ml=flask_volume_ml,
            stock_mass_g=stock_mass_g,
            c23_tag_factor=c23_tag_factor,
            filename=str(method_file)
        )

        report_file = (
            Path(temp_folder)
            / f"{Path(uploaded_file.name).stem}.xlsx"
        )

        pipeline_result = run_pipeline(
            temp_folder,
            str(parameter_file),
            str(method_file),
            str(report_file)
        )

        st.write(edited)
        edited.to_csv(
            "debug.csv",
            index=False
        )


        results = pipeline_result[
            "results"
        ]

        pvgc2_report = pipeline_result[
            "pvgc2_report"
        ]

        report_100g = pipeline_result[
            "report_100g"
        ]

        st.subheader(
            "Vista previa %Area"
        )

        st.dataframe(
            pvgc2_report,
            use_container_width=True
        )

        st.subheader(
            "Vista previa g/100g"
        )

        st.dataframe(
            report_100g,
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