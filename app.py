from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

@app.route("/")
def dashboard():

    # === CARGAR DATOS ===
    # Cambiá el nombre por tu archivo real
    df = pd.read_excel("datos.xlsx")

    # Limpiar nulos
    df = df.fillna("")

    # === KPIs ===
    total_registros = len(df)
    vencidos = len(df[df["Estado"] == "Vencido"]) if "Estado" in df.columns else 0
    por_vencer = len(df[df["Estado"] == "Por vencer"]) if "Estado" in df.columns else 0

    # === GRÁFICO ESTADO ===
    if "Estado" in df.columns:
        estado_counts = df["Estado"].value_counts()
        labels_estado = estado_counts.index.tolist()
        data_estado = estado_counts.values.tolist()
    else:
        labels_estado = []
        data_estado = []

    # === GRÁFICO CERTIFICACIÓN ===
    if "Certificación" in df.columns:
        cert_counts = df["Certificación"].value_counts().head(5)
        labels_cert = cert_counts.index.tolist()
        data_cert = cert_counts.values.tolist()
    else:
        labels_cert = []
        data_cert = []

    # === TABLA ===
    tabla = df.values.tolist()

    return render_template(
        "dashboard.html",
        tabla=tabla,
        total_registros=total_registros,
        vencidos=vencidos,
        por_vencer=por_vencer,
        labels_estado=json.dumps(labels_estado),
        data_estado=json.dumps(data_estado),
        labels_cert=json.dumps(labels_cert),
        data_cert=json.dumps(data_cert)
    )

if __name__ == "__main__":
    app.run(debug=True)
