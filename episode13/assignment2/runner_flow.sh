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
timeout -s KILL 10 /usr/local/bin/python3 -m pytest test_assignment.py -v --tb=no -p no:cacheprovider 2>&1 > /tmp/pytest_output.txt || true

echo "5" >&2

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
    if 'PASSED' in line:
        parts = line.split('::')
        if len(parts) >= 3:
            test_name = parts[2].split(' ')[0]
            if test_name:
                tests.append({'name': test_name, 'status': 'passed', 'passed': True})
    elif 'FAILED' in line:
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

# Write to multiple locations for platform compatibility
with open('/app/results.json', 'w') as f:
    json.dump(result, f, indent=2)

# Also output as single line to stdout (some platforms prefer this)
print(json.dumps(result))
sys.stdout.flush()
EOF

echo "6" >&2
exit 0



