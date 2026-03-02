import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(layout="wide")

# -------------------------
# CARGA DE DATOS
# -------------------------
df = pd.read_csv("certificaciones.csv", encoding="latin-1")

# -------------------------
# SIDEBAR - FILTROS
# -------------------------
st.sidebar.header("Filtros")

empresa = st.sidebar.multiselect(
    "Empresa",
    sorted(df["Empresa"].dropna().unique())
)

estado = st.sidebar.multiselect(
    "Estado",
    sorted(df["Estado"].dropna().unique())
)

area = st.sidebar.multiselect(
    "Área",
    sorted(df["Área"].dropna().unique())
)

# -------------------------
# APLICAR FILTROS
# -------------------------
df_filtrado = df.copy()

if empresa:
    df_filtrado = df_filtrado[df_filtrado["Empresa"].isin(empresa)]

if estado:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estado)]

if area:
    df_filtrado = df_filtrado[df_filtrado["Área"].isin(area)]

# -------------------------
# BOTÓN BORRAR FILTROS
# -------------------------
if st.sidebar.button("🧹 Borrar filtros"):
    st.experimental_rerun()

# -------------------------
# BOTÓN DESCARGAR FILTRADOS
# -------------------------
st.download_button(
    label="📥 Descargar datos filtrados",
    data=df_filtrado.to_csv(index=False),
    file_name="certificaciones_filtradas.csv",
    mime="text/csv"
)

# -------------------------
# INYECTAR DATOS FILTRADOS EN HTML
# -------------------------
csv_string = df_filtrado.to_csv(index=False)

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

components.html(html_code, height=1200, scrolling=True)
