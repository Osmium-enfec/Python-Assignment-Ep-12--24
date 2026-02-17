# Episode 14 - Assignment 2: Advanced Templates & Data Rendering

## Overview

Build an advanced template system with dictionary iteration, table generation, and complete CRUD (Create, Read, Update, Delete) operations for student management.

**Core Concepts:**
- Template composition and layout inheritance
- Dictionary iteration for building HTML from data
- Safe rendering of lists and collections
- Attribute vs content escaping
- Data persistence with JSON
- Complete application with multiple routes

---

## Learning Objectives

By completing this assignment, you'll understand:

1. **Template Composition**
   - Base layouts with `{{content}}` placeholders
   - Combining multiple template renders
   - Layout inheritance patterns

2. **Dictionary Iteration**
   - Looping through list of dictionaries
   - Accessing dict values safely with `.get()`
   - Building HTML from structured data

3. **HTML Table Generation**
   - Creating `<table>`, `<thead>`, `<tbody>` with dynamic data
   - Rendering table rows from dict records
   - Safe handling of mixed data types

4. **Advanced Security**
   - `escape_attribute()` vs `html_escape()`
   - Escaping values used in HTML attributes
   - XSS prevention in URLs (href parameters)
   - Safe `<a href>` generation

5. **Complete CRUD Application**
   - Create: POST to /students/add
   - Read: GET list, GET edit form
   - Update: POST to /students/update
   - Delete: POST to /students/delete
   - Redirect pattern (Post-Redirect-Get)

6. **Data Persistence**
   - JSON file storage
   - Thread-safe file operations
   - Loading/saving data structures

---

## Key Concepts Explained

### 1. Template Composition

```python
# Create inner content
message_html = render_template('message.html', message='Welcome!')

# Wrap in layout (use __raw_content to prevent double-escaping)
page_html = render_template('layout.html', __raw_content=message_html)
```

**Why use `__raw_` prefix?**
- First render: message.html → HTML with user input escaped
- Second render: Should NOT re-escape the HTML
- `__raw_content` tells render_template: "Don't escape this, it's pre-rendered HTML"

### 2. Dictionary Iteration for Tables

```python
# List of student dicts
students = [
    {'id': '1', 'name': 'Alice', 'email': 'alice@ex.com', 'grade': '85'},
    {'id': '2', 'name': 'Bob', 'email': 'bob@ex.com', 'grade': '92'},
]

# Iterate and build rows
rows = []
for student in students:
    row = student_row_html(student)  # Converts dict to <tr>...</tr>
    rows.append(row)

table = f"<table>{''.join(rows)}</table>"
```

**Key Pattern: Safe dict access**
```python
def student_row_html(student):
    # Use .get() to safely access dict values
    name = student.get('name', 'Unknown')     # Default if missing
    email = student.get('email', '')          # Empty string default
    grade = student.get('grade', '0')         # Default number
    
    # Always escape before using in HTML
    escaped_name = html_escape(name)
    return f'<td>{escaped_name}</td>'
```

### 3. Attribute Escaping

Different contexts need different escaping:

```html
<!-- Content: User data displayed as text -->
<p>{{message}}</p>  <!-- Use html_escape() -->

<!-- Attribute: User data in href, onclick, style, etc. -->
<a href="/edit?id={{student_id}}">Edit</a>  <!-- Use escape_attribute() -->
<div onclick="deleteStudent('{{id}}')">...</div>
```

**Why attribute escaping is stricter:**
```python
def html_escape(value):
    """For content - escapes &, <, >, " """
    return value.replace('&', '&amp;').replace('<', '&lt;')...

def escape_attribute(value):
    """For attributes - also escapes single quotes """
    return html_escape(value).replace("'", '&#x27;')
```

**Attack example:**
```python
# Without attribute escaping
student_id = '1" onclick="alert(\'XSS\')'
html = f'<a href="/edit?id={student_id}">Edit</a>'
# Result: <a href="/edit?id=1" onclick="alert('XSS')">Edit</a>  ❌ VULNERABLE!

# With attribute escaping
escaped_id = escape_attribute(student_id)
html = f'<a href="/edit?id={escaped_id}">Edit</a>'
# Result: <a href="/edit?id=1&quot; onclick=&quot;alert(&#x27;XSS&#x27;)">Edit</a>  ✓ SAFE
```

