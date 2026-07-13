import csv
import os
import shutil
from datetime import datetime
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from psycopg2.extras import execute_values
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "development-secret-key",
)

# Limit uploaded CSV files to 2 MB.
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

PROJECT_ROOT = Path(__file__).resolve().parent
QUERY_FILE = PROJECT_ROOT / "sql" / "queries.sql"

DATA_FOLDER = PROJECT_ROOT / "data"
ARCHIVE_FOLDER = DATA_FOLDER / "archive"
CURRENT_DATA_FILE = DATA_FOLDER / "students.csv"

EXPECTED_COLUMNS = [
    "student_id",
    "school",
    "course",
    "current_progress",
    "weekly_progress",
    "grade",
    "days_since_login",
    "courses_remaining",
    "grade_level",
]


def get_database_connection():
    """Create and return a PostgreSQL connection."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )


def read_and_validate_csv(csv_path):
    """Read the uploaded CSV and validate its headings and data."""
    students = []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("The CSV does not contain a header row.")

        actual_columns = {
            column.strip()
            for column in reader.fieldnames
        }

        expected_columns = set(EXPECTED_COLUMNS)

        missing_columns = expected_columns - actual_columns
        extra_columns = actual_columns - expected_columns

        if missing_columns or extra_columns:
            error_parts = []

            if missing_columns:
                error_parts.append(
                    "Missing columns: "
                    + ", ".join(sorted(missing_columns))
                )

            if extra_columns:
                error_parts.append(
                    "Unexpected columns: "
                    + ", ".join(sorted(extra_columns))
                )

            raise ValueError("; ".join(error_parts))

        for row_number, row in enumerate(reader, start=2):
            try:
                student = (
                    row["student_id"].strip(),
                    row["school"].strip(),
                    row["course"].strip(),
                    int(row["current_progress"]),
                    int(row["weekly_progress"]),
                    int(row["grade"]),
                    int(row["days_since_login"]),
                    int(row["courses_remaining"]),
                    int(row["grade_level"]),
                )

            except (ValueError, AttributeError, KeyError) as error:
                raise ValueError(
                    f"Invalid data found on CSV row {row_number}."
                ) from error

            students.append(student)

    if not students:
        raise ValueError(
            "The uploaded CSV does not contain any student rows."
        )

    return students


def replace_database_students(students):
    """Replace all rows in the students table in one transaction."""
    insert_query = """
        INSERT INTO students (
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
        VALUES %s
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students;")
            execute_values(
                cursor,
                insert_query,
                students,
            )


@app.route("/")
def home():
    with QUERY_FILE.open("r", encoding="utf-8") as file:
        priority_query = file.read()

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(priority_query)
            students = cursor.fetchall()

    selected_grade_level = request.args.get(
        "grade_level",
        "all",
    )

    selected_school = request.args.get(
        "school",
        "all",
    )

    student_id_search = request.args.get(
        "student_id",
        "",
    ).strip()

    try:
        minimum_score = int(
            request.args.get("minimum_score", 0)
        )
    except ValueError:
        minimum_score = 0

    schools = sorted({
        student[1]
        for student in students
    })

    filtered_students = []

    for student in students:
        student_id = str(student[0])
        school = student[1]
        grade_level = str(student[3])
        priority_score = student[8]

        grade_matches = (
            selected_grade_level == "all"
            or grade_level == selected_grade_level
        )

        school_matches = (
            selected_school == "all"
            or school == selected_school
        )

        student_id_matches = (
            not student_id_search
            or student_id_search.lower() in student_id.lower()
        )

        score_matches = priority_score >= minimum_score

        if (
            grade_matches
            and school_matches
            and student_id_matches
            and score_matches
        ):
            filtered_students.append(student)

    return render_template(
        "index.html",
        students=filtered_students,
        student_count=len(filtered_students),
        selected_grade_level=selected_grade_level,
        selected_school=selected_school,
        student_id_search=student_id_search,
        minimum_score=minimum_score,
        schools=schools,
    )


@app.route("/upload", methods=["POST"])
def upload_csv():
    uploaded_file = request.files.get("student_file")

    if uploaded_file is None or uploaded_file.filename == "":
        flash(
            "Choose a CSV file before uploading.",
            "error",
        )
        return redirect(url_for("home"))

    filename = secure_filename(uploaded_file.filename)

    if not filename.lower().endswith(".csv"):
        flash(
            "Only CSV files can be uploaded.",
            "error",
        )
        return redirect(url_for("home"))

    DATA_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    ARCHIVE_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_file = DATA_FOLDER / f"upload_{filename}"

    try:
        uploaded_file.save(temporary_file)

        students = read_and_validate_csv(
            temporary_file
        )

        # Update PostgreSQL only after the CSV passes validation.
        replace_database_students(students)

        # Archive the previous current CSV after the database update succeeds.
        if CURRENT_DATA_FILE.exists():
            timestamp = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )

            archive_file = (
                ARCHIVE_FOLDER
                / f"students_before_{timestamp}.csv"
            )

            shutil.copy2(
                CURRENT_DATA_FILE,
                archive_file,
            )

        shutil.move(
            temporary_file,
            CURRENT_DATA_FILE,
        )

        flash(
            f"Upload successful. {len(students)} students loaded.",
            "success",
        )

    except (ValueError, psycopg2.Error) as error:
        flash(
            f"Upload failed: {error}",
            "error",
        )

    finally:
        if temporary_file.exists():
            temporary_file.unlink()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
    