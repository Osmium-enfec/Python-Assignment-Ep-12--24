#!/bin/bash

set +e
cd /app

export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

echo "DEBUG: Starting tests..." >&2

# Run pytest and capture to file
pytest test_assignment.py -v --tb=no -p no:cacheprovider > /tmp/pytest_output.txt 2>&1

echo "DEBUG: Pytest completed, exit code: $?" >&2
echo "DEBUG: Output file exists: $(test -f /tmp/pytest_output.txt && echo 'YES' || echo 'NO')" >&2
echo "DEBUG: Output file size: $(wc -c < /tmp/pytest_output.txt 2>/dev/null || echo '0') bytes" >&2
echo "DEBUG: First 10 lines of output:" >&2
head -10 /tmp/pytest_output.txt >&2

# Simple parser to output JSON
python3 << 'EOF'
import json
import sys

print("DEBUG: Starting JSON parsing...", file=sys.stderr)

# Read the pytest output
try:
    with open('/tmp/pytest_output.txt', 'r') as f:
        content = f.read()
    print(f"DEBUG: Read {len(content)} bytes from pytest output", file=sys.stderr)
except Exception as e:
    print(f"DEBUG: ERROR reading file: {e}", file=sys.stderr)
    content = ""

# Simple parsing - just count lines with PASSED/FAILED
tests = []
passed_count = 0
failed_count = 0

for line in content.split('\n'):
    if 'PASSED' in line and 'test_assignment.py' in line:
        parts = line.split('::')
        if len(parts) >= 3:
            test_name = parts[2].split(' ')[0]
            if test_name:
                tests.append({'name': test_name, 'status': 'passed', 'passed': True})
                passed_count += 1
    elif 'FAILED' in line and 'test_assignment.py' in line:
        parts = line.split('::')
        if len(parts) >= 3:
            test_name = parts[2].split(' ')[0]
            if test_name:
                tests.append({'name': test_name, 'status': 'failed', 'passed': False})
                failed_count += 1

print(f"DEBUG: Found {passed_count} passed, {failed_count} failed", file=sys.stderr)

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

print(f"DEBUG: Building JSON with {total} tests", file=sys.stderr)

# Output JSON to stdout
json_str = json.dumps(result, indent=2)
print(json_str)
print(f"DEBUG: JSON output complete ({len(json_str)} bytes)", file=sys.stderr)
sys.stdout.flush()

# Save to file
try:
    with open('/app/results.json', 'w') as f:
        json.dump(result, f, indent=2)
    print("DEBUG: Saved to /app/results.json", file=sys.stderr)
except Exception as e:
    print(f"DEBUG: ERROR saving file: {e}", file=sys.stderr)
EOF

echo "DEBUG: Script complete" >&2
exit 0

