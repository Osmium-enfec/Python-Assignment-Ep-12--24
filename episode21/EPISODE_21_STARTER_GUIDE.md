# Episode 21: Django Forms and Validation - Starter Code Guide

## Overview
Episode 21 teaches Django form fundamentals and advanced validation techniques. Students progress from basic form creation (Assignment 1) to complex validation and user feedback (Assignment 2).

**Total Tests:** 80+ (40+ per assignment)
- Assignment 1: 40+ tests on form basics and submission
- Assignment 2: 40+ tests on validation, saving, and messages

---

## Assignment 1: Form Fundamentals and Setup

### Topics Covered: 1-40

### What Students Implement

#### 1. **Student Model** (Topics 1-10, 14-20)
```python
from django.db import models

class Student(models.Model):
    # These fields auto-generate form widgets
    roll_no = models.CharField(max_length=20, unique=True)           # Topic 7: TextInput
    name = models.CharField(max_length=100)                          # Topic 7: TextInput
    email = models.EmailField(unique=True)                           # Topic 8: EmailInput
    phone = models.CharField(max_length=15, blank=True)              # Topic 7: TextInput
    address = models.TextField(blank=True)                           # Topic 12: Textarea
    gpa = models.FloatField(default=0.0)                             # Topic 20: NumberInput
    is_active = models.BooleanField(default=True)                    # Topic 10: CheckboxInput
    enrolled_date = models.DateField(auto_now_add=True)              # Topic 9: DateInput
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['roll_no']

    def __str__(self):
        return f"{self.name} ({self.roll_no})"
```

**Topics Covered:**
- Topic 4: Model to Form Conversion (automatic field generation)
- Topic 5: Automatic Field Generation from model
- Topics 7-10, 20: Widget types (TextInput, EmailInput, DateInput, CheckboxInput, NumberInput)

#### 2. **StudentForm** (Topics 1-30)
```python
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    # Topics 1-3: ModelForm basics
    class Meta:
        # Topic 3: Meta class configuration
        model = Student
        fields = ['roll_no', 'name', 'email', 'phone', 'address', 'gpa', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Topics 13, 21-22: Widget attributes and labels
        # Add placeholders, help text, CSS classes
        self.fields['roll_no'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'e.g., STU001'
        }
        self.fields['roll_no'].help_text = "Student roll number (max 20 characters)"
        
        # Topics 23-30: Custom validation
        # clean_email() for email validation
        # clean_phone() for phone validation

    def clean_email(self):
        """Topic 29: Custom email validation"""
        # Validate email format or uniqueness
        email = self.cleaned_data.get('email')
        # Custom validation logic
        return email

    def clean_phone(self):
        """Topic 30: Custom phone validation"""
        # Validate phone format
        phone = self.cleaned_data.get('phone')
        # Custom validation logic
        return phone
```

**Topics Covered:**
- Topic 1: Django Forms Module
- Topic 2: ModelForm Class
- Topic 3: Form Meta Class configuration
- Topic 4: Model to Form Conversion
- Topic 5: Automatic Field Generation
- Topic 6: Widget System
- Topics 7-10: Specific widget types
- Topics 11-13: Widget attributes and CSS classes
- Topics 14-20: Django form field types (CharField, EmailField, etc.)
- Topics 21-22: Labels and help text
- Topics 23-30: Form validation and custom validators

#### 3. **Views** (Topics 31-40)
```python
from django.shortcuts import render
from django.contrib import messages
from .forms import StudentForm

def student_form(request):
    """Topics 31-40: GET/POST form handling"""
    
    # Topic 33: Check request method
    if request.method == 'POST':
        # Topic 32, 36: POST request with form data
        form = StudentForm(request.POST)
        
        # Topic 26: is_valid() check
        if form.is_valid():
            # Topic 27: Access cleaned_data
            cleaned_data = form.cleaned_data
            
            # Topic 50: Save form
            student = form.save()
            
            # Show success message
            messages.success(request, f"Student {student.name} added successfully!")
            
            # Redirect or return
            return redirect('students:list')
    else:
        # Topic 31, 35: GET request - blank form instance
        form = StudentForm()
    
    # Topic 38: Render template with form context
    return render(request, 'students/form.html', {
        'form': form
    })
```

