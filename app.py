from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db
from models import Usuario

app = Flask(__name__)
CORS(app)

# Configura Render DB (usa External URL)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://proyecto_db_m5bf_user:rwqNLOlHLdP3qIRyNSZVy6YontarLkbp@dpg-d2sugijipnbc73b5n3n0-a.oregon-postgres.render.com/proyecto_db_m5bf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return {"message": "API funcionando 🚀"}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = Usuario.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # ⚠️ Si tus contraseñas NO están en hash, usa comparación directa:
    if user.password != password:
        return jsonify({"error": "Contraseña incorrecta"}), 401

    return jsonify({
        "message": "Login exitoso",
        "user": user.to_dict()
    }), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
