import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard de Certificaciones")

# --- Leer CSV ---
df = pd.read_csv("certificaciones.csv", encoding="latin-1")

# --- Normalizar nombres de columna ---
df.columns = df.columns.str.strip()  # quita espacios al inicio/final

# --- Convertir columnas de fecha a datetime ---
for col in df.columns:
    if "fecha" in col.lower():
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')

# --- Calcular estado ---
def estado(fecha_vencimiento):
    if pd.isna(fecha_vencimiento):
        return "Vencida"
    hoy = pd.Timestamp.today()
    dias = (fecha_vencimiento - hoy).days
    if dias < 0:
        return "Vencida"
    elif dias <= 90:
        return "Por Vencer"
    else:
        return "Vigente"

# Usa los nombres exactos de tu CSV
df["Estado"] = df["Fecha_vencimiento"].apply(estado)

# --- KPIs ---
st.header("📋 Dashboard de Certificaciones")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Vigentes", (df["Estado"]=="Vigente").sum())
col2.metric("Por Vencer", (df["Estado"]=="Por Vencer").sum())
col3.metric("Vencidas", (df["Estado"]=="Vencida").sum())
col4.metric("Total", len(df))

# --- Tabla ---
st.subheader("Detalle de Certificaciones")
st.dataframe(df, use_container_width=True)

# --- Gráfico de estado ---
st.subheader("Estado de Certificaciones")
estado_counts = df["Estado"].value_counts().reset_index()
estado_counts.columns = ["Estado", "Cantidad"]
fig = px.pie(
    estado_counts,
    names="Estado",
    values="Cantidad",
    color="Estado",
    color_discrete_map={"Vigente":"green","Por Vencer":"orange","Vencida":"red"}
)
st.plotly_chart(fig, use_container_width=True)

# --- Gráfico de comentarios / on hold ---
if "Comentarios" in df.columns:
    st.subheader("Certificaciones on hold")
    hold_counts = df[df["Comentarios"].notna()]["Comentarios"].value_counts().reset_index()
    hold_counts.columns = ["Comentario", "Cantidad"]
    fig2 = px.bar(hold_counts, x="Comentario", y="Cantidad")
    st.plotly_chart(fig2, use_container_width=True)
