#!/bin/bash

# Episode 12 - Assignment 1: Form Data Processing & HTTP Request Handling
# Simple bash runner that outputs JSON results

cd /app

# Run pytest and capture output
pytest test_assignment.py -v --tb=line > /tmp/pytest_output.txt 2>&1

# Parse pytest output and generate JSON
python3 << 'EOF'
import json
import re

# Read pytest output
with open('/tmp/pytest_output.txt', 'r') as f:
    output = f.read()

# Parse test results
tests = []
for line in output.split('\n'):
    match = re.search(r'test_assignment\.py::TestFormHandler::(\w+)\s+(PASSED|FAILED)', line)
    if match:
        test_name = match.group(1)
        status = 'passed' if match.group(2) == 'PASSED' else 'failed'
        tests.append({
            "name": test_name,
            "status": status,
            "passed": status == 'passed'
        })

# Calculate summary
total = len(tests)
passed = sum(1 for t in tests if t["passed"])
failed = total - passed
percentage = (passed / total * 100) if total > 0 else 0
marks = passed / total if total > 0 else 0

# Build JSON result
result = {
    "tests": tests,
    "summary": {
        "total": total,
        "passed": passed,
        "failed": failed,
        "percentage": round(percentage, 1),
        "marks": round(marks, 2)
    }
}

# Output JSON
print(json.dumps(result, indent=2))

# Save to file too
with open('/app/results.json', 'w') as f:
    json.dump(result, f, indent=2)
EOF

# Exit successfully
exit 0

