# Episode 17: Django Apps, Models, Migrations, Views, and Templates
## Complete Learning Guide

---

## Episode Overview

Episode 17 introduces the core of Django development: **database-backed web applications**. Students will move from hardcoded HTTP responses to dynamic data handling using Django's powerful ORM (Object-Relational Mapping).

### What's Covered

- Creating reusable Django applications
- Defining database models using ORM
- Managing schema with migrations
- Writing views that fetch and filter data
- Building templates to display database records
- Handling model relationships

### Learning Path

**From Episode 16 → Episode 17:**
- Episode 16: Basic views returning hardcoded HTML
- Episode 17: Views fetching data from database and rendering templates
- Episode 18: User input handling with forms

---

## Assignment 1: Basic Student Database

### Difficulty Level: Beginner

**Focus:** Single model, basic CRUD operations, simple queries

### What Students Learn

1. Define a single Student model with basic fields
2. Run migrations to create database tables
3. Query data using simple `Student.objects.all()` and `get()`
4. Display data in templates with loops and conditionals
5. Create links between pages using URL reversal

### Key Topics Covered

- CharField, IntegerField, BooleanField, DateTimeField
- Model `__str__()` and Meta class
- makemigrations and migrate commands
- Template variables, for loops, if conditions
- URL parameters and reverse lookups

### Deliverables

- Student model with: name, roll_no, email, fees_paid, created_at
- Views: student_list, student_detail
- Templates: list.html (table of students), detail.html (single student info)
- 22 comprehensive tests

### Time Estimate: 2-3 hours

---

## Assignment 2: Advanced Course Management System

### Difficulty Level: Advanced

**Focus:** Model relationships, complex queries, nested templates

### What Students Learn

1. Create multiple related models (Student, Course, Enrollment)
2. Implement ForeignKey and ManyToMany relationships
3. Use through models to store extra data in relationships
4. Access related objects and reverse relationships
5. Build complex templates that traverse relationships
6. Filter and order querysets efficiently

### Key Topics Covered

- ForeignKey relationships (one-to-many)
- ManyToMany relationships
- Through models for intermediate data
- Reverse relationships (e.g., enrollment_set)
- QuerySet filtering, ordering, counting
- Nested template loops with related objects
- Template filters (default, date formatting)

### Deliverables

- Student model (name, roll_no, email)
- Course model (title, code, credits, students ManyToMany)
- Enrollment model (student FK, course FK, grade, date)
- Views: student_list, course_list, course_detail, student_detail, enrollment_list
- Templates: 5 templates displaying relationships
- 30 comprehensive tests

### Time Estimate: 4-5 hours

---

## Core Django Concepts

### 1. Django Models

**Purpose:** Define database structure using Python classes

```python
from django.db import models

class Student(models.Model):
    # Fields map to database columns
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField(unique=True)
    email = models.CharField(max_length=100)
    fees_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # String representation
    def __str__(self):
        return f"{self.name} ({self.roll_no})"
    
    # Metadata options
    class Meta:
        ordering = ['roll_no']
        verbose_name = "Student"
        verbose_name_plural = "Students"
```

**Field Types:**
- `CharField` - Text (max_length required)
- `IntegerField` - Whole numbers
- `BooleanField` - True/False
- `DateTimeField` - Date and time
- `ForeignKey` - One-to-many relationship
- `ManyToManyField` - Many-to-many relationship
- `DateField` - Date only
- `TextField` - Long text
- `EmailField` - Email validation
- `URLField` - URL validation

**Field Options:**
- `max_length` - Maximum characters (CharField required)
- `unique=True` - Must be unique in database
- `null=True` - Can be empty in database
- `blank=True` - Can be left blank in forms
- `default=value` - Default value
- `auto_now_add=True` - Set to current time on creation
- `auto_now=True` - Update to current time on save
- `choices=[]` - Restrict to predefined values

### 2. Migrations System

**Purpose:** Version control for database schema

```bash
# Step 1: Define model
# Edit models.py

# Step 2: Create migration file
python manage.py makemigrations
# Generates: students/migrations/0001_initial.py

# Step 3: Apply migration to database
python manage.py migrate
# Creates table in db.sqlite3

# View migration status
python manage.py showmigrations

# View migration details
cat students/migrations/0001_initial.py
```

**Migration Workflow:**
1. Change model definition
2. Run `makemigrations` (creates .py file)
3. Review migration file
4. Run `migrate` (executes against database)
5. Commit migration files to version control

### 3. ORM QuerySets

**Purpose:** Query database without writing SQL

```python
# Get all records
students = Student.objects.all()

# Get single record
student = Student.objects.get(id=1)

# Filter records
paid_students = Student.objects.filter(fees_paid=True)
python_students = Course.objects.filter(code='PY101')

# Exclude records
unpaid = Student.objects.exclude(fees_paid=True)

# Order results
ordered = Student.objects.all().order_by('roll_no')
reversed_order = Student.objects.all().order_by('-created_at')

# Count records
count = Student.objects.count()
paid_count = Student.objects.filter(fees_paid=True).count()

# Check existence
exists = Student.objects.filter(roll_no=1).exists()

# Chain operations
result = Student.objects.filter(fees_paid=True).order_by('roll_no').count()
```

