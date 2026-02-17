# Episode 13: Variable Scopes, Routing & Dynamic Templates

## Overview
This episode covers Python variable scopes (LEGB rule), data persistence, HTTP routing, redirects, and dynamic HTML template rendering.

---

## Assignment Structure

```
episode13/
├── README.md (This file)
├── assignment1/ (Variable Scopes & Data Persistence)
│   ├── starter_code.py
│   ├── solution.py
│   ├── stores.py (data module)
│   └── test_assignment.py
└── assignment2/ (HTTP Routing & Dynamic Templates)
    ├── starter_code.py
    ├── solution.py
    ├── page.py (template module)
    ├── stores.py
    └── test_assignment.py
```

---

## Assignment 1: Variable Scopes & Data Persistence

### Topics Covered
- Python Variable Scopes
- LEGB Rule (Local, Enclosing, Global, Built-in)
- Global Keyword Usage
- Closures and Enclosing Scope
- nonlocal Keyword
- Data Persistence with Stores Module
- *args Parameter
- Thread-Safe Logging
- ThreadingHTTPServer

### What You'll Build
A student management server with:
- Closure-based validation (enclosing scope)
- Global variable management
- File-based persistence (JSON)
- Thread-safe operations
- Custom logging with *args

### Key Concepts

**LEGB Rule:**
```python
# Local: defined in function
def function():
    x = 1  # Local scope

# Enclosing: in outer function
def outer():
    x = 1  # Enclosing scope for inner
    def inner():
        print(x)  # Can access x
    
# Global: module-level
x = 1

# Built-in: Python's built-ins
print(x)  # uses built-in print
```

**Closures with nonlocal:**
```python
def create_counter():
    count = 0  # Enclosing scope
    def increment():
        nonlocal count  # Modify enclosing variable
        count += 1
        return count
    return increment

counter = create_counter()
print(counter())  # 1
print(counter())  # 2
```

**Global Keyword:**
```python
STUDENTS = []

def add_student(student):
    global STUDENTS  # Declare we're modifying global
    STUDENTS.append(student)
```

### Running Assignment 1

```bash
cd episode13/assignment1

# Run solution
python3 solution.py

# Test with curl
curl -X POST -d "id=101&name=John&grade=85" http://localhost:8005/add-student

# Run tests
python3 test_assignment.py -v
```

---

## Assignment 2: HTTP Routing & Dynamic Templates

### Topics Covered
- URL Routing and Parameter Parsing
- HTTP Redirects (302 status code)
- Post-Redirect-Get (PRG) Pattern
- Flash Messages with Redirects
- HTML Template Rendering
- Base Template Pattern
- Dynamic Content Injection (f-strings)
- Statistics Calculation
- ThreadingHTTPServer for Concurrency

### What You'll Build
A complete student dashboard with:
- Multi-endpoint routing (/, /students, /add, /edit, /delete)
- URL parameter parsing (?id=101)
- PRG pattern (POST → Redirect → GET)
- Flash notifications
- Dynamic HTML templates
- Statistics display
- Persistent storage

### Key Concepts

**PRG Pattern (Best Practice for Forms):**
```
1. User submits form (POST /add)
   ↓
2. Server processes and saves data
   ↓
3. Server redirects (302 Found)
   ↓
4. Browser navigates to GET /students
   ↓
5. User sees confirmation

Benefits:
- Prevents form resubmission on refresh
- Shows success state
- Cleaner browser history
```

**URL Parameter Parsing:**
```python
from urllib.parse import urlparse, parse_qs

path = '/edit?id=101&action=view'
parsed = urlparse(path)
params = parse_qs(parsed.query)
student_id = params.get('id', [None])[0]
```

**Dynamic Templates with f-strings:**
```python
def render_page(name, grade):
    return f'''
    <h1>Student: {name}</h1>
    <p>Grade: {grade}</p>
    '''
```

**HTTP Redirects:**
```python
def _redirect(self, path, status=302):
    self.send_response(status)  # 302 = temporary redirect
    self.send_header('Location', path)
    self.end_headers()
```

**Statistics Calculation:**
```python
def calculate_stats(students):
    total = len(students)
    average = sum(s['grade'] for s in students) / total
    passing = len([s for s in students if s['grade'] >= 60])
    pass_rate = (passing / total) * 100
    return {'total': total, 'average': average, 'pass_rate': pass_rate}
```

### Running Assignment 2

```bash
cd episode13/assignment2

# Run solution
python3 solution.py

# Visit in browser
# http://localhost:8007/ - Dashboard
# http://localhost:8007/students - Student list
# http://localhost:8007/add - Add form

# Run tests
python3 test_assignment.py -v
```

