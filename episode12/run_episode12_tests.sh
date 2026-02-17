#!/bin/bash
# Episode 12 Quick Test Runner

echo "╔════════════════════════════════════════════╗"
echo "║  Episode 12 Assignment Test Runner         ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to run tests
run_tests() {
    local assignment=$1
    local dir="$SCRIPT_DIR/$assignment"
    
    if [ ! -d "$dir" ]; then
        echo -e "${RED}✗ Directory not found: $dir${NC}"
        return 1
    fi
    
    echo -e "${BLUE}Testing $assignment...${NC}"
    echo "Running: python3 $dir/test_assignment.py"
    echo ""
    
    cd "$dir" || return 1
    python3 test_assignment.py
    local result=$?
    
    if [ $result -eq 0 ]; then
        echo -e "${GREEN}✓ $assignment tests passed!${NC}"
    else
        echo -e "${RED}✗ $assignment tests failed!${NC}"
    fi
    echo ""
    return $result
}

# Run Assignment 1 tests
run_tests "assignment1"
assign1_result=$?

# Run Assignment 2 tests
run_tests "assignment2"
assign2_result=$?

# Summary
echo "╔════════════════════════════════════════════╗"
echo "║  Test Summary                              ║"
echo "╚════════════════════════════════════════════╝"

if [ $assign1_result -eq 0 ]; then
    echo -e "${GREEN}✓ Assignment 1: PASSED (11/11 tests)${NC}"
else
    echo -e "${RED}✗ Assignment 1: FAILED${NC}"
fi

if [ $assign2_result -eq 0 ]; then
    echo -e "${GREEN}✓ Assignment 2: PASSED (10/10 tests)${NC}"
else
    echo -e "${RED}✗ Assignment 2: FAILED${NC}"
fi

if [ $assign1_result -eq 0 ] && [ $assign2_result -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed! 🎉${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed. Check output above.${NC}"
    exit 1
fi
