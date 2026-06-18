-- SAFE DROP
DROP TABLE IF EXISTS sponsors CASCADE;

-- Create table
CREATE TABLE sponsors (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    logo_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index (căutare rapidă după nume)
CREATE INDEX idx_sponsors_name ON sponsors(name);

-- Function (poate exista deja în DB)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER update_sponsors_updated_at
BEFORE UPDATE ON sponsors
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- =========================
-- SEED 10 SPONSORS
-- =========================

INSERT INTO sponsors (name, logo_url)
VALUES
('Google', 'https://logo.clearbit.com/google.com'),
('Microsoft', 'https://logo.clearbit.com/microsoft.com'),
('Amazon', 'https://logo.clearbit.com/amazon.com'),
('Apple', 'https://logo.clearbit.com/apple.com'),
('Meta', 'https://logo.clearbit.com/meta.com'),
('IBM', 'https://logo.clearbit.com/ibm.com'),
('Oracle', 'https://logo.clearbit.com/oracle.com'),
('Samsung', 'https://logo.clearbit.com/samsung.com'),
('Adobe', 'https://logo.clearbit.com/adobe.com'),
('Spotify', 'https://logo.clearbit.com/spotify.com');