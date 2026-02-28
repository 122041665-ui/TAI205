from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

usuarios = [
    {"id": "1", "nombre": "Rafael", "edad": "20"},
    {"id": "2", "nombre": "Berna", "edad": "25"},
    {"id": "3", "nombre": "Yahir", "edad": "30"},
]

# Vista 
@app.get("/")
def web():
    return render_template("index.html")

# GET - consultar todos
@app.get("/v1/usuario/")
def consulta_todos():
    return jsonify({
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    })

# POST - crear
@app.post("/v1/usuarios/")
def crear_usuario():
    usuario = request.get_json(silent=True) or {}

    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            return jsonify({"detail": "El usuario ya existe"}), 400

    usuarios.append({
        "id": str(usuario.get("id", "")),
        "nombre": str(usuario.get("nombre", "")),
        "edad": str(usuario.get("edad", ""))
    })

    return jsonify({
        "mensaje": "Usuario creado exitosamente",
        "status": "200",
        "usuario": usuario
    })

# PUT - actualizar
@app.put("/v1/usuarios/<int:id>")
def actualizar_usuario(id):
    usuario = request.get_json(silent=True) or {}

    for usr in usuarios:
        if usr["id"] == str(id):
            usr["nombre"] = usuario.get("nombre", usr["nombre"])
            usr["edad"] = usuario.get("edad", usr["edad"])
            return jsonify({
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usr
            })

    return jsonify({"detail": "Usuario no encontrado"}), 404

# DELETE - eliminar
@app.delete("/v1/usuarios/<int:id>")
def eliminar_usuario(id):
    for usr in usuarios:
        if usr["id"] == str(id):
            usuarios.remove(usr)
            return jsonify({
                "mensaje": "Usuario eliminado correctamente",
                "status": "200"
            })

    return jsonify({"detail": "Usuario no encontrado"}), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5010, debug=True)
