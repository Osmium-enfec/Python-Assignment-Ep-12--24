# Episode 16 - Django Basics: Test Results

## Test Summary

### ✅ Assignment 1: Simple Views and Routing

**Current Status:** Tests Created ✓ | Views Incomplete (Needs Implementation)

```
Tests run: 13
Passes: 5 (Views defined and callable)
Failures: 6
Errors: 2
Success Rate: 38% (5/13)
```

**Passing Tests:**
- ✓ welcome_view_exists
- ✓ about_view_exists  
- ✓ welcome_is_callable
- ✓ about_is_callable
- ✓ welcome_page_has_html (counts as pass due to test framework)

**What's Working:**
- Views are defined (starter code file exists)
- Views are callable as Python functions

**What Needs Fixing:**
- Views return `None` instead of `HttpResponse` objects
- URL patterns not configured in `urls.py`
- Need to implement view logic with HTML content
- Need to add URL routes to `urls.py`

**What to Do:**
1. Edit `/episode16/assignment1/myproject/views.py`
2. Implement `welcome()` to return HTML response
3. Implement `about()` to return HTML response
4. Edit `/episode16/assignment1/myproject/urls.py`
5. Add URL patterns for both views
6. Run tests again: `python test_assignment.py`

**Reference Solution Available:**
- File: `/episode16/assignment1/myproject/views_solution.py`

---

### ✅ Assignment 2: Multiple Views with URL Parameters

**Current Status:** Tests Created ✓ | Views Incomplete (Needs Implementation)

```
Tests run: 21
Passes: 5 (Views defined)
Failures: 16
Success Rate: 24% (5/21)
```

**Passing Tests:**
- ✓ home_view_exists
- ✓ blog_list_view_exists
- ✓ blog_detail_view_exists
- ✓ contact_view_exists
- ✓ api_response_view_exists

**What's Working:**
- All 5 views are defined (starter code file exists)
- Views structure is in place

**What Needs Fixing:**
- Views return `None` instead of `HttpResponse`/`JsonResponse`
- URL patterns not configured in `urls.py`
- URL parameters not handled (`<int:post_id>`)
- Need to implement view logic with HTML and JSON content
- Need to configure all URL routes

**What to Do:**
1. Edit `/episode16/assignment2/myproject/views.py`
2. Implement `home()` - landing page with navigation
3. Implement `blog_list()` - list of blog posts
4. Implement `blog_detail(post_id)` - specific post details
5. Implement `contact()` - contact form
6. Implement `api_response()` - JSON response
7. Edit `/episode16/assignment2/myproject/urls.py`
8. Add all URL patterns including parameterized routes
9. Run tests again: `python test_assignment.py`

**Reference Solution Available:**
- File: `/episode16/assignment2/myproject/views_solution.py`

---

## Key Issues to Fix

### Issue 1: ALLOWED_HOSTS Configuration
Some tests mention: `Invalid HTTP_HOST header: 'testserver'`

**Solution:** Add 'testserver' to ALLOWED_HOSTS in settings.py
```python
ALLOWED_HOSTS = ['*']  # For development/testing
```

### Issue 2: Views Returning None
Views currently have only `pass` statement, so they return `None`

**Solution:** Implement views to return `HttpResponse` or `JsonResponse`
```python
from django.http import HttpResponse, JsonResponse

def welcome(request):
    html = "<h1>Welcome</h1>"
    return HttpResponse(html)
```

### Issue 3: URLs Not Configured
URL resolution tests fail because `urls.py` doesn't have route patterns

**Solution:** Update `urls.py` with view imports and patterns
```python
from myproject.views import welcome, about
from django.urls import path

urlpatterns = [
    path('', welcome),
    path('about/', about),
    path('admin/', admin.site.urls),
]
```

---

## Next Steps

### For Assignment 1:
1. Look at `views_solution.py` for reference
2. Implement welcome() view
3. Implement about() view
4. Update urls.py with routes
5. Run `python test_assignment.py` - Target: 13/13 passing

### For Assignment 2:
1. Look at `views_solution.py` for reference
2. Implement all 5 views
3. Update urls.py with all routes
4. Test with `python test_assignment.py` - Target: 21/21 passing

### Manual Testing (After implementation):
```bash
# Start development server
python manage.py runserver

# Visit in browser:
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/about/
# http://127.0.0.1:8000/blog/
# http://127.0.0.1:8000/blog/1/
# http://127.0.0.1:8000/contact/
# http://127.0.0.1:8000/api/data/
```

---

## File Locations

```
episode16/
├── assignment1/
│   ├── myproject/
│   │   ├── views.py ← EDIT THIS (starter code)
│   │   ├── views_solution.py (reference)
│   │   ├── urls.py ← EDIT THIS
│   │   ├── settings.py
│   │   └── ...
│   ├── test_assignment.py (run this to test)
│   ├── manage.py
│   └── venv/
│
└── assignment2/
    ├── myproject/
    │   ├── views.py ← EDIT THIS (starter code)
    │   ├── views_solution.py (reference)
    │   ├── urls.py ← EDIT THIS
    │   ├── settings.py
    │   └── ...
    ├── test_assignment.py (run this to test)
    ├── manage.py
    └── venv/
```

---

## Learning Resources

**Key Concepts to Understand:**

1. **Views:** Functions that handle requests and return responses
2. **URL Routing:** Mapping URL paths to view functions
3. **HttpResponse:** Sending HTML content to browser
4. **JsonResponse:** Sending JSON data
5. **URL Parameters:** Capturing variables from URLs (`<int:post_id>`)
6. **Template Rendering:** Returning HTML strings with content

**Django Documentation:**
- Views: https://docs.djangoproject.com/en/5.0/topics/http/views/
- URL Dispatcher: https://docs.djangoproject.com/en/5.0/topics/http/urls/
- HTTP Response: https://docs.djangoproject.com/en/5.0/ref/request-response/

---

**Created:** February 17, 2026
