-- Calculate intervention priority scores using the same rules as analyze.py
SELECT
    student_id,
    school,
    course,
    grade_level,
    weekly_progress,
    grade,
    days_since_login,
    courses_remaining,

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
    END AS priority_score

FROM students
ORDER BY priority_score DESC;
