import streamlit as st
import pandas as pd
import os
from datetime import datetime
import shutil

st.set_page_config(layout="wide")

# ==============================
# CONFIGURACIÓN
# ==============================

DATA_FILE = "certificaciones.csv"
BACKUP_FOLDER = "backup"

COLUMNAS_REQUERIDAS = [
    "Nombre",
    "SAP ID",
    "Certificacion",
    "Certification Type",
    "Activity Type",
    "OU 4",
    "Fecha_Vencimiento",
    "Comentarios"
]

if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

# ==============================
# VALIDAR CSV
# ==============================

def validar_columnas(df):
    return [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]

# ==============================
# UPLOAD + BACKUP
# ==============================

st.sidebar.header("Administración de Datos")

uploaded_file = st.sidebar.file_uploader(
    "Subir nuevo archivo CSV",
    type="csv"
)

if uploaded_file is not None:
    try:
        df_nuevo = pd.read_csv(uploaded_file)
        faltantes = validar_columnas(df_nuevo)

        if faltantes:
            st.sidebar.error(f"Faltan columnas: {faltantes}")
        else:
            if os.path.exists(DATA_FILE):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = os.path.join(
                    BACKUP_FOLDER,
                    f"certificaciones_{timestamp}.csv"
                )
                shutil.copy(DATA_FILE, backup_path)

            df_nuevo.to_csv(DATA_FILE, index=False)
            st.sidebar.success("Archivo actualizado correctamente ✅")
            st.rerun()

    except Exception as e:
        st.sidebar.error(f"Error: {e}")

# ==============================
# CARGA DE DATOS
# ==============================

if not os.path.exists(DATA_FILE):
    st.error("No existe certificaciones.csv")
    st.stop()

df = pd.read_csv(DATA_FILE)
df["Fecha_Vencimiento"] = pd.to_datetime(
    df["Fecha_Vencimiento"],
    errors="coerce"
)

# ==============================
# FILTRO ARRIBA (Certification Type)
# ==============================

st.title("Dashboard de Certificaciones")

col_filtro, col_info = st.columns([2, 1])

with col_filtro:
    filtro_cert_type = st.multiselect(
        "Filtrar por Certification Type",
        sorted(df["Certification Type"].dropna().unique())
    )

with col_info:
    st.markdown(f"**Total registros:** {len(df)}")

if filtro_cert_type:
    df = df[df["Certification Type"].isin(filtro_cert_type)]

st.markdown("---")

# ==============================
# EXPORTAR
# ==============================

st.download_button(
    "Exportar datos filtrados",
    df.to_csv(index=False),
    "certificaciones_filtradas.csv",
    "text/csv"
)

# ==============================
# INYECTAR EN HTML
# ==============================

csv_string = df.to_csv(index=False)

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

st.components.v1.html(html_code, height=900, scrolling=True)
