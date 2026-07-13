COPY students (
    student_id,
    school,
    course,
    current_progress,
    weekly_progress,
    grade,
    days_since_login,
    courses_remaining,
    grade_level
)
FROM '/docker-entrypoint-initdb.d/students.csv'
WITH (
    FORMAT CSV,
    HEADER
);
