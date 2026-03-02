import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Leer CSV fijo del repo
df = pd.read_csv("certificaciones.csv", encoding="latin-1")

# Si usás tu Dashboard.html
with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()
# Mostrar algunos datos (opcional)
st.write("Vista previa de datos")
st.dataframe(df)

components.html(html_code, height=800, scrolling=True)







