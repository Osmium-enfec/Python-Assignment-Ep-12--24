# Episode 22: Template Inheritance and Forms - Starter Code Guide

## Overview
Episode 22 covers Django template inheritance system and form creation with Bootstrap styling. Students progress from understanding template reusability (Assignment 1) to advanced form integration (Assignment 2).

**Total Tests:** 140+ (40+ per assignment)
- Assignment 1: 40+ tests on template inheritance
- Assignment 2: 50+ tests on forms and CRUD operations

---

## Assignment 1: Template Inheritance Fundamentals

### Topics Covered: 1-40

### What Students Implement

#### 1. **Product Model** (Topics 11, 17-22)
```
8 fields with key information:
- code: CharField (max_length=20, unique=True)
- name: CharField (max_length=200)
- description: TextField (optional)
- price: DecimalField (max_digits=10, decimal_places=2)
- category: CharField (max_length=50)
- is_active: BooleanField (default=True)
- created_at: DateTimeField (auto_now_add=True)
- updated_at: DateTimeField (auto_now=True)

Meta:
- ordering: ['code']

Methods:
- __str__(): Return "{code} - {name}"
```

#### 2. **Base Template** (Topics 1-22, 36-40)
```html
<!DOCTYPE html>
<html>
<head>
    <!-- Meta tags (viewport, charset) - Topics 22 -->
    <!-- Static assets (Bootstrap, Font Awesome) - Topics 21 -->
    {% block title %}Default Title{% endblock %}
</head>
<body>
    <!-- Navbar block - Topics 17, 37 -->
    {% block navbar %}...{% endblock %}
    
    <!-- Main content block - Topics 5, 6, 26 -->
    {% block content %}{% endblock %}
    
    <!-- Footer block - Topics 18 -->
    {% block footer %}...{% endblock %}
</body>
</html>
```

**Key Features:**
- Bootstrap 5.3 CSS CDN
- Font Awesome 6.4 icons
- Responsive design with viewport meta tag
- Navigation bar (Topics 17, 37)
- Footer section (Topics 18)
- Content block for child templates (Topics 5, 6)

#### 3. **Product List Template** (Topics 1-30, 36-40)
```html
{% extends 'base.html' %}

{% block title %}Product List{% endblock %}

{% block content %}
    <!-- Topics 6, 26: Block override and content -->
    <!-- Topics 23-25: URL tag, if/for tags -->
    <!-- Topics 31-35: Filters (date, upper, lower, join, length) -->
    <!-- Topics 36: Semantic HTML -->
    
    <h1>Product List</h1>
    
    {% if products %}
        <table>
            {% for product in products %}
                <tr>
                    <td>{{ product.code }}</td>
                    <td>{{ product.name }}</td>
                    <td>{{ product.category }}</td>
                    <td>{{ product.price|floatformat:2 }}</td>
                    <td>
                        <a href="{% url 'products:detail' product.id %}">View</a>
                    </td>
                </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>No products available.</p>
    {% endif %}
{% endblock %}
```

#### 4. **Product Detail Template** (Topics 1-30)
```html
{% extends 'base.html' %}

{% block title %}{{ product.name }}{% endblock %}

{% block content %}
    <!-- Topics 23: URL tag for back link -->
    <!-- Topics 24-28: If tags, variables, filters -->
    <!-- Topics 31: Date filter for timestamps -->
    
    <h1>{{ product.name|upper }}</h1>
    <p>Code: {{ product.code }}</p>
    <p>{{ product.description }}</p>
    <p>Price: ${{ product.price|floatformat:2 }}</p>
    <p>Category: {{ product.category|title }}</p>
    <p>Status: 
        {% if product.is_active %}
            <span>Active</span>
        {% else %}
            <span>Inactive</span>
        {% endif %}
    </p>
    <p>Created: {{ product.created_at|date:"Y-m-d H:i" }}</p>
    
    <a href="{% url 'products:list' %}">Back to List</a>
{% endblock %}
```

#### 5. **Views** (Topics 23-30)
```python
# Two simple views:
def product_list(request):
    # Get all products
    # Context: products
    # Template: products/list.html
    # Topics: Template rendering with context
    pass

def product_detail(request, product_id):
    # Get single product (or 404)
    # Context: product
    # Template: products/detail.html
    # Topics: Template rendering with instance
    pass
```

