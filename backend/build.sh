#!/usr/bin/env bash
# Render build script

# Exit on error
set -e

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Running database migrations if needed..."
# Optional: Add any migration commands here if you use Alembic
# alembic upgrade head

echo "Build completed successfully!"
