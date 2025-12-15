from datetime import datetime
from ..admin.models import Producto


from app import db

class Venta(db.Model):
    __tablename__ = 'Ventas'
    id = db.Column(db.Integer, primary_key=True)
    ID_Usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))
    Fecha_Venta = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    Total_Venta = db.Column(db.Numeric(10, 2), nullable=False)
    Método_Pago = db.Column(db.Enum('efectivo', 'tarjeta', 'tarjeta credito', 'tarjeta debito', 'transferencia'), nullable=False)
    Descuento_Aplicado = db.Column(db.Numeric(10, 2), default=0)
    Detalle = db.Column(db.String(255))

    def __init__(self, id_usuario,fecha_venta, total_venta, metodo_pago, descuento = 0.0):
        self.ID_Usuario=id_usuario
        self.Fecha_Venta=fecha_venta
        self.Total_Venta=total_venta
        self.Método_Pago=metodo_pago
        self.Descuento_Aplicado=descuento

class DetalleVenta(db.Model):
    __tablename__ = 'Detalles_Venta'
    id = db.Column(db.Integer, primary_key=True)
    ID_Venta = db.Column(db.Integer, db.ForeignKey('Ventas.id'))
    ID_Producto = db.Column(db.Integer, db.ForeignKey('Productos.id'))
    Cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    Precio_Unitario = db.Column(db.Numeric(10, 2), nullable=False)
    Subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    def __init__(self, id_venta, id_producto, cantidad, precio_unitario, subtotal):
        self.ID_Venta=id_venta
        self.ID_Producto=id_producto
        self.Cantidad=cantidad
        self.Precio_Unitario=precio_unitario
        self.Subtotal=subtotal
    
    def get_nombre_producto(self):
        id = self.ID_Producto
        producto = Producto.get_by_id(id)
        return producto.Nombre_Producto