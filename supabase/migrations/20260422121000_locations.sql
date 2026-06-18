-- SAFE DROP (trebuie să fie primul)
DROP TABLE IF EXISTS locations CASCADE;

-- Create table
CREATE TABLE locations (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index
CREATE INDEX idx_locations_city ON locations(city);

-- Function (poate exista deja, dar e ok)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger (ACUM e sigur, pentru că tabela există)
CREATE TRIGGER update_locations_updated_at
BEFORE UPDATE ON locations
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Seed data
INSERT INTO locations (name, address, city)
VALUES
('Universitatea Ștefan cel Mare', 'Strada Universității 13', 'Suceava'),
('Biblioteca USV', 'Strada Universității 13', 'Suceava'),
('Cămin C1 USV', 'Strada Universității 13', 'Suceava'),
('Cămin C2 USV', 'Strada Universității 13', 'Suceava'),
('Cămin C3 USV', 'Strada Universității 13', 'Suceava'),
('Aula Magna', 'Strada Universității 13', 'Suceava'),
('Corp E USV', 'Strada Universității 13', 'Suceava'),
('Corp D USV', 'Strada Universității 13', 'Suceava'),
('Cantina USV', 'Strada Universității 13', 'Suceava'),
('Parc USV', 'Strada Universității 13', 'Suceava');