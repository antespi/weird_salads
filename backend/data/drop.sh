#!/bin/bash

cd "$(dirname "$0")"

source credentials


PGPASSWORD=$PASSWORD psql -h $HOST -U $USER $DATABASE < drop.sql

echo "Reloading DB schema"
python3 ../app/main.py
