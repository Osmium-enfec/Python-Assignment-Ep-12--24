#!/usr/bin/env python3
"""
Generate JSON test results from pytest output
"""
import subprocess
import json
import sys
import os

def run_tests():
    """Run pytest and capture output"""
    # Run pytest with verbose output
    result = subprocess.run(
        ["pytest", "test_assignment.py", "-v"],
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr, result.returncode

def parse_pytest_output(stdout, stderr):
    """Parse pytest output to extract test results"""
    tests = []
    
    # Combine both outputs for parsing
    full_output = stdout + "\n" + stderr
    
    # Split by lines and look for test results
    lines = full_output.split('\n')
    for line in lines:
        # Look for lines with test names and PASSED/FAILED
        if 'test_assignment.py::' in line and ('PASSED' in line or 'FAILED' in line):
            # Extract test name - format: test_assignment.py::TestFormHandler::test_name PASSED
            try:
                # Split to get the parts
                if '::' in line:
                    # Get the test name (after last ::)
                    parts = line.split('::')
                    test_info = parts[-1]  # Gets "test_name PASSED" or similar
                    
                    # Split to separate name from status
                    test_parts = test_info.split()
                    if len(test_parts) >= 2:
                        test_name = test_parts[0]
                        # Get the status from the line
                        status = 'passed' if 'PASSED' in line else 'failed'
                        
                        tests.append({
                            "name": test_name,
                            "status": status,
                            "passed": status == 'passed'
                        })
            except Exception as e:
                # Skip malformed lines
                pass
    
    return tests

def calculate_summary(tests):
    """Calculate summary statistics"""
    total = len(tests)
    passed = sum(1 for t in tests if t["passed"])
    failed = total - passed
    percentage = (passed / total * 100) if total > 0 else 0
    marks = passed / total if total > 0 else 0
    
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "percentage": round(percentage, 2),
        "marks": round(marks, 2)
    }

def main():
    # Run tests
    stdout, stderr, returncode = run_tests()
    
    # Parse results
    tests = parse_pytest_output(stdout, stderr)
    summary = calculate_summary(tests)
    
    # Build final JSON
    result = {
        "tests": tests,
        "summary": summary
    }
    
    # Save to file
    with open('/app/results.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    # Output JSON to stdout
    print(json.dumps(result, indent=2), flush=True)
    
    # Exit with appropriate code
    sys.exit(0 if summary["failed"] == 0 else 1)

if __name__ == "__main__":
    main()
