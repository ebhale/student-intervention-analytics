CREATE OR REPLACE VIEW public.student_intervention_view AS
SELECT
    students.*,

    (
        CASE
            WHEN grade_level::text = '12' THEN 20
            ELSE 0
        END

        +

        CASE
            WHEN weekly_progress < 10 THEN 10
            ELSE 0
        END

        +

        CASE
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
            WHEN days_since_login IN (12, 13) THEN 20
            WHEN days_since_login >= 14 THEN 40
            ELSE 0
        END

        +

        CASE
            WHEN courses_remaining = 1 THEN 10
            WHEN courses_remaining >= 2 THEN 20
            ELSE 0
        END
    ) AS priority_score,

    CONCAT_WS(
        ', ',

        CASE
            WHEN grade_level::text = '12'
            THEN 'Senior'
        END,

        CASE
            WHEN weekly_progress < 10
            THEN 'Weekly progress below 10%'
        END,

        CASE
            WHEN grade < 70
            THEN 'Grade below 70'
        END,

        CASE
            WHEN days_since_login = 7
            THEN 'Inactive 7 days'
            WHEN days_since_login = 8
            THEN 'Inactive 8 days'
            WHEN days_since_login = 9
            THEN 'Inactive 9 days'
            WHEN days_since_login = 10
            THEN 'Inactive 10 days'
            WHEN days_since_login = 11
            THEN 'Inactive 11 days'
            WHEN days_since_login IN (12, 13)
            THEN 'Inactive 12–13 days'
            WHEN days_since_login >= 14
            THEN 'Inactive 14+ days'
        END,

        CASE
            WHEN courses_remaining = 1
            THEN '1 course remaining'
            WHEN courses_remaining >= 2
            THEN '2+ courses remaining'
        END
    ) AS intervention_reasons

FROM public.students;
