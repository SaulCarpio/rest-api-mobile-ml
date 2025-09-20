from db import db

class Usuario(db.Model):
    __tablename__ = "usuarios"  # ajusta si tu tabla se llama distinto
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # puede ser plaintext o hash
    rol_id = db.Column(db.Integer, nullable=False)  # 1 = admin, 2 = usuario

    def to_dict(self):
        return {"id": self.id, "username": self.username, "rol_id": self.rol_id}


class NotaVenta(db.Model):
    __tablename__ = "nota_venta"
    id = db.Column(db.Integer, primary_key=True)
    nro_proforma = db.Column(db.String(50))
    cliente = db.Column(db.String(150))
    cel = db.Column(db.String(30))
    vendedor = db.Column(db.String(100))
    fecha = db.Column(db.String(30))
    producto = db.Column(db.String(150))
    color = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    longitud = db.Column(db.Float)
    precio_unitario = db.Column(db.Float)
    importe = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    anticipo = db.Column(db.Float)
    saldo = db.Column(db.Float)
    total = db.Column(db.Float)
    fecha_entrega = db.Column(db.String(30))
    nombre_cliente = db.Column(db.String(150))
    nit = db.Column(db.String(50))
    firma_caja = db.Column(db.String(150))
    firma_cliente = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "nro_proforma": self.nro_proforma,
            "cliente": self.cliente,
            "cel": self.cel,
            "vendedor": self.vendedor,
            "fecha": self.fecha,
            "producto": self.producto,
            "color": self.color,
            "cantidad": self.cantidad,
            "longitud": self.longitud,
            "precio_unitario": self.precio_unitario,
            "importe": self.importe,
            "subtotal": self.subtotal,
            "anticipo": self.anticipo,
            "saldo": self.saldo,
            "total": self.total,
            "fecha_entrega": self.fecha_entrega,
            "nombre_cliente": self.nombre_cliente,
            "nit": self.nit,
            "firma_caja": self.firma_caja,
            "firma_cliente": self.firma_cliente,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
