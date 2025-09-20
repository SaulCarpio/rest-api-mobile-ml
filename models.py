from db import db

class Usuario(db.Model):
    __tablename__ = "usuarios"  # asegúrate que coincide con tu tabla real

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # puede estar en texto plano o hash
    rol_id = db.Column(db.Integer, nullable=False)  # 1 = admin, 2 = usuario

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "rol_id": self.rol_id
        }
