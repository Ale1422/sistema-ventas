ALTER TABLE Productos CONVERT TO CHARACTER SET utf8mb4 COLLATE UTF8MB4_UNICODE_CI;
ALTER DATABASE nuevacarniceria CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

INSERT INTO productos (Nombre_Producto, Descripción, Precio, Stock_Cantidad, Umbral_Stock, Fecha_Creación, Estado) VALUES('Choquizuela', 'Corte de carne de res', 7500.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Tortuguita', 'Corte de carne de res', 7500.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Paleta Chata', 'Corte de carne de res', 7500.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Jamón de Paleta', 'Corte de carne de res', 7500.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Trasjamón', 'Corte de carne de res', 7500.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Picana', 'Corte premium de carne de res', 8200.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Filet', 'Corte premium de carne de res', 8200.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Nalga', 'Corte premium de carne de res', 8200.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Lomo', 'Corte premium de carne de res', 8200.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Peceto', 'Corte premium de carne de res', 8200.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Verija', 'Corte premium de carne de res', 8200.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Vacio', 'Corte de carne de res', 7000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Faldita', 'Corte de carne de res', 7000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Entraña', 'Corte de carne de res', 7000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Tapa de Nalga', 'Corte de carne de res', 7000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Matambre', 'Corte de carne de res', 7000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Paleta Rolliza', 'Corte de carne de res', 7000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Costeleta Lisa', 'Corte de carne de res', 7000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Milanesa Preparada', 'Carne preparada para milanesa', 7000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Milanesa Molida Preparada', 'Carne molida preparada para milanesa', 5000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Primo', 'Corte de carne de res', 6500.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Duro', 'Corte de carne de res', 6500.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Molida Especial', 'Carne molida especial', 6000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Puchero Especial', 'Corte especial para puchero', 5000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Morcilla', 'Producto de cerdo', 5500.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Costilla Especial', 'Costilla de res especial', 7000.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Chorizo Criollo', 'Chorizo típico criollo', 5500.00, 0, 0, CURRENT_TIMESTAMP, 'disponible'),
('Chorizo Parrillero', 'Chorizo para parrilla', 5500.00, 0, 0, CURRENT_TIMESTAMP, 'disponible');
