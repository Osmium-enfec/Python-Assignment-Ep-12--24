# Episode 17 - Assignment 1: Django Models, Migrations, and Basic Views

## Learning Objectives

After completing this assignment, you should understand:

1. **Django Apps** - Creating and configuring reusable Django applications
2. **Models** - Defining database tables using Django ORM
3. **Migrations** - Version controlling database schema changes
4. **Views** - Fetching data from database and passing to templates
5. **Templates** - Rendering database records using Django template language
6. **QuerySets** - Basic database queries using `Student.objects.all()`

## What You'll Build

A simple student management system with:
- Student model with fields: name, roll_no, email, fees_paid, created_at
- Display all students in a list view
- Display individual student details
- Use Django templates to render HTML

## Files Overview

### Key Files to Edit

```
assignment1/
├── students/
│   ├── models.py                    ← TODO 1: Create Student model
│   ├── models_solution.py           (Reference solution)
│   ├── views.py                     ← TODO 2-3: Create views
│   ├── views_solution.py            (Reference solution)
│   └── templates/students/
│       ├── list.html                ← TODO 4: Display student list
│       ├── list_solution.html       (Reference template)
│       ├── detail.html              ← TODO 5: Display student details
│       └── detail_solution.html     (Reference template)
├── myproject/
│   ├── settings.py                  (Already configured)
│   └── urls.py                      (Already configured)
└── test_assignment.py               (Test your implementation)
```

## Step-by-Step Instructions

### Step 1: Define the Student Model

Edit `students/models.py`:

```python
# TODO 1: Create a Student model with:
# - name: CharField, max_length=100
# - roll_no: IntegerField, unique=True
# - email: CharField, max_length=100
# - fees_paid: BooleanField, default=False
# - created_at: DateTimeField, auto_now_add=True
# 
# Add __str__() method
# Add Meta class with ordering by 'roll_no'
```

**Key Concepts:**
- `CharField` - Text field with max length
- `IntegerField` - Whole number field
- `BooleanField` - True/False field
- `DateTimeField` - Date and time with auto_now_add for timestamps
- `__str__()` - How model appears as text
- `Meta.ordering` - Default sort order

### Step 2: Create Migrations

After defining the model:

```bash
# Activate virtual environment
source venv/bin/activate

# Create migration file
python manage.py makemigrations

# Apply migration to database
python manage.py migrate
```

**What happens:**
1. `makemigrations` creates a migration file describing the schema
2. `migrate` creates the actual database table

### Step 3: Create Views

Edit `students/views.py`:

```python
# TODO 2: student_list view
# - Fetch all students: Student.objects.all()
# - Pass to template as context: {'students': students}
# - Render 'students/list.html'

# TODO 3: student_detail view
# - Take student_id parameter
# - Fetch student: Student.objects.get(id=student_id)
# - Pass to template: {'student': student}
# - Render 'students/detail.html'
```

**Key Concepts:**
- `render()` - Combines template + context + returns response
- `Student.objects.all()` - Fetch all records
- `Student.objects.get()` - Fetch single record
- Context dict - Variables available in template

### Step 4: Create Templates

Edit `students/templates/students/list.html`:

```django
<!-- TODO 4: Display student list -->
{% if students %}
<table>
    {% for student in students %}
    <tr>
        <td>{{ student.roll_no }}</td>
        <td>{{ student.name }}</td>
        <td>{{ student.email }}</td>
        <td>{% if student.fees_paid %}Yes{% else %}No{% endif %}</td>
        <td><a href="{% url 'student_detail' student.id %}">View</a></td>
    </tr>
    {% endfor %}
</table>
{% else %}
<p>No students found.</p>
{% endif %}
```

Edit `students/templates/students/detail.html`:

```django
<!-- TODO 5: Display student details -->
<div class="card">
    <p><strong>Name:</strong> {{ student.name }}</p>
    <p><strong>Roll No:</strong> {{ student.roll_no }}</p>
    <p><strong>Email:</strong> {{ student.email }}</p>
    <p><strong>Fees Paid:</strong> {% if student.fees_paid %}Yes{% else %}No{% endif %}</p>
    <p><strong>Created At:</strong> {{ student.created_at|date:"d-m-Y H:i" }}</p>
</div>
```

