from db import db
from werkzeug.security import check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    rol_id = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, server_default=db.func.now())
    temp_password = db.Column(db.Boolean, default=False)

    def check_password(self, password):
        """Verifica la contraseña usando bcrypt"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rol_id": self.rol_id,
            "activo": self.activo
        }


class NotaVenta(db.Model):
    __tablename__ = "nota_venta"
    id = db.Column(db.Integer, primary_key=True)
    nro_proforma = db.Column(db.String(20), unique=True, nullable=False)
    cliente = db.Column(db.String(150), nullable=False)
    cel = db.Column(db.String(20))
    vendedor = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    producto = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50))
    cantidad = db.Column(db.Integer, nullable=False)
    longitud = db.Column(db.Numeric(10,2))
    precio_unitario = db.Column(db.Numeric(10,2), nullable=False)
    importe = db.Column(db.Numeric(10,2), nullable=False)
    subtotal = db.Column(db.Numeric(10,2), nullable=False)
    anticipo = db.Column(db.Numeric(10,2))
    saldo = db.Column(db.Numeric(10,2))
    total = db.Column(db.Numeric(10,2), nullable=False)
    fecha_entrega = db.Column(db.DateTime)
    nombre_cliente = db.Column(db.String(150))
    nit = db.Column(db.String(50))
    firma_caja = db.Column(db.String(100))
    firma_cliente = db.Column(db.String(100))
    creado_en = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "nro_proforma": self.nro_proforma,
            "cliente": self.cliente,
            "cel": self.cel,
            "vendedor": self.vendedor,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "producto": self.producto,
            "color": self.color,
            "cantidad": self.cantidad,
            "longitud": float(self.longitud) if self.longitud else None,
            "precio_unitario": float(self.precio_unitario) if self.precio_unitario else None,
            "importe": float(self.importe) if self.importe else None,
            "subtotal": float(self.subtotal) if self.subtotal else None,
            "anticipo": float(self.anticipo) if self.anticipo else None,
            "saldo": float(self.saldo) if self.saldo else None,
            "total": float(self.total) if self.total else None,
            "fecha_entrega": self.fecha_entrega.isoformat() if self.fecha_entrega else None,
            "nombre_cliente": self.nombre_cliente,
            "nit": self.nit,
            "firma_caja": self.firma_caja,
            "firma_cliente": self.firma_cliente,
            "creado_en": self.creado_en.isoformat() if self.creado_en else None
        }