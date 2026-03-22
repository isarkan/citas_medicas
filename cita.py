from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

archivo = "datos.xlsx"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/datos", methods=["GET"])
def leer():
    df = pd.read_excel(archivo)
    return df.to_json(orient="records")


@app.route("/crear", methods=["POST"])
def crear():
    data = request.json
    df = pd.read_excel(archivo)

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(archivo, index=False)

    return {"mensaje": "registro creado"}


@app.route("/actualizar/<int:id>", methods=["PUT"])
def actualizar(id):
    data = request.json
    df = pd.read_excel(archivo)

    df.loc[df["id"] == id, ["nombre","edad"]] = [data["nombre"], data["edad"]]
    df.to_excel(archivo, index=False)

    return {"mensaje": "actualizado"}


@app.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar(id):
    df = pd.read_excel(archivo)

    df = df[df["id"] != id]
    df.to_excel(archivo, index=False)

    return {"mensaje": "eliminado"}


if __name__ == "__main__":
    app.run(debug=True)
