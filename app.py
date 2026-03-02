import streamlit as st
import streamlit.components.v1 as components

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=800, scrolling=True)
