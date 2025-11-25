-- Active: 1764069994031@@127.0.0.1@5432
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    status VARCHAR(50) DEFAULT 'On Track'
);

CREATE TABLE daily_logs (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id),
    quiz_score INT,
    focus_minutes INT,
    log_date TIMESTAMP
);

CREATE TABLE interventions (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id),
    task TEXT,
    assigned_at TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE
);
