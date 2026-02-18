#!/bin/bash

# Episode 12 - Assignment 1: Form Data Processing & HTTP Request Handling
# Simple bash runner that outputs JSON results

cd /app

# Run pytest and save output to file (no tee)
pytest test_assignment.py -v --tb=short > /tmp/pytest_output.txt 2>&1
PYTEST_EXIT=$?

# Parse output and generate JSON using Python
python3 << 'PYTHON_EOF'
import json
import re
import sys

try:
    # Read pytest output from file
    with open('/tmp/pytest_output.txt', 'r') as f:
        output = f.read()
    
    # Parse test results using regex - look for the test line pattern
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
    import traceback
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

# Output JSON to stdout
print(json.dumps(result, indent=2))
sys.stdout.flush()

# Save to file
with open('/app/results.json', 'w') as f:
    json.dump(result, f, indent=2)

PYTHON_EOF

exit 0

