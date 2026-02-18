#!/bin/bash

set +e
cd /app

export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Run pytest and capture to file
pytest test_assignment.py -v --tb=no -p no:cacheprovider > /tmp/pytest_output.txt 2>&1

# Simple parser to output JSON
python3 << 'EOF'
import json

# Read the pytest output
try:
    with open('/tmp/pytest_output.txt', 'r') as f:
        content = f.read()
except:
    content = ""

# Simple parsing - just count lines with PASSED/FAILED
tests = []
for line in content.split('\n'):
    if 'PASSED' in line and 'test_assignment.py' in line:
        parts = line.split('::')
        if len(parts) >= 3:
            test_name = parts[2].split(' ')[0]
            if test_name:
                tests.append({'name': test_name, 'status': 'passed', 'passed': True})
    elif 'FAILED' in line and 'test_assignment.py' in line:
        parts = line.split('::')
        if len(parts) >= 3:
            test_name = parts[2].split(' ')[0]
            if test_name:
                tests.append({'name': test_name, 'status': 'failed', 'passed': False})

# Build result
total = len(tests)
passed = sum(1 for t in tests if t['passed'])
failed = total - passed

result = {
    'tests': tests,
    'summary': {
        'total': total,
        'passed': passed,
        'failed': failed,
        'percentage': round((passed / total * 100) if total > 0 else 0, 1),
        'marks': round((passed / total) if total > 0 else 0, 2)
    }
}

# Output JSON to stdout
print(json.dumps(result, indent=2))

# Save to file
with open('/app/results.json', 'w') as f:
    json.dump(result, f, indent=2)
EOF

exit 0
