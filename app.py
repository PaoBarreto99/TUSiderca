import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# -------------------------
# CARGA DE DATOS
# -------------------------
df = pd.read_csv("certificaciones.csv", encoding="latin-1")

# Unificar nombres de columnas
df.rename(columns={
    "Fecha_vencimiento": "Fecha_Vencimiento",
    "Fecha_certificacion": "Fecha_Certificacion"
}, inplace=True)

df["Fecha_Vencimiento"] = pd.to_datetime(df["Fecha_Vencimiento"], errors="coerce")

# -------------------------
# FILTROS
# -------------------------
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1.2])

with col1:
    filtro_cert = st.multiselect("", sorted(df["Certificacion"].dropna().unique()), placeholder="Certificación")

with col2:
    filtro_estado = st.multiselect("", ["Vigente","Por Vencer","Vencida"], placeholder="Estado")

with col3:
    filtro_activity = st.multiselect("", sorted(df["Activity Type"].dropna().unique()), placeholder="Activity Type")

with col4:
    fecha_min = df["Fecha_Vencimiento"].min()
    fecha_max = df["Fecha_Vencimiento"].max()
    filtro_fecha = st.date_input("", value=(fecha_min, fecha_max))

with col5:
    borrar = st.button("Borrar filtros", use_container_width=True)

# -------------------------
# APLICAR FILTROS
# -------------------------
df_filtrado = df.copy()

if filtro_cert:
    df_filtrado = df_filtrado[df_filtrado["Certificacion"].isin(filtro_cert)]

if filtro_activity:
    df_filtrado = df_filtrado[df_filtrado["Activity Type"].isin(filtro_activity)]

if isinstance(filtro_fecha, tuple):
    df_filtrado = df_filtrado[
        (df_filtrado["Fecha_Vencimiento"] >= pd.to_datetime(filtro_fecha[0])) &
        (df_filtrado["Fecha_Vencimiento"] <= pd.to_datetime(filtro_fecha[1]))
    ]

# -------------------------
# DASHBOARD
# -------------------------
csv_string = df_filtrado.to_csv(index=False)

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

components.html(html_code, height=950, scrolling=True)

# -------------------------
# BORRAR
# -------------------------
if borrar:
    st.rerun()
