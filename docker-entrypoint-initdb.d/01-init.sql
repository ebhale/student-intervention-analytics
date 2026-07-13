CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    school TEXT NOT NULL,
    course TEXT NOT NULL,
    current_progress INTEGER NOT NULL,
    weekly_progress INTEGER NOT NULL,
    grade INTEGER NOT NULL,
    days_since_login INTEGER NOT NULL,
    courses_remaining INTEGER NOT NULL,
    grade_level INTEGER NOT NULL
);

CREATE OR REPLACE VIEW public.student_intervention_view AS
SELECT
    students.*,
    (
        CASE
            WHEN grade_level = 12 THEN 20
            ELSE 0
        END
        +
        CASE
            WHEN weekly_progress < 10 THEN 10
            ELSE 0
        END
        +
        CASE
            WHEN grade < 50 THEN 20
            WHEN grade < 60 THEN 15
            WHEN grade < 70 THEN 10
            ELSE 0
        END
        +
        CASE
            WHEN days_since_login = 7 THEN 10
            WHEN days_since_login = 8 THEN 12
            WHEN days_since_login = 9 THEN 14
            WHEN days_since_login = 10 THEN 16
            WHEN days_since_login = 11 THEN 18
            WHEN days_since_login = 12 THEN 20
            WHEN days_since_login = 13 THEN 22
            WHEN days_since_login = 14 THEN 25
            WHEN days_since_login >= 15 THEN 30
            ELSE 0
        END
        +
        CASE
            WHEN courses_remaining = 1 THEN 10
            WHEN courses_remaining >= 2 THEN 20
            ELSE 0
        END
    ) AS priority_score
FROM public.students;
