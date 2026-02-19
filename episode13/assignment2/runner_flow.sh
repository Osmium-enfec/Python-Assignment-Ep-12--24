#!/bin/bash

set +e
cd /app

export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

echo "1" >&2
echo "2" >&2  
echo "3" >&2

# Try to run pytest with explicit python path
echo "4" >&2
/usr/local/bin/python3 -m pytest test_assignment.py -v --tb=no -p no:cacheprovider > /tmp/pytest_output.txt 2>&1 &
PYTEST_PID=$!

# Wait with timeout
sleep 20
if kill -0 $PYTEST_PID 2>/dev/null; then
    echo "DEBUG: Killing pytest (timeout)" >&2
    kill $PYTEST_PID 2>/dev/null
    wait $PYTEST_PID 2>/dev/null
fi

echo "5" >&2
PYTEST_EXIT=$?
echo "DEBUG: Pytest exit: $PYTEST_EXIT" >&2

# Parse and output JSON
python3 << 'EOF'
import json
import sys

try:
    with open('/tmp/pytest_output.txt', 'r') as f:
        content = f.read()
except:
    content = ""

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

print(json.dumps(result, indent=2))
sys.stdout.flush()

with open('/app/results.json', 'w') as f:
    json.dump(result, f, indent=2)
EOF

echo "6" >&2
exit 0



