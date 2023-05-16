#!/bin/bash

cd "$(dirname "$0")"

source credentials

FOLDER=location_01

PGPASSWORD=$PASSWORD psql -h $HOST -U $USER $DATABASE < cleanup.sql
PGPASSWORD=$PASSWORD psql -h $HOST -U $USER $DATABASE < $FOLDER/01_staff.sql
PGPASSWORD=$PASSWORD psql -h $HOST -U $USER $DATABASE < $FOLDER/02_ingredient.sql
PGPASSWORD=$PASSWORD psql -h $HOST -U $USER $DATABASE < $FOLDER/03_recipe.sql
PGPASSWORD=$PASSWORD psql -h $HOST -U $USER $DATABASE < $FOLDER/04_recipe_ingredient.sql
PGPASSWORD=$PASSWORD psql -h $HOST -U $USER $DATABASE < $FOLDER/05_menu.sql
PGPASSWORD=$PASSWORD psql -h $HOST -U $USER $DATABASE < $FOLDER/06_initial_stock.sql
