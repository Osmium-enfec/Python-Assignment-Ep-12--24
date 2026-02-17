# Episode 13 Summary: Variable Scopes, Routing & Dynamic Templates

## ✅ Completion Status

**All Tests Passing!**
- Assignment 1: 14/14 ✅ 
- Assignment 2: 16/16 ✅

---

## What Was Created

```
episode13/
├── README.md (Comprehensive learning guide)
├── run_episode13_tests.sh (Test runner - executable)
├── assignment1/ (Variable Scopes & Data Persistence)
│   ├── starter_code.py - Student template with TODOs
│   ├── solution.py - Complete working solution
│   ├── stores.py - Data persistence module
│   └── test_assignment.py - 14 comprehensive tests
└── assignment2/ (HTTP Routing & Dynamic Templates)
    ├── starter_code.py - Template with TODOs
    ├── solution.py - Complete working solution
    ├── page.py - HTML template rendering module
    ├── stores.py - Data persistence module
    └── test_assignment.py - 16 comprehensive tests
```

---

## Assignment 1: Variable Scopes & Data Persistence

### Core Concepts Taught
✓ **LEGB Rule** - Local, Enclosing, Global, Built-in scope hierarchy  
✓ **Global Keyword** - Modifying global variables from functions  
✓ **Closures** - Inner functions accessing outer scope variables  
✓ **nonlocal Keyword** - Modifying enclosing scope variables  
✓ ***args Parameter** - Variable number of function arguments  
✓ **Thread-Safe Operations** - Using locks for concurrent access  
✓ **Data Persistence** - Saving/loading JSON files  
✓ **ThreadingHTTPServer** - Handling multiple concurrent requests

### What Students Build
- Student management HTTP server on port 8005
- Closure-based validator with enclosing scope state tracking
- Global STUDENTS list with proper `global` keyword usage
- Thread-safe file operations with locks
- Custom logging with *args formatting
- File persistence with error handling

### Key Code Patterns

**LEGB Rule in Action:**
```python
STUDENTS = []  # Global scope

def create_validator():
    student_ids = set()  # Enclosing scope
    
    def validate_student(data):  # Local scope
        nonlocal student_ids  # Access enclosing
        if data['id'] in student_ids:  # Uses enclosing variable
            return False
        student_ids.add(data['id'])
        return True
    
    return validate_student
```

**Global Variable Management:**
```python
def do_POST(self):
    global STUDENTS  # Declare at function start
    # Now can modify STUDENTS
    STUDENTS.append(student)
```

**Thread-Safe Logging:**
```python
LOG_LOCK = Lock()

def log_message(format_string, *args):
    with LOG_LOCK:  # Thread-safe
        message = format_string % args
        print(f"[timestamp] {message}")
```

### Test Results
- ✓ Closure validator basics
- ✓ Duplicate ID detection
- ✓ Field validation (name, grade, ID)
- ✓ Data persistence to file
- ✓ Load/save operations
- ✓ HTTP server integration
- ✓ Global variable management

---

## Assignment 2: HTTP Routing & Dynamic Templates

### Core Concepts Taught
✓ **URL Routing** - Parsing paths and routing to handlers  
✓ **URL Parameters** - Parsing query strings (?id=101)  
✓ **HTTP Redirects** - 302 temporary redirects  
✓ **PRG Pattern** - Post-Redirect-Get best practice  
✓ **Flash Messages** - One-time notifications with persistence  
✓ **Template Rendering** - Dynamic HTML with f-strings  
✓ **Base Template Pattern** - DRY principle for HTML  
✓ **Statistics Calculation** - Computing dashboard metrics  
✓ **ThreadingHTTPServer** - Multi-request concurrency

### What Students Build
- Complete student dashboard on port 8007
- Multi-endpoint routing (/, /students, /add, /edit, /delete)
- PRG pattern implementation for forms
- Flash message system
- Dynamic HTML templates
- Statistics display (total, average, pass rate)
- Edit and delete functionality
- 100% persistence to JSON

### Key Code Patterns

**URL Routing:**
```python
def do_GET(self):
    parsed = urlparse(self.path)
    path = parsed.path
    
    if path == '/':
        self._handle_home()
    elif path == '/students':
        self._handle_student_list()
    elif path == '/edit':
        params = parse_qs(parsed.query)
        student_id = params.get('id', [None])[0]
        self._handle_edit_form(student_id)
```

**PRG Pattern (Best Practice):**
```python
def _handle_add_post(self):
    form_data = self._read_form()
    # Validate...
    STUDENTS.append(student)
    stores.save_students(STUDENTS)
    
    # Redirect (PRG pattern)
    self._redirect('/students', session_id)
```

**Dynamic Templates with f-strings:**
```python
def render_home(students, stats):
    return f'''
    <h1>Dashboard</h1>
    <p>Total: {stats['total_students']}</p>
    <p>Average: {stats['average_grade']:.2f}</p>
    '''
```