### 4. Views with Database

**Purpose:** Fetch data and render templates

```python
from django.shortcuts import render
from .models import Student

def student_list(request):
    # Fetch data from database
    students = Student.objects.all()
    
    # Pass to template in context
    context = {'students': students}
    
    # Render template with context
    return render(request, 'students/list.html', context)

def student_detail(request, student_id):
    # Get single record
    student = Student.objects.get(id=student_id)
    
    context = {'student': student}
    return render(request, 'students/detail.html', context)
```

### 5. Django Templates

**Purpose:** Display data in HTML

```django
{# Variables #}
{{ student.name }}
{{ student.roll_no }}

{# Filters #}
{{ value|upper }}
{{ value|default:"N/A" }}
{{ date|date:"d-m-Y" }}

{# Loops #}
{% for student in students %}
    <p>{{ student.name }}</p>
{% endfor %}

{# Conditionals #}
{% if student.fees_paid %}
    <span>Paid</span>
{% else %}
    <span>Pending</span>
{% endif %}

{# URL reversal #}
<a href="{% url 'student_detail' student.id %}">View</a>
```

### 6. Model Relationships

**ForeignKey (One-to-Many):**
```python
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

# Access from enrollment
enrollment.student.name
enrollment.course.title

# Reverse access
student.enrollment_set.all()  # All enrollments for student
course.enrollment_set.all()   # All enrollments for course
```

**ManyToMany:**
```python
class Course(models.Model):
    students = models.ManyToManyField(Student)

# Access
course.students.all()      # All students in course
student.course_set.all()   # All courses for student
```

**Through Model:**
```python
class Course(models.Model):
    students = models.ManyToManyField(Student, through='Enrollment')

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1)  # Extra data

# Access through model
enrollment.student, enrollment.course, enrollment.grade
```

---

## Assignment Structure

### File Organization

```
episode17/
├── assignment1/                          # Basic Student Model
│   ├── students/
│   │   ├── models.py                    (TODO: Write Student model)
│   │   ├── models_solution.py           (Reference)
│   │   ├── views.py                     (TODO: Write views)
│   │   ├── views_solution.py            (Reference)
│   │   ├── templates/students/
│   │   │   ├── list.html                (TODO: Write template)
│   │   │   ├── list_solution.html       (Reference)
│   │   │   ├── detail.html              (TODO: Write template)
│   │   │   └── detail_solution.html     (Reference)
│   │   └── migrations/
│   ├── myproject/
│   │   ├── settings.py                  (Ready - students app installed)
│   │   └── urls.py                      (Ready - routes configured)
│   ├── manage.py
│   ├── db.sqlite3                       (Auto-created)
│   ├── requirements.txt                 (Django==5.0)
│   ├── test_assignment.py               (22 tests)
│   ├── README.md                        (Learning guide)
│   └── venv/                            (Virtual environment)
│
└── assignment2/                         # Advanced Course Management
    ├── courses/
    │   ├── models.py                    (TODO: 3 models with relationships)
    │   ├── models_solution.py           (Reference)
    │   ├── views.py                     (TODO: 5 views)
    │   ├── views_solution.py            (Reference)
    │   ├── templates/courses/
    │   │   ├── student_list.html        (TODO)
    │   │   ├── student_list_solution.html
    │   │   ├── course_list.html         (TODO)
    │   │   ├── course_list_solution.html
    │   │   ├── course_detail.html       (TODO)
    │   │   ├── course_detail_solution.html
    │   │   ├── student_detail.html      (TODO)
    │   │   ├── student_detail_solution.html
    │   │   ├── enrollment_list.html     (TODO)
    │   │   └── enrollment_list_solution.html
    │   └── migrations/
    ├── myproject/
    │   ├── settings.py                  (Ready)
    │   └── urls.py                      (Ready)
    ├── manage.py
    ├── db.sqlite3                       (Auto-created)
    ├── requirements.txt                 (Django==5.0)
    ├── test_assignment.py               (30 tests)
    ├── README.md                        (Learning guide)
    └── venv/                            (Virtual environment)
```

---

## Learning Progression

### Phase 1: Models & Migrations (Assignment 1)
1. Define Student model
2. Run migrations
3. Understand table creation
4. Query basics with .all() and .get()

### Phase 2: Views & Templates (Assignment 1)
1. Fetch data in views
2. Pass to templates via context
3. Display in templates
4. Create links between pages

### Phase 3: Relationships (Assignment 2)
1. Create multiple models
2. Define ForeignKey relationships
3. Use through models
4. Access related objects

### Phase 4: Complex Queries (Assignment 2)
1. Filter by related fields
2. Order by multiple fields
3. Count related objects
4. Combine filter operations

