#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run database setup and seed script safely
python -c "from app import setup_database; setup_database()"
python seed_products.py
