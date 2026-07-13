import csv
from pathlib import Path


def calculate_priority_score(row):
    score = 0
    reasons = []

    if row.get("grade_level") == "12":
        score += 20
        reasons.append("Senior")

    weekly_progress = int(row.get("weekly_progress", "0"))
    if weekly_progress < 10:
        score += 10
        reasons.append("Weekly progress below 10%")

    grade = int(row.get("grade", "0"))
    if grade < 70:
        score += 10
        reasons.append("Grade below 70")

    days_since_login = int(row.get("days_since_login", "0"))

    if days_since_login == 7:
        score += 10
        reasons.append("Inactive 7 days")
    elif days_since_login == 8:
        score += 12
        reasons.append("Inactive 8 days")
    elif days_since_login == 9:
        score += 14
        reasons.append("Inactive 9 days")
    elif days_since_login == 10:
        score += 16
        reasons.append("Inactive 10 days")
    elif days_since_login == 11:
        score += 18
        reasons.append("Inactive 11 days")
    elif days_since_login in (12, 13):
        score += 20
        reasons.append("Inactive 12–13 days")
    elif days_since_login >= 14:
        score += 40
        reasons.append("Inactive 14+ days")

    courses_remaining = int(row.get("courses_remaining", "0"))

    if courses_remaining == 1:
        score += 10
        reasons.append("1 course remaining")
    elif courses_remaining >= 2:
        score += 20
        reasons.append("2+ courses remaining")

    return score, reasons


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "students.csv"

ranked_students = []

with open(DATA_FILE, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        score, reasons = calculate_priority_score(row)

        row["priority_score"] = score
        row["reasons"] = reasons

        ranked_students.append(row)

ranked_students.sort(
    key=lambda student: student["priority_score"],
    reverse=True
)

print("Top 10 Students for Intervention")
print("--------------------------------")

for rank, student in enumerate(ranked_students[:10], start=1):
    print(
        f"{rank}. {student['student_id']} | "
        f"Score: {student['priority_score']} | "
        f"Grade Level: {student['grade_level']} | "
        f"Grade: {student['grade']} | "
        f"Progress: {student['weekly_progress']}% | "
        f"Inactive: {student['days_since_login']} days"
    )

    print(f"   Reasons: {', '.join(student['reasons'])}")
    print()
 
