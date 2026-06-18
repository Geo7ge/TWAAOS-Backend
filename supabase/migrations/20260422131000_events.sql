-- SAFE DROP
DROP TABLE IF EXISTS events CASCADE;

-- CREATE TABLE
CREATE TABLE events (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    location_id BIGINT,
    category_name VARCHAR(100),
    organizer_id BIGINT,
    participation_type VARCHAR(50),
    registration_link VARCHAR(255),
    qr_code VARCHAR(255),
    max_participants INTEGER,
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- INDEX-uri (foarte importante pentru query-uri)
CREATE INDEX idx_events_location_id ON events(location_id);
CREATE INDEX idx_events_organizer_id ON events(organizer_id);
CREATE INDEX idx_events_category ON events(category_name);
CREATE INDEX idx_events_start_time ON events(start_time);

-- UPDATE FUNCTION (dacă nu există deja global)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER
CREATE TRIGGER update_events_updated_at
BEFORE UPDATE ON events
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- =========================
-- SEED DATA (10 EVENTS)
-- ATENȚIE: presupunem că ai deja users + locations
-- =========================

INSERT INTO events (
    title,
    description,
    start_time,
    end_time,
    location_id,
    category_name,
    organizer_id,
    participation_type,
    registration_link,
    qr_code,
    max_participants,
    deadline
)
VALUES

('Hackathon USV 2026', 'Competiție de programare de 24h', NOW(), NOW() + INTERVAL '1 day', 1, 'IT', 6, 'offline', NULL, NULL, 100, NOW() + INTERVAL '2 days'),
('Workshop React', 'Introducere în React pentru începători', NOW(), NOW() + INTERVAL '3 hours', 2, 'IT', 6, 'online', NULL, NULL, 50, NOW() + INTERVAL '1 day'),
('Career Day', 'Întâlnire cu companii IT', NOW(), NOW() + INTERVAL '5 hours', 1, 'Career', 7, 'offline', NULL, NULL, 200, NOW() + INTERVAL '3 days'),
('AI Seminar', 'Discuții despre inteligența artificială', NOW(), NOW() + INTERVAL '2 hours', 6, 'AI', 7, 'offline', NULL, NULL, 80, NOW() + INTERVAL '2 days'),
('Python Bootcamp', 'Curs intensiv Python', NOW(), NOW() + INTERVAL '2 days', 3, 'Programming', 8, 'online', NULL, NULL, 120, NOW() + INTERVAL '4 days'),
('Cybersecurity Talk', 'Bazele securității cibernetice', NOW(), NOW() + INTERVAL '4 hours', 4, 'Security', 8, 'offline', NULL, NULL, 90, NOW() + INTERVAL '2 days'),
('Startup Pitch', 'Prezentare idei de startup', NOW(), NOW() + INTERVAL '6 hours', 5, 'Business', 9, 'offline', NULL, NULL, 60, NOW() + INTERVAL '3 days'),
('Mobile Dev Meetup', 'Flutter & React Native', NOW(), NOW() + INTERVAL '3 hours', 7, 'Mobile', 9, 'online', NULL, NULL, 70, NOW() + INTERVAL '2 days'),
('Database Workshop', 'SQL și design baze de date', NOW(), NOW() + INTERVAL '5 hours', 8, 'Data', 10, 'offline', NULL, NULL, 110, NOW() + INTERVAL '3 days'),
('Tech Conference USV', 'Conferință tehnologică anuală', NOW(), NOW() + INTERVAL '1 day 6 hours', 9, 'Conference', 10, 'offline', NULL, NULL, 300, NOW() + INTERVAL '5 days');