# Episode 16 - Assignment 1: Django Setup and First View

## Assignment Overview

Create your first Django view and test that the development server runs properly.

## What You Need to Do

1. **Complete the `views.py` file** in the `myproject` directory
   - Create a `welcome` view that returns an HTTP response
   - Create a `about` view that displays some information

2. **Update `urls.py`** to route URLs to your views
   - Map `/` to the `welcome` view
   - Map `/about/` to the `about` view

3. **Run the development server**
   - `python manage.py runserver`
   - Test both URLs in your browser

4. **Run the tests**
   - `python test_assignment.py` to verify everything works

## Project Structure

```
assignment1/
├── manage.py              # Django management utility
├── requirements.txt       # Installed packages
├── myproject/            # Configuration package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py          # ADD YOUR URL PATTERNS HERE
│   ├── wsgi.py
│   ├── asgi.py
│   └── views.py         # ADD YOUR VIEWS HERE (starter code provided)
└── venv/                # Virtual environment
```

## Starter Code Location

**File to Edit:** `myproject/views.py`

This file has been created with TODO comments. Implement the following functions:

1. `welcome(request)` - Returns HTML showing "Welcome to Django"
2. `about(request)` - Returns HTML showing "About" information

## How to Test

### Option 1: Run Tests
```bash
cd /Users/enfec/Desktop/Python\ Assignment\ Ep\ 12-24/Python-Assignment-Ep-12--24/episode16/assignment1
source venv/bin/activate
python test_assignment.py
```

### Option 2: Manual Testing
```bash
cd /Users/enfec/Desktop/Python\ Assignment\ Ep\ 12-24/Python-Assignment-Ep-12--24/episode16/assignment1
source venv/bin/activate
python manage.py runserver
```

Then visit:
- `http://127.0.0.1:8000/` - Should see welcome page
- `http://127.0.0.1:8000/about/` - Should see about page

## Learning Outcomes

After completing this assignment, you should understand:
- How Django views work
- How URL routing connects URLs to views
- How to return HTTP responses with HTML content
- How to run the development server
- How to test Django applications

## Key Concepts

### Views
A view is a Python function that receives a web request and returns a web response. It contains the logic for processing data and rendering responses.

### URL Routing
URL patterns map URL paths to view functions. This is configured in `urls.py`.

### HTTP Response
An HttpResponse object contains the data to send to the browser (HTML, JSON, etc.).

## Expected Test Results

All 6 tests should pass:
- ✓ Views file exists
- ✓ Welcome view returns correct content
- ✓ About view returns correct content
- ✓ Welcome URL resolves correctly
- ✓ About URL resolves correctly
- ✓ Development server can start

## Tips

1. Import HttpResponse from django.http in views.py
2. Use simple HTML strings for responses: `<h1>Welcome</h1>`
3. Add views to INSTALLED_APPS if needed
4. Test each URL in browser before running tests
5. Check console output for errors

## Next Steps

After Assignment 1, you'll learn about:
- Django apps (startapp)
- Models and databases
- Templates (HTML files)
- Forms and validation
- Admin interface

---

**Duration:** 1-2 hours  
**Difficulty:** Beginner  
**Points:** 5
