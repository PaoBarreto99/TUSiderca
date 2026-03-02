import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# -------------------------
# CARGA DE DATOS
# -------------------------
df = pd.read_csv("certificaciones.csv", encoding="latin-1")

# Convertir fecha
df["Fecha_vencimiento"] = pd.to_datetime(df["Fecha_vencimiento"], errors="coerce")

st.title("📋 Dashboard de Certificaciones")

st.markdown("### 🔎 Filtros")

# -------------------------
# FILTROS (UNO POR COLUMNA)
# -------------------------

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7 = st.columns(1)[0]

with col1:
    filtro_nombre = st.multiselect(
        "Nombre",
        sorted(df["Nombre"].dropna().unique())
    )

with col2:
    filtro_sap = st.multiselect(
        "SAP ID",
        sorted(df["SAP ID"].dropna().unique())
    )

with col3:
    filtro_cert = st.multiselect(
        "Certificacion",
        sorted(df["Certificacion"].dropna().unique())
    )

with col4:
    filtro_activity = st.multiselect(
        "Activity Type",
        sorted(df["Activity Type"].dropna().unique())
    )

with col5:
    filtro_estado = st.multiselect(
        "Estado",
        sorted(df["Estado"].dropna().unique())
    )

with col6:
    fecha_min = df["Fecha_vencimiento"].min()
    fecha_max = df["Fecha_vencimiento"].max()

    filtro_fecha = st.date_input(
        "Rango Fecha Vencimiento",
        value=(fecha_min, fecha_max)
    )

with col7:
    filtro_comentarios = st.multiselect(
        "Comentarios",
        sorted(df["Comentarios"].dropna().unique())
    )

# -------------------------
# APLICAR FILTROS
# -------------------------

df_filtrado = df.copy()

if filtro_nombre:
    df_filtrado = df_filtrado[df_filtrado["Nombre"].isin(filtro_nombre)]

if filtro_sap:
    df_filtrado = df_filtrado[df_filtrado["SAP ID"].isin(filtro_sap)]

if filtro_cert:
    df_filtrado = df_filtrado[df_filtrado["Certificacion"].isin(filtro_cert)]

if filtro_activity:
    df_filtrado = df_filtrado[df_filtrado["Activity Type"].isin(filtro_activity)]

if filtro_estado:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(filtro_estado)]

if filtro_comentarios:
    df_filtrado = df_filtrado[df_filtrado["Comentarios"].isin(filtro_comentarios)]

# Filtro por fecha
if isinstance(filtro_fecha, tuple) and len(filtro_fecha) == 2:
    df_filtrado = df_filtrado[
        (df_filtrado["Fecha_vencimiento"] >= pd.to_datetime(filtro_fecha[0])) &
        (df_filtrado["Fecha_vencimiento"] <= pd.to_datetime(filtro_fecha[1]))
    ]

st.markdown("---")

# -------------------------
# BOTONES
# -------------------------

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    st.download_button(
        "Exportar datos",
        df_filtrado.to_csv(index=False),
        "certificaciones.csv",
        "text/csv"
    )

with col_btn2:
    if st.button("Borrar filtros"):
        st.experimental_rerun()

st.markdown("---")

# -------------------------
# ENVIAR DATOS AL HTML
# -------------------------

csv_string = df_filtrado.to_csv(index=False)

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

components.html(html_code, height=1200, scrolling=True)
