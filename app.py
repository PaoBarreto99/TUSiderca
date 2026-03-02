import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# -------------------------
# CARGA DE DATOS
# -------------------------
df = pd.read_csv("certificaciones.csv", encoding="latin-1")
df["Fecha_vencimiento"] = pd.to_datetime(df["Fecha_vencimiento"], errors="coerce")

st.title("Dashboard de Certificaciones")

# -------------------------
# FILTROS HORIZONTALES
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    certificacion = st.multiselect(
        "Certificación",
        sorted(df["Certificacion"].dropna().unique())
    )

with col2:
    estado = st.multiselect(
        "Estado",
        sorted(df["Estado"].dropna().unique())
    )

with col3:
    activity = st.multiselect(
        "Activity Type",
        sorted(df["Activity Type"].dropna().unique())
    )

# -------------------------
# APLICAR FILTROS
# -------------------------
df_filtrado = df.copy()

if certificacion:
    df_filtrado = df_filtrado[df_filtrado["Certificacion"].isin(certificacion)]

if estado:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estado)]

if activity:
    df_filtrado = df_filtrado[df_filtrado["Activity Type"].isin(activity)]

# -------------------------
# BOTONES
# -------------------------
col4, col5 = st.columns([1,1])

with col4:
    st.download_button(
        "📥 Descargar datos filtrados",
        df_filtrado.to_csv(index=False),
        "certificaciones_filtradas.csv",
        "text/csv"
    )

with col5:
    if st.button("🧹 Borrar filtros"):
        st.experimental_rerun()

st.markdown("---")

# -------------------------
# ENVIAR AL HTML
# -------------------------
csv_string = df_filtrado.to_csv(index=False)

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

components.html(html_code, height=1200, scrolling=True)
