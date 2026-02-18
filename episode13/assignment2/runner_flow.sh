#!/bin/bash

# Episode 13 - Assignment 2: Routing, Templates & PRG Pattern
# Portal-optimized runner matching Assignment 1 format

set +e
cd /app

# Memory-efficient Python environment
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Run pytest with aggressive timeout (90 seconds) to prevent hanging
timeout 90 pytest test_assignment.py -v --tb=no -p no:cacheprovider 2>&1 > /tmp/pytest_output.txt
PYTEST_EXIT=$?

# Parse output and generate JSON using Python
python3 << 'PYTHON_EOF'
import json
import re
import sys
import os

try:
    # Read pytest output
    output = ""
    if os.path.exists('/tmp/pytest_output.txt'):
        try:
            with open('/tmp/pytest_output.txt', 'r') as f:
                output = f.read()
        except:
            output = ""
    
    # Parse ALL test results (including partial output)
    tests = []
    seen_tests = set()
    
    for line in output.split('\n'):
        # Match: test_assignment.py::ClassName::test_name PASSED or FAILED
        match = re.search(r'test_assignment\.py::(\w+)::(\w+)\s+(PASSED|FAILED)', line)
        if match:
            test_name = match.group(2)
            # Avoid duplicates
            if test_name not in seen_tests:
                seen_tests.add(test_name)
                status = 'passed' if match.group(3) == 'PASSED' else 'failed'
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
    
    # Build result
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
    
    # Flag if partial output (16 tests total)
    if total < 16:
        result['note'] = 'Partial execution - portal may have timeout'

except Exception as e:
    result = {
        'tests': [],
        'summary': {'total': 0, 'passed': 0, 'failed': 0, 'percentage': 0, 'marks': 0},
        'error': str(e)
    }

# Output JSON immediately (exact format as Assignment 1)
sys.stdout.write(json.dumps(result, indent=2))
sys.stdout.write('\n')
sys.stdout.flush()

# Save to file
with open('/app/results.json', 'w') as f:
    json.dump(result, f, indent=2)

PYTHON_EOF

exit 0
