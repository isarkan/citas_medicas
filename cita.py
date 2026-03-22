from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# 📁 Ruta automática al escritorio
def obtener_escritorio():
    home = os.path.expanduser("~")

    posibles_rutas = [
        os.path.join(home, "Desktop"),
        os.path.join(home, "Escritorio"),
        os.path.join(home, "OneDrive", "Desktop"),
        os.path.join(home, "OneDrive", "Escritorio"),
    ]

    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            return ruta

    # Si no encuentra, crea uno por defecto
    ruta = os.path.join(home, "Desktop")
    os.makedirs(ruta, exist_ok=True)
    return ruta


desktop = obtener_escritorio()
archivo = os.path.join(desktop, "citas.xlsx")


@app.route("/")
def index():
    return render_template("index.html")


# 🔹 LEER DATOS DEL DÍA ACTUAL
@app.route("/datos", methods=["GET"])
def leer():
    hoy = datetime.now().strftime("%Y-%m-%d")

    try:
        df = pd.read_excel(archivo, sheet_name=hoy)
        return df.to_json(orient="records")
    except:
        return jsonify([])


# 🔹 CREAR REGISTRO
@app.route("/crear", methods=["POST"])
def crear():
    data = request.json
    hoy = datetime.now().strftime("%Y-%m-%d")

    nuevo_df = pd.DataFrame([data])

    # Si no existe el archivo → crearlo
    if not os.path.exists(archivo):
        with pd.ExcelWriter(archivo, engine="openpyxl") as writer:
            nuevo_df.to_excel(writer, sheet_name=hoy, index=False)

    else:
        # Si ya existe
        with pd.ExcelWriter(archivo, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            try:
                df_existente = pd.read_excel(archivo, sheet_name=hoy)
                df_total = pd.concat([df_existente, nuevo_df], ignore_index=True)

                df_total.to_excel(writer, sheet_name=hoy, index=False)
            except:
                nuevo_df.to_excel(writer, sheet_name=hoy, index=False)

    return {"mensaje": "registro creado"}


# 🔹 ACTUALIZAR (solo en la hoja del día)
@app.route("/actualizar/<int:id>", methods=["PUT"])
def actualizar(id):
    data = request.json
    hoy = datetime.now().strftime("%Y-%m-%d")

    try:
        df = pd.read_excel(archivo, sheet_name=hoy)

        df.loc[df["id"] == id, ["nombre", "edad"]] = [data["nombre"], data["edad"]]

        with pd.ExcelWriter(archivo, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=hoy, index=False)

        return {"mensaje": "actualizado"}

    except:
        return {"error": "No hay datos hoy"}


# 🔹 ELIMINAR (solo en la hoja del día)
@app.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar(id):
    hoy = datetime.now().strftime("%Y-%m-%d")

    try:
        df = pd.read_excel(archivo, sheet_name=hoy)

        df = df[df["id"] != id]

        with pd.ExcelWriter(archivo, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=hoy, index=False)

        return {"mensaje": "eliminado"}

    except:
        return {"error": "No hay datos hoy"}


if __name__ == "__main__":
    app.run(debug=True)