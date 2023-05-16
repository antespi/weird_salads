#!/bin/bash

# Exit in case of error
set -e

# Add initial data
docker-compose run --rm backend data/drop.sh
