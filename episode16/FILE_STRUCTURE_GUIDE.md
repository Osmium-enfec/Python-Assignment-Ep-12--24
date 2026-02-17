# Episode 16 - Django Basics: File Structure Explanation

## Correct File Organization

### ✅ Assignment 1 Structure

```
assignment1/
├── myproject/
│   ├── views.py              ← STARTER CODE (with TODOs and pass statements)
│   ├── views_solution.py     ← SOLUTION (complete working implementation)
│   └── urls.py               ← TO BE UPDATED by students
```

**views.py** (What students see - Starter Code):
```python
from django.http import HttpResponse

# TODO 1: Create a 'welcome' view
def welcome(request):
    """Display welcome page at root URL '/'"""
    # WRITE YOUR CODE HERE
    pass

# TODO 2: Create an 'about' view
def about(request):
    """Display about page at '/about/' URL"""
    # WRITE YOUR CODE HERE
    pass
```

**views_solution.py** (Reference Solution):
```python
from django.http import HttpResponse

def welcome(request):
    """Display welcome page at root URL '/'"""
    html_content = """
    <html>
        <head>
            <title>Welcome to Django</title>
            ...complete implementation...
        </head>
    </html>
    """
    return HttpResponse(html_content)

def about(request):
    """Display about page at '/about/' URL"""
    html_content = """..."""
    return HttpResponse(html_content)
```

---

### ✅ Assignment 2 Structure

```
assignment2/
├── myproject/
│   ├── views.py              ← STARTER CODE (with 5 TODOs and pass statements)
│   ├── views_solution.py     ← SOLUTION (complete working implementation)
│   └── urls.py               ← TO BE UPDATED by students
```

**views.py** (What students see - Starter Code):
```python
from django.http import HttpResponse, JsonResponse

# TODO 1: Create a 'home' view
def home(request):
    """Display home page at root URL '/'"""
    # WRITE YOUR CODE HERE
    pass

# TODO 2: Create a 'blog_list' view
def blog_list(request):
    """Display list of blog posts at '/blog/'"""
    # WRITE YOUR CODE HERE
    pass

# TODO 3: Create a 'blog_detail' view
def blog_detail(request, post_id):
    """Display details of a blog post at '/blog/<post_id>/'"""
    # WRITE YOUR CODE HERE
    pass

# TODO 4: Create a 'contact' view
def contact(request):
    """Display contact form at '/contact/'"""
    # WRITE YOUR CODE HERE
    pass

# TODO 5: Create an 'api_response' view
def api_response(request):
    """Return JSON response at '/api/data/'"""
    # WRITE YOUR CODE HERE
    pass
```

**views_solution.py** (Reference Solution - Complete Implementation):
- Contains all 5 views fully implemented
- Returns proper HTML and JSON responses
- Can be used for reference when stuck

---

## Student Workflow

1. **Edit `views.py`** - Replace `pass` statements with actual implementations
2. **Reference `views_solution.py`** - Look at working examples when stuck
3. **Update `urls.py`** - Add URL patterns to route to the views
4. **Run tests** - `python test_assignment.py` to verify
5. **Manual test** - `python manage.py runserver` to test in browser

---

## How to Use Reference Solution

If a student gets stuck on implementing a view:

```bash
# View the solution
cat myproject/views_solution.py

# Copy specific pattern and adapt it
# Example: Copy welcome() implementation from solution
# Paste into views.py and modify as needed
```

---

## Testing Progression

### Initial State (With Starter Code Only)
- Tests: 13/13 for Assignment 1, 21/21 for Assignment 2
- But many will FAIL because views return `None` instead of HttpResponse
- This is expected - students need to implement them

### After Student Implementation
- Tests should all PASS (13/13 and 21/21)
- Views properly return responses
- URL routing configured

---

## Files Reference

### Assignment 1

| File | Purpose | For | Contains |
|------|---------|-----|----------|
| `views.py` | Learning File | Students | TODOs, hints, pass statements |
| `views_solution.py` | Reference | Teachers/Students | Complete working code |
| `urls.py` | Configuration | Students | URL patterns to add |
| `test_assignment.py` | Verification | Everyone | Test cases |

### Assignment 2

| File | Purpose | For | Contains |
|------|---------|-----|----------|
| `views.py` | Learning File | Students | 5 TODOs, hints, pass statements |
| `views_solution.py` | Reference | Teachers/Students | 5 complete views |
| `urls.py` | Configuration | Students | URL patterns with parameters |
| `test_assignment.py` | Verification | Everyone | 21 test cases |

---

## Learning Experience

**With Proper Structure:**
1. Student sees `views.py` with TODOs ✓
2. Student writes code to implement functions ✓
3. Student can peek at `views_solution.py` if needed ✓
4. Student runs tests to verify implementation ✓
5. Student learns Django best practices ✓

**This is the correct way!**

---

## Summary

✅ **views.py** = Starter code for learning (with TODOs)
✅ **views_solution.py** = Reference solution (complete)
✅ **urls.py** = Configuration file (students update)
✅ **test_assignment.py** = Test suite (verify progress)

Now the assignments are properly structured for learning! 🎓

---

**Created:** February 17, 2026
**Status:** ✅ Correct file structure established
