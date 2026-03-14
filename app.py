import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Configuración de página
st.set_page_config(layout="wide")

# Ocultar header y padding de Streamlit
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


# Leer CSV
df = pd.read_csv("certificaciones.csv", encoding="latin-1")

# Convertir a string CSV para pasarlo al HTML
csv_string = df.to_csv(index=False)


# Leer el HTML del dashboard
with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()


# Inyectar el CSV en el HTML
html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)


# Renderizar HTML dentro de Streamlit
components.html(
    html_code,
    height=1200,
    scrolling=True
)