**Topics Covered:**
- Topic 31: GET Request Handling (display blank form)
- Topic 32: POST Request Handling (process submission)
- Topic 33: request.method Check
- Topic 34: GET and POST Differentiation
- Topic 35: Creating Blank Form Instance
- Topic 36: Creating Form with POST Data
- Topic 37: Form Submission Processing
- Topic 38: Template Form Rendering with context
- Topics 39-40: CSRF token (automatic in template)

#### 4. **Template** (Topics 35-40)
```html
{% extends 'base.html' %}

{% block title %}Add Student{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <h1>Add Student</h1>
        
        <!-- Topic 38: Form rendering -->
        <form method="post">
            <!-- Topic 40: CSRF token -->
            {% csrf_token %}
            
            {% for field in form %}
                <!-- Topic 21: Field label -->
                {{ field.label_tag }}
                
                <!-- Topic 46-47: Field rendering -->
                {{ field }}
                
                <!-- Topic 22: Help text -->
                {% if field.help_text %}
                    <small class="form-text text-muted">{{ field.help_text }}</small>
                {% endif %}
                
                <!-- Topic 52-53: Error display -->
                {% if field.errors %}
                    <div class="alert alert-danger">
                        {{ field.errors }}
                    </div>
                {% endif %}
            {% endfor %}
            
            <button type="submit" class="btn btn-primary">Add Student</button>
        </form>
    </div>
</div>
{% endblock %}
```

**Topics Covered:**
- Topic 35: Blank form instance in GET request
- Topic 37: Form submission processing
- Topic 38: Form rendering with context
- Topic 40: {% csrf_token %} tag security
- Topic 46: {{ form }} rendering
- Topic 47: {{ form.field }} individual field rendering

### Test Structure: 40+ tests organized by topic

**Test Classes:**
- FormFundamentalsTestCase (8 tests): Topics 1-10 (ModelForm, Meta, widgets)
- FormFieldsWidgetsTestCase (8 tests): Topics 11-20 (Widget types, form fields)
- FormCustomizationTestCase (10 tests): Topics 21-30 (Labels, validation, custom clean)
- GetPostHandlingTestCase (10 tests): Topics 31-40 (Request handling, CSRF, rendering)

---

## Assignment 2: Advanced Validation and User Feedback

### Topics Covered: 41-80

### What Students Implement

#### 1. **Course Model** (Topics 41-48)
```python
from django.db import models

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)          # Topic 47: Unique field
    name = models.CharField(max_length=200)
    credit_hours = models.IntegerField(default=3)                # Topic 20: IntegerField
    instructor_email = models.EmailField(unique=True)            # Topic 47: Unique email
    description = models.TextField(blank=True)
    max_students = models.IntegerField(default=30)
    enrollment_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"
```

**Topics Covered:**
- Topic 41: CSRF Protection (automatic in Django POST)
- Topic 44: ValidationError exception support
- Topic 47: Unique field constraints for database validation
- Topic 48: Database lookup validation

#### 2. **CourseForm** (Topics 41-70)
```python
from django import forms
from django.core.exceptions import ValidationError
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'credit_hours', 'instructor_email', 
                  'description', 'max_students', 'enrollment_fee', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Topic 61: Bootstrap form-control classes
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control'
            }
        
        # Topic 62: Form feedback classes
        # Add is-invalid class for errors

    def clean(self):
        """Topic 43: Form-level clean() method"""
        cleaned_data = super().clean()
        
        # Topic 45-46: Cross-field validation
        credit_hours = cleaned_data.get('credit_hours')
        enrollment_fee = cleaned_data.get('enrollment_fee')
        
        # Topic 46: Raising ValidationError
        if credit_hours and credit_hours > 4:
            raise ValidationError("Credit hours cannot exceed 4")
        
        if enrollment_fee and enrollment_fee < 0:
            # Topic 59: Non-field error
            raise ValidationError("Enrollment fee cannot be negative")
        
        return cleaned_data

    def clean_code(self):
        """Topic 28: Field cleaning method"""
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper()
        return code

    def clean_instructor_email(self):
        """Topic 47: Unique validation"""
        email = self.cleaned_data.get('instructor_email')
        # Topic 48: Database lookup validation
        if email and Course.objects.filter(instructor_email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This instructor email is already in use")
        return email
```

**Topics Covered:**
- Topic 41: CSRF Protection in POST
- Topic 42: Form-Level Validation
- Topic 43: clean() Method in Forms
- Topic 44: ValidationError Exception
- Topic 45: Cross-Field Validation
- Topic 46: Raising ValidationError
- Topic 47: Unique Email Validation
- Topic 48: Database Lookup Validation
- Topic 49: Conditional Field Exclusion
- Topic 50: Form Save Method

