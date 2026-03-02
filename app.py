import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# -------------------------
# ESTILO COMPACTO PROFESIONAL
# -------------------------
st.markdown("""
<style>
div[data-baseweb="select"] {
    font-size: 13px;
}
div[data-baseweb="input"] {
    font-size: 13px;
}
button[kind="secondary"] {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# CARGA DE DATOS
# -------------------------
df = pd.read_csv("certificaciones.csv", encoding="latin-1")
df["Fecha_vencimiento"] = pd.to_datetime(df["Fecha_vencimiento"], errors="coerce")

# -------------------------
# ESTADO DE FILTROS (persistente)
# -------------------------
if "df_filtrado" not in st.session_state:
    st.session_state.df_filtrado = df.copy()

df_filtrado = st.session_state.df_filtrado

# -------------------------
# 1️⃣ DASHBOARD ARRIBA
# -------------------------
csv_string = df_filtrado.to_csv(index=False)

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

components.html(html_code, height=950, scrolling=True)

st.markdown("---")

# -------------------------
# 2️⃣ FILTROS COMPACTOS ABAJO
# -------------------------

st.markdown("#### Filtros")

col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1.2])

with col1:
    filtro_cert = st.multiselect(
        "",
        sorted(df["Certificacion"].dropna().unique()),
        placeholder="Certificación"
    )

with col2:
    filtro_estado = st.multiselect(
        "",
        sorted(df["Estado"].dropna().unique()),
        placeholder="Estado"
    )

with col3:
    filtro_activity = st.multiselect(
        "",
        sorted(df["Activity Type"].dropna().unique()),
        placeholder="Activity Type"
    )

with col4:
    fecha_min = df["Fecha_vencimiento"].min()
    fecha_max = df["Fecha_vencimiento"].max()

    filtro_fecha = st.date_input(
        "",
        value=(fecha_min, fecha_max)
    )

with col5:
    col_btn1, col_btn2 = st.columns([1,1])

    with col_btn1:
        st.download_button(
            "Exportar datos",
            df_filtrado.to_csv(index=False),
            "certificaciones.csv",
            "text/csv",
            use_container_width=True
        )

    with col_btn2:
        if st.button("Borrar filtros", use_container_width=True):
            st.session_state.df_filtrado = df.copy()
            st.experimental_rerun()

# -------------------------
# APLICAR FILTROS
# -------------------------
df_filtrado = df.copy()

if filtro_cert:
    df_filtrado = df_filtrado[df_filtrado["Certificacion"].isin(filtro_cert)]

if filtro_estado:
    df_filtrado = df_filtrado[df_filtrado["Estado"].isin(filtro_estado)]

if filtro_activity:
    df_filtrado = df_filtrado[df_filtrado["Activity Type"].isin(filtro_activity)]

if isinstance(filtro_fecha, tuple) and len(filtro_fecha) == 2:
    df_filtrado = df_filtrado[
        (df_filtrado["Fecha_vencimiento"] >= pd.to_datetime(filtro_fecha[0])) &
        (df_filtrado["Fecha_vencimiento"] <= pd.to_datetime(filtro_fecha[1]))
    ]

st.session_state.df_filtrado = df_filtrado
