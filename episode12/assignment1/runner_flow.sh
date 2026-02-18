#!/bin/bash

# Episode 12 - Assignment 1: Form Data Processing & HTTP Request Handling
# Runner flow - executed inside Docker container at /app/runner.sh
# Outputs results in JSON format with test cases and summary

set -e

cd /app

# Set Python to unbuffered mode
export PYTHONUNBUFFERED=1

# Run the Python test results generator
# Save output to both a log file and stdout
python3 -u /app/generate_results.py 2>&1 | tee /app/runner.log

# Exit successfully even if tests fail (we captured the results)
exit 0

