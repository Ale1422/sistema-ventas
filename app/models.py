# from . import db
# from datetime import datetime

# class Rol(db.Model):
#     __tablename__ = 'Roles'
#     ID_Rol = db.Column(db.Integer, primary_key=True)
#     Nombre_Rol = db.Column(db.String(50), nullable=False)
#     Permisos = db.Column(db.Text)

# class Usuario(db.Model):
#     __tablename__ = 'Usuarios'
#     ID_Usuario = db.Column(db.Integer, primary_key=True)
#     Nombre = db.Column(db.String(50), nullable=False)
#     Apellido = db.Column(db.String(50), nullable=False)
#     Email = db.Column(db.String(100), unique=True, nullable=False)
#     Contraseña = db.Column(db.String(255), nullable=False)
#     Rol = db.Column(db.Integer, db.ForeignKey('Roles.ID_Rol'))
#     Fecha_Creación = db.Column(db.TIMESTAMP, default=datetime.utcnow)
#     Estado = db.Column(db.Enum('activo', 'inactivo'), default='activo')

# class Producto(db.Model):
#     __tablename__ = 'Productos'
#     ID_Producto = db.Column(db.Integer, primary_key=True)
#     Nombre_Producto = db.Column(db.String(100), nullable=False)
#     Descripción = db.Column(db.Text)
#     Precio = db.Column(db.Numeric(10, 2), nullable=False)
#     Stock_Cantidad = db.Column(db.Integer, default=0)
#     Umbral_Stock = db.Column(db.Integer, default=0)
#     Fecha_Creación = db.Column(db.TIMESTAMP, default=datetime.utcnow)
#     Estado = db.Column(db.Enum('disponible', 'no disponible'), default='disponible')

# class Venta(db.Model):
#     __tablename__ = 'Ventas'
#     ID_Venta = db.Column(db.Integer, primary_key=True)
#     ID_Usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.ID_Usuario'))
#     Fecha_Venta = db.Column(db.TIMESTAMP, default=datetime.utcnow)
#     Total_Venta = db.Column(db.Numeric(10, 2), nullable=False)
#     Método_Pago = db.Column(db.Enum('efectivo', 'tarjeta'), nullable=False)
#     Descuento_Aplicado = db.Column(db.Numeric(10, 2), default=0)

# class DetalleVenta(db.Model):
#     __tablename__ = 'Detalles_Venta'
#     ID_Detalle = db.Column(db.Integer, primary_key=True)
#     ID_Venta = db.Column(db.Integer, db.ForeignKey('Ventas.ID_Venta'))
#     ID_Producto = db.Column(db.Integer, db.ForeignKey('Productos.ID_Producto'))
#     Cantidad = db.Column(db.Integer, nullable=False)
#     Precio_Unitario = db.Column(db.Numeric(10, 2), nullable=False)
#     Subtotal = db.Column(db.Numeric(10, 2), nullable=False)

# class Caja(db.Model):
#     __tablename__ = 'Caja'
#     ID_Caja = db.Column(db.Integer, primary_key=True)
#     ID_Usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.ID_Usuario'))
#     Fecha_Apertura = db.Column(db.TIMESTAMP, default=datetime.utcnow)
#     Fecha_Cierre = db.Column(db.TIMESTAMP)
#     Total_Inicial = db.Column(db.Numeric(10, 2), nullable=False)
#     Total_Final = db.Column(db.Numeric(10, 2))
#     Estado = db.Column(db.Enum('abierta', 'cerrada'), default='abierta')

# class Gasto(db.Model):
#     __tablename__ = 'Gastos'
#     ID_Gasto = db.Column(db.Integer, primary_key=True)
#     ID_Usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.ID_Usuario'))
#     Descripción = db.Column(db.Text)
#     Monto = db.Column(db.Numeric(10, 2), nullable=False)
#     Fecha = db.Column(db.TIMESTAMP, default=datetime.utcnow)

# class Proveedor(db.Model):
#     __tablename__ = 'Proveedores'
#     ID_Proveedor = db.Column(db.Integer, primary_key=True)
#     Nombre = db.Column(db.String(100), nullable=False)
#     Contacto = db.Column(db.String(100))
#     Teléfono = db.Column(db.String(15))
#     Email = db.Column(db.String(100))
#     Dirección = db.Column(db.Text)

# class Recepcion(db.Model):
#     __tablename__ = 'Recepciones'
#     ID_Recepcion = db.Column(db.Integer, primary_key=True)
#     ID_Proveedor = db.Column(db.Integer, db.ForeignKey('Proveedores.ID_Proveedor'))
#     Fecha_Recepcion = db.Column(db.TIMESTAMP, default=datetime.utcnow)
#     Total_Productos = db.Column(db.Integer, default=0)

# class DetalleRecepcion(db.Model):
#     __tablename__ = 'Detalles_Recepcion'
#     ID_Detalle_Recepcion = db.Column(db.Integer, primary_key=True)
#     ID_Recepcion = db.Column(db.Integer, db.ForeignKey('Recepciones.ID_Recepcion'))
#     ID_Producto = db.Column(db.Integer, db.ForeignKey('Productos.ID_Producto'))
#     Cantidad_Recibida = db.Column(db.Integer, nullable=False)
#     Precio_Costo = db.Column(db.Numeric(10, 2), nullable=False)

