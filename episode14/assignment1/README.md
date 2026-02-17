# Episode 14 - Assignment 1: Template Systems & XSS Security

## Overview

Build a secure template rendering system using Python's `os.path` module for file handling, and implement HTML escaping to prevent Cross-Site Scripting (XSS) attacks.

**Core Concepts:**
- File path handling with `os.path`
- Template loading and rendering
- HTML entity escaping
- XSS vulnerability prevention
- Context dictionaries in rendering
- Safe type conversion

---

## Learning Objectives

By completing this assignment, you'll understand:

1. **File Path Management**
   - Using `os.path.dirname()`, `os.path.abspath()`, `os.path.join()`
   - BASE_DIR pattern for project organization
   - Absolute vs relative paths

2. **Template Systems**
   - Loading templates from files
   - Placeholder substitution ({{variable}})
   - Context dictionaries
   - Template inheritance/composition

3. **Security - XSS Prevention**
   - HTML entity encoding/escaping
   - Common XSS attack vectors
   - Safe data rendering
   - Defense-in-depth approach

4. **HTTP Integration**
   - Combining templates with HTTP responses
   - Handling form data securely
   - POST request processing with template rendering

---

## Key Concepts Explained

### 1. File Paths with os.path

```python
import os

# Get absolute path of current file
__file__ = '/path/to/solution.py'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# BASE_DIR = '/path/to'

# Build path to templates
templates_dir = os.path.join(BASE_DIR, 'templates')
# templates_dir = '/path/to/templates'

# Build path to specific template
template_path = os.path.join(templates_dir, 'user.html')
# template_path = '/path/to/templates/user.html'
```

**Why use `os.path`?**
- Works across Windows, macOS, Linux (cross-platform)
- Handles path separators automatically (/ on Unix, \ on Windows)
- Safer than string concatenation

### 2. HTML Entity Escaping

XSS attacks inject malicious JavaScript through user input. HTML escaping prevents this:

```python
# Without escaping (VULNERABLE)
message = '<script>alert("XSS")</script>'
html = f'<p>{message}</p>'
# Result: <p><script>alert("XSS")</script></p>  ❌ DANGEROUS!
# Browser executes the script!

# With escaping (SAFE)
message = '<script>alert("XSS")</script>'
escaped = html_escape(message)  # &lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;
html = f'<p>{escaped}</p>'
# Result: <p>&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;</p>  ✓ SAFE
# Browser displays the text, doesn't execute
```

**Key Escape Sequences:**
```
& → &amp;    (MUST escape first! Otherwise & in other escapes will be double-escaped)
< → &lt;     (prevents <tag> interpretation)
> → &gt;     (completes tag closing)
" → &quot;   (prevents attribute escaping)
' → &#x27;   (alternate for single quotes, not always needed)
```

**Order matters! Always escape & first:**
```python
# WRONG ORDER:
value = '&<>'
value = value.replace('<', '&lt;')     # '&<>' → '&<&gt;'
value = value.replace('&', '&amp;')    # '&<&gt;' → '&amp;&lt;&amp;gt;' ❌

# RIGHT ORDER:
value = '&<>'
value = value.replace('&', '&amp;')    # '&<>' → '&amp;<>'
value = value.replace('<', '&lt;')     # '&amp;<>' → '&amp;&lt;'
value = value.replace('>', '&gt;')     # '&amp;&lt;' → '&amp;&lt;&gt;' ✓
```

### 3. Template Rendering with Context

```python
def render_template(template_name, **context):
    # Load template file
    template_html = read_template(template_name)
    
    # For each variable in context
    for key, value in context.items():
        # Escape the value to prevent XSS
        escaped_value = html_escape(value)
        
        # Replace {{key}} with escaped value
        placeholder = f'{{{{{key}}}}}'  # {{key}}
        template_html = template_html.replace(placeholder, escaped_value)
    
    return template_html

# Usage
html = render_template('user.html', username='<script>alert("XSS")</script>')
# {{username}} in template → &lt;script&gt;...&lt;/script&gt;
```

**Context Dictionary Unpacking:**
```python
# Explicit dictionary
context = {'username': 'Alice', 'age': 30}
render_template('user.html', **context)
# Same as: render_template('user.html', username='Alice', age=30)
```

### 4. Type Conversion in Escaping

The `html_escape()` function must handle multiple types:

```python
html_escape(None)      # → ''           (None → empty string)
html_escape(True)      # → 'True'       (bool → string)
html_escape(False)     # → 'False'
html_escape(42)        # → '42'         (int → string)
html_escape(3.14)      # → '3.14'       (float → string)
html_escape('<tag>')   # → '&lt;tag&gt;'
```

---

## Assignment Tasks

### Task 1: Implement Path Handling
**File:** `solution.py` - `get_templates_dir()` function

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_templates_dir():
    """Return absolute path to templates directory"""
    # Return os.path.join(BASE_DIR, 'templates')
    pass
```

**Test:** Directory should exist and contain template files

### Task 2: Implement Template Loading
**File:** `solution.py` - `read_template()` function

```python
def read_template(template_name):
    """Load template file from templates directory
    
    Args:
        template_name: str - Name of template file (e.g., 'user.html')
    
    Returns:
        str - Template content
    
    Raises:
        FileNotFoundError - If template doesn't exist
    """
    # 1. Get templates directory
    # 2. Build full path: os.path.join(templates_dir, template_name)
    # 3. Open with encoding='utf-8'
    # 4. Read and return content
    pass
