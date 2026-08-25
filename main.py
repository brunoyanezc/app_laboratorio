import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Librerías de ReportLab para diseñar el PDF desde código puro
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ----------------------------------------------------
# CONFIGURACIÓN DE LA INTERFAZ
# ----------------------------------------------------
st.set_page_config(page_title="API In-House - Impresión Labs", layout="wide", page_icon="🧪")

st.title("🧪 API In-House: Emisor de Informes de Laboratorio")
st.write("Generación automatizada de PDFs a partir de planillas de datos.")

# ----------------------------------------------------
# FUNCIONES NATIVAS (NUESTRA "API" INTERNA)
# ----------------------------------------------------
def transformar_link_onedrive(url):
    """Transforma el link visual de OneDrive en un link de descarga directa para Python."""
    if ":x:" in url:
        return url.replace(":x:", ":x:?download=1").split("&")[0]
    return url

def generar_pdf_laboratorio(datos_fila):
    """
    Construye el PDF en la memoria del servidor de forma dinámica.
    Modifica las claves según los nombres de columna reales de tu Excel.
    """
    buffer = BytesIO()
    # Márgenes del documento de 40 puntos
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []

    # Estilos de texto
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'TituloLab',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1A365D"),
        alignment=1
    )
    texto_style = ParagraphStyle(
        'TextoLab',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#2D3748")
    )

    # 1. Encabezado del PDF
    story.append(Paragraph("<b>INFORME DE RESULTADOS DE LABORATORIO</b>", titulo_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Documento emitido de manera automatizada a través de la API In-House.", texto_style))
    story.append(Spacer(1, 25))

    # 2. Estructura de la Tabla de Datos (Ajusta los nombres a tu Excel real)
    tabla_datos = [
        [Paragraph("<b>Identificador / Campo</b>", texto_style), Paragraph("<b>Detalle Registrado</b>", texto_style)],
        [Paragraph("<b>Paciente:</b>", texto_style), Paragraph(str(datos_fila.get("Paciente", "N/A")), texto_style)],
        [Paragraph("<b>Tipo de Examen:</b>", texto_style), Paragraph(str(datos_fila.get("Examen", "N/A")), texto_style)],
        [Paragraph("<b>Resultado Analítico:</b>", texto_style), Paragraph(str(datos_fila.get("Resultado", "N/A")), texto_style)],
        [Paragraph("<b>Observaciones Médicas:</b>", texto_style), Paragraph(str(datos_fila.get("Observaciones", "-")), texto_style)]
    ]

    # Configuración de ancho de columnas y estilos visuales
    t = Table(tabla_datos, colWidths=[150, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#2B6CB0")), # Encabezado Azul
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")), # Bordes grises
    ]))

    story.append(t)
    doc.build(story)
    buffer.seek(0)
    return buffer

# ----------------------------------------------------
# FLUJO DE LA PLATAFORMA WEB
# ----------------------------------------------------
# Control lateral para elegir método de entrada de datos
metodo_entrada = st.sidebar.radio("Método de conexión de datos:", ["Link de OneDrive corporativo", "Subir archivo Excel (.xlsx)"])

df = None

if metodo_entrada == "Link de OneDrive corporativo":
    enlace_input = st.text_input("Pega el enlace de compartir de tu Excel aquí:", placeholder="https://sharepoint.com...")
    if enlace_input:
        try:
            url_directa = transformar_link_onedrive(enlace_input)
            respuesta = requests.get(url_directa)
            df = pd.read_excel(BytesIO(respuesta.content))
            st.success("⚡ Conexión exitosa con el DataSheet en la nube.")
        except Exception as e:
            st.error(f"Error de acceso. Si tu empresa restringe el link, usa la opción lateral 'Subir archivo Excel'. Detalles: {e}")

else:
    archivo_subido = st.file_uploader("Arrastra tu reporte de laboratorios en formato Excel:", type=["xlsx"])
    if archivo_subido:
        try:
            df = pd.read_excel(archivo_subido)
            st.success("⚡ Archivo cargado en memoria correctamente.")
        except Exception as e:
            st.error(f"Error leyendo el archivo local: {e}")

# ----------------------------------------------------
# RENDERIZADO Y ACCIONES DE IMPRESIÓN
# ----------------------------------------------------
if df is not None:
    st.subheader("📋 Vista previa del DataSheet")
    st.dataframe(df, use_container_width=True)

    st.subheader("🖨️ Cola de Impresión Dinámica")
    st.write("Selecciona el paciente para generar y descargar su informe en formato PDF listo para imprimir.")

    # Crear la lista interactiva de pacientes
    for indice, fila in df.iterrows():
        col_id, col_nombre, col_accion = st.columns([1, 4, 2])

        with col_id:
            st.write(f"**ID:** {indice}")
        with col_nombre:
            st.write(f"👤 **Paciente:** {fila.get('Paciente', 'No definido')}")
        with col_accion:
            # Generar el binario del PDF exclusivo para esta fila
            pdf_bytes = generar_pdf_laboratorio(fila)

            st.download_button(
                label="📄 Generar PDF",
                data=pdf_bytes,
                file_name=f"Informe_{fila.get('Paciente', indice)}.pdf",
                mime="application/pdf",
                key=f"btn_{indice}"
            )
else:
    st.info("Esperando carga de datos desde el menú seleccionado para inicializar la API...")