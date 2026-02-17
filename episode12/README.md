# Episode 12: HTTP Request Handling & Session Management

## Overview
This episode covers fundamental concepts of HTTP request handling, form data processing, cookies, and session management using Python's `http.server` module.

---

## Assignment Structure

```
episode12/
├── assignment1/
│   ├── starter_code.py      # Template with TODO comments
│   ├── solution.py          # Complete working solution
│   └── test_assignment.py   # Comprehensive test suite
└── assignment2/
    ├── starter_code.py      # Template with TODO comments
    ├── solution.py          # Complete working solution
    └── test_assignment.py   # Comprehensive test suite
```

---

## Assignment 1: Form Data Processing & HTTP Request Handling

### Topics Covered
- HTTP Content-Length Header
- Request Body Reading (self.rfile)
- Form Data Encoding/Decoding (UTF-8)
- Form Data Parsing with `parse_qs()`
- Dictionary Comprehensions
- Helper Functions & Code Organization
- Error Handling

### What You'll Build
A simple registration form server that:
- Accepts POST requests to `/register`
- Reads request body using Content-Length header
- Parses form data (username, email, password, age)
- Validates input according to business rules
- Returns JSON responses with success/error messages

### Running Assignment 1

#### Option 1: Run the Solution
```bash
cd episode12/assignment1
python solution.py
```

Then in another terminal, test with curl:
```bash
# Valid registration
curl -X POST -d "username=john&email=john@example.com&password=securepass123&age=25" http://localhost:8000/register

# Invalid username (too short)
curl -X POST -d "username=ab&email=john@example.com&password=securepass123&age=25" http://localhost:8000/register

# Invalid email (missing @)
curl -X POST -d "username=john&email=johnexample.com&password=securepass123&age=25" http://localhost:8000/register

# Invalid password (too short)
curl -X POST -d "username=john&email=john@example.com&password=short&age=25" http://localhost:8000/register
```

#### Option 2: Complete the Starter Code
1. Open `starter_code.py`
2. Complete the TODO sections:
   - `do_POST()` - Handle POST requests
   - `_read_form()` - Read and parse form data
   - `_validate_form()` - Validate form fields
   - `_send_response()` - Send JSON response

#### Option 3: Run Tests
```bash
cd episode12/assignment1
python test_assignment.py
```

### Key Concepts to Learn

**Content-Length Header**
```python
content_length = int(self.headers.get('Content-Length', 0))
```

**Reading Request Body**
```python
body = self.rfile.read(content_length)
```

**Decoding Bytes to String**
```python
body_string = body.decode('utf-8')
```

**Parsing Form Data**
```python
from urllib.parse import parse_qs
parsed = parse_qs(body_string)  # Returns {key: [list_of_values]}
```

**Flattening with Dictionary Comprehension**
```python
form_data = {k: v[0] for k, v in parsed.items()}
```

---

## Assignment 2: Cookie Management & Session System

### Topics Covered
- Cookie Fundamentals
- Cookie Management with `http.cookies.SimpleCookie`
- Cookie Expiration and Clearing
- Flash Messaging System
- Session Management
- URL Parsing and Routing
- State Management Across Requests

### What You'll Build
A complete authentication system with:
- Login page with form
- Session-based authentication
- Protected endpoints (profile)
- Flash messages for notifications
- Proper session cleanup on logout

### Running Assignment 2

#### Option 1: Run the Solution
```bash
cd episode12/assignment2
python solution.py
```

Then visit in your browser:
- Login: http://localhost:8002/
- Profile: http://localhost:8002/profile (requires login)
- Logout: http://localhost:8002/logout

**Default Credentials:**
- Username: `admin`
- Password: `password123`

#### Option 2: Complete the Starter Code
1. Open `starter_code.py`
2. Complete the TODO sections:
   - `do_GET()` - Route GET requests
   - `do_POST()` - Route POST requests
   - `_parse_path()` - Extract path from URL
   - `_get_session_from_cookie()` - Read session cookie
   - `_create_session()` - Create new session
   - `_set_session_cookie()` - Set session cookie
   - `_clear_session_cookie()` - Clear session on logout
   - `_set_flash_message()` - Store flash messages
   - `_get_and_clear_flash_message()` - Retrieve and delete flash messages

#### Option 3: Run Tests
```bash
cd episode12/assignment2
python test_assignment.py
```

### Key Concepts to Learn

