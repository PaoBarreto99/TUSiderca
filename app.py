import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Configuración de página en ancho completo
st.set_page_config(layout="wide")

# 🔧 Estilos para pantalla completa sin márgenes ni header de Streamlit
st.markdown("""
<style>
/* Quitar padding del contenedor principal */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
}

/* Quitar padding del main */
.main {
    padding: 0rem !important;
}

/* Ocultar header y footer de Streamlit */
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 📄 Leer CSV original
# Asegúrate que el archivo "certificaciones.csv" esté en la misma carpeta que app.py
df = pd.read_csv("certificaciones.csv", encoding="latin-1")

# Convertir las columnas de fecha a datetime (sin cambiar el nombre que HTML espera)
# Suponemos que en el CSV vienen como: Fecha_certificacion y Fecha_vencimiento
df["Fecha_certificacion"] = pd.to_datetime(df["Fecha_certificacion"], errors="coerce")
df["Fecha_vencimiento"] = pd.to_datetime(df["Fecha_vencimiento"], errors="coerce")

# Si quieres, puedes formatear las fechas a string legible para el HTML
df["Fecha_certificacion"] = df["Fecha_certificacion"].dt.strftime("%Y-%m-%d")
df["Fecha_vencimiento"] = df["Fecha_vencimiento"].dt.strftime("%Y-%m-%d")

# Convertir el DataFrame a CSV en formato string para inyectarlo en el HTML
csv_string = df.to_csv(index=False)

# 📄 Cargar el HTML del dashboard
with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Inyectar los datos del CSV en una variable JavaScript global window.csvData
# para que el HTML/JS pueda leer el CSV y construir tablas y gráficos
html_code = html_code.replace(
    "</head>",
    "<script>window.csvData = `" + csv_string + "`;</script></head>"
)

# Renderizar el HTML dentro de Streamlit
components.html(html_code, height=1200, scrolling=True)
