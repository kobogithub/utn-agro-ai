-- Schema de Base de Datos Agrícola
-- SQLite Database Schema

-- Tabla de Agricultores
CREATE TABLE IF NOT EXISTS farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Cultivos
CREATE TABLE IF NOT EXISTS crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,  -- cereal, oleaginosa, leguminosa, etc.
    variety TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Parcelas
CREATE TABLE IF NOT EXISTS plots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hectares REAL NOT NULL CHECK(hectares > 0),
    farmer_id INTEGER NOT NULL,
    crop_id INTEGER,  -- Puede ser NULL si no tiene cultivo asignado
    planting_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id) ON DELETE CASCADE,
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE SET NULL
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_farmers_region ON farmers(region);
CREATE INDEX IF NOT EXISTS idx_farmers_email ON farmers(email);
CREATE INDEX IF NOT EXISTS idx_crops_type ON crops(type);
CREATE INDEX IF NOT EXISTS idx_plots_farmer ON plots(farmer_id);
CREATE INDEX IF NOT EXISTS idx_plots_crop ON plots(crop_id);
CREATE INDEX IF NOT EXISTS idx_plots_planting_date ON plots(planting_date);

-- Datos de ejemplo

-- Agricultores
INSERT INTO farmers (name, email, region) VALUES
    ('Juan Pérez', 'juan.perez@example.com', 'Pampa Húmeda'),
    ('María González', 'maria.gonzalez@example.com', 'Zona Núcleo'),
    ('Carlos Rodríguez', 'carlos.rodriguez@example.com', 'NOA'),
    ('Ana Martínez', 'ana.martinez@example.com', 'Zona Núcleo'),
    ('Luis Fernández', 'luis.fernandez@example.com', 'Pampa Húmeda');

-- Cultivos
INSERT INTO crops (name, type, variety) VALUES
    ('Soja', 'oleaginosa', 'RR2 Intacta'),
    ('Maíz', 'cereal', 'DK7210'),
    ('Trigo', 'cereal', 'Baguette 31'),
    ('Girasol', 'oleaginosa', 'VDH 487'),
    ('Sorgo', 'cereal', 'ACA 546'),
    ('Algodón', 'fibra', 'Guazuncho 3'),
    ('Trigo', 'cereal', 'ACA 315'),
    ('Soja', 'oleaginosa', 'NA 5009');

-- Parcelas
INSERT INTO plots (name, hectares, farmer_id, crop_id, planting_date) VALUES
    ('Lote Norte A', 120.5, 1, 1, '2024-11-15'),
    ('Lote Sur B', 85.3, 1, 2, '2024-10-20'),
    ('Campo Central', 200.0, 2, 1, '2024-11-10'),
    ('Lote Este', 150.75, 2, 3, '2024-06-15'),
    ('Potrero Grande', 95.0, 3, 6, '2024-09-01'),
    ('Lote Oeste', 110.25, 3, 5, '2024-10-05'),
    ('Campo La Esperanza', 180.5, 4, 1, '2024-11-20'),
    ('Lote Chico', 45.0, 4, 4, '2024-08-15'),
    ('Parcela Norte', 130.0, 5, 2, '2024-10-25'),
    ('Lote Bajo', 75.5, 5, NULL, NULL);  -- Sin cultivo asignado aún

-- Triggers para mantener updated_at actualizado
CREATE TRIGGER IF NOT EXISTS update_farmers_timestamp
AFTER UPDATE ON farmers
BEGIN
    UPDATE farmers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_crops_timestamp
AFTER UPDATE ON crops
BEGIN
    UPDATE crops SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_plots_timestamp
AFTER UPDATE ON plots
BEGIN
    UPDATE plots SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Views útiles

-- Vista de parcelas con información completa
CREATE VIEW IF NOT EXISTS plots_full_info AS
SELECT
    p.id,
    p.name AS plot_name,
    p.hectares,
    p.planting_date,
    f.name AS farmer_name,
    f.email AS farmer_email,
    f.region,
    c.name AS crop_name,
    c.type AS crop_type,
    c.variety AS crop_variety
FROM plots p
JOIN farmers f ON p.farmer_id = f.id
LEFT JOIN crops c ON p.crop_id = c.id;

-- Vista de resumen por agricultor
CREATE VIEW IF NOT EXISTS farmer_summary AS
SELECT
    f.id,
    f.name,
    f.email,
    f.region,
    COUNT(p.id) AS total_plots,
    ROUND(SUM(p.hectares), 2) AS total_hectares,
    COUNT(p.crop_id) AS plots_with_crops
FROM farmers f
LEFT JOIN plots p ON f.id = p.farmer_id
GROUP BY f.id, f.name, f.email, f.region;

-- Vista de resumen por cultivo
CREATE VIEW IF NOT EXISTS crop_summary AS
SELECT
    c.id,
    c.name,
    c.type,
    c.variety,
    COUNT(p.id) AS total_plots,
    ROUND(SUM(p.hectares), 2) AS total_hectares
FROM crops c
LEFT JOIN plots p ON c.id = p.crop_id
GROUP BY c.id, c.name, c.type, c.variety;