**Key Concepts:**
- `{{ variable }}` - Display variable value
- `{% for item in items %}` - Loop through list/queryset
- `{% if condition %}` - Conditional rendering
- `{{ value|filter }}` - Apply filter (date, upper, etc.)
- `{% url 'name' %}` - Generate URL dynamically

## Running the Assignment

### 1. Activate Virtual Environment

```bash
cd assignment1
source venv/bin/activate
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Run Tests

```bash
python test_assignment.py
```

Expected: Some tests may fail initially - this is expected! Tests guide what you need to implement.

### 4. Create Sample Data (Optional)

```bash
python manage.py shell
```

```python
from students.models import Student

# Create students
Student.objects.create(name="Raj Kumar", roll_no=1, email="raj@example.com", fees_paid=True)
Student.objects.create(name="Priya Singh", roll_no=2, email="priya@example.com", fees_paid=False)
Student.objects.create(name="Amit Patel", roll_no=3, email="amit@example.com", fees_paid=True)

# Exit
exit()
```

### 5. Start Development Server

```bash
python manage.py runserver
```

### 6. Test in Browser

- Student List: http://localhost:8000/students/
- Student Detail: http://localhost:8000/students/1/

## Debugging Tips

### Migration Issues

```bash
# Check migration status
python manage.py showmigrations

# Check migration content
cat students/migrations/0001_initial.py
```

### Query Issues

```bash
python manage.py shell

# Test queryset in Python shell
from students.models import Student
students = Student.objects.all()
print(students)

# Test single student
student = Student.objects.get(id=1)
print(student.name)
```

### Template Issues

- Check context variables in view
- Use `{{ student }}` to debug object
- Check file paths: templates/students/list.html

## Test Cases (22 total)

The test suite covers:

1. **Model Tests (7 tests)**
   - Student creation
   - __str__ method
   - Unique roll_no
   - Ordering
   - Default values
   - Timestamps

2. **List View Tests (5 tests)**
   - URL routing
   - Template usage
   - Context variables
   - Content rendering
   - Empty list handling

3. **Detail View Tests (6 tests)**
   - URL routing with parameter
   - Template usage
   - Context variables
   - Content rendering
   - 404 handling
   - Field display

4. **Integration Tests (4 tests)**
   - List to detail navigation
   - Count queries
   - Filter operations
   - Template filters

## Reference Solutions

When stuck, check:
- `students/models_solution.py` - Complete model
- `students/views_solution.py` - Complete views
- `students/templates/students/list_solution.html` - Complete list template
- `students/templates/students/detail_solution.html` - Complete detail template

## Key Django Concepts

### Models

```python
class Student(models.Model):
    name = models.CharField(max_length=100)      # Text field
    roll_no = models.IntegerField(unique=True)   # Number field, unique
    email = models.CharField(max_length=100)     # Email field
    fees_paid = models.BooleanField(default=False)  # True/False
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['roll_no']
```

### Views

```python
from django.shortcuts import render
from .models import Student

def student_list(request):
    students = Student.objects.all()  # Get all students
    context = {'students': students}
    return render(request, 'students/list.html', context)

def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)  # Get single student
    context = {'student': student}
    return render(request, 'students/detail.html', context)
```

### Templates

```django
{% for student in students %}
    <p>{{ student.name }} - Roll: {{ student.roll_no }}</p>
{% endfor %}

{% if student.fees_paid %}
    <span>Fees Paid</span>
{% else %}
    <span>Pending</span>
{% endif %}
```

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `No such table: students_student` | Migration not applied | Run `python manage.py migrate` |
| `TemplateDoesNotExist` | Template not found | Check path: templates/students/list.html |
| `ValueError: invalid literal for int()` | URL parameter type | Check URL pattern uses `<int:id>` |
| `Student matching query does not exist` | No student with that ID | Add 404 handling with try/except |

## Learning Progression

1. **Basic:** Create model, run migrations, test in shell
2. **Intermediate:** Create views, fetch data, render templates
3. **Advanced:** Handle edge cases, use filters, optimize queries
4. **Expert:** Add model methods, custom querysets, admin interface

## Next Steps

After completing this assignment:
1. Explore Django admin interface: `python manage.py createsuperuser`
2. Try adding more models (Teacher, Course)
3. Create relationships between models (ForeignKey)
4. Add forms for creating/updating students (Episode 18)

---

**Happy Learning!** 🎓

Created: February 17, 2026
Status: Ready for Student Implementation