#### 3. **Views** (Topics 41-80)
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CourseForm
from .models import Course

def course_add(request):
    """Topics 41-80: Add course with validation and messages"""
    
    # Topic 49: CSRF protection automatic
    if request.method == 'POST':
        # Topic 42: Form-level validation with clean()
        form = CourseForm(request.POST)
        
        if form.is_valid():
            # Topic 52: Save without commit
            course = form.save(commit=False)
            
            # Topic 53: Modify data before save
            # (optional processing)
            
            course.save()
            
            # Topic 75: Success message
            messages.success(request, f"Course {course.code} created successfully!")
            
            # Topic 73: Redirect after success
            return redirect('students:add')
    else:
        # Topic 50: Fresh form instance
        form = CourseForm()
    
    # Topic 67: Pass form to template context
    return render(request, 'students/form.html', {'form': form})


def course_edit(request, course_id):
    """Topics 78-80: Edit with pre-filled data"""
    
    # Get course instance
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        # Topic 79: Instance in form constructor for pre-filling
        form = CourseForm(request.POST, instance=course)
        
        if form.is_valid():
            # Topic 52: Save form
            form.save()
            
            # Topic 75: Success message
            messages.success(request, f"Course {course.code} updated successfully!")
            
            # Topic 73: Redirect after success
            return redirect('students:edit', course.id)
    else:
        # Topic 79: Pre-fill form with instance data
        form = CourseForm(instance=course)
    
    # Topic 68: Context variables
    return render(request, 'students/form.html', {
        'form': form,
        'course': course,
        'is_edit': True
    })
```

**Topics Covered:**
- Topics 41-60: Validation and form handling
- Topic 72: {% url %} tag for navigation
- Topic 73: Redirect after success
- Topic 74: messages Framework setup
- Topic 75: messages.success() function
- Topic 76: messages.error() function
- Topic 78: Form edit pattern
- Topic 79: Instance in form constructor
- Topic 80: Update vs Add operations

#### 4. **Template** (Topics 41-80)
```html
{% extends 'base.html' %}

