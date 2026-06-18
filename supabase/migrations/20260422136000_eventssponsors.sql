-- SAFE DROP
DROP TABLE IF EXISTS event_sponsors CASCADE;

-- CREATE TABLE
CREATE TABLE event_sponsors (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    event_id BIGINT NOT NULL,
    sponsor_id BIGINT NOT NULL,

    -- FOREIGN KEYS
    CONSTRAINT fk_event_sponsors_event
        FOREIGN KEY (event_id)
        REFERENCES events(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_event_sponsors_sponsor
        FOREIGN KEY (sponsor_id)
        REFERENCES sponsors(id)
        ON DELETE CASCADE,

    -- evităm duplicate (același sponsor la același event)
    CONSTRAINT unique_event_sponsor UNIQUE (event_id, sponsor_id)
);

-- =========================
-- INDEX-uri (pentru query-uri rapide)
-- =========================
CREATE INDEX idx_event_sponsors_event_id ON event_sponsors(event_id);
CREATE INDEX idx_event_sponsors_sponsor_id ON event_sponsors(sponsor_id);

-- =========================
-- SEED DATA (5 relații)
-- presupunem:
-- events: 1-10
-- sponsors: 1-5
-- =========================

INSERT INTO event_sponsors (event_id, sponsor_id)
VALUES
(1, 1),
(1, 2),
(2, 2),
(3, 3),
(4, 5);