### 4. Type Conversion in Tables

```python
def student_row_html(student):
    grade = student.get('grade', '0')
    
    # Convert to int for comparison
    try:
        grade_int = int(grade)
    except (ValueError, TypeError):
        grade_int = 0
    
    # Determine pass/fail based on numeric value
    status = 'Pass' if grade_int >= 60 else 'Fail'
    
    return f'<tr><td>{grade_int}</td><td>{status}</td></tr>'
```

### 5. Data Persistence Pattern

```python
def get_students():
    """Load from JSON file"""
    file_path = os.path.join(BASE_DIR, 'students.json')
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    return []

def save_students(students):
    """Save to JSON file"""
    file_path = os.path.join(BASE_DIR, 'students.json')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2, ensure_ascii=False)
```

---

## Assignment Tasks

### Task 1: Implement escape_attribute()
**File:** `solution.py` - `escape_attribute()` function

```python
def escape_attribute(value):
    """
    Escape values for HTML attributes
    
    Escapes: & < > " '
    Security: Prevent attribute breaking and event handler injection
    """
    # 1. Convert to string
    # 2. Escape & first
    # 3. Escape <, >, "
    # 4. Also escape ' (single quotes in attributes)
    pass
```

**Tests:**
- Double quotes
- Single quotes
- Angle brackets
- Ampersands first

### Task 2: Implement student_row_html()
**File:** `solution.py` - `student_row_html()` function

```python
def student_row_html(student):
    """
    Build HTML table row from student dict
    
    Args:
        student: dict with id, name, email, grade, status
    
    Returns:
        str - HTML <tr>...</tr>
    
    Security:
    - Escape dict values for content
    - Escape ID for use in href attributes
    """
    # 1. Extract values from student dict using .get()
    # 2. Convert grade to int for pass/fail logic
    # 3. Determine status: Pass if grade >= 60, else Fail
    # 4. Build HTML with escaped values
    # 5. Escape student ID for href attribute
    pass
```

**Tests:**
- Pass status (grade 60+)
- Fail status (grade <60)
- XSS in name
- XSS in attributes
- Missing fields

### Task 3: Implement render_student_list()
**File:** `solution.py` - `render_student_list()` function

```python
def render_student_list(students):
    """
    Render list of students as HTML table
    
    Args:
        students: list of dicts
    
    Returns:
        str - HTML <table>...</table>
    
    Security: Safe handling of all student data
    """
    # 1. Check if list is empty → return "No students found"
    # 2. Iterate through students
    # 3. Call student_row_html() for each
    # 4. Build complete <table> with headers and rows
    pass
```

**Tests:**
- Empty list
- Single student
- Multiple students
- Table headers present
- Edit/Delete links

### Task 4: Implement Data Persistence
**File:** `solution.py` - `get_students()` and `save_students()`

```python
def get_students():
    """Load students from JSON file (thread-safe)"""
    # 1. Build file path: os.path.join(BASE_DIR, 'students.json')
    # 2. Check if exists
    # 3. Load JSON with try/except
    # 4. Return list or []
    pass

def save_students(students):
    """Save students to JSON file (thread-safe)"""
    # 1. Build file path
    # 2. Open for writing with UTF-8 encoding
    # 3. json.dump() with indent=2, ensure_ascii=False
    pass
```

**Tests:**
- Save and load
- Nonexistent file
- Valid JSON format

### Task 5: Implement StudentListHandler Routes
**File:** `solution.py` - `StudentListHandler.do_GET()` and `do_POST()`

**GET Routes:**
```
GET /             → Home page with student list
GET /add          → Form to add new student
GET /students/edit?id=1 → Edit form for student
```

**POST Routes:**
```
POST /students/add    → Save new student, redirect to /
POST /students/update → Save changes, redirect to /
POST /students/delete → Delete student, redirect to /
```

