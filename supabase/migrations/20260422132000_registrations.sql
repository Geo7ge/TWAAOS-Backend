-- =========================
-- CLEANUP (SAFE MIGRATION)
-- =========================

-- Drop table first (CASCADE removes triggers, constraints, indexes)
DROP TABLE IF EXISTS registrations CASCADE;


-- =========================
-- CREATE TABLE
-- =========================

CREATE TABLE registrations (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    event_id BIGINT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, confirmed, cancelled, attended
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Foreign keys
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_event
        FOREIGN KEY (event_id)
        REFERENCES events(id)
        ON DELETE CASCADE,

    -- Prevent duplicate registrations
    CONSTRAINT unique_user_event_registration UNIQUE (user_id, event_id)
);


-- =========================
-- INDEXES
-- =========================

CREATE INDEX idx_registrations_user_id ON registrations(user_id);
CREATE INDEX idx_registrations_event_id ON registrations(event_id);
CREATE INDEX idx_registrations_status ON registrations(status);


-- =========================
-- TRIGGER (updated_at)
-- =========================

-- This function must already exist:
-- update_updated_at_column()

CREATE TRIGGER update_registrations_updated_at
BEFORE UPDATE ON registrations
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


-- =========================
-- TEST DATA
-- =========================

INSERT INTO registrations (user_id, event_id, status)
VALUES
(2, 2, 'confirmed'),
(2, 3, 'pending'),
(3, 4, 'confirmed'),
(4, 5, 'cancelled'),
(5, 3, 'attended');