# Episode 12 Assignment 1 - Portal Submission Package

## ✅ Files Ready for Upload

All files have been created and tested. Ready to upload to the online portal.

### Required Files:

| File | Type | Size | Purpose |
|------|------|------|---------|
| `startercode.zip` | ZIP | 2.7KB | Starter code for students |
| `solution.zip` | ZIP | 3.0KB | Reference solution |
| `x86.tar` | TAR | 50MB | OCI Docker image (x86/amd64) |

### Supporting Files:

| File | Type | Purpose |
|------|------|---------|
| `runner_flow.json` | JSON | Runner configuration (copy to portal) |
| `docker-compose.yml` | YAML | Docker Compose setup (for reference) |
| `Dockerfile` | Docker | Image definition (for reference) |

## 📋 Portal Upload Instructions

1. **Upload Starter Code File**
   - File: `startercode.zip`
   - Contains: starter_code.py, test_assignment.py
   - Students implement TODO sections in starter_code.py

2. **Upload Solution Code File**
   - File: `solution.zip`
   - Contains: solution.py, test_assignment.py
   - Used by portal to validate student submissions

3. **Upload Container Image File**
   - File: `x86.tar`
   - Docker Image: ep12-assignment1:latest
   - Architecture: x86/amd64
   - Python: 3.14-slim

4. **Runner Flow Code**
   - Copy contents of `runner_flow.json`
   - Simple 3-step execution: Build → Test → Check Results

5. **Docker Compose Configuration**
   - Copy contents of `docker-compose.yml`
   - Version: 3.8
   - Service: assignment1
   - Port: 8000

## 🧪 Verification

All tests pass successfully:
```
11 passed in 1.15s
```

Test Coverage:
- ✅ Valid registration form submission
- ✅ Username validation (length 3-20)
- ✅ Email validation (@ symbol required)
- ✅ Password validation (minimum 8 chars)
- ✅ Age validation (13-120 range)
- ✅ UTF-8 encoding/decoding
- ✅ Missing field handling
- ✅ Invalid endpoint handling

## 🐳 Docker Image Details

**Image:** ep12-assignment1:latest
- **Base:** python:3.14-slim
- **Architecture:** linux/amd64 (x86)
- **Workdir:** /app
- **Port:** 8000
- **Dependencies:** pytest, requests

**Load image locally:**
```bash
docker load -i x86.tar
docker run --rm ep12-assignment1:latest pytest test_assignment.py -v
```

## 📝 Assignment Details

**Episode 12 - Assignment 1: Form Data Processing & HTTP Request Handling**

Topics: HTTP Content-Length, Form Data Parsing, UTF-8 Encoding, parse_qs(), Validation

Students implement:
- POST handler for /register endpoint
- Form data parsing and validation
- 4 field validations with error messages
- JSON response generation

## ✨ Simple & Clean Setup

- **Minimal Dockerfile:** 13 lines, only essential dependencies
- **Simple Docker Compose:** Single service, clear configuration
- **Simple Runner Flow:** 3 steps, straightforward execution
- **Fast Tests:** Complete in ~1.15 seconds
- **Self-contained:** No external dependencies or APIs required

---

**Ready for portal submission!** 🚀
