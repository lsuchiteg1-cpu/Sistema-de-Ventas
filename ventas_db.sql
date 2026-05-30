__ ===================================
__ TABLA PRODUCTOS
__ ===================================
CREATE DATABASE ventas_db;
CREATE TABLE IF NOT EXISTS productos(
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  precio DECIMAL(10, 2) NOT NULL
);

__ ===============================
__ TABLA VENTAS
__ ===============================
CREATE TABLE IF NOT EXISTS ventas(
  id SERIAL PRIMARY KEY,
  total NUMERIC(10,2)
);

__ =================================
__ TABLA FACTURAS
__ =================================
CREATE TABLE IF NOT EXISTS facturas(
  id SERIAL PRIMARY KEY,
  cliente VARCHAR(100),
  nit VARCHAR(30),
  total NUMERIC(10,2),
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===================================
-- DATOS DE PRUEBA PRODUCTOS
-- ===================================

INSERT INTO productos(nombre, precio)
VALUES
('Mouse Gamer', 150.00),
('Teclado Mecánico', 350.00),
('Monitor LED', 1200.00),
('Laptop HP', 4500.00),
('Auriculares', 250.00);

-- ===================================
-- DATOS DE PRUEBA VENTAS
-- ===================================

INSERT INTO ventas(total)
VALUES
(500.00),
(1200.00),
(3500.00);

-- ===================================
-- DATOS DE PRUEBA FACTURAS
-- ===================================

INSERT INTO facturas(cliente, nit, total)
VALUES
('Juan Perez', '1234567-8', 500.00),
('Maria Lopez', '9876543-1', 1200.00),
('Carlos Gomez', '4567891-2', 3500.00);

SELECT * FROM productos;

SELECT * FROM ventas;

SELECT * FROM facturas;