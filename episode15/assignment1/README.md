# Episode 15 - Student Management System (CRUD Application)
## The Capstone Project

This is the final integration project that brings together everything from Episodes 12-14!

### Overview

You'll build a **complete student management application** with full CRUD (Create, Read, Update, Delete) operations. This application demonstrates all the concepts learned in the previous episodes:

- **Episode 12**: HTTP form parsing, validation, sessions
- **Episode 13**: Closures, routing, redirects, templates
- **Episode 14**: HTML escaping, security, complex templates

### Learning Outcomes

By completing this assignment, you will:
1. ✅ Build a complete web application from scratch
2. ✅ Implement all CRUD operations on data
3. ✅ Parse and validate user input
4. ✅ Persist data to JSON files
5. ✅ Render dynamic HTML pages
6. ✅ Prevent security vulnerabilities (XSS)
7. ✅ Handle concurrent requests with threading
8. ✅ Manage error cases gracefully

### Architecture

```
Student Management System
├── HTTP Server (ThreadingHTTPServer)
│   ├── StudentHandler class
│   ├── do_GET() - Handle page requests
│   └── do_POST() - Handle form submissions
├── Data Layer (stores.py)
│   ├── load_students() - Load from JSON
│   ├── save_students() - Save to JSON
│   └── Thread-safe file operations
├── Presentation Layer (page.py)
│   ├── HTML rendering functions
│   ├── html_escape() - Security
│   └── Template generation
└── Global State
    └── STUDENTS dict (in-memory cache)
```

### Assignment 1: Basic CRUD with Forms

**Build a student management system with the following features:**

#### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | Display list of all students |
| GET | `/add` | Show form to add new student |
| POST | `/add` | Process form and add student |
| GET | `/view/{roll_no}` | Display student details |
| GET | `/edit/{roll_no}` | Show form to edit student |
| POST | `/edit/{roll_no}` | Process form and update student |
| GET | `/delete/{roll_no}` | Show delete confirmation |
| POST | `/delete/{roll_no}` | Delete student if confirmed |

#### Student Data Structure

```python
{
    '101': {
        'name': 'John Doe',
        'grade': 'A',
        'attendance': 95,
        'fees_paid': True,
        'added_on': '2024-01-01 10:00:00'
    }
}
```

#### Key Requirements

1. **Form Validation**
   - Required fields: `roll_no`, `name`, `grade`, `attendance`
   - Attendance must be 0-100
   - Roll number must be unique
   - Show validation errors on form

2. **Data Persistence**
   - Load students from `students_ep15.json` on startup
   - Save after every modification
   - Thread-safe file operations

3. **Security**
   - Escape HTML in all user input (prevent XSS)
   - Escape order: `&` → `<` → `>` → `"`

4. **User Experience**
   - Display all students in table on home page
   - Show detailed student info on view page
   - Confirm deletion before removing student
   - Show success messages

5. **Error Handling**
   - 404 for non-existent students
   - Validation errors on form pages
   - Graceful handling of file I/O errors

### Implementation Guide

#### Step 1: Implement `html_escape()` Function

```python
def html_escape(value):
    # Escape special characters in correct order
    # & must be escaped first!
    # Test: '<script>alert("XSS")</script>' → '&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;'
```

#### Step 2: Implement `parse_form_data()` Function

```python
def parse_form_data(content):
    # Parse URL-encoded form data
    # content is bytes from rfile.read()
    # Return dict of form fields
    # Handle multiple values with same key
```

#### Step 3: Implement `validate_student_data()` Function

```python
def validate_student_data(form_data, roll_no=None):
    # Check all required fields present
    # Validate attendance is integer 0-100
    # Check for duplicate roll numbers (except on edit)
    # Return list of error strings (empty if valid)
```

#### Step 4: Implement `StudentHandler.do_GET()`

```python
def do_GET(self):
    # Parse path to identify endpoint
    # Route to appropriate template renderer from page.py
    # Examples:
    #   / → page.render_home(STUDENTS)
    #   /add → page.render_add_form()
    #   /view/101 → page.render_view_student('101', STUDENTS['101'])
    # Send 200 for valid pages, 404 for invalid
```

#### Step 5: Implement `StudentHandler.do_POST()`

