#!/usr/bin/env python3
"""
Generate JSON test results from pytest output
"""
import subprocess
import json
import sys
import os
import re

def run_tests():
    """Run pytest and save output to file, then capture"""
    # Run pytest and save output to file first
    with open('/app/pytest_output.txt', 'w') as f:
        result = subprocess.run(
            ["pytest", "test_assignment.py", "-v", "--tb=line"],
            stdout=f,
            stderr=subprocess.STDOUT,
            text=True
        )
    
    # Read the saved output
    with open('/app/pytest_output.txt', 'r') as f:
        output = f.read()
    
    return output, result.returncode

def parse_pytest_output(output):
    """Parse pytest output to extract test results"""
    tests = []
    
    lines = output.split('\n')
    
    for line in lines:
        # Match lines like: test_assignment.py::TestFormHandler::test_name PASSED
        match = re.search(r'test_assignment\.py::TestFormHandler::(\w+)\s+(PASSED|FAILED)', line)
        if match:
            test_name = match.group(1)
            status = 'passed' if match.group(2) == 'PASSED' else 'failed'
            tests.append({
                "name": test_name,
                "status": status,
                "passed": status == 'passed'
            })
    
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
    try:
        # Run tests
        output, returncode = run_tests()
        
        # Parse results
        tests = parse_pytest_output(output)
        summary = calculate_summary(tests)
        
        # Build final JSON
        result = {
            "tests": tests,
            "summary": summary
        }
        
        # Save to results.json
        results_file = '/app/results.json'
        with open(results_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        # Make sure file is synced
        os.fsync(f.fileno()) if not f.closed else None
        
        # Output JSON to stdout with newline
        json_output = json.dumps(result, indent=2)
        print(json_output, flush=True)
        sys.stdout.flush()
        
        # Exit with success (0) regardless - we captured the results
        sys.exit(0)
    except Exception as e:
        # Output error as JSON
        error_result = {
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "percentage": 0,
                "marks": 0
            },
            "error": str(e)
        }
        print(json.dumps(error_result, indent=2), flush=True)
        sys.stdout.flush()
        sys.exit(0)

if __name__ == "__main__":
    main()
