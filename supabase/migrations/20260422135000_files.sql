-- SAFE DROP
DROP TABLE IF EXISTS files CASCADE;

-- CREATE TABLE
CREATE TABLE files (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    event_id BIGINT NOT NULL,
    file_url VARCHAR(255) NOT NULL,
    file_type VARCHAR(50), -- pdf | image | presentation
    uploaded_at TIMESTAMP DEFAULT NOW(),

    -- FOREIGN KEY
    CONSTRAINT fk_files_event
        FOREIGN KEY (event_id)
        REFERENCES events(id)
        ON DELETE CASCADE
);

-- =========================
-- INDEX-uri
-- =========================
CREATE INDEX idx_files_event_id ON files(event_id);
CREATE INDEX idx_files_file_type ON files(file_type);
CREATE INDEX idx_files_uploaded_at ON files(uploaded_at);

-- =========================
-- SEED DATA (10 FILES)
-- presupunem că events 1–10 există
-- =========================

INSERT INTO files (event_id, file_url, file_type)
VALUES

(1, 'https://example.com/files/hackathon_agenda.pdf', 'pdf'),
(1, 'https://example.com/files/hackathon_rules.pdf', 'pdf'),
(2, 'https://example.com/files/react_intro_slides.pdf', 'presentation'),
(2, 'https://example.com/files/react_examples.zip', 'presentation'),
(3, 'https://example.com/files/career_companies_list.pdf', 'pdf'),
(4, 'https://example.com/files/ai_seminar_notes.pdf', 'pdf'),
(5, 'https://example.com/files/python_bootcamp_materials.pdf', 'pdf'),
(6, 'https://example.com/files/cybersecurity_talk.pdf', 'pdf'),
(7, 'https://example.com/files/startup_pitch_template.pptx', 'presentation'),
(8, 'https://example.com/files/mobile_dev_resources.pdf', 'pdf');