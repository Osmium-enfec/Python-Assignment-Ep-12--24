# Episode 20: URL Routing, Views, and Modals - Starter Code Guide

## Overview
Episode 20 covers URL routing fundamentals and advanced modal/AJAX interactions. Students progress from basic URL patterns and view functions (Assignment 1) to complex modal interactions and AJAX requests (Assignment 2).

**Total Tests:** 80+ (40+ per assignment)
- Assignment 1: 40 tests on URL routing, views, and object retrieval
- Assignment 2: 40 tests on modals, AJAX, and action buttons

---

## Assignment 1: URL Routing and View Fundamentals

### Topics Covered: 1-40

### What Students Implement

#### 1. **Student Model** (Topics 36-40)
```python
from django.db import models

class Student(models.Model):
    roll_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    gpa = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['roll_no']

    def __str__(self):
        return f"{self.name} ({self.roll_no})"
```

**Topics Covered:**
- Topics 36-40: QuerySet operations (all(), filter(), get(), get_object_or_404())

#### 2. **Views** (Topics 27-40)
```python
from django.shortcuts import render, get_object_or_404
from .models import Student

def student_list(request):
    """Topics 27-40: View function fundamentals"""
    # Topic 38: Get all students with QuerySet
    students = Student.objects.all()
    
    # Topic 32: Create context dictionary
    context = {
        'students': students
    }
    
    # Topic 33: Render template with context
    return render(request, 'students/list.html', context)

def student_detail(request, student_id):
    """Topics 27-40: View with URL parameter"""
    # Topic 34: View receives parameter from URL
    # Topic 36: get_object_or_404 for safe retrieval
    student = get_object_or_404(Student, id=student_id)
    
    # Topic 32: Context with single object
    context = {'student': student}
    
    # Topic 33: Render template
    return render(request, 'students/detail.html', context)

def student_by_roll(request, roll_no):
    """Topics 27-40: View with str parameter converter"""
    # Topic 5: str converter for non-integer parameters
    student = get_object_or_404(Student, roll_no=roll_no)
    return render(request, 'students/detail.html', {'student': student})

def student_redirect(request):
    """Topics 19-26: Redirect example"""
    # Topic 20: redirect() shortcut
    from django.shortcuts import redirect
    return redirect('students:list')
```

**Topics Covered:**
- Topic 27: View Function definition
- Topic 28: Request parameter
- Topic 29: View return value
- Topic 30: HTTP Methods (GET, POST, etc.)
- Topic 31: request.method checking
- Topic 32: Context dictionary creation
- Topic 33: render() function
- Topic 34: View receives parameters
- Topic 35: Access request data
- Topic 36: get_object_or_404()
- Topic 37: QuerySet operations
- Topic 38: Model.objects.all()
- Topic 39: Model.objects.filter()
- Topic 40: Model.objects.get()

#### 3. **URL Routing** (Topics 1-18)
```python
from django.urls import path
from . import views

# Topic 7: Namespace for URL names
app_name = 'students'

# Topic 8: URL patterns list
urlpatterns = [
    # Topic 1-2: Basic URL routing with path()
    # Topic 6: URL name for reverse lookup
    path('', views.student_list, name='list'),
    
    # Topic 3-4: URL parameters with int converter
    path('<int:student_id>/', views.student_detail, name='detail'),
    
    # Topic 5: str converter for non-integer parameters
    path('roll/<str:roll_no>/', views.student_by_roll, name='by_roll'),
    
    # Topic 19-26: Redirect routing
    path('redirect/', views.student_redirect, name='redirect'),
]
```

**Topics Covered:**
- Topic 1: URL Routing concept
- Topic 2: path() function
- Topic 3: URL Parameters
- Topic 4: int Converter
- Topic 5: str Converter
- Topic 6: URL Name for reverse
- Topic 7: app_name for namespace
- Topic 8: URL patterns list
- Topic 9: Trailing slash handling (automatic in Django)
- Topic 10: URL Inclusion (in main urls.py)

#### 4. **URL Reversal** (Topics 11-18)
```python
# Topic 11: reverse() function in Python
from django.urls import reverse

# Generate URL by name
url = reverse('students:list')  # '/students/'
url = reverse('students:detail', args=[1])  # '/students/1/'
url = reverse('students:by_roll', kwargs={'roll_no': 'S001'})  # '/students/roll/S001/'
```

**Topics Covered:**
- Topic 11: reverse() function
- Topic 12: reverse() with args
- Topic 13: reverse() with kwargs
- Topic 14: Namespace usage
- Topic 15: {% url %} template tag
- Topic 16: URL generation
- Topic 17: Flexibility (single source of truth)
- Topic 18: Maintainability (change URLs in one place)