### Phase 5: Complex Templates (Assignment 2)
1. Nested loops through relationships
2. Access nested object properties
3. Use template filters
4. Conditional display of related data

---

## Debugging Guide

### Problem: "No such table: students_student"
**Cause:** Migrations not applied
```bash
python manage.py migrate
```

### Problem: "TemplateDoesNotExist: students/list.html"
**Cause:** Template file not found or wrong path
- Check: `students/templates/students/list.html`
- Verify: TEMPLATES configuration in settings.py

### Problem: "AttributeError: 'QuerySet' object has no attribute 'name'"
**Cause:** Trying to access single object properties on QuerySet
```python
# Wrong
students.name  # QuerySet has no 'name'

# Right
for student in students:
    print(student.name)
```

### Problem: "Student matching query does not exist"
**Cause:** Trying to get() non-existent record
```python
# Handle with try/except
try:
    student = Student.objects.get(id=9999)
except Student.DoesNotExist:
    # Handle error
```

### Problem: "RelatedObjectDoesNotExist"
**Cause:** Accessing related object that doesn't exist
```python
# Use .all() to get QuerySet (always works)
enrollments = student.enrollment_set.all()

# Use .first() safely
first_enrollment = student.enrollment_set.first()
```

---

## Comparison: Episode 16 vs Episode 17

| Aspect | Episode 16 | Episode 17 |
|--------|-----------|-----------|
| **Data** | Hardcoded in view | In database |
| **Storage** | Each request fresh | Persists across requests |
| **Queries** | N/A | Using ORM QuerySets |
| **Scalability** | Limited | Unlimited records |
| **Schema** | Implicit | Explicit with migrations |
| **Relationships** | Not possible | ForeignKey, ManyToMany |
| **Templates** | Show static data | Show dynamic data |
| **Complexity** | Simple | More involved |
| **Real-world use** | Prototypes | Production apps |

---

## Next Steps (Episode 18)

Episode 18 will cover:
1. **Forms** - User input validation
2. **CRUD Operations** - Create, read, update, delete with forms
3. **Form Validation** - Built-in and custom validation
4. **Model Forms** - Auto-generate forms from models
5. **POST Requests** - Handling form submissions
6. **Redirects** - After successful form submission

---

## Reference Materials

### Django ORM Documentation Patterns

```python
# Creating
Student.objects.create(name="John", roll_no=1, email="john@example.com")

# Reading
all_students = Student.objects.all()
one_student = Student.objects.get(id=1)
filtered = Student.objects.filter(fees_paid=True)

# Updating
student = Student.objects.get(id=1)
student.fees_paid = True
student.save()

# Deleting
Student.objects.get(id=1).delete()
Student.objects.filter(fees_paid=False).delete()

# Querying relationships
course.students.all()
student.enrollment_set.all()
enrollment.student, enrollment.course
```

### Template Patterns

```django
{# Single variable #}
{{ student.name }}

{# Related objects #}
{{ enrollment.student.name }}
{{ enrollment.course.title }}

{# Loops #}
{% for student in students %}
    {{ student.name }}
{% endfor %}

{# Nested loops #}
{% for course in courses %}
    {% for enrollment in course.enrollment_set.all %}
        {{ enrollment.student.name }}
    {% endfor %}
{% endfor %}

{# Conditionals #}
{% if enrollments %}
    {% for enrollment in enrollments %}
        ...
    {% endfor %}
{% else %}
    No enrollments
{% endif %}

{# Filters #}
{{ student.created_at|date:"d-m-Y" }}
{{ status|default:"Pending" }}
{{ text|upper }}
```

---

## Success Criteria

### Assignment 1 (Basic)
- [ ] Student model has all required fields
- [ ] Migrations create students table
- [ ] student_list view displays all students
- [ ] student_detail view shows individual student
- [ ] Templates display data correctly
- [ ] Links navigate between pages
- [ ] All 22 tests pass

### Assignment 2 (Advanced)
- [ ] Three models with correct relationships
- [ ] Migrations create all tables correctly
- [ ] 5 views handle all pages
- [ ] ManyToMany relationship works
- [ ] Reverse relationships accessible
- [ ] Templates display related data
- [ ] Nested loops work correctly
- [ ] All 30 tests pass

---

## Vocabulary

| Term | Definition |
|------|-----------|
| **Model** | Python class representing database table |
| **ORM** | Object-Relational Mapping - use Python objects for database |
| **Migration** | Version-controlled database schema change |
| **QuerySet** | Lazy database query object with filtering/ordering |
| **ForeignKey** | One-to-many relationship between models |
| **ManyToMany** | Many-to-many relationship with through model |
| **Context** | Dictionary passed from view to template |
| **Template** | HTML file with Django template language |
| **Field** | Model attribute representing database column |
| **Reverse Relationship** | Access related objects from opposite side (e.g., student.enrollment_set) |

---

**Episode 17 Complete!** 🎉

Ready to move to Episode 18: Forms and CRUD Operations

Created: February 17, 2026
