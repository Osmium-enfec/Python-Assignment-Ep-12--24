#!/bin/bash

# Episode 12 - Assignment 1: Form Data Processing & HTTP Request Handling
# Simple bash runner that outputs JSON results

set -e
cd /app

# Run pytest and capture output
pytest test_assignment.py -v --tb=line 2>&1 | tee /tmp/pytest_output.txt

# Generate JSON using Python and output immediately
python3 -c "
import json
import re
import sys

try:
    # Read pytest output from file
    with open('/tmp/pytest_output.txt', 'r') as f:
        output = f.read()
    
    # Parse test results using regex
    tests = []
    for line in output.split('\n'):
        if 'test_assignment.py::TestFormHandler::' in line and ('PASSED' in line or 'FAILED' in line):
            match = re.search(r'::(\w+)\s+(PASSED|FAILED)', line)
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
    
    # Output JSON to stdout
    print(json.dumps(result, indent=2), file=sys.stdout, flush=True)
    sys.stdout.flush()
    
    # Save to file as backup
    with open('/app/results.json', 'w') as f:
        json.dump(result, f, indent=2)
        
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
        'error': str(e),
        'traceback': traceback.format_exc()
    }
    print(json.dumps(result, indent=2), file=sys.stdout, flush=True)
    sys.stdout.flush()
" 2>&1

exit 0