#### 5. **HTTP Redirects** (Topics 19-26)
```python
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def my_redirect_view(request):
    # Topic 20: redirect() shortcut (preferred)
    return redirect('students:list')  # By name
    
    # Topic 24: Redirect to URL
    return redirect('/students/')
    
    # Topic 23: Redirect to named URL
    return redirect('students:detail', student_id=1)
    
    # Topic 25: Post-Redirect-Get pattern
    if request.method == 'POST':
        # Process form
        return redirect('students:list')
```

**Topics Covered:**
- Topic 19: HttpResponseRedirect
- Topic 20: redirect() shortcut
- Topic 21: Redirect after POST (PRG pattern)
- Topic 22: Status codes (301, 302, 303, 307)
- Topic 23: Redirect to named URL
- Topic 24: Redirect to literal URL
- Topic 25: Post-Redirect-Get pattern
- Topic 26: Session data persistence across redirects

#### 6. **Templates** (Topics 1-40)
```html
<!-- list.html -->
{% extends 'base.html' %}

{% block title %}Student List{% endblock %}

{% block content %}
    <h1>Students</h1>
    
    <table class="table">
        {% for student in students %}
            <tr>
                <td>{{ student.roll_no }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.email }}</td>
                <td>{{ student.gpa }}</td>
                <td>
                    <!-- Topic 15: {% url %} tag for URL reversal -->
                    <!-- Topic 16: URL generation in templates -->
                    <a href="{% url 'students:detail' student.id %}">View by ID</a>
                    <a href="{% url 'students:by_roll' student.roll_no %}">View by Roll</a>
                </td>
            </tr>
        {% endfor %}
    </table>
{% endblock %}
```

### Test Structure: 40 tests organized by topic

**Test Classes:**
- URLRoutingTestCase (10 tests): Topics 1-10 (path, parameters, converters, app_name)
- URLReversalTestCase (8 tests): Topics 11-18 (reverse, url tag, flexibility)
- HTTPRedirectsTestCase (8 tests): Topics 19-26 (redirects, PRG pattern)
- ViewFunctionsTestCase (9 tests): Topics 27-35 (view functions, context, render)
- ObjectRetrievalTestCase (5 tests): Topics 36-40 (QuerySets, get_object_or_404)

---

## Assignment 2: Modals, AJAX, and Action Buttons

### Topics Covered: 41-80

### What Students Implement

#### 1. **Course and Enrollment Models** (Topics 41-80)
```python
from django.db import models

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)
    max_students = models.IntegerField(default=30)
    enrolled_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code}: {self.title}"
    
    def is_full(self):
        """Check if course is at capacity"""
        return self.enrolled_count >= self.max_students
    
    def available_seats(self):
        """Get available seats"""
        return self.max_students - self.enrolled_count


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    enrolled_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-enrolled_date']

    def __str__(self):
        return f"{self.student_name} - {self.course.code}"
```

#### 2. **Views** (Topics 41-80)
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import Course, Enrollment

def course_list(request):
    """Topics 41-80: Display courses with modals"""
    # Topic 38: Get all courses
    courses = Course.objects.all()
    
    # Topic 44-45: Context with modal data
    context = {'courses': courses}
    
    return render(request, 'courses/list.html', context)

def course_data(request, course_id):
    """Topics 62-68: AJAX endpoint returning JSON"""
    # Topic 63: fetch() API target
    course = get_object_or_404(Course, id=course_id)
    
    # Topic 64: JsonResponse
    data = {
        'id': course.id,
        'code': course.code,
        'title': course.title,
        'description': course.description,
        'instructor': course.instructor,
        'credits': course.credits,
        'enrolled': course.enrolled_count,
        'max_students': course.max_students,
        'available': course.available_seats(),
        'is_full': course.is_full()
    }
    
    return JsonResponse(data)

def course_delete_confirm(request, course_id):
    """Topics 41-80: Delete confirmation modal"""
    course = get_object_or_404(Course, id=course_id)
    
    # Topic 78-79: Pre-filled modal with data attributes
    context = {
        'course': course,
        'enrollments': course.enrollment_set.all()
    }
    
    return render(request, 'courses/delete_confirm.html', context)

def course_delete(request, course_id):
    """Topics 19-26, 71: Delete with redirect"""
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    
    # Topic 20: Redirect after POST
    return redirect('courses:list')