#### 6. **URL Routing** (Topics 23)
```python
# patterns with app_name
urlpatterns = [
    path('', product_list, name='list'),
    path('<int:product_id>/', product_detail, name='detail'),
]
```

### Test Structure: 40+ tests organized by topic
- **TemplateInheritanceTestCase** (10 tests): Topics 1-12 (extends, blocks, inheritance)
- **MultiLevelInheritanceTestCase** (4 tests): Topics 13-16 (three-tier, chaining)
- **BaseTemplateStructureTestCase** (4 tests): Topics 17-22 (navbar, footer, meta)
- **TemplateTagsTestCase** (7 tests): Topics 23-30 (url, if, for, block, variables)
- **TemplateFiltersTestCase** (5 tests): Topics 31-35 (date, join, length, upper, lower)
- **BestPracticesTestCase** (3 tests): Topics 36-40 (HTML, navigation, reusability)
- **ProductListTestCase** (3 tests): View and template integration
- **ProductDetailTestCase** (4 tests): Detail view and template

---

## Assignment 2: Advanced Forms and Template Integration

### Topics Covered: 41-80

### What Students Implement

#### 1. **Book Model** (Topics 41-48)
```
9 fields with form-relevant structure:
- title: CharField (max_length=200)
- isbn: CharField (max_length=20, unique=True)
- author: CharField (max_length=200)
- description: TextField (optional)
- price: DecimalField (max_digits=10, decimal_places=2)
- genre: CharField (max_length=50)
- is_published: BooleanField (default=True)
- created_at: DateTimeField (auto_now_add=True)
- updated_at: DateTimeField (auto_now=True)

Meta:
- ordering: ['-created_at']

Methods:
- __str__(): Return "{title} by {author}"
```

#### 2. **BookForm** (Topics 41-64)
```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'author', 'description', 'price', 'genre', 'is_published']
    
    # Topic 44-45: Widget customization
    # Topic 57-62: Bootstrap classes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control, form-select classes
        # Add placeholder text (Topic 60)
        # Add help_text
        # Bootstrap form groups (mb-3)
```

**Key Features:**
- Topics 41-42: ModelForm with Meta configuration
- Topics 43-45: Widget attributes with Bootstrap classes
- Topics 49-56: CSRF protection (automatic in template)
- Topics 57-64: Bootstrap styling (form-control, form-group, etc.)

#### 3. **Views** (Topics 65-80)
```python
# Topic 65: book_list - Display all books
def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

# Topic 65: book_create - Add new book
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            # Topic 69: Success message
            messages.success(request, f"Book '{book.title}' created!")
            # Topic 78: Button action (save)
            return redirect('books:list')
    else:
        # Topic 65: Empty form
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form})

# Topic 66: book_update - Edit existing book
def book_update(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        # Topic 66: Pre-filled form data
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            # Topic 77: Data persistence
            messages.success(request, f"Book '{book.title}' updated!")
            return redirect('books:list')
    else:
        # Topic 66: Instance pre-fills form
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'book': book})

# Topic 68: book_delete - Confirm and delete
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        title = book.title
        book.delete()
        # Topic 70: Success message after delete
        messages.success(request, f"Book '{title}' deleted!")
        return redirect('books:list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})
```

**Key Features:**
- Topics 49: CSRF token (automatic in template)
- Topics 52-56: Form validation and error handling
- Topics 69-70: Success/error messages
- Topics 71-72: Field validation indicators
- Topics 73-80: Complete form workflow

#### 4. **Book List Template** (Topics 65, 73-80)
```html
{% extends 'base.html' %}

{% block title %}Books{% endblock %}

{% block content %}
    <!-- Topic 73: Form template integration -->
    <!-- Topic 78: Button actions -->
    <!-- Topic 79: Icon integration -->
    
    <h1>Books</h1>
    <a href="{% url 'books:create' %}" class="btn btn-primary">
        <!-- Topic 79: Font Awesome icon -->
        Create Book
    </a>
    
    <table>
        {% for book in books %}
            <tr>
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.isbn }}</td>
                <td>${{ book.price|floatformat:2 }}</td>
                <td>
                    <!-- Topic 78: Action buttons -->
                    <a href="{% url 'books:edit' book.id %}" class="btn btn-warning btn-sm">Edit</a>
                    <a href="{% url 'books:delete' book.id %}" class="btn btn-danger btn-sm">Delete</a>
                </td>
            </tr>
        {% endfor %}
    </table>
{% endblock %}
```