{% block title %}{% if is_edit %}Edit{% else %}Add{% endif %} Course{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <h1>{% if is_edit %}Edit{% else %}Add{% endif %} Course</h1>
        
        <!-- Topic 77: Display messages -->
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        <form method="post">
            <!-- Topic 49: CSRF token -->
            {% csrf_token %}
            
            {% for field in form %}
                <div class="mb-3">
                    <!-- Topic 56: Label rendering -->
                    {{ field.label_tag }}
                    
                    <!-- Topic 55: Field rendering -->
                    {{ field }}
                    
                    <!-- Topic 58, 64: Error display with styling -->
                    {% if field.errors %}
                        <div class="invalid-feedback d-block">
                            {{ field.errors }}
                        </div>
                    {% endif %}
                </div>
            {% endfor %}
            
            <!-- Topic 59: Non-field errors -->
            {% if form.non_field_errors %}
                <div class="alert alert-danger">
                    {{ form.non_field_errors }}
                </div>
            {% endif %}
            
            <!-- Topic 78: Form action buttons -->
            <button type="submit" class="btn btn-primary">
                {% if is_edit %}Update{% else %}Create{% endif %} Course
            </button>
            <a href="{% url 'students:list' %}" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</div>
{% endblock %}
```

**Topics Covered:**
- Topic 54: Form HTML generation
- Topic 55: {{ form.field }} rendering
- Topic 56: {{ form.field.label }} rendering
- Topic 57: {{ form.field.errors }} rendering
- Topic 58: Field error display
- Topic 59: Non-field errors display
- Topic 60: Bootstrap integration
- Topic 61: form-control classes
- Topic 62: Feedback classes
- Topic 63: Alert component
- Topic 64: Error styling
- Topic 65: Success styling
- Topic 66: Context dictionary
- Topic 68: Context variables
- Topic 69-70: URL routing and names
- Topic 77: Message display

### Test Structure: 40+ tests organized by topic

**Test Classes:**
- AdvancedValidationTestCase (10 tests): Topics 41-50 (validation, clean, save)
- FormSavingTestCase (10 tests): Topics 51-60 (save with commit, rendering)
- StylingFeedbackTestCase (10 tests): Topics 61-70 (Bootstrap, context, routing)
- RoutingMessagesTestCase (10 tests): Topics 71-80 (redirect, messages, patterns)

---

## Key Learning Objectives

### Episode 21 A1: Form Fundamentals
1. Understanding ModelForm and automatic field generation
2. Widget system and customization
3. Field types and their widgets
4. Basic form validation
5. GET/POST request handling
6. CSRF token security
7. Template form rendering

### Episode 21 A2: Advanced Forms
1. All A1 concepts retained
2. Form-level validation with clean()
3. Field-level custom validation
4. Cross-field validation
5. ValidationError exception handling
6. Database lookup validation
7. Form save with commit parameter
8. Messages framework for user feedback
9. Edit pattern with instance pre-filling
10. Bootstrap form styling and error display

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
├── students/
│   ├── models.py (TODO - Student model)
│   ├── forms.py (TODO - StudentForm)
│   ├── views.py (TODO - student_form view)
│   ├── urls.py (TODO - 1 URL pattern)
│   ├── admin.py (TODO)
│   ├── tests.py (40+ test stubs)
│   └── __init__.py
└── templates/
    ├── base.html
    └── students/
        └── form.html (TODO)
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
├── students/
│   ├── models.py (TODO - Course model)
│   ├── forms.py (TODO - CourseForm with validation)
│   ├── views.py (TODO - course_add and course_edit)
│   ├── urls.py (TODO - 2 URL patterns)
│   ├── admin.py (TODO)
│   ├── tests.py (40+ test stubs)
│   └── __init__.py
└── templates/
    ├── base.html (with messages)
    └── students/
        └── form.html (TODO)
```

---

## Implementation Patterns

### ModelForm Creation
```python
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['field1', 'field2', 'field3']
        # Topics 1-3, 5
```

### Custom Validation
```python
def clean_email(self):
    """Topic 29: Field-level validation"""
    email = self.cleaned_data.get('email')
    # Custom validation logic
    return email

def clean(self):
    """Topic 43: Form-level validation"""
    cleaned_data = super().clean()
    field1 = cleaned_data.get('field1')
    field2 = cleaned_data.get('field2')
    
    if field1 and field2 and field1 > field2:
        raise ValidationError("Field1 must be less than Field2")
    
    return cleaned_data
```

### GET/POST Handling
```python
def my_view(request):
    """Topics 31-40: Form submission"""
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Success!")
            return redirect('app:view')
    else:
        form = MyForm()
    
    return render(request, 'template.html', {'form': form})
```

### Bootstrap Form Styling
```html
{% for field in form %}
    <div class="mb-3">
        {{ field.label_tag }}
        {{ field }}
        {% if field.errors %}
            <div class="invalid-feedback d-block">
                {{ field.errors }}
            </div>
        {% endif %}
    </div>
{% endfor %}
```

---

## Success Criteria

### Assignment 1: All 40+ tests pass ✓
- Form fields auto-generated correctly
- Widgets configured properly
- GET request displays blank form
- POST request validates and saves
- CSRF token present in template
- Messages displayed on success

### Assignment 2: All 40+ tests pass ✓
- Form-level validation working
- Custom clean methods executing
- ValidationError raised correctly
- Bootstrap styling applied
- Messages framework displaying
- Edit pattern pre-filling form
- Database validation working

---

## Debugging Tips

1. **Form not validating**: Check form.errors and form.cleaned_data
2. **CSRF token missing**: Ensure {% csrf_token %} in form template
3. **Validation not running**: Check clean() method indentation and super() call
4. **Messages not showing**: Verify messages middleware in settings
5. **Form fields wrong**: Check fields list in Meta class
6. **Widget not rendering**: Check widget type and attributes
7. **Save failing**: Check form.save(commit=False) for pre-save modifications

---

## Resources

- ModelForm Documentation: https://docs.djangoproject.com/en/5.1/topics/forms/modelforms/
- Form Validation: https://docs.djangoproject.com/en/5.1/ref/forms/validation/
- Built-in Field Types: https://docs.djangoproject.com/en/5.1/ref/forms/fields/
- Built-in Widgets: https://docs.djangoproject.com/en/5.1/ref/forms/widgets/
- Messages Framework: https://docs.djangoproject.com/en/5.1/contrib/messages/
- CSRF Protection: https://docs.djangoproject.com/en/5.1/middleware/csrf/
