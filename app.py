import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# -------------------------
# CARGA DE DATOS
# -------------------------
df = pd.read_csv("certificaciones.csv", encoding="latin-1")
df["Fecha_vencimiento"] = pd.to_datetime(df["Fecha_vencimiento"], errors="coerce")

st.title("📋 Dashboard de Certificaciones")

st.markdown("### 🔎 Filtrar datos (tipo Excel)")

# Data editor con filtros integrados
df_editado = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# -------------------------
# BOTONES
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "📥 Descargar datos filtrados",
        df_editado.to_csv(index=False),
        "certificaciones_filtradas.csv",
        "text/csv"
    )

with col2:
    if st.button("🧹 Resetear datos"):
        st.experimental_rerun()

st.markdown("---")

# -------------------------
# ENVIAR DATOS AL HTML
# -------------------------
csv_string = df_editado.to_csv(index=False)

with open("Dashboard.html", "r", encoding="utf-8") as f:
    html_code = f.read()

html_code = html_code.replace(
    "</head>",
    f"<script>window.csvData = `{csv_string}`;</script></head>"
)

components.html(html_code, height=1200, scrolling=True)
