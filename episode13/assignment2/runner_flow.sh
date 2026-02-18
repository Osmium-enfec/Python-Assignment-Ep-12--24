#!/bin/bash
set +e
cd /app
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Clean up port 8008 before running tests using Python
python3 << 'CLEANUP_EOF'
import socket
import time

for port in [8008]:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', port))
        sock.close()
        print(f"Port {port} is free")
    except OSError:
        print(f"Port {port} still in use, waiting...")
        time.sleep(2)
CLEANUP_EOF

# RUN pytest with timeout to prevent server hanging tests from stalling
timeout 60 pytest test_assignment.py -v --tb=short -p no:cacheprovider 2>&1 | tee /tmp/pytest_output.txt
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

# Parse individual test results - capture PASSED, FAILED, ERROR
# Match format: test_assignment.py::ClassName::test_name STATUS
pattern = r'test_assignment\.py::(\w+)::(\w+)\s+(PASSED|FAILED|ERROR)'
matches = re.findall(pattern, content)

for test_class, test_name, status in matches:
    total += 1
    is_passed = status == 'PASSED'
    if is_passed:
        passed += 1
    else:
        failed += 1
    
    test_entry = {
        "name": test_name,
        "status": status.lower(),
        "passed": is_passed
    }
    
    # Extract error message if ERROR status
    if status == 'ERROR':
        error_pattern = f'ERROR at setup of {test_class}::{test_name}.*?(?=ERROR at setup|=====|$)'
        error_match = re.search(error_pattern, content, re.DOTALL)
        if error_match:
            error_text = error_match.group(0)
            # Extract the actual error line
            error_line_match = re.search(r'E\s+(.*?)$', error_text, re.MULTILINE)
            if error_line_match:
                test_entry["error"] = error_line_match.group(1).strip()
    
    tests.append(test_entry)

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
