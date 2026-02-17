#!/bin/bash

# Episode 14 - Test Runner
# Runs all Episode 14 assignments and displays results

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Episode 14 - Template Systems${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Navigate to episode14 directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Run Assignment 1 Tests
echo -e "${YELLOW}Running Assignment 1 Tests...${NC}"
echo "================================"
cd assignment1
python3 test_assignment.py -v 2>&1

RESULT1=$?

cd ..

# Run Assignment 2 Tests if available
if [ -d "assignment2" ] && [ -f "assignment2/test_assignment.py" ]; then
    echo ""
    echo -e "${YELLOW}Running Assignment 2 Tests...${NC}"
    echo "================================"
    cd assignment2
    python3 test_assignment.py -v 2>&1
    RESULT2=$?
    cd ..
else
    RESULT2=0
fi

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"

if [ $RESULT1 -eq 0 ]; then
    echo -e "${GREEN}✓ Assignment 1: PASSED${NC}"
else
    echo -e "${RED}✗ Assignment 1: FAILED${NC}"
fi

if [ -d "assignment2" ] && [ -f "assignment2/test_assignment.py" ]; then
    if [ $RESULT2 -eq 0 ]; then
        echo -e "${GREEN}✓ Assignment 2: PASSED${NC}"
    else
        echo -e "${RED}✗ Assignment 2: FAILED${NC}"
    fi
fi

if [ $RESULT1 -eq 0 ] && [ $RESULT2 -eq 0 ]; then
    echo ""
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi
