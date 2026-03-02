import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Leer CSV
df = pd.read_csv("certificaciones.csv", encoding="latin-1")

# Convertir a CSV string
csv_string = df.to_csv(index=False)

# Leer HTML
with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Inyectar CSV dentro del HTML como variable JS
html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

components.html(html_code, height=1000, scrolling=True)

