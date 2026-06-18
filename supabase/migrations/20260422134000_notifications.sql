-- SAFE DROP
DROP TABLE IF EXISTS notifications CASCADE;

-- CREATE TABLE
CREATE TABLE notifications (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    event_id BIGINT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- FOREIGN KEYS
    CONSTRAINT fk_notifications_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_notifications_event
        FOREIGN KEY (event_id)
        REFERENCES events(id)
        ON DELETE CASCADE
);

-- =========================
-- INDEX-uri (IMPORTANT)
-- =========================
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_event_id ON notifications(event_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);

-- =========================
-- TRIGGER updated_at
-- =========================
CREATE TRIGGER update_notifications_updated_at
BEFORE UPDATE ON notifications
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- =========================
-- SEED DATA (opțional)
-- =========================

INSERT INTO notifications (user_id, event_id, message, is_read)
VALUES
(6, 1, 'Te-ai înscris la Hackathon USV 2026', FALSE),
(2, 1, 'Evenimentul începe în curând', FALSE),
(3, 2, 'Workshop React a fost actualizat', TRUE),
(6, 3, 'Ai primit confirmarea participării', FALSE),
(4, 4, 'Evenimentul AI Seminar începe în 1 oră', FALSE),
(5, 5, 'Bootcamp Python a fost mutat online', TRUE);