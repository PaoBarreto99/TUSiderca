import streamlit as st
import streamlit.components.v1 as components
import requests

# Pega aquí el link "raw" de tu HTML en GitHub
html_url = "https://github.com/PaoBarreto99/TUSiderca.git"

# Descargar contenido del HTML
html_code = requests.get(html_url).text

# Mostrar HTML en Streamlit
components.html(html_code, height=600, scrolling=True)