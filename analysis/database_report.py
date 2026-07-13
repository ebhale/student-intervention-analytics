import csv
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
QUERY_FILE = PROJECT_ROOT / "sql" / "queries.sql"
REPORT_FILE = PROJECT_ROOT / "reports" / "intervention_report.csv"


def create_intervention_report():
    load_dotenv(ENV_FILE)

    query = QUERY_FILE.read_text(encoding="utf-8")

    with psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)

            column_names = [
                column.name for column in cursor.description
            ]

            rows = cursor.fetchall()

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(rows)

    print(f"Report created: {REPORT_FILE}")
    print(f"Rows exported: {len(rows)}")


if __name__ == "__main__":
    try:
        create_intervention_report()
    except psycopg.Error as error:
        print(f"Database error: {error}")
    except FileNotFoundError as error:
        print(f"File not found: {error}")