-- SAFE DROP
DROP TABLE IF EXISTS feedback CASCADE;

-- CREATE TABLE
CREATE TABLE feedback (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    event_id BIGINT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    -- FOREIGN KEYS
    CONSTRAINT fk_feedback_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_feedback_event
        FOREIGN KEY (event_id)
        REFERENCES events(id)
        ON DELETE CASCADE,

    -- OPTIONAL: un user poate da un singur feedback per event
    CONSTRAINT unique_user_event_feedback UNIQUE (user_id, event_id)
);

-- =========================
-- INDEX-uri (important pentru performanță)
-- =========================
CREATE INDEX idx_feedback_user_id ON feedback(user_id);
CREATE INDEX idx_feedback_event_id ON feedback(event_id);
CREATE INDEX idx_feedback_rating ON feedback(rating);

-- =========================
-- TRIGGER updated_at
-- =========================
CREATE TRIGGER update_feedback_updated_at
BEFORE UPDATE ON feedback
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- =========================
-- SEED DATA (opțional)
-- =========================

INSERT INTO feedback (user_id, event_id, rating, comment)
VALUES
(3, 1, 5, 'Super eveniment!'),
(2, 1, 4, 'Foarte bun, dar putea fi mai lung'),
(3, 2, 5, 'Explicații excelente'),
(4, 3, 3, 'OK, dar nu foarte util'),
(4, 4, 5, 'Foarte interesant'),
(5, 5, 4, 'Mi-a plăcut mult');