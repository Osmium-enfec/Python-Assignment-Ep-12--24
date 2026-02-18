#!/bin/bash

# Episode 12 - Assignment 1: Form Data Processing & HTTP Request Handling
# Runner flow - executed inside Docker container at /app/runner.sh
# Outputs results in JSON format with test cases and summary

cd /app

# Run the Python test results generator with unbuffered output
export PYTHONUNBUFFERED=1
exec python3 -u /app/generate_results.py

