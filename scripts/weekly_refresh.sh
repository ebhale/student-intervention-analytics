#!/bin/bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SOURCE_FILE="${1:-}"
SNAPSHOT_DATE="${2:-$(date +%F)}"

DATA_FILE="$PROJECT_ROOT/data/students.csv"
REPORT_FILE="$PROJECT_ROOT/reports/intervention_report.csv"

DATA_ARCHIVE="$PROJECT_ROOT/data/archive"
REPORT_ARCHIVE="$PROJECT_ROOT/reports/archive"

if [[ -z "$SOURCE_FILE" ]]; then
    echo "Usage:"
    echo "  ./scripts/weekly_refresh.sh SOURCE_CSV [YYYY-MM-DD]"
    exit 1
fi

if [[ ! -f "$SOURCE_FILE" ]]; then
    echo "Source file not found: $SOURCE_FILE"
    exit 1
fi

mkdir -p "$DATA_ARCHIVE" "$REPORT_ARCHIVE"

echo "Starting weekly refresh for $SNAPSHOT_DATE"

# Preserve the current files before replacing them.
if [[ -f "$DATA_FILE" ]]; then
    cp "$DATA_FILE" \
        "$DATA_ARCHIVE/students_before_$SNAPSHOT_DATE.csv"
fi

if [[ -f "$REPORT_FILE" ]]; then
    cp "$REPORT_FILE" \
        "$REPORT_ARCHIVE/intervention_report_before_$SNAPSHOT_DATE.csv"
fi

# Copy the new weekly student file into the working location.
cp "$SOURCE_FILE" "$DATA_FILE"

echo "New student file copied."

# Confirm the CSV contains data.
LINE_COUNT=$(wc -l < "$DATA_FILE")

if [[ "$LINE_COUNT" -lt 2 ]]; then
    echo "The CSV is empty or contains only a header."
    exit 1
fi

echo "CSV line count: $LINE_COUNT"

cd "$PROJECT_ROOT"

sudo -u postgres psql \
    -d credit_recovery \
    < "$PROJECT_ROOT/sql/import_data.sql"

echo "PostgreSQL refreshed."

# Generate the intervention report using the active Python environment.
python "$PROJECT_ROOT/analysis/database_report.py"

echo "Report generated."

# Save dated copies of the new input and output.
cp "$DATA_FILE" \
    "$DATA_ARCHIVE/students_$SNAPSHOT_DATE.csv"

cp "$REPORT_FILE" \
    "$REPORT_ARCHIVE/intervention_report_$SNAPSHOT_DATE.csv"

echo
echo "Weekly refresh complete."
echo "Input archive:"
echo "  $DATA_ARCHIVE/students_$SNAPSHOT_DATE.csv"
echo "Report archive:"
echo "  $REPORT_ARCHIVE/intervention_report_$SNAPSHOT_DATE.csv"