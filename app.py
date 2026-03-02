import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# ===== CARGAR DATOS =====
df = pd.read_excel("datos.xlsx")
df = df.fillna("")

# ===== KPIs =====
total = len(df)
vencidos = len(df[df["Estado"] == "Vencido"]) if "Estado" in df.columns else 0
por_vencer = len(df[df["Estado"] == "Por vencer"]) if "Estado" in df.columns else 0

col1, col2, col3 = st.columns(3)

col1.metric("Total registros", total)
col2.metric("Vencidos", vencidos)
col3.metric("Por vencer", por_vencer)

st.markdown("---")

# ===== GRÁFICOS =====
col4, col5 = st.columns(2)

if "Estado" in df.columns:
    fig_estado = px.bar(df, x="Estado")
    col4.plotly_chart(fig_estado, use_container_width=True)

if "Certificación" in df.columns:
    fig_cert = px.pie(df, names="Certificación")
    col5.plotly_chart(fig_cert, use_container_width=True)

st.markdown("---")

# ===== FILTROS DEBAJO DE GRÁFICOS =====
st.subheader("Filtros")

filtro_nombre = st.text_input("Filtrar por Nombre")
filtro_sap = st.text_input("Filtrar por SAP ID")
filtro_estado = st.selectbox("Filtrar por Estado", ["Todos"] + list(df["Estado"].unique()) if "Estado" in df.columns else ["Todos"])

df_filtrado = df.copy()

if filtro_nombre:
    df_filtrado = df_filtrado[df_filtrado["Nombre"].astype(str).str.contains(filtro_nombre, case=False)]

if filtro_sap:
    df_filtrado = df_filtrado[df_filtrado["SAP ID"].astype(str).str.contains(filtro_sap, case=False)]

if filtro_estado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Estado"] == filtro_estado]

st.markdown("---")

# ===== BOTÓN EXPORTAR =====
st.download_button(
    label="Exportar datos",
    data=df_filtrado.to_csv(index=False).encode("utf-8"),
    file_name="datos_filtrados.csv",
    mime="text/csv"
)

# ===== TABLA CON SCROLL =====
st.subheader("Datos")

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=400
)
