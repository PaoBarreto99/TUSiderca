import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# 👇 Oculta el título negro
st.markdown("""
<style>
h1 { display: none; }
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("certificaciones.csv", encoding="latin-1")

df.rename(columns={
    "Fecha_vencimiento": "Fecha_Vencimiento",
    "Fecha_certificacion": "Fecha_Certificacion"
}, inplace=True)

df["Fecha_Vencimiento"] = pd.to_datetime(df["Fecha_Vencimiento"], errors="coerce")

csv_string = df.to_csv(index=False)

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

components.html(html_code, height=1000, scrolling=True)