#### 5. **Book Form Template** (Topics 57-80)
```html
{% extends 'base.html' %}

{% block title %}{% if form.instance.pk %}Edit{% else %}Add{% endif %} Book{% endblock %}

{% block content %}
    <form method="post">
        <!-- Topic 49: CSRF token -->
        {% csrf_token %}
        
        <!-- Topic 57-62: Form groups with Bootstrap -->
        {% for field in form %}
            <div class="mb-3">
                <!-- Topic 48: Field label -->
                {{ field.label_tag }}
                
                <!-- Topic 46-47: Field rendering with widget -->
                <!-- Topic 57-58: Bootstrap classes -->
                {{ field }}
                
                <!-- Topic 71: Field error display -->
                {% if field.errors %}
                    <div class="invalid-feedback">
                        {{ field.errors }}
                    </div>
                {% endif %}
            </div>
        {% endfor %}
        
        <!-- Topic 78: Button actions -->
        <button type="submit" class="btn btn-success">Save</button>
        <a href="{% url 'books:list' %}" class="btn btn-secondary">Cancel</a>
    </form>
{% endblock %}
```

#### 6. **Book Delete Template** (Topics 68-70)
```html
{% extends 'base.html' %}

{% block title %}Delete {{ book.title }}{% endblock %}

{% block content %}
    <!-- Topic 68: Delete confirmation -->
    <h1>Delete Book?</h1>
    
    <!-- Topic 69: Warning message -->
    <div class="alert alert-warning">
        This action cannot be undone!
    </div>
    
    <!-- Topic 68: Show what will be deleted -->
    <p>Title: {{ book.title }}</p>
    <p>Author: {{ book.author }}</p>
    <p>ISBN: {{ book.isbn }}</p>
    
    <!-- Topic 49: CSRF token -->
    <!-- Topic 78: Confirm button -->
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Confirm Delete</button>
        <a href="{% url 'books:list' %}" class="btn btn-secondary">Cancel</a>
    </form>
{% endblock %}
```

### Test Structure: 50+ tests organized by topic
- **BookModelTestCase** (8 tests): Topics 41-48 (model creation, fields, timestamps)
- **BookFormTestCase** (8 tests): Topics 49-64 (form rendering, widgets, validation)
- **BookListViewTestCase** (5 tests): Topics 65, 73-80 (list display, links)
- **BookCreateViewTestCase** (7 tests): Topics 65, 73-80 (form rendering, validation, redirect)
- **BookUpdateViewTestCase** (7 tests): Topics 66-77 (pre-filled form, data persistence)
- **BookDeleteViewTestCase** (5 tests): Topics 68-70 (confirmation, deletion)
- **FormSecurityTestCase** (4 tests): Topics 49-56 (CSRF, error handling)
- **FormIntegrationTestCase** (6 tests): Topics 73-80 (complete workflow)

---

## Key Learning Objectives

### Episode 22 A1: Template Inheritance
1. Understanding template inheritance and {% extends %} tag
2. Block system for flexible templates
3. Multi-level inheritance patterns
4. Base template structure with Bootstrap
5. Template tags ({% url %}, {% if %}, {% for %})
6. Template filters (date, upper, lower, join, length)
7. DRY principle and code reusability
8. Semantic HTML and responsive design

### Episode 22 A2: Forms and Integration
1. All A1 concepts retained
2. ModelForm creation and configuration
3. Form widget customization with Bootstrap
4. Form rendering in templates
5. CSRF token security
6. Form validation and error display
7. Complete CRUD workflow with forms
8. User feedback with messages
9. Data persistence and pre-filled forms
10. Professional form UI/UX

---

## File Structure

### Assignment 1
```
assignment1_starter/
├── manage.py (provided)
├── myapp/
│   ├── settings.py (provided)
│   ├── urls.py (scaffold)
│   ├── wsgi.py (provided)
│   └── __init__.py
├── products/
│   ├── models.py (TODO)
│   ├── forms.py
│   ├── views.py (TODO)
│   ├── urls.py (TODO)
│   ├── admin.py (TODO)
│   ├── tests.py (40+ test stubs)
│   └── __init__.py
└── templates/
    ├── base.html (TODO - main structure)
    └── products/
        ├── list.html (TODO)
        └── detail.html (TODO)
```

