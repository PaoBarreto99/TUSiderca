import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Leer CSV fijo del repo
df = pd.read_csv("certificacions.csv")

# Mostrar algunos datos (opcional)
st.write("Vista previa de datos")
st.dataframe(df)

# Si usás tu Dashboard.html
with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=800, scrolling=True)

