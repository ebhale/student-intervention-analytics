# Student Intervention Analytics Project

This project simulates a real-world student intervention analytics workflow.

It uses fictional student data to identify students who may need additional support based on factors such as:

- Grade level
- Weekly course progress
- Current grade
- Days since last login
- Number of courses remaining

## Project Goals

This project demonstrates how to:

- Work in a Linux environment
- Store structured student data in PostgreSQL
- Import CSV data into a database
- Query and rank students using SQL
- Connect Python directly to PostgreSQL
- Export intervention reports with Python
- Explore database results with DBeaver
- Package the application with Docker
- Build a Flask application in a later stage

## Technologies

- Linux / Ubuntu through WSL
- Python
- PostgreSQL
- SQL
- DBeaver
- Docker
- Flask
- CSV

## Project Structure

```text
credit_recovery/
├── analysis/
│   ├── analyze.py
│   └── database_report.py
├── data/
│   └── students.csv
├── reports/
│   └── intervention_report.csv
├── sql/
│   ├── create_tables.sql
│   ├── import_data.sql
│   └── queries.sql
├── .env
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt

## Power BI Dashboard

The Power BI dashboard connects to the PostgreSQL
`public.student_intervention_view`.

It includes:

- Total student count
- High-priority student count
- Average grade
- Average weekly progress
- Priority score distribution
- School and grade-level filters
- Ranked student intervention table

Dashboard file:

`powerbi/Student_Intervention_Dashboard.pbix`