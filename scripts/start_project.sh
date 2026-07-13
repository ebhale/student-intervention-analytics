#!/usr/bin/env bash

set -euo pipefail

ENV_FILE=".env"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "Error: .env does not exist."
    echo
    echo "Create it with:"
    echo "  cp .env.example .env"
    echo
    echo "Then edit the password and secret key before starting."
    exit 1
fi

get_env_value() {
    local variable_name="$1"

    grep -E "^${variable_name}=" "$ENV_FILE" \
        | tail -n 1 \
        | cut -d "=" -f 2-
}

DB_PASSWORD="$(get_env_value "DB_PASSWORD")"
FLASK_SECRET_KEY="$(get_env_value "FLASK_SECRET_KEY")"

if [[ -z "$DB_PASSWORD" ]]; then
    echo "Error: DB_PASSWORD is empty in .env."
    exit 1
fi

if [[ "$DB_PASSWORD" == "replace-with-a-secure-password" ]]; then
    echo "Error: Replace the placeholder DB_PASSWORD in .env."
    exit 1
fi

if [[ -z "$FLASK_SECRET_KEY" ]]; then
    echo "Error: FLASK_SECRET_KEY is empty in .env."
    exit 1
fi

if [[ "$FLASK_SECRET_KEY" == "replace-with-a-random-secret-key" ]]; then
    echo "Error: Replace the placeholder FLASK_SECRET_KEY in .env."
    exit 1
fi

echo "Environment configuration looks valid."
echo "Starting Student Intervention Analytics..."

docker compose up -d --build

echo
echo "Application started."
echo "Open: http://localhost:5000"
