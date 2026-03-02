import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ==============================
# CARGA DE DATOS
# ==============================

df = pd.read_csv("certificaciones.csv", encoding="latin-1")

# Normalizar nombres si vienen distintos
df.rename(columns={
    "Fecha_vencimiento": "Fecha_Vencimiento",
    "Fecha_certificacion": "Fecha_Certificacion"
}, inplace=True)

# Convertir fecha
if "Fecha_Vencimiento" in df.columns:
    df["Fecha_Vencimiento"] = pd.to_datetime(
        df["Fecha_Vencimiento"],
        errors="coerce"
    )

# ==============================
# FILTRO ARRIBA (Certification Type)
# ==============================

st.title("Dashboard de Certificaciones")

if "Certification Type" in df.columns:

    col1, col2 = st.columns([2, 1])

    with col1:
        filtro_cert_type = st.multiselect(
            "Filtrar por Certification Type",
            sorted(df["Certification Type"].dropna().unique())
        )

    with col2:
        st.markdown(f"**Total registros:** {len(df)}")

    if filtro_cert_type:
        df = df[df["Certification Type"].isin(filtro_cert_type)]

st.markdown("---")

# ==============================
# INYECTAR CSV EN HTML
# ==============================

csv_string = df.to_csv(index=False)

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

components.html(html_code, height=1000, scrolling=True)
