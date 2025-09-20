import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db
from models import Usuario, NotaVenta
from werkzeug.security import check_password_hash

app = Flask(__name__)
CORS(app)

# Use env var DATABASE_URL en Render. Localmente puedes usar .env o poner la URL aquí.
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL.startswith("postgres://"):
    # SQLAlchemy requiere postgresql://
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Si no hay DATABASE_URL, puedes poner la URL completa aquí temporalmente (no recomendado)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL or "postgresql://proyecto_db_m5bf_user:rwqNLOlHLdP3qIRyNSZVy6YontarLkbp@dpg-d2sugijipnbc73b5n3n0-a.oregon-postgres.render.com/proyecto_db_m5bf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Crear tablas (si falta). Si ya existen, no afecta.
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API NotaVenta - OK"})


def verify_password(stored_password, provided_password):
    """
    Intenta verificar hash con werkzeug; si falla, compara texto plano.
    Esto te permite soportar contraseñas hashed o plaintext en BD.
    """
    try:
        return check_password_hash(stored_password, provided_password)
    except Exception:
        return stored_password == provided_password


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username y password requeridos"}), 400

    user = Usuario.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not verify_password(user.password, password):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    return jsonify({"message": "Login exitoso", "user": user.to_dict()}), 200


@app.route("/notaventa", methods=["POST"])
def crear_nota():
    data = request.get_json() or {}
    try:
        nota = NotaVenta(
            nro_proforma=data.get("nro_proforma"),
            cliente=data.get("cliente"),
            cel=data.get("cel"),
            vendedor=data.get("vendedor"),
            fecha=data.get("fecha"),
            producto=data.get("producto"),
            color=data.get("color"),
            cantidad=data.get("cantidad"),
            longitud=data.get("longitud"),
            precio_unitario=data.get("precio_unitario"),
            importe=data.get("importe"),
            subtotal=data.get("subtotal"),
            anticipo=data.get("anticipo"),
            saldo=data.get("saldo"),
            total=data.get("total"),
            fecha_entrega=data.get("fecha_entrega"),
            nombre_cliente=data.get("nombre_cliente"),
            nit=data.get("nit"),
            firma_caja=data.get("firma_caja"),
            firma_cliente=data.get("firma_cliente")
        )
        db.session.add(nota)
        db.session.commit()
        return jsonify({"message": "Nota creada", "nota": nota.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    traceback.print_exc()
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