```

**Topics Covered:**
- Topics 41-60: Modal components and rendering
- Topics 61-68: AJAX and JsonResponse
- Topics 69-77: Action buttons and styling
- Topics 78-80: Advanced modal features

#### 3. **Templates** (Topics 41-80)
```html
<!-- list.html -->
{% extends 'base.html' %}

{% block title %}Courses{% endblock %}

{% block content %}
    <!-- Course list table -->
    <table class="table">
        {% for course in courses %}
            <tr>
                <td>{{ course.code }}</td>
                <td>{{ course.title }}</td>
                <td>{{ course.instructor }}</td>
                <td>{{ course.credits }}</td>
                <td>
                    <!-- Topics 69-73: Action buttons with icons -->
                    <button class="btn btn-primary btn-sm" 
                            data-bs-toggle="modal" 
                            data-bs-target="#viewModal"
                            data-course-id="{{ course.id }}">
                        <i class="fas fa-eye"></i> View
                    </button>
                    
                    <button class="btn btn-warning btn-sm">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    
                    <!-- Topic 71, 74: Delete with confirmation -->
                    <button class="btn btn-danger btn-sm" 
                            data-bs-toggle="modal" 
                            data-bs-target="#deleteModal"
                            data-course-id="{{ course.id }}">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </td>
            </tr>
        {% endfor %}
    </table>

    <!-- Topics 41-60: Bootstrap Modal -->
    <div class="modal fade" id="viewModal" tabindex="-1">
        <!-- Topic 41-45: Modal structure -->
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- Topic 43: Modal Header -->
                <div class="modal-header">
                    <h5 class="modal-title">Course Details</h5>
                    <!-- Topic 55: Close button -->
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                
                <!-- Topic 44: Modal Body -->
                <div class="modal-body" id="modalBody">
                    <!-- Topic 68: Dynamic content loaded via AJAX -->
                    Loading...
                </div>
                
                <!-- Topic 45: Modal Footer -->
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete confirmation modal -->
    <div class="modal fade" id="deleteModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Delete Course?</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                
                <!-- Topic 44: Modal body with warning -->
                <div class="modal-body">
                    <p>Are you sure you want to delete this course?</p>
                    <p id="courseNameInModal"></p>
                </div>
                
                <!-- Topic 45: Modal footer with action -->
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <!-- Topic 71: Delete button -->
                    <button type="button" class="btn btn-danger" id="confirmDeleteBtn">Delete</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Topics 61-68: AJAX script -->
    <script>
        // Topic 56-57: Modal instance and show
        const viewModal = document.getElementById('viewModal');
        viewModal.addEventListener('show.bs.modal', function(e) {
            // Topic 79: Get data from button attributes
            const courseId = e.relatedTarget.dataset.courseId;
            
            // Topic 63: fetch() AJAX request
            fetch(`{% url 'courses:data' 0 %}`.replace('0', courseId))
                .then(response => response.json())
                .then(data => {
                    // Topic 68: Dynamic content update
                    document.getElementById('modalBody').innerHTML = `
                        <p><strong>${data.code}</strong>: ${data.title}</p>
                        <p>${data.description}</p>
                        <p>Instructor: ${data.instructor}</p>
                        <p>Enrolled: ${data.enrolled}/${data.max_students}</p>
                    `;
                })
                .catch(error => console.error('Error:', error));
        });
        
        // Topic 71, 78: Delete button functionality
        const deleteModal = document.getElementById('deleteModal');
        deleteModal.addEventListener('show.bs.modal', function(e) {
            const courseId = e.relatedTarget.dataset.courseId;
            
            // Topic 79: Pre-fill modal with data
            document.getElementById('confirmDeleteBtn').onclick = function() {
                // Topic 20-21: POST redirect
                window.location.href = `/courses/${courseId}/delete_confirm/`;
            };
        });
    </script>
{% endblock %}
```

### Test Structure: 40 tests organized by topic

**Test Classes:**
- BootstrapModalTestCase (14 tests): Topics 41-58 (modal components, structure, sizing)
- ModalInteractionsTestCase (6 tests): Topics 55-60 (buttons, events, listeners)
- AJAXDynamicLoadingTestCase (8 tests): Topics 61-68 (fetch, JSON, dynamic content)
- ActionButtonsTestCase (9 tests): Topics 69-77 (buttons, styling, icons, confirmation)
- AdvancedModalFeaturesTestCase (3 tests): Topics 78-80 (pre-filled, data attributes, workflows)

---

## Key Learning Objectives

### Episode 20 A1: URL Routing & Views
1. Understanding URL routing and path patterns
2. URL converters (int, str)
3. URL naming and namespaces
4. URL reversal with reverse() and {% url %} tag
5. HTTP redirects and redirect patterns
6. View functions and HTTP request/response
7. Context dictionaries and template rendering
8. QuerySet operations (all, filter, get)
9. Safe object retrieval with get_object_or_404()

### Episode 20 A2: Modals & AJAX
1. All A1 concepts retained
2. Bootstrap modal structure and components
3. Modal triggering and data attributes
4. Modal sizing and positioning
5. AJAX requests with Fetch API
6. JsonResponse for AJAX endpoints
7. Dynamic content loading into modals
8. Action buttons (view, edit, delete)
9. Button styling with Bootstrap
10. Icon integration with Font Awesome

---

## File Structure

### Assignment 1
```
assignment1_starter/
├── manage.py (provided)
├── myapp/
│   ├── settings.py (provided)
│   ├── urls.py (with URL inclusion)
│   ├── wsgi.py (provided)
│   └── __init__.py
├── students/
│   ├── models.py (TODO - Student model)
│   ├── views.py (TODO - 4 views)
│   ├── urls.py (TODO - 4 URL patterns)
│   ├── admin.py (TODO)
│   ├── tests.py (40 test stubs)
│   └── __init__.py
└── templates/
    └── students/
        ├── list.html (TODO)
        └── detail.html (TODO)
