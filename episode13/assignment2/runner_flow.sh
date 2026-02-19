#!/bin/bash

# Episode 13 - Assignment 2: Routing, Templates & PRG Pattern
# Following Assignment 1 proven approach

set +e
cd /app

export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Run pytest in background - let portal control timeout
pytest test_assignment.py -v --tb=no -p no:cacheprovider 2>&1 > /tmp/pytest_output.txt &
PYTEST_PID=$!

# Wait for pytest
wait $PYTEST_PID 2>/dev/null
PYTEST_EXIT=$?

# Parse and output JSON
python3 << 'PYTHON_EOF'
import json
import re
import sys
import os

try:
    output = ""
    if os.path.exists('/tmp/pytest_output.txt'):
        with open('/tmp/pytest_output.txt', 'r') as f:
            output = f.read()
    
    tests = []
    seen_tests = set()
    
    # Match: test_assignment.py::ClassName::test_name PASSED or FAILED
    for line in output.split('\n'):
        match = re.search(r'test_assignment\.py::(\w+)::(\w+)\s+(PASSED|FAILED)', line)
        if match:
            test_name = match.group(2)
            if test_name not in seen_tests:
                seen_tests.add(test_name)
                status = 'passed' if match.group(3) == 'PASSED' else 'failed'
                tests.append({
                    'name': test_name,
                    'status': status,
                    'passed': status == 'passed'
                })
    
    total = len(tests)
    passed = sum(1 for t in tests if t['passed'])
    failed = total - passed
    percentage = (passed / total * 100) if total > 0 else 0
    marks = passed / total if total > 0 else 0
    
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
    
    if total < 16:
        result['note'] = 'Partial execution - portal may have timeout'

except Exception as e:
    result = {
        'tests': [],
        'summary': {'total': 0, 'passed': 0, 'failed': 0, 'percentage': 0, 'marks': 0},
        'error': str(e)
    }

sys.stdout.write(json.dumps(result, indent=2))
sys.stdout.write('\n')
sys.stdout.flush()

with open('/app/results.json', 'w') as f:
    json.dump(result, f, indent=2)

PYTHON_EOF

exit 0





