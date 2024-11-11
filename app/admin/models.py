from datetime import datetime

from app import db

class Producto(db.Model):
    __tablename__ = 'Productos'
    id = db.Column(db.Integer, primary_key=True)
    Nombre_Producto = db.Column(db.String(100), nullable=False)
    Descripción = db.Column(db.Text)
    Precio = db.Column(db.Numeric(10, 2), nullable=False)
    Stock_Cantidad = db.Column(db.Numeric(10, 2), default=0)
    Umbral_Stock = db.Column(db.Integer, default=0)
    Fecha_Creación = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    Estado = db.Column(db.Enum('disponible', 'no disponible'), default='disponible')

    def __init__(self, nombre,descripcion, precio, stock):
        self.Nombre_Producto=nombre
        self.Descripción=descripcion
        self.Precio=precio
        self.Stock_Cantidad=stock
        self.Fecha_Creación=datetime.now()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_by_id(id):
        return Producto.query.get(id)


    @staticmethod
    def get_all():
        return Producto.query.all()