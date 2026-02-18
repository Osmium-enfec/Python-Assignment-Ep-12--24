# Episode 12 Assignment 1 - JSON Results Format

## Output Structure

The runner script outputs results in a clean JSON format with individual test cases and a summary.

## Sample Output

```json
{
  "test_cases": [
    {
      "name": "TestFormHandler::test_endpoint_not_found",
      "status": "PASSED",
      "message": "Test passed successfully"
    },
    {
      "name": "TestFormHandler::test_invalid_age_not_number",
      "status": "PASSED",
      "message": "Test passed successfully"
    },
    {
      "name": "TestFormHandler::test_invalid_age_too_old",
      "status": "PASSED",
      "message": "Test passed successfully"
    },
    {
      "name": "TestFormHandler::test_invalid_age_too_young",
      "status": "PASSED",
      "message": "Test passed successfully"
    },
    {
      "name": "TestFormHandler::test_invalid_email",
      "status": "PASSED",
      "message": "Test passed successfully"
    },
    {
      "name": "TestFormHandler::test_invalid_password_short",
      "status": "PASSED",
      "message": "Test passed successfully"
    },
    {
      "name": "TestFormHandler::test_invalid_username_long",
      "status": "PASSED",
      "message": "Test passed successfully"
    },
    {
      "name": "TestFormHandler::test_invalid_username_short",
      "status": "PASSED",
      "message": "Test passed successfully"
    },
    {
      "name": "TestFormHandler::test_missing_required_fields",
      "status": "PASSED",
      "message": "Test passed successfully"
    },
    {
      "name": "TestFormHandler::test_utf8_encoding",
      "status": "PASSED",
      "message": "Test passed successfully"
    },
    {
      "name": "TestFormHandler::test_valid_registration",
      "status": "PASSED",
      "message": "Test passed successfully"
    }
  ],
  "summary": {
    "total": 11,
    "passed": 11,
    "failed": 0,
    "percentage": 100.0,
    "marks": 1.0
  }
}
```

## JSON Schema

### Test Case Object
```json
{
  "name": "TestClassName::test_method_name",
  "status": "PASSED" | "FAILED",
  "message": "Human readable message"
}
```

### Summary Object
```json
{
  "total": <integer>,           // Total number of test cases
  "passed": <integer>,          // Number of passed tests
  "failed": <integer>,          // Number of failed tests
  "percentage": <float>,        // Pass percentage (0-100)
  "marks": <float>              // Score (0-1 scale)
}
```

## Key Metrics

- **total**: Complete count of all test cases
- **passed**: Number of successfully executed tests
- **failed**: Number of failed tests
- **percentage**: Calculated as (passed/total) * 100
- **marks**: Calculated as (passed/total), ranges from 0.0 to 1.0
  - 1.0 = 100% (perfect score)
  - 0.5 = 50% (half score)
  - 0.0 = 0% (no score)

## Running the Container

```bash
# Load image
docker load -i x86.tar

# Run and capture JSON output
docker run --rm ep12-assignment1-x86:latest /app/runner.sh > results.json 2>&1

# Extract only JSON section
docker run --rm ep12-assignment1-x86:latest /app/runner.sh 2>&1 | grep -A 1000 "TEST RESULTS (JSON)" | grep -v "^=" | tail -n +2
```

## Parsing the JSON

**Python Example:**
```python
import json
import subprocess

result = subprocess.run(
    ['docker', 'run', '--rm', 'ep12-assignment1-x86:latest', '/app/runner.sh'],
    capture_output=True,
    text=True
)

# Extract JSON from output
output_lines = result.stdout.split('\n')
json_start = next(i for i, line in enumerate(output_lines) if '"test_cases"' in line) - 1
json_text = '\n'.join(output_lines[json_start:])
data = json.loads(json_text.split('==')[0].strip())

print(f"Total: {data['summary']['total']}")
print(f"Passed: {data['summary']['passed']}")
print(f"Failed: {data['summary']['failed']}")
print(f"Percentage: {data['summary']['percentage']}%")
print(f"Marks: {data['summary']['marks']}/1.0")
```

## Portal Integration

The JSON output is ideal for:
- ✅ Database storage of results
- ✅ Parsing and grading
- ✅ Student dashboards
- ✅ Progress tracking
- ✅ API responses

Simply parse the JSON and extract the summary metrics for grading!
