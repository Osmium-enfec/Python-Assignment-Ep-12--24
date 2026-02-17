# Episode 16 - Assignment 2: Multiple Views and Advanced Routing

## Assignment Overview

Build on Assignment 1 by creating multiple views with different functionality, implementing URL routing with parameters, and understanding view organization.

## What You Need to Do

1. **Complete the `views.py` file** with multiple views
   - `home` - Main landing page
   - `blog_list` - List all blog posts
   - `blog_detail` - Show details of a specific post (with URL parameter)
   - `contact` - Contact form page
   - `api_response` - Return JSON response

2. **Update `urls.py`** with URL patterns
   - Route `/` to home view
   - Route `/blog/` to blog_list view
   - Route `/blog/<int:post_id>/` to blog_detail view (with URL parameter)
   - Route `/contact/` to contact view
   - Route `/api/data/` to api_response view

3. **Test the implementation**
   - Run the tests to verify all views work
   - Test URLs in browser with and without parameters
   - Test JSON response endpoint

4. **Understand URL parameters**
   - Learn how to capture values from URLs
   - Learn how to pass parameters to views

## Project Structure

```
assignment2/
├── manage.py              # Django management utility
├── requirements.txt       # Installed packages
├── README.md             # This file
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

1. `home(request)` - Landing page with links to all sections
2. `blog_list(request)` - Shows a list of blog posts
3. `blog_detail(request, post_id)` - Shows details of a specific post
4. `contact(request)` - Contact form page
5. `api_response(request)` - Returns JSON with data

## How to Test

### Option 1: Run Tests (Recommended)
```bash
cd /Users/enfec/Desktop/Python\ Assignment\ Ep\ 12-24/Python-Assignment-Ep-12--24/episode16/assignment2
source venv/bin/activate
python test_assignment.py
```

### Option 2: Manual Testing
```bash
cd /Users/enfec/Desktop/Python\ Assignment\ Ep\ 12-24/Python-Assignment-Ep-12--24/episode16/assignment2
source venv/bin/activate
python manage.py runserver
```

Then visit:
- `http://127.0.0.1:8000/` - Home page
- `http://127.0.0.1:8000/blog/` - Blog list
- `http://127.0.0.1:8000/blog/1/` - Blog post 1
- `http://127.0.0.1:8000/blog/42/` - Blog post 42
- `http://127.0.0.1:8000/contact/` - Contact page
- `http://127.0.0.1:8000/api/data/` - JSON response

## Learning Outcomes

After completing this assignment, you should understand:
- How to create multiple related views
- URL parameter capture and routing
- URL patterns with variables
- JSON responses in Django
- View organization and structure
- Advanced URL configuration

## Key Concepts

### URL Parameters
URLs can include variable parameters that get passed to views:
- `/blog/1/` - `post_id=1`
- `/blog/42/` - `post_id=42`

In `urls.py`: `path('blog/<int:post_id>/', blog_detail)`
In `views.py`: `def blog_detail(request, post_id):`

### JSON Responses
Use `JsonResponse` to return JSON data instead of HTML:
```python
from django.http import JsonResponse
return JsonResponse({'key': 'value'})
```

### View Organization
Group related URLs and views together:
- Content views (home, about)
- Blog views (list, detail)
- API views (json responses)
    }
]
```

### Critical Settings

#### 1. SECRET_KEY
- Cryptographic key for security-sensitive operations
- Used for: CSRF tokens, session cookies, password resets
- **CRITICAL**: Never hardcode in production
- Should be random and long

**Production pattern:**
```python
SECRET_KEY = os.environ.get('SECRET_KEY')
```

#### 2. DEBUG
- `True`: Development mode with detailed error pages
- `False`: Production mode with generic errors
- **CRITICAL**: Never `True` in production (security risk!)
- Exposes sensitive info: file paths, code, environment variables

**Production pattern:**
```python
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

#### 3. ALLOWED_HOSTS
- List of domain names Django will accept
- Prevents Host header attacks
- For development: `['localhost', '127.0.0.1']`
- For production: `['yourdomain.com', 'www.yourdomain.com']`

