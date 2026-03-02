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
    "Activity Type",
    "OU 4",
    "Fecha_Vencimiento",
    "Comentarios"
]

if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

# ==============================
# FUNCION VALIDAR CSV
# ==============================

def validar_columnas(df):
    columnas_faltantes = [c for c in COLUMNAS_REQUERIDAS if c not in df.columns]
    return columnas_faltantes

# ==============================
# SUBIDA DE ARCHIVO
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
            # Backup del archivo actual
            if os.path.exists(DATA_FILE):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = os.path.join(BACKUP_FOLDER, f"certificaciones_{timestamp}.csv")
                shutil.copy(DATA_FILE, backup_path)

            # Guardar nuevo archivo
            df_nuevo.to_csv(DATA_FILE, index=False)
            st.sidebar.success("Archivo actualizado correctamente ✅")
            st.rerun()

    except Exception as e:
        st.sidebar.error(f"Error al procesar el archivo: {e}")

# ==============================
# CARGA DE DATOS
# ==============================

if not os.path.exists(DATA_FILE):
    st.error("No existe certificaciones.csv")
    st.stop()

df = pd.read_csv(DATA_FILE)

# Convertir fecha
df["Fecha_Vencimiento"] = pd.to_datetime(df["Fecha_Vencimiento"], errors="coerce")

# ==============================
# EXPORTACIÓN
# ==============================

st.sidebar.download_button(
    "Descargar archivo actual",
    df.to_csv(index=False),
    "certificaciones_actual.csv",
    "text/csv"
)

# ==============================
# INFORMACIÓN DE ARCHIVOS
# ==============================

st.sidebar.markdown("---")
st.sidebar.subheader("Historial de Backups")

archivos_backup = sorted(os.listdir(BACKUP_FOLDER), reverse=True)

if archivos_backup:
    for archivo in archivos_backup[:5]:
        st.sidebar.write(archivo)
else:
    st.sidebar.write("Sin backups todavía")

# ==============================
# RESTO DE TU APP
# ==============================

st.title("Dashboard de Certificaciones")

st.write("Datos cargados correctamente ✅")

# Aquí sigue tu integración con el HTML
csv_string = df.to_csv(index=False)

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

st.components.v1.html(html_code, height=900, scrolling=True)
