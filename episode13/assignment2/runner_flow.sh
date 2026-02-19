#!/bin/bash

set +e
cd /app

export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Create default results immediately
cat > /tmp/results.json << 'EOF'
{"tests": [], "summary": {"total": 0, "passed": 0, "failed": 0, "percentage": 0, "marks": 0}}
EOF

# Run tests with aggressive timeout
timeout 8 /usr/local/bin/python3 -m pytest test_assignment.py -v --tb=no -p no:cacheprovider > /tmp/pytest.txt 2>&1 || true

# Parse and output results
python3 << 'PYEOF'
import json

tests = []
try:
    with open('/tmp/pytest.txt', 'r') as f:
        for line in f:
            if ' PASSED ' in line and '::' in line:
                parts = line.split('::')
                if len(parts) >= 3:
                    name = parts[2].split(' ')[0]
                    if name:
                        tests.append({'name': name, 'status': 'passed', 'passed': True})
            elif ' FAILED ' in line and '::' in line:
                parts = line.split('::')
                if len(parts) >= 3:
                    name = parts[2].split(' ')[0]
                    if name:
                        tests.append({'name': name, 'status': 'failed', 'passed': False})
except:
    pass

total = len(tests)
passed = sum(1 for t in tests if t['passed'])

result = {
    'tests': tests,
    'summary': {
        'total': total,
        'passed': passed,
        'failed': total - passed,
        'percentage': round(100 * passed / total) if total > 0 else 0,
        'marks': round(passed / total, 2) if total > 0 else 0
    }
}

print(json.dumps(result))
with open('/app/results.json', 'w') as f:
    json.dump(result, f)
PYEOF

exit 0