**Implementation pattern:**
```python
def do_GET(self):
    if self.path == '/':
        # Render student list
        students = get_students()
        table = render_student_list(students)
        content = f'<h2>Students</h2>{table}'
        html = render_template('layout.html', __raw_content=content)
        self._send_html(html)
    
    elif self.path == '/add':
        # Render form template
        pass
```

---

## Files Included

- `starter_code.py` - Template with TODO comments
- `solution.py` - Complete working implementation (~280 lines)
- `test_assignment.py` - 35+ test cases
- `templates/layout.html` - Base layout template
- `students.json` - Data file (created at runtime)

---

## Running Tests

```bash
cd episode14/assignment2
python3 test_assignment.py -v
```

**Expected Output:**
```
test_add_student_persists ... ok
test_delete_student ... ok
test_escape_single_quotes ... ok
test_edit_student_page ... ok
test_multiple_students_display ... ok
test_pass_fail_display ... ok
test_render_empty_list ... ok
test_render_multiple_students ... ok
test_student_row_fail_status ... ok
test_student_row_pass_status ... ok
test_student_row_xss_in_attribute ... ok
test_student_row_xss_in_name ... ok
test_update_student ... ok
... (35+ tests total)

Ran 35+ tests in X.XXXs
OK
```

---

## Running the Server

```bash
python3 solution.py
```

Then visit: `http://localhost:8011`

---

## Key Takeaways

1. **Always escape appropriately** - Different contexts need different escaping
2. **Attribute escaping is different** - Include single quote escaping
3. **Safe dict access with .get()** - Prevents KeyError on missing fields
4. **Type conversion matters** - Convert strings to numbers for logic
5. **Build HTML from data safely** - Iterate and escape each value
6. **Composition prevents double-escaping** - Use `__raw_` prefix for pre-rendered HTML
7. **Persist data safely** - Use JSON with try/except for loading

---

## Common Mistakes

❌ **Mistake 1:** Not escaping in attributes
```python
# Wrong
href = f'/edit?id={student_id}'  # If ID has quotes, breaks HTML!

# Right
href = f'/edit?id={escape_attribute(student_id)}'
```

---

❌ **Mistake 2:** Double-escaping in composition
```python
# Wrong - renders message twice
message = render_template('msg.html', message=data)
page = render_template('layout.html', content=message)
# content gets escaped again!

# Right - use __raw_content
page = render_template('layout.html', __raw_content=message)
```

---

❌ **Mistake 3:** Not handling missing dict keys
```python
# Wrong - KeyError if 'grade' missing
grade = int(student['grade'])

# Right - Use .get() with default
grade = int(student.get('grade', '0'))
```

---

❌ **Mistake 4:** Not checking empty lists
```python
# Wrong - renders empty table
rows = [student_row_html(s) for s in students]
return f'<table>{"".join(rows)}</table>'

# Right - check first
if not students:
    return '<p>No students</p>'
```

---

## Learning Path

**After completing this assignment, you understand:**
1. ✓ File path handling (Episode 14 Assign 1)
2. ✓ Template loading and rendering (Episode 14 Assign 1)
3. ✓ HTML escaping and XSS prevention (Episode 14 Assign 1)
4. ✓ Attribute escaping (Episode 14 Assign 2)
5. ✓ Dictionary iteration and safe access (Episode 14 Assign 2)
6. ✓ Building HTML from collections (Episode 14 Assign 2)
7. ✓ Data persistence (Episode 14 Assign 2)
8. ✓ Complete CRUD application (Episode 14 Assign 2)

**Next: Episode 15 - MVC Pattern & Frameworks**
- Model-View-Controller architecture
- Separation of concerns
- Introduction to web frameworks

---

## Episode 14 Topics Covered

✓ **Template Systems & Organization**
- Template composition and layout
- Placeholder-based rendering
- Template inheritance patterns

✓ **Data Rendering Security**
- Content vs attribute escaping
- HTML table generation
- XSS prevention in complex structures

✓ **Collections & Iteration**
- Dictionary iteration
- Safe data access patterns
- Building HTML from lists

✓ **Data Management**
- Persistence with JSON
- Thread-safe operations
- CRUD operations

✓ **Complete Application**
- Multi-route HTTP handler
- Form handling and validation
- Redirect pattern implementation
