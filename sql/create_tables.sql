CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    school TEXT NOT NULL,
    course TEXT NOT NULL,
    current_progress INTEGER NOT NULL,
    weekly_progress INTEGER NOT NULL,
    grade INTEGER NOT NULL,
    days_since_login INTEGER NOT NULL,
    courses_remaining INTEGER NOT NULL,
    grade_level integer NOT NULL
);