**Production pattern:**
```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
```

#### 4. INSTALLED_APPS

Default Django apps:
- `django.contrib.admin` - Admin interface
- `django.contrib.auth` - User authentication
- `django.contrib.contenttypes` - Content type framework
- `django.contrib.sessions` - Session management
- `django.contrib.messages` - User messaging
- `django.contrib.staticfiles` - Static file serving

Your own apps go here too.

#### 5. DATABASES

Default SQLite configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

For PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### 6. TEMPLATES

Configuration for template engine:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### BASE_DIR

Important constant pointing to project root:
```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

Used for dynamic paths:
```python
'NAME': BASE_DIR / 'db.sqlite3',
```

## Tasks

### Task 1: Examine settings.py
- Open `myproject/settings.py`
- Identify each major section
- Understand how BASE_DIR is used
- Note security-sensitive settings

### Task 2: Understand SECRET_KEY
- Find the SECRET_KEY setting
- Understand its purpose
- Note that it should never be committed
- Plan how to handle in production

### Task 3: Configure ALLOWED_HOSTS
- Find ALLOWED_HOSTS setting
- Set it to: `['localhost', '127.0.0.1']`
- Understand why this is needed
- Test with different hosts

### Task 4: Review INSTALLED_APPS
- List all installed apps
- Understand purpose of each default app
- Note where custom apps would go
- See dependencies between apps

### Task 5: Understand DATABASES
- Find database configuration
- Note it uses SQLite by default
- Understand the path to db.sqlite3
- Know where to add PostgreSQL config

### Task 6: Review TEMPLATES
- Find TEMPLATES setting
- Understand BACKEND specification
- Note DIRS and APP_DIRS
- Understand context processors

### Task 7: Run Development Server
```bash
python manage.py runserver
```
Then visit: http://127.0.0.1:8000/

### Task 8: Test Configuration
```bash
python manage.py check
```

This verifies all settings are correct.

### Task 9: Explore Django Commands
```bash
python manage.py help
python manage.py help migrate
python manage.py help runserver
```

### Task 10: Document Key Settings
Create a summary document explaining:
- What each major setting does
- Why it matters for development vs production
- How to configure for different environments

## Common Settings Patterns

### Development Environment
```python
DEBUG = True
ALLOWED_HOSTS = ['*']  # Less restrictive for local testing
SECRET_KEY = 'any-random-secret'  # Doesn't need to be super secure
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Production Environment
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')  # From environment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
```

## Security Checklist

- [ ] Understand what SECRET_KEY does
- [ ] Know why DEBUG=False is critical in production
- [ ] Understand ALLOWED_HOSTS purpose
- [ ] Know which settings are security-sensitive
- [ ] Plan how to handle secrets in production
- [ ] Understand environment variable usage
- [ ] Know about HTTPS enforcement
- [ ] Understand CSRF protection
- [ ] Know about SQL injection prevention
- [ ] Understand XSS protection

## Running Tests

```bash
python test_assignment.py
```

Tests verify:
- Project structure exists
- All required settings are present
- Django check passes
- Development commands available

## Key Takeaways

1. **settings.py is critical** - Contains all project configuration
2. **Security-sensitive settings** - SECRET_KEY, DEBUG, ALLOWED_HOSTS
3. **Environment variables** - Use for production secrets
4. **Different configurations** - Development vs production
5. **Installed apps** - Control what features are available
6. **Database configuration** - Easy to change, impacts everything
7. **Templates** - Configure where to find HTML templates
8. **Middleware** - Request/response processing pipeline
9. **Static files** - CSS, JS, images configuration
10. **Localization** - Language and timezone settings

## Next Steps

- Complete both Assignment 1 and 2
- Understand your project's settings
- Plan security configuration for production
- Ready for Episode 17: Creating your first Django app

---

**Duration:** 2-3 hours  
**Difficulty:** Beginner  
**Prerequisites:** Completed Episode 16 Assignment 1  
**Next:** Episode 17 - Creating Django Apps
