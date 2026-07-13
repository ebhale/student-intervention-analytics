# Student Intervention Analytics

I built this project to simulate a real student intervention workflow using fictional student data.

The goal was to take a process that could easily live in spreadsheets and turn it into a more complete system using Python, PostgreSQL, Flask, Docker, and Power BI.

The application:

- accepts a student CSV upload;
- checks the file for missing or invalid data;
- loads the records into PostgreSQL;
- calculates intervention priority scores;
- lets users search and filter student records;
- displays the results in a Flask web app;
- supports reporting in Power BI.

All student data in this repository is fictional.

## Why I Built It

In a real school setting, staff may need to review hundreds of student records and decide who needs outreach first.

I wanted to build a system that could help answer questions such as:

- Which students have not logged in recently?
- Which students are making less than 10% weekly progress?
- Which students have grades below 70%?
- Which seniors may need more immediate attention?
- Which students still have multiple courses remaining?

The project ranks students using a priority score so staff can focus on the highest-risk records first.

## Main Features

- Upload a new student CSV
- Validate the file before updating the database
- Archive the previous CSV
- Search by student ID
- Filter by school
- Filter by grade level
- Filter by minimum priority score
- Display ranked intervention records
- Store data in PostgreSQL
- Run the Flask app and PostgreSQL with Docker Compose
- Preserve database data with a Docker volume
- Load sample data automatically on a new installation

## Technologies

- Python
- Flask
- PostgreSQL
- SQL
- Docker
- Docker Compose
- Power BI
- Git and GitHub
- Linux / Ubuntu through WSL
- HTML and CSS
- DBeaver

## How the Priority Score Works

Students receive points based on risk factors such as:

| Risk factor | Points |
|---|---:|
| Grade 12 student | +20 |
| Weekly progress below 10% | +10 |
| Grade below 70% | +10 to +20 |
| Extended time since last login | Increasing points |
| One course remaining | +10 |
| Two or more courses remaining | +20 |

A higher score means the student may need more immediate outreach.

## Project Structure

```text
student-intervention-analytics/
├── analysis/
├── data/
├── docker-entrypoint-initdb.d/
├── powerbi/
├── reports/
├── scripts/
├── sql/
├── templates/
├── app.py
├── compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/ebhale/student-intervention-analytics.git
cd student-intervention-analytics
```

### 2. Create the environment file

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder password and secret key.

```bash
nano .env
```

### 3. Start the project

```bash
./scripts/start_project.sh
```

Then open:

```text
http://localhost:5000
```

The startup script checks the environment file, builds the containers, starts PostgreSQL, loads the sample data, and starts the Flask app.

## Docker Commands

Start the project:

```bash
docker compose up -d
```

Rebuild after changing Python or HTML files:

```bash
docker compose up -d --build
```

View the running containers:

```bash
docker compose ps
```

Stop the project:

```bash
docker compose down
```

Avoid using this unless you intentionally want to delete the PostgreSQL data volume:

```bash
docker compose down -v
```

## Power BI Dashboard

The Power BI dashboard connects to the PostgreSQL intervention view.

It includes:

- total student count;
- high-priority student count;
- average grade;
- average weekly progress;
- priority score distribution;
- school and grade-level filters;
- ranked student intervention table.

The dashboard file is located here:

```text
powerbi/Student_Intervention_Dashboard.pbix
```

## What I Learned

This project helped me practice how different tools work together as one system.

I worked with:

- Linux file and project management;
- Python data validation;
- Flask routes and forms;
- PostgreSQL tables, queries, and views;
- Docker images, containers, networks, and volumes;
- Git and GitHub version control;
- Power BI reporting;
- planning for future multi-user access.

## Future Improvements

The next version could include:

- user login;
- administrator and school-level roles;
- school-specific access;
- intervention notes and follow-up dates;
- upload history;
- audit logs;
- upsert logic instead of replacing the full table;
- production deployment.

## Project Status

This is a working portfolio prototype built with fictional student data. It is not intended for use with real student information in its current form.