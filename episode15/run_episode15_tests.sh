#!/bin/bash
# Test runner for Episode 15 - Both Assignments
# Tests Assignment 1 and Assignment 2 sequentially

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║       EPISODE 15 - COMPLETE TEST SUITE                        ║"
echo "║  Assignment 1: Basic CRUD System                              ║"
echo "║  Assignment 2: Advanced Features                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

BASE_DIR=$(cd "$(dirname "$0")" && pwd)

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📋 Starting Episode 15 Test Suite...${NC}\n"

# Test Assignment 1
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}  ASSIGNMENT 1: Basic CRUD System${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

if [ -f "$BASE_DIR/assignment1/test_assignment.py" ]; then
    cd "$BASE_DIR/assignment1"
    
    echo "Running Assignment 1 tests..."
    if python3 test_assignment.py; then
        echo -e "${GREEN}✓ Assignment 1 tests PASSED${NC}\n"
        ASSIGNMENT1_PASS=true
    else
        echo -e "${RED}✗ Assignment 1 tests FAILED${NC}\n"
        ASSIGNMENT1_PASS=false
    fi
else
    echo -e "${RED}✗ Assignment 1 test file not found${NC}\n"
    ASSIGNMENT1_PASS=false
fi

# Test Assignment 2
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}  ASSIGNMENT 2: Advanced Features${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

if [ -f "$BASE_DIR/assignment2/test_assignment.py" ]; then
    cd "$BASE_DIR/assignment2"
    
    echo "Running Assignment 2 tests..."
    if python3 test_assignment.py; then
        echo -e "${GREEN}✓ Assignment 2 tests PASSED${NC}\n"
        ASSIGNMENT2_PASS=true
    else
        echo -e "${RED}✗ Assignment 2 tests FAILED${NC}\n"
        ASSIGNMENT2_PASS=false
    fi
else
    echo -e "${RED}✗ Assignment 2 test file not found${NC}\n"
    ASSIGNMENT2_PASS=false
fi

# Summary
echo ""
echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║            EPISODE 15 TEST SUMMARY                             ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════╝${NC}"

if [ "$ASSIGNMENT1_PASS" = true ] && [ "$ASSIGNMENT2_PASS" = true ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
    echo ""
    echo "Assignment 1 (CRUD): ✓"
    echo "Assignment 2 (Advanced): ✓"
    echo ""
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo ""
    if [ "$ASSIGNMENT1_PASS" = true ]; then
        echo "Assignment 1 (CRUD): ✓"
    else
        echo -e "Assignment 1 (CRUD): ${RED}✗${NC}"
    fi
    
    if [ "$ASSIGNMENT2_PASS" = true ]; then
        echo "Assignment 2 (Advanced): ✓"
    else
        echo -e "Assignment 2 (Advanced): ${RED}✗${NC}"
    fi
    echo ""
    exit 1
fi
