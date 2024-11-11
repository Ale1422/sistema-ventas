-- Crear la base de datos
CREATE DATABASE CarniceriaDB;
USE CarniceriaDB;

-- Tabla de Roles
CREATE TABLE Roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Rol VARCHAR(50) NOT NULL,
    Permisos TEXT
);

-- Tabla de Usuarios
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Contraseña VARCHAR(255) NOT NULL,
    Rol INT,
    Fecha_Creación TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    FOREIGN KEY (Rol) REFERENCES Roles(id)
);

-- Tabla de Productos
CREATE TABLE Productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre_Producto VARCHAR(100) NOT NULL,
    Descripción TEXT,
    Precio DECIMAL(10, 2) NOT NULL,
    Stock_Cantidad INT DEFAULT 0,
    Umbral_Stock INT DEFAULT 0,
    Fecha_Creación TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Estado ENUM('disponible', 'no disponible') DEFAULT 'disponible'
);

-- Tabla de Ventas
CREATE TABLE Ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    ID_Caja INT,
    Fecha_Venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Total_Venta DECIMAL(10, 2) NOT NULL,
    Método_Pago ENUM('efectivo', 'tarjeta') NOT NULL,
    Descuento_Aplicado DECIMAL(10, 2) DEFAULT 0,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(id)
    FOREIGN KEY (ID_Caja) REFERENCES Caja(id)
);

-- Tabla de Detalles_Venta
CREATE TABLE Detalles_Venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ID_Venta INT,
    ID_Producto INT,
    Cantidad INT NOT NULL,
    Precio_Unitario DECIMAL(10, 2) NOT NULL,
    Subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ID_Venta) REFERENCES Ventas(id),
    FOREIGN KEY (ID_Producto) REFERENCES Productos(id)
);

-- Tabla de Caja
CREATE TABLE Caja (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    Fecha_Apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Fecha_Cierre TIMESTAMP,
    Total_Inicial DECIMAL(10, 2) NOT NULL,
    Total_Final DECIMAL(10, 2),
    Estado ENUM('abierta', 'cerrada') DEFAULT 'abierta',
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(id)
);

-- Tabla de Gastos
CREATE TABLE Gastos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,
    Descripción TEXT,
    Monto DECIMAL(10, 2) NOT NULL,
    Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(id)
);

-- Tabla de Proveedores
CREATE TABLE Proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Contacto VARCHAR(100),
    Teléfono VARCHAR(15),
    Email VARCHAR(100),
    Dirección TEXT
);

-- Tabla de Recepciones
CREATE TABLE Recepciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ID_Proveedor INT,
    Fecha_Recepcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Total_Productos INT DEFAULT 0,
    FOREIGN KEY (ID_Proveedor) REFERENCES Proveedores(id)
);

-- Tabla de Detalles_Recepcion
CREATE TABLE Detalles_Recepcion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ID_Recepcion INT,
    ID_Producto INT,
    Cantidad_Recibida INT NOT NULL,
    Precio_Costo DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ID_Recepcion) REFERENCES Recepciones(id),
    FOREIGN KEY (ID_Producto) REFERENCES Productos(id)
);