```

**Tests:** 
- Load existing templates
- Raise FileNotFoundError for missing templates

### Task 3: Implement HTML Escaping
**File:** `solution.py` - `html_escape()` function

```python
def html_escape(value):
    """Escape HTML entities to prevent XSS attacks
    
    Args:
        value: Any type - Value to escape
    
    Returns:
        str - Escaped string safe for HTML
    
    Security: CRITICAL - Escape & FIRST
    """
    # 1. Convert to string (handle None, int, bool, etc.)
    # 2. Replace & with &amp;    (MUST be first!)
    # 3. Replace < with &lt;
    # 4. Replace > with &gt;
    # 5. Replace " with &quot;
    # 6. Return escaped string
    pass
```

**Tests:**
- Each special character (& < > ")
- Script tags (<script>)
- Type conversions (None, int, bool)
- Safe strings (no change)

### Task 4: Implement Template Rendering
**File:** `solution.py` - `render_template()` function

```python
def render_template(template_name, **context):
    """Render template with context variables
    
    Args:
        template_name: str - Template filename
        **context: dict - Variables to inject into template
    
    Returns:
        str - Rendered HTML with placeholders replaced
    
    Security: All context values are automatically escaped
    """
    # 1. Load template using read_template()
    # 2. For each key, value in context.items():
    #    - Escape the value using html_escape()
    #    - Build placeholder: f'{{{{{key}}}}}'  (results in {{key}})
    #    - Replace placeholder with escaped value
    # 3. Return rendered template
    pass
```

**Tests:**
- Simple substitution
- Multiple variables
- XSS attack blocking
- Type conversion

### Task 5: Implement HTTP Server Integration
**File:** `solution.py` - `TemplateHandler` class

Implement the following endpoints:

```python
class TemplateHandler(BaseHTTPRequestHandler):
    """HTTP request handler with template rendering"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            # Render home page (layout.html with content: "Welcome to the Template Engine")
            pass
        elif self.path == '/user':
            # Render user.html with username='Guest'
            pass
        elif self.path == '/test-xss':
            # Render message.html with XSS payload: <script>alert("XSS")</script>
            # This demonstrates that XSS is prevented
            pass
        else:
            # Return 404 Not Found
            pass
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/render':
            # 1. Read Content-Length
            # 2. Read form data
            # 3. Parse message parameter
            # 4. Render message.html with context={'message': message}
            # 5. Send HTML response
            pass
        else:
            # Return 404
            pass
```

---

## Files Included

- `starter_code.py` - Template with TODO comments
- `solution.py` - Complete working implementation
- `test_assignment.py` - 24 test cases covering all functionality
- `templates/layout.html` - Base template
- `templates/message.html` - Simple message template
- `templates/user.html` - User profile template

---

## Running Tests

```bash
cd episode14/assignment1
python test_assignment.py -v
```

**Expected Output:**
```
test_base_dir_exists ... ok
test_escape_ampersand ... ok
test_escape_script_tag ... ok
test_home_page ... ok
test_post_with_xss_attack ... ok
... (24 tests total)

Ran 24 tests in X.XXXs
OK
```

---

## Key Takeaways

1. **Always escape user input** - Never trust data from forms, URLs, or APIs
2. **Order matters in escaping** - Ampersand first to avoid double-escaping
3. **Use os.path for portability** - Works across all platforms
4. **Test security issues** - Include XSS payloads in tests
5. **Centralize escaping** - Apply in one place (render_template) not scattered
6. **Defense in depth** - Escaping + Content Security Policy (CSP) headers

---

## Common Mistakes

❌ **Mistake 1:** Not escaping & first
```python
# Wrong
value = value.replace('<', '&lt;').replace('&', '&amp;')
# Results in: &amp;lt; instead of &lt;
```

✓ **Solution:** Escape & first always

---

❌ **Mistake 2:** Forgetting to handle None values
```python
# Wrong
html_escape(None)  # TypeError: 'NoneType' object has no attribute 'replace'
```

✓ **Solution:** Convert to string first: `str(value) if value is not None else ''`

---

❌ **Mistake 3:** Not using context dict unpacking
```python
# Works but verbose
render_template('file.html', username='Alice', age=30, email='alice@example.com')

# Better - use **dict unpacking
context = {'username': 'Alice', 'age': 30, 'email': 'alice@example.com'}
render_template('file.html', **context)
```

---

## Additional Resources

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Python os.path Documentation](https://docs.python.org/3/library/os.path.html)
- [HTML Entities Reference](https://html.spec.whatwg.org/multipage/named-characters.html)
- [Content Security Policy (CSP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

---

## Episode 14 Topics Covered

From the episode topics, this assignment covers:

✓ **File Paths & Organization**
- Using os.path module for cross-platform path handling
- BASE_DIR pattern for project organization
- Absolute vs relative paths
- Template directory management

✓ **Template Systems**
- Reading templates from files
- Placeholder-based substitution
- Context dictionaries
- Dictionary unpacking (**context)

✓ **HTML & Security**
- HTML entity encoding
- XSS attack prevention
- Safe rendering of user content
- Type conversion and escaping

✓ **HTTP Integration**
- GET requests returning rendered templates
- POST request handling
- Form data processing with security
- Response content-type and encoding

Ready for **Assignment 2** which will cover template composition, layout inheritance, and advanced rendering patterns!
