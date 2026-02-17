#!/bin/bash

# Episode 15 Test Runner
# Runs all tests for Episode 15 assignments

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Episode 15 - Student Management System - Test Runner       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Track results
total_tests=0
passed_tests=0
failed_tests=0

# Function to run tests for an assignment
run_assignment_tests() {
    local assignment=$1
    local assignment_path="assignment$assignment"
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}Running Assignment $assignment Tests${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if [ -f "$assignment_path/test_assignment.py" ]; then
        echo "📁 Directory: $assignment_path"
        echo "📄 Test file: test_assignment.py"
        echo ""
        
        # Run the tests
        cd "$assignment_path"
        python3 test_assignment.py 2>&1
        local result=$?
        cd ..
        
        echo ""
        if [ $result -eq 0 ]; then
            echo -e "${GREEN}✅ Assignment $assignment: ALL TESTS PASSED${NC}"
            ((passed_tests++))
        else
            echo -e "${RED}❌ Assignment $assignment: SOME TESTS FAILED${NC}"
            ((failed_tests++))
        fi
    else
        echo -e "${RED}❌ Test file not found: $assignment_path/test_assignment.py${NC}"
        ((failed_tests++))
    fi
    
    echo ""
}

# Main execution
cd "$(dirname "$0")"

echo "📍 Current directory: $(pwd)"
echo ""

# Run Assignment 1 tests
if [ -d "assignment1" ]; then
    run_assignment_tests 1
else
    echo -e "${RED}❌ Assignment 1 directory not found${NC}"
    ((failed_tests++))
fi

# Run Assignment 2 tests (if exists)
if [ -d "assignment2" ]; then
    run_assignment_tests 2
else
    echo -e "${YELLOW}⚠️  Assignment 2 not yet available${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}TEST SUMMARY${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Assignments with passing tests: $passed_tests"
echo "Assignments with failing tests: $failed_tests"
echo ""

if [ $failed_tests -eq 0 ]; then
    echo -e "${GREEN}🎉 All Assignment Tests Passed!${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}⚠️  Some assignments need attention${NC}"
    echo ""
    exit 1
fi