```python
def do_POST(self):
    # Read Content-Length and body
    # Parse form data
    # Validate (call validate_student_data)
    # If errors: show form with errors
    # If valid: modify STUDENTS dict, save, redirect
    # Endpoint examples:
    #   /add → Add new student to STUDENTS
    #   /edit/101 → Update existing student
    #   /delete/101 → Delete if confirmed
```

#### Step 6: Implement `start_server()`

```python
def start_server(port=5000):
    global STUDENTS
    # Load existing students from stores.load_students()
    # Create ThreadingHTTPServer on ('127.0.0.1', port)
    # Setup signal handler for graceful shutdown
    # Call server.serve_forever()
```

### Testing

Run the test suite:

```bash
python -m pytest test_assignment.py -v
# or
python test_assignment.py
```

The test suite includes:
- ✅ Adding students with validation
- ✅ Listing students
- ✅ Viewing student details
- ✅ Editing student information
- ✅ Deleting students
- ✅ XSS prevention (HTML escaping)
- ✅ Data persistence
- ✅ Error handling
- ✅ Form validation

### Common Implementation Patterns

#### Redirecting After POST (PRG Pattern)

```python
# After successfully modifying data:
self.send_response(302)
self.send_header('Location', '/')
self.end_headers()
```

#### Rendering Template with Response

```python
self.send_response(200)
self.send_header('Content-type', 'text/html; charset=utf-8')
self.end_headers()
self.wfile.write(page.render_home(STUDENTS).encode('utf-8'))
```

#### Handling Form Data

```python
content_length = int(self.headers.get('Content-Length', 0))
body = self.rfile.read(content_length)
form_data = parse_form_data(body)
```

#### Checking for Endpoint

```python
if self.path == '/add':
    # Handle /add
elif self.path.startswith('/view/'):
    roll_no = self.path.replace('/view/', '')
    # Handle view with roll_no
```

### Security Considerations

1. **HTML Escaping**: All user input must be escaped before rendering in HTML
2. **Validation**: Check all inputs server-side (never trust client)
3. **Session/CSRF**: Not required for this basic version
4. **SQL Injection**: Using JSON, not applicable here

### Debugging Tips

1. **Check the browser console** for client-side errors
2. **Print statements** in do_GET/do_POST to trace flow
3. **Inspect Network tab** to see request/response details
4. **Test with curl**: `curl -X POST -d "roll_no=101&name=John" http://127.0.0.1:5000/add`
5. **Check students_ep15.json** to verify data persistence

### Example Usage

```bash
# Terminal 1: Start the server
python solution.py

# Terminal 2: Test with curl
curl http://127.0.0.1:5000/  # Get home page
curl -X POST -d "roll_no=101&name=John&grade=A&attendance=95" \
  http://127.0.0.1:5000/add  # Add student
curl http://127.0.0.1:5000/view/101  # View student
curl http://127.0.0.1:5000/  # See updated list
```

### File Structure

```
episode15/
├── assignment1/
│   ├── starter_code.py        # Start here - implement the TODOs
│   ├── solution.py            # Complete reference implementation
│   ├── stores.py              # Data persistence layer
│   ├── page.py                # HTML rendering templates
│   ├── test_assignment.py     # Comprehensive test suite
│   └── README.md              # This file
└── assignment2/
    └── [Advanced CRUD features - coming next]
```

### What You'll Learn

✨ **Building Complete Web Applications**
- Full CRUD operations
- Multi-page application
- HTML form handling

🔒 **Security & Validation**
- Input validation
- XSS prevention with escaping
- Error handling

⚡ **Concurrency**
- ThreadingHTTPServer
- Thread-safe file operations

💾 **Data Persistence**
- JSON serialization
- File I/O
- In-memory caching

🎨 **User Interface**
- Dynamic HTML generation
- Form rendering
- Navigation

### Next Steps (Assignment 2)

Advanced features you might add:
- 🔍 Search and filter students
- 📊 Sort by different columns
- 📄 Pagination for large lists
- ⭐ Favorite/bookmark students
- 📈 Statistics dashboard
- 🔐 User authentication
- 🗂️ Data export (CSV)

---

**Remember**: This is the capstone project! You're building a real, working web application that integrates everything from the entire series. Great job getting here! 🎉
