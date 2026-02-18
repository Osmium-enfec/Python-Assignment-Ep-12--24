# Episode 12 - Assignment 1: Form Data Processing & HTTP Request Handling

## Portal Submission Files

This assignment includes all required files for online portal submission:

### 1. **startercode.zip**
Contains the initial project structure for students to implement:
- `starter_code.py` - Skeleton with TODO markers
- `test_assignment.py` - Test suite for validation

### 2. **solution.zip**
Contains the complete solution code:
- `solution.py` - Full implementation
- All passing test cases

### 3. **x86.tar**
OCI Docker image (x86/amd64 architecture):
- Pre-built Python 3.14 environment
- All dependencies installed (pytest, requests)
- `/app/runner.sh` entrypoint
- Ready to run tests immediately

## Quick Start

### Load and Run Docker Image
```bash
# Load the tar file
docker load -i x86.tar

# Run with runner script
docker run --rm ep12-assignment1-x86:latest /app/runner.sh

# Run with docker-compose
docker-compose up --abort-on-container-exit
```

## Assignment Overview

**Topics:** Form Data Processing, HTTP Request Handling, POST Requests

**Learning Objectives:**
- HTTP Content-Length header processing
- Form data encoding/decoding with UTF-8
- Form data parsing using `parse_qs()`
- Dictionary comprehensions
- Error handling in request processing

**Requirements:**
Students must implement:
1. HTTP POST handler for `/register` endpoint
2. Content-Length header reading
3. Form data parsing and validation
4. Field validation (username, email, password, age)
5. JSON response generation

## Docker Image Details

- **Image Name:** ep12-assignment1-x86:latest
- **Base Image:** python:3.14-slim
- **Architecture:** x86 (amd64)
- **Working Directory:** /app
- **Runner Script:** /app/runner.sh
- **Exposed Port:** 8000
- **Default Command:** /app/runner.sh (runs tests)

## Docker Compose Setup

Service: `judge`
- Image: ep12-assignment1-x86:latest
- Working Directory: /app
- Submission Mount: ./src:/app/submission (read-only)
- Security: no-new-privileges, dropped all capabilities
- Resource Limits: 1 CPU, 512MB memory
- tmpfs: /tmp with 50MB size

## Runner Flow

The runner script (`/app/runner.sh`) defines:
1. Change to /app directory
2. Execute pytest with verbose output
3. Return test results

Simple and straightforward execution!

## File Structure

```
assignment1/
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Judge service configuration
├── runner_flow.sh          # Runner entrypoint script
├── starter_code.py         # Student implementation template
├── solution.py             # Reference solution
├── test_assignment.py      # Test suite
├── startercode.zip         # Starter package for portal
├── solution.zip            # Solution package for portal
├── x86.tar                 # OCI image file (50MB)
└── SUBMISSION_README.md    # This file
```

## Notes

- Image size: ~50MB
- Test execution time: < 5 seconds
- No external API calls required
- Self-contained environment
- Compatible with Docker daemon and docker-compose