**Statistics Calculation:**
```python
def _calculate_statistics(self, students):
    total = len(students)
    average = sum(s['grade'] for s in students) / total if total else 0
    passing = len([s for s in students if s['grade'] >= 60])
    pass_rate = (passing / total) * 100 if total else 0
    return {
        'total_students': total,
        'average_grade': average,
        'pass_rate': pass_rate
    }
```

### Test Results
- ✓ Page template rendering
- ✓ Statistics calculations
- ✓ Home page functionality
- ✓ Student list display
- ✓ Add form rendering
- ✓ POST /add redirects (PRG pattern)
- ✓ Data persistence
- ✓ Student editing
- ✓ Student deletion
- ✓ URL parameter parsing
- ✓ 404 error handling
- ✓ Flash message persistence

---

## How to Run

### Quick Test Everything
```bash
cd episode13
chmod +x run_episode13_tests.sh
./run_episode13_tests.sh
```

### Test Individual Assignments

**Assignment 1:**
```bash
cd episode13/assignment1
python3 solution.py  # Server runs on 8005
# In another terminal:
curl -X POST -d "id=101&name=John&grade=85" http://localhost:8005/add-student
python3 test_assignment.py -v
```

**Assignment 2:**
```bash
cd episode13/assignment2
python3 solution.py  # Server runs on 8007
# Visit: http://localhost:8007 in browser
python3 test_assignment.py -v
```

---

## Key Learnings

### Variable Scoping
- **Local** variables are function-specific and temporary
- **Global** variables persist across function calls
- **Enclosing** scope enables closures for data encapsulation
- **nonlocal** keyword allows inner functions to modify enclosing variables
- LEGB rule determines variable lookup order

### Web Patterns
- **PRG Pattern** prevents form resubmission on refresh
- **Flash Messages** provide one-time user notifications
- **HTTP Redirects** guide users after form submission
- **URL Parameters** enable resource-specific operations
- **Statistics** provide dashboard insights from data

### Code Organization
- **stores.py** centralizes data operations
- **page.py** centralizes HTML rendering
- **Closure pattern** provides encapsulation without classes
- **ThreadingHTTPServer** handles concurrent requests automatically

---

## Connection to Django

### Django Equivalents

| Episode 13 | Django |
|-----------|--------|
| Manual routing in do_GET/do_POST | URL patterns in urls.py |
| Global variable management | Django models (ORM) |
| Closure validators | Form validators |
| Manual flash messages | Django messages framework |
| Manual redirects | redirect() function |
| Manual templates | Django template engine |
| ThreadingHTTPServer | runserver command |
| PRG pattern | Django form best practice |

### Learning Progression
1. **Episode 12:** Raw HTTP fundamentals (requests, responses, cookies)
2. **Episode 13:** Routing, state, templates (THIS EPISODE)
3. **Episode 14:** More patterns (API endpoints, more advanced routing)
4. **Episode 15+:** Framework abstractions (Flask/FastAPI/Django)

**Understanding these fundamentals makes Django much easier!**

---

## Files Overview

### `stores.py` (Both Assignments)
Centralized data persistence module:
- `load_students()` - Read from JSON file
- `save_students(students)` - Write to JSON file  
- `delete_file()` - Clean up for testing
- Thread-safe operations with file locks

Benefits: Single source of truth for data operations

### `page.py` (Assignment 2 Only)
Centralized HTML template rendering:
- `render_base(title, content)` - Common HTML structure
- `render_home(students, stats)` - Dashboard
- `render_student_list(students)` - Student table
- `render_add_form()` - Form for adding students
- `render_edit_form(student)` - Form for editing
- `render_error(message)` - Error pages

Benefits: 
- DRY principle (shared HTML structure)
- Consistent styling across pages
- Easy to maintain and update

### `solution.py` (Both Assignments)
Main server logic with handlers and routing:
- Request routing (do_GET, do_POST)
- Endpoint handlers
- Business logic
- Data persistence calls
- Template rendering

---

## Next Steps

After completing Episode 13:
1. Practice URL parameter parsing with complex paths
2. Experiment with nested data structures in JSON
3. Try building a more complex dashboard
4. Move to Episode 14 for API endpoints
5. Then transition to Django framework

Excellent progress! You're building real web fundamentals! 🚀

---

## Command Reference

```bash
# Run all tests
cd episode13 && ./run_episode13_tests.sh

# Run specific assignment
cd episode13/assignment1 && python3 test_assignment.py -v
cd episode13/assignment2 && python3 test_assignment.py -v

# Run server for manual testing
cd episode13/assignment1 && python3 solution.py
cd episode13/assignment2 && python3 solution.py

# Test with curl (Assignment 1)
curl -X POST -d "id=101&name=John&grade=85" http://localhost:8005/add-student

# Rebuild from starter code (if needed)
cd episode13/assignment1 && rm students.json 2>/dev/null; python3 starter_code.py
```

---

**Total Tests: 30/30 ✅**
**Episode 13: Complete! 🎉**