---

## Testing Your Implementation

### Assignment 1 Tests
```bash
cd episode13/assignment1
python3 test_assignment.py -v
```

Covers:
- ✓ Closure validator with enclosing scope
- ✓ Duplicate ID detection
- ✓ Field validation (name, grade, ID)
- ✓ Data persistence to file
- ✓ Load/save operations
- ✓ HTTP server integration
- ✓ Global variable management

### Assignment 2 Tests
```bash
cd episode13/assignment2
python3 test_assignment.py -v
```

Covers:
- ✓ Page template rendering
- ✓ Statistics calculation
- ✓ Home page loads
- ✓ Student list display
- ✓ Add form rendering
- ✓ POST /add redirects (PRG pattern)
- ✓ Data persistence
- ✓ Student editing
- ✓ Student deletion
- ✓ URL parameter parsing
- ✓ 404 error handling

---

## Advanced Concepts Explained

### Variable Scoping

**Problem without proper scoping:**
```python
# WRONG: Using global when not needed
students = []

def add_student(s):
    global students  # Unnecessary
    students.append(s)

# BETTER: Only use global when modifying
def get_students():
    return students  # No global needed, just reading
```

**Closure Pattern (Advanced):**
```python
def create_validator():
    ids_used = set()  # Enclosing scope
    
    def validate(student):
        nonlocal ids_used  # Access enclosing
        if student['id'] in ids_used:
            return False
        ids_used.add(student['id'])
        return True
    
    return validate  # Returns closure
```

### PRG Pattern Benefits

**Without PRG (Bad):**
```
POST /add → Response with HTML
User refreshes → Form resubmits → Duplicate added
```

**With PRG (Good):**
```
POST /add → Response 302 redirect
User refreshes → GET /students → No duplicate
```

### Template Rendering

**Base Template Pattern:**
```python
def render_base(title, content):
    return f'''
    <!DOCTYPE html>
    <html>
    <head><title>{title}</title></head>
    <body>
        <nav>Navigation here</nav>
        <main>{content}</main>
    </body>
    </html>
    '''

def render_home(students):
    content = f'<h1>Welcome! {len(students)} students</h1>'
    return render_base('Home', content)
```

Benefits:
- DRY principle (shared HTML structure)
- Consistent styling
- Easy maintenance
- Separation of concerns

---

## How This Connects to Django

### Django Equivalents

| Episode 13 | Django |
|-----------|--------|
| Manual routing in do_GET/do_POST | URL routing in urls.py |
| Manual flash messages | Django messages framework |
| Manual template f-strings | Django template engine |
| Closures for validation | Django form validators |
| Global STUDENTS list | Django ORM models |
| ThreadingHTTPServer | Built-in runserver |
| HTTP 302 redirects | redirect() helper |
| PRG pattern | Django form best practice |

### Learning Path

1. **Episode 12:** Raw HTTP mechanics
2. **Episode 13:** Routing, state, templates
3. **Episode 14:** More patterns (API endpoints, etc.)
4. **Episode 15+:** Framework abstractions (Flask/Django)

Understanding these fundamentals makes Django much clearer!

---

## Common Issues & Solutions

### Issue: "Duplicate ID still added"
**Solution:** Make sure closure captures ID set with `nonlocal`

### Issue: Flash message not showing
**Solution:** Session cookie must persist across requests

### Issue: Statistics showing old data
**Solution:** Recalculate after each POST operation

### Issue: Redirect loop
**Solution:** Check redirect destination doesn't redirect back

### Issue: Form fields reset after error
**Solution:** Re-display form with submitted values preserved

---

## File Structure Explained

### stores.py
Centralized data operations:
- `load_students()` - Read from JSON
- `save_students()` - Write to JSON
- `delete_file()` - Clean up (testing)

Benefits: Single source of truth for data operations

### page.py
Centralized HTML rendering:
- `render_base()` - Common structure
- `render_home()` - Dashboard
- `render_add_form()` - Form pages
- `render_student_list()` - List views

Benefits: Consistent styling, DRY principle

### solution.py
Main server logic:
- Routing (do_GET, do_POST)
- Business logic
- Data persistence calls
- Template rendering calls

---

## Next Steps

After completing Episode 13:
- Practice URL parameter parsing patterns
- Understand redirect use cases
- Learn when to use closures
- Experiment with ThreadingHTTPServer
- Build more complex routing
- Move to Episode 14 for API endpoints

Enjoy the journey to understanding web frameworks!