### Assignment 2
```
assignment2_starter/
├── manage.py (provided)
├── myapp/
│   ├── settings.py (provided)
│   ├── urls.py (scaffold)
│   ├── wsgi.py (provided)
│   └── __init__.py
├── books/
│   ├── models.py (TODO - Book model)
│   ├── forms.py (TODO - BookForm)
│   ├── views.py (TODO - 4 CRUD views)
│   ├── urls.py (TODO - 4 patterns)
│   ├── admin.py (TODO)
│   ├── tests.py (50+ test stubs)
│   └── __init__.py
└── templates/
    ├── base.html (TODO)
    └── books/
        ├── book_list.html (TODO)
        ├── book_form.html (TODO - add/edit)
        └── book_confirm_delete.html (TODO)
```

---

## Implementation Patterns

### Template Inheritance
```html
<!-- base.html -->
{% block title %}Default{% endblock %}
{% block navbar %}...{% endblock %}
{% block content %}...{% endblock %}

<!-- child.html -->
{% extends 'base.html' %}
{% block title %}Custom Title{% endblock %}
{% block content %}Custom content{% endblock %}
```

### Template Tags
```html
<!-- URL tag - Topics 23 -->
<a href="{% url 'app:view' object.id %}">Link</a>

<!-- If tag - Topics 24 -->
{% if condition %}Yes{% else %}No{% endif %}

<!-- For tag - Topics 25 -->
{% for item in items %}{{ item }}{% endfor %}

<!-- Block Super - Topics 8 -->
{% block content %}
    {{ block.super }}
    Additional content
{% endblock %}
```

### Template Filters
```html
<!-- Date filter - Topics 31 -->
{{ date|date:"Y-m-d" }}

<!-- Upper/Lower - Topics 34-35 -->
{{ text|upper }} {{ text|lower }}

<!-- Join - Topics 32 -->
{{ list|join:", " }}

<!-- Length - Topics 33 -->
{{ list|length }}
```

### Form Rendering
```html
<!-- Full form rendering - Topics 46 -->
<form method="post">{% csrf_token %}{{ form }}</form>

<!-- Manual field rendering - Topics 47-48 -->
<form method="post">
    {% csrf_token %}
    {% for field in form %}
        {{ field.label_tag }}
        {{ field }}
        {{ field.errors }}
    {% endfor %}
    <button type="submit">Submit</button>
</form>
```

---

## Testing

Each assignment has comprehensive test coverage organized by topic:

**Run tests:**
```bash
python manage.py test
python manage.py test -v 2
python manage.py test assignment1_app.tests.TemplateInheritanceTestCase
```

---

## Success Criteria

### Assignment 1: All 40+ tests pass ✓
- Template inheritance working
- All blocks properly overridden
- URL tags generating correct URLs
- Filters applying correctly
- Bootstrap styling applied

### Assignment 2: All 50+ tests pass ✓
- Forms rendering correctly
- CSRF tokens present
- Validation working
- Messages displaying
- Complete CRUD workflow functioning

---

## Debugging Tips

1. **Template not found**: Check DIRS in settings, app_directories setting
2. **Block not found**: Check spelling of {% block %} names
3. **URL tag error**: Verify URL pattern name in urls.py
4. **Form not rendering**: Check form field definitions in forms.py
5. **CSRF error**: Ensure {% csrf_token %} in form template
6. **Filter error**: Check filter syntax and data type
7. **Messages not showing**: Ensure Django messages middleware is configured

---

## Resources

- Template Inheritance: https://docs.djangoproject.com/en/5.1/ref/templates/language/
- Built-in Tags: https://docs.djangoproject.com/en/5.1/ref/templates/builtins/
- Built-in Filters: https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#built-in-filter-reference
- Form Rendering: https://docs.djangoproject.com/en/5.1/topics/forms/
- Bootstrap Documentation: https://getbootstrap.com/docs/5.3/
- Font Awesome: https://fontawesome.com/docs/web/setup/get-started