```

### Assignment 2
```
assignment2_starter/
├── manage.py (provided)
├── myapp/
│   ├── settings.py (provided)
│   ├── urls.py (with URL inclusion)
│   ├── wsgi.py (provided)
│   └── __init__.py
├── courses/
│   ├── models.py (TODO - Course + Enrollment)
│   ├── views.py (TODO - 5 views with AJAX)
│   ├── urls.py (TODO - 5 URL patterns)
│   ├── admin.py (TODO)
│   ├── tests.py (40 test stubs)
│   └── __init__.py
└── templates/
    └── courses/
        └── list.html (TODO - with modals)
```

---

## Implementation Patterns

### URL Routing
```python
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='list'),
    path('<int:student_id>/', views.student_detail, name='detail'),
    path('roll/<str:roll_no>/', views.student_by_roll, name='by_roll'),
]
```

### View with get_object_or_404
```python
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'students/detail.html', {'student': student})
```

### URL Reversal in Templates
```html
<a href="{% url 'students:detail' student.id %}">View</a>
<a href="{% url 'students:by_roll' student.roll_no %}">By Roll</a>
```

### Bootstrap Modal
```html
<button class="btn btn-primary" 
        data-bs-toggle="modal" 
        data-bs-target="#myModal">
    Open Modal
</button>

<div class="modal fade" id="myModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">...</div>
            <div class="modal-body">...</div>
            <div class="modal-footer">...</div>
        </div>
    </div>
</div>
```

### AJAX with Fetch
```javascript
const modal = document.getElementById('myModal');
modal.addEventListener('show.bs.modal', function(e) {
    const id = e.relatedTarget.dataset.itemId;
    fetch(`/api/item/${id}/`)
        .then(r => r.json())
        .then(data => {
            // Update modal content
        });
});
```

---

## Success Criteria

### Assignment 1: All 40 tests pass ✓
- URL patterns correctly defined
- All URL converters working
- reverse() and {% url %} generating correct URLs
- Redirects working properly
- Views rendering correct templates
- get_object_or_404 returning objects or 404

### Assignment 2: All 40 tests pass ✓
- Modals rendering on page
- All modal components (header, body, footer) present
- Action buttons triggering modals
- AJAX requests returning JSON
- Modal content updating dynamically
- Delete confirmations working
- Button styling and icons applied

---

## Debugging Tips

1. **URL not found**: Check URL pattern spelling and app_name
2. **reverse() error**: Verify URL name and arguments match pattern
3. **404 error**: Confirm object exists and ID is correct
4. **Modal not opening**: Check data-bs-toggle and data-bs-target attributes
5. **AJAX not loading**: Check Network tab in DevTools, verify endpoint exists
6. **Modal content blank**: Check JSON response format and JavaScript updating DOM

---

## Resources

- URL Dispatcher: https://docs.djangoproject.com/en/5.1/topics/http/urls/
- View Decorators: https://docs.djangoproject.com/en/5.1/topics/http/views/
- QuerySet API: https://docs.djangoproject.com/en/5.1/ref/models/querysets/
- Bootstrap Modals: https://getbootstrap.com/docs/5.3/components/modal/
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- JsonResponse: https://docs.djangoproject.com/en/5.1/ref/request-response/#jsonresponse