**Reading Cookies**
```python
from http.cookies import SimpleCookie
cookies = SimpleCookie()
cookies.load(self.headers.get('Cookie', ''))
session_id = cookies.get('session_id').value
```

**Setting Cookies**
```python
cookie = SimpleCookie()
cookie['session_id'] = session_id
cookie['session_id']['path'] = '/'
cookie['session_id']['max-age'] = 3600  # 1 hour
cookie['session_id']['httponly'] = True
self.send_header('Set-Cookie', cookie['session_id'].OutputString())
```

**Clearing Cookies**
```python
cookie = SimpleCookie()
cookie['session_id'] = ''
cookie['session_id']['max-age'] = 0
```

**Session Storage**
```python
SESSIONS = {
    'session-id-uuid': {
        'username': 'john',
        'created_at': '2026-02-17T10:30:00'
    }
}
```

**URL Parsing**
```python
from urllib.parse import urlparse
parsed = urlparse(self.path)
path = parsed.path  # '/profile'
```

---

## Testing Your Implementation

### Running Tests for Assignment 1
```bash
cd episode12/assignment1
python test_assignment.py
```

Test cases include:
- Valid registration
- Username validation (too short, too long)
- Email validation (missing @)
- Password validation (too short)
- Age validation (not number, too young, too old)
- Missing required fields
- Invalid endpoints
- UTF-8 encoding

### Running Tests for Assignment 2
```bash
cd episode12/assignment2
python test_assignment.py
```

Test cases include:
- Login page loads
- Profile access without session (redirect)
- Successful login
- Failed login
- Session persistence
- Profile shows user info
- Logout clears session
- Invalid endpoints
- Cookie security attributes

---

## Common Issues & Solutions

### Issue: "Address already in use" error
**Solution:** Change the port in the code (8000 → 8001) or kill the previous process:
```bash
lsof -ti:8000 | xargs kill -9
```

### Issue: Tests fail with "Connection refused"
**Solution:** Make sure the server starts in the background. The test suite starts its own server on a different port.

### Issue: Form data not being parsed
**Solution:** Ensure the Content-Type header is set to `application/x-www-form-urlencoded` when making requests.

### Issue: Cookies not persisting
**Solution:** Make sure to use a session object that preserves cookies across requests:
```python
session = requests.Session()
```

---

## How to Run in Sequence

### For Complete Learning:
1. **Start with Assignment 1 (starter_code.py)**
   - Write the code yourself
   - Test with curl commands
   - Run the test suite

2. **Review Assignment 1 (solution.py)**
   - See the complete implementation
   - Understand the patterns

3. **Move to Assignment 2 (starter_code.py)**
   - Apply knowledge from Assignment 1
   - Implement session management

4. **Review Assignment 2 (solution.py)**
   - See cookie/session patterns
   - Understand state management

---

## Testing APIs with Django Later

When you move to Django (Episodes 15+), you'll appreciate the patterns learned here:

### Django View Equivalents
```python
# Episode 12 (HTTP Server)
class FormHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        form_data = self._read_form()
        # validate and respond

# Django Equivalent (Later Episodes)
@login_required
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # save and redirect
```

The HTTP concepts from Assignment 1 & 2 are the foundation for:
- Django request/response cycle
- Cookie-based session middleware
- CSRF protection
- Form validation
- Authentication decorators

---

## Quick Reference: HTTP Concepts

| Concept | Assignment | Key Code |
|---------|-----------|----------|
| Content-Length | 1 | `int(self.headers.get('Content-Length', 0))` |
| Read Request Body | 1 | `self.rfile.read(content_length)` |
| Decode Bytes | 1 | `body.decode('utf-8')` |
| Parse Form Data | 1 | `parse_qs(body_string)` |
| Dict Comprehension | 1 | `{k: v[0] for k, v in dict.items()}` |
| Read Cookie | 2 | `SimpleCookie().load(headers.get('Cookie'))` |
| Set Cookie | 2 | `SimpleCookie()['name'] = value` |
| Clear Cookie | 2 | `cookie['name']['max-age'] = 0` |
| Session Storage | 2 | `SESSIONS[session_id] = user_data` |
| Route URLs | 2 | `if path == '/endpoint'` |

---

## Next Steps

After completing Episode 12:
- Move to Episode 13 for more advanced HTTP concepts
- Continue building before transitioning to Django framework
- Practice with curl and browser testing
- Understand the raw HTTP before abstractions

Enjoy learning!
