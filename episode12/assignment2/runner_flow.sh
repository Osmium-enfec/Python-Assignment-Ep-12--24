#!/bin/bash
set +e
cd /app
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# RUN pytest WITHOUT timeout - let portal control execution
pytest test_assignment.py -v --tb=no -p no:cacheprovider 2>&1 > /tmp/pytest_output.txt &
PYTEST_PID=$!

wait $PYTEST_PID 2>/dev/null
PYTEST_EXIT=$?

# Python subprocess parses output and generates JSON
python3 << 'PYTHON_EOF'
import json
import re
import sys
import os

output_file = '/tmp/pytest_output.txt'
tests = []
passed = 0
failed = 0
total = 0

# Read pytest output
try:
    with open(output_file, 'r') as f:
        content = f.read()
except:
    content = ""

# Parse individual test results
pattern = r'test_assignment\.py::TestSessionHandler::(\w+)\s+(PASSED|FAILED)'
matches = re.findall(pattern, content)

for test_name, status in matches:
    total += 1
    is_passed = status == 'PASSED'
    if is_passed:
        passed += 1
    else:
        failed += 1
    tests.append({
        "name": test_name,
        "status": status.lower(),
        "passed": is_passed
    })

if total == 0 and content:
    note = "Partial execution - some tests may not have been captured"
else:
    note = None

percentage = (passed / total * 100.0) if total > 0 else 0.0
marks = (passed / total) if total > 0 else 0.0

result = {
    "tests": tests,
    "summary": {
        "total": total,
        "passed": passed,
        "failed": failed,
        "percentage": percentage,
        "marks": marks
    }
}

if note:
    result["note"] = note

# Output JSON to stdout
sys.stdout.write(json.dumps(result, indent=2) + '\n')
sys.stdout.flush()

# Also save to file
with open('/app/results.json', 'w') as f:
    json.dump(result, f, indent=2)

PYTHON_EOF

exit 0
