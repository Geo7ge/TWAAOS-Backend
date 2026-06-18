-- Drop trigger if exists
DROP TRIGGER IF EXISTS update_users_updated_at ON users;

-- Drop function if exists
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Drop table if exists
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE users (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    role VARCHAR(100) DEFAULT 'student',
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index on email
CREATE INDEX idx_users_email ON users(email);

-- Function for automatic updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for updated_at
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Insert test users with password: password123
INSERT INTO users (email, name, role, password)
VALUES
-- 5 STUDENȚI
('student1@student.usv.ro', 'Student One', 'student', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2'),
('student2@student.usv.ro', 'Student Two', 'student', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2'),
('student3@student.usv.ro', 'Student Three', 'student', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2'),
('student4@student.usv.ro', 'Student Four', 'student', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2'),
('student5@student.usv.ro', 'Student Five', 'student', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2'),

-- 5 ORGANIZATORI
('organizer1@usv.ro', 'Organizer One', 'organizer', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2'),
('organizer2@usv.ro', 'Organizer Two', 'organizer', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2'),
('organizer3@usv.ro', 'Organizer Three', 'organizer', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2'),
('organizer4@usv.ro', 'Organizer Four', 'organizer', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2'),
('organizer5@usv.ro', 'Organizer Five', 'organizer', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2'),
-- 1 ADMIN
('admin@usv.ro', 'Admin User', 'admin', '$2b$12$e0NRa9Fqzj0s0xY4f6y2Xu7M8e3UjNQxXjJkY4zYxgW4v0f3xK6m2');