#!/bin/bash

# Episode 12 - Assignment 1: Form Data Processing & HTTP Request Handling
# Simple bash runner that outputs JSON results

set +e  # Don't exit on errors
cd /app

# Ensure we have enough resources
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Run pytest with minimal output overhead
timeout 120 pytest test_assignment.py -v --tb=short 2>&1 > /tmp/pytest_output.txt
PYTEST_EXIT=$?

# If pytest times out or fails hard, still try to output something
if [ $PYTEST_EXIT -eq 137 ] || [ $PYTEST_EXIT -eq 124 ]; then
    # Killed or timeout - output error JSON
    cat > /tmp/results_error.json << 'EOF'
{
  "tests": [],
  "summary": {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "percentage": 0,
    "marks": 0
  },
  "error": "Test execution timeout or killed (exit 137/124)"
}
EOF
    cat /tmp/results_error.json
    exit 0
fi

# Parse output and generate JSON using Python
python3 << 'PYTHON_EOF'
import json
import re
import sys
import os

try:
    # Read pytest output from file
    if not os.path.exists('/tmp/pytest_output.txt'):
        output = ""
    else:
        with open('/tmp/pytest_output.txt', 'r') as f:
            output = f.read()
    
    # Parse test results using regex
    tests = []
    for line in output.split('\n'):
        # Match: test_assignment.py::TestFormHandler::test_name PASSED or FAILED
        match = re.search(r'test_assignment\.py::TestFormHandler::(\w+)\s+(PASSED|FAILED)', line)
        if match:
            test_name = match.group(1)
            status = 'passed' if match.group(2) == 'PASSED' else 'failed'
            tests.append({
                'name': test_name,
                'status': status,
                'passed': status == 'passed'
            })
    
    # Calculate summary
    total = len(tests)
    passed = sum(1 for t in tests if t['passed'])
    failed = total - passed
    percentage = (passed / total * 100) if total > 0 else 0
    marks = passed / total if total > 0 else 0
    
    # Build JSON result
    result = {
        'tests': tests,
        'summary': {
            'total': total,
            'passed': passed,
            'failed': failed,
            'percentage': round(percentage, 1),
            'marks': round(marks, 2)
        }
    }

except Exception as e:
    result = {
        'tests': [],
        'summary': {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'percentage': 0,
            'marks': 0
        },
        'error': str(e)
    }

# Output JSON
sys.stdout.write(json.dumps(result, indent=2))
sys.stdout.write('\n')
sys.stdout.flush()

# Save to file
with open('/app/results.json', 'w') as f:
    json.dump(result, f, indent=2)

PYTHON_EOF

exit 0

