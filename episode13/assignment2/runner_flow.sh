#!/bin/bash

set +e
cd /app

export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

echo "DEBUG: Starting tests..." >&2
echo "DEBUG: PWD=$(pwd)" >&2
echo "DEBUG: Files: $(ls -la /app/*.py 2>/dev/null | wc -l)" >&2

# Run pytest and capture to file with timeout
echo "DEBUG: Running pytest..." >&2
timeout 30 pytest test_assignment.py -v --tb=short -p no:cacheprovider > /tmp/pytest_output.txt 2>&1
PYTEST_EXIT=$?
echo "DEBUG: Pytest exit code: $PYTEST_EXIT" >&2
echo "DEBUG: Pytest output size: $(wc -c < /tmp/pytest_output.txt 2>/dev/null || echo '0') bytes" >&2

# Show first 5 and last 5 lines
echo "DEBUG: First 5 lines:" >&2
head -5 /tmp/pytest_output.txt >&2
echo "DEBUG: Last 5 lines:" >&2
tail -5 /tmp/pytest_output.txt >&2

# Simple parser to output JSON
python3 << 'EOF'
import json
import sys

print("DEBUG: Starting JSON parsing...", file=sys.stderr)

# Try to read pytest output
try:
    with open('/tmp/pytest_output.txt', 'r') as f:
        content = f.read()
    print(f"DEBUG: Read {len(content)} bytes", file=sys.stderr)
except Exception as e:
    print(f"DEBUG: ERROR reading: {e}", file=sys.stderr)
    content = ""

# Parse tests
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

print(f"DEBUG: Found {total} tests ({passed} passed, {failed} failed)", file=sys.stderr)

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

print("DEBUG: Complete", file=sys.stderr)
EOF

exit 0


