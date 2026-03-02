st.markdown("""
<style>

/* Quita padding general */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
}

/* Quita margen del main */
.main {
    padding: 0rem !important;
}

/* Oculta header y footer de Streamlit */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Hace que el iframe ocupe todo */
iframe {
    width: 100vw !important;
    height: 100vh !important;
}

</style>
""", unsafe_allow_html=True)
