import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# 🔥 Pantalla completa sin márgenes ni header de Streamlit
st.markdown("""
<style>

/* Quitar padding */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
}

.main {
    padding: 0rem !important;
}

/* Ocultar header y footer */
header {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


# 📄 Leer CSV
df = pd.read_csv("certificaciones.csv", encoding="latin-1")

df.rename(columns={
    "Fecha_vencimiento": "Fecha_Vencimiento",
    "Fecha_certificacion": "Fecha_Certificacion"
}, inplace=True)

df["Fecha_Vencimiento"] = pd.to_datetime(df["Fecha_Vencimiento"], errors="coerce")

csv_string = df.to_csv(index=False)


# 📄 Cargar HTML
with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

components.html(html_code, height=1200, scrolling=True)
