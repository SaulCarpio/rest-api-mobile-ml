import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db
from models import Usuario, NotaVenta
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL or "postgresql://proyecto_db_m5bf_user:rwqNLOlHLdP3qIRyNSZVy6YontarLkbp@dpg-d2sugijipnbc73b5n3n0-a.oregon-postgres.render.com/proyecto_db_m5bf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API NotaVenta - OK"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")  # Esto será el email
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Email y password requeridos"}), 400

    # Buscar por email en lugar de username
    user = Usuario.query.filter_by(email=username).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not user.check_password(password):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    return jsonify({
        "message": "Login exitoso", 
        "user": user.to_dict()
    }), 200

@app.route("/notaventa", methods=["POST"])
def crear_nota():
    data = request.get_json() or {}
    try:
        # Convertir fechas de string a objetos datetime
        fecha_str = data.get("fecha")
        fecha = None
        if fecha_str:
            try:
                # Intentar diferentes formatos de fecha
                if '/' in fecha_str:
                    day, month, year = fecha_str.split('/')
                    fecha = datetime(int(year), int(month), int(day))
                elif '-' in fecha_str:
                    year, month, day = fecha_str.split('-')
                    fecha = datetime(int(year), int(month), int(day))
            except (ValueError, AttributeError):
                fecha = datetime.now()

        fecha_entrega_str = data.get("fecha_entrega")
        fecha_entrega = None
        if fecha_entrega_str:
            try:
                if '/' in fecha_entrega_str:
                    day, month, year = fecha_entrega_str.split('/')
                    fecha_entrega = datetime(int(year), int(month), int(day))
                elif '-' in fecha_entrega_str:
                    year, month, day = fecha_entrega_str.split('-')
                    fecha_entrega = datetime(int(year), int(month), int(day))
            except (ValueError, AttributeError):
                fecha_entrega = None

        nota = NotaVenta(
            nro_proforma=data.get("nro_proforma"),
            cliente=data.get("cliente"),
            cel=data.get("cel"),
            vendedor=data.get("vendedor"),
            fecha=fecha or datetime.now(),
            producto=data.get("producto"),
            color=data.get("color"),
            cantidad=data.get("cantidad"),
            longitud=data.get("longitud"),
            precio_unitario=data.get("precio_unitario"),
            importe=data.get("importe"),
            subtotal=data.get("subtotal") or data.get("importe"),
            anticipo=data.get("anticipo"),
            saldo=data.get("saldo"),
            total=data.get("total") or data.get("importe"),
            fecha_entrega=fecha_entrega,
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