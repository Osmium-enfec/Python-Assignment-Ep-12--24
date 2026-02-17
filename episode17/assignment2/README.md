# Episode 17 - Assignment 2: Django Models with Relationships, Advanced Views, and Templates

## Learning Objectives

After completing this assignment, you should understand:

1. **Model Relationships** - ForeignKey and ManyToMany relationships between models
2. **Through Models** - Using intermediate model (Enrollment) for ManyToMany with extra data
3. **Reverse Relationships** - Accessing related objects from both sides
4. **Advanced QuerySets** - Filtering, ordering, and accessing related data
5. **Complex Templates** - Nested loops with related objects
6. **Template Filters** - Formatting data like dates with filters
7. **Database Integrity** - Constraints like unique_together

## What You'll Build

A complete course management system with:
- **Student** model: name, roll_no, email
- **Course** model: title, code, credits, students (ManyToMany)
- **Enrollment** model: student, course, grade (intermediate model)
- Views to display students, courses, and enrollments
- Templates showing relationships and filtered data

## Files Overview

### Key Files to Edit

```
assignment2/
├── courses/
│   ├── models.py                    ← TODO 1-3: Create models with relationships
│   ├── models_solution.py           (Reference solution)
│   ├── views.py                     ← TODO 4-8: Create views
│   ├── views_solution.py            (Reference solution)
│   └── templates/courses/
│       ├── student_list.html        ← TODO 9: Display students
│       ├── course_list.html         ← TODO 10: Display courses
│       ├── course_detail.html       ← TODO 11: Show course with students
│       ├── student_detail.html      ← TODO 12: Show student with courses
│       ├── enrollment_list.html     ← TODO 13: Show all enrollments
│       └── *_solution.html          (Reference templates)
├── myproject/
│   ├── settings.py                  (Already configured)
│   └── urls.py                      (Already configured)
└── test_assignment.py               (Test your implementation)
```

## Step-by-Step Instructions

### Step 1: Define Models with Relationships

Edit `courses/models.py`:

#### TODO 1: Student Model
```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField(unique=True)
    email = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.roll_no})"
    
    class Meta:
        ordering = ['roll_no']
```

#### TODO 2: Course Model with ManyToMany
```python
class Course(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credits = models.IntegerField()
    # ManyToMany through Enrollment model
    students = models.ManyToManyField(Student, through='Enrollment')
    
    def __str__(self):
        return f"{self.code}: {self.title}"
    
    class Meta:
        ordering = ['code']
```

#### TODO 3: Enrollment Model (Through Model)
```python
class Enrollment(models.Model):
    GRADES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GRADES)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.course.code}"
    
    class Meta:
        ordering = ['-enrollment_date']
        unique_together = ('student', 'course')
```

**Key Concepts:**
- **ForeignKey** - One-to-many relationship (many enrollments to one student/course)
- **ManyToManyField** - Many-to-many through intermediate model
- **through='Enrollment'** - Use Enrollment as the join table
- **on_delete=models.CASCADE** - Delete enrollments when student/course deleted
- **unique_together** - Prevent duplicate student-course pairs
- **choices** - Restrict field values to predefined options

### Step 2: Run Migrations

```bash
source venv/bin/activate

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Step 3: Create Views for All Pages

Edit `courses/views.py`:

```python
# TODO 4: student_list - Show all students
def student_list(request):
    students = Student.objects.all().order_by('roll_no')
    context = {'students': students}
    return render(request, 'courses/student_list.html', context)

# TODO 5: course_list - Show all courses
def course_list(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses/course_list.html', context)

# TODO 6: course_detail - Show course with enrolled students
def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    enrollments = course.enrollment_set.all()  # Reverse relationship
    context = {'course': course, 'enrollments': enrollments}
    return render(request, 'courses/course_detail.html', context)

# TODO 7: student_detail - Show student with enrolled courses
def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    enrollments = student.enrollment_set.all()  # Reverse relationship
    context = {'student': student, 'enrollments': enrollments}
    return render(request, 'courses/student_detail.html', context)

# TODO 8: enrollment_list - Show all enrollments ordered by date
def enrollment_list(request):
    enrollments = Enrollment.objects.all().order_by('-enrollment_date')
    context = {'enrollments': enrollments}
    return render(request, 'courses/enrollment_list.html', context)
```

**Key Concepts:**
- `course.enrollment_set.all()` - Access enrollments from course (reverse FK)
- `student.enrollment_set.all()` - Access enrollments from student (reverse FK)
- `enrollments` has access to both student and course objects

### Step 4: Create Templates

#### TODO 9: Student List Template
```django
<table>
    <tr>
        <th>Roll No</th>
        <th>Name</th>
        <th>Email</th>
        <th>Action</th>
    </tr>
    {% for student in students %}
    <tr>
        <td>{{ student.roll_no }}</td>
        <td>{{ student.name }}</td>
        <td>{{ student.email }}</td>
        <td><a href="{% url 'student_detail' student.id %}">View</a></td>
    </tr>
    {% endfor %}
</table>
```

#### TODO 10: Course List Template
```django
<table>
    <tr>
        <th>Code</th>
        <th>Title</th>
        <th>Credits</th>
        <th>Students</th>
        <th>Action</th>
    </tr>
    {% for course in courses %}
    <tr>
        <td>{{ course.code }}</td>
        <td>{{ course.title }}</td>
        <td>{{ course.credits }}</td>
        <td>{{ course.students.count }}</td>
        <td><a href="{% url 'course_detail' course.id %}">View</a></td>
    </tr>
    {% endfor %}
</table>
```

#### TODO 11: Course Detail with Enrolled Students
```django
<h2>{{ course.code }}: {{ course.title }}</h2>
<p><strong>Credits:</strong> {{ course.credits }}</p>

<table>
    <tr>
        <th>Student</th>
        <th>Roll No</th>
        <th>Grade</th>
    </tr>
    {% for enrollment in enrollments %}
    <tr>
        <td>{{ enrollment.student.name }}</td>
        <td>{{ enrollment.student.roll_no }}</td>
        <td>{{ enrollment.grade|default:"Pending" }}</td>
    </tr>
    {% endfor %}
</table>
```

#### TODO 12: Student Detail with Enrolled Courses
```django
<h2>{{ student.name }}</h2>
<p><strong>Roll No:</strong> {{ student.roll_no }}</p>
<p><strong>Email:</strong> {{ student.email }}</p>

<table>
    <tr>
        <th>Code</th>
        <th>Title</th>
        <th>Grade</th>
    </tr>
    {% for enrollment in enrollments %}
    <tr>
        <td>{{ enrollment.course.code }}</td>
        <td>{{ enrollment.course.title }}</td>
        <td>{{ enrollment.grade|default:"Pending" }}</td>
    </tr>
    {% endfor %}
</table>
```

#### TODO 13: Enrollment List Template
```django
<table>
    <tr>
        <th>Student</th>
        <th>Course</th>
        <th>Grade</th>
        <th>Date</th>
    </tr>
    {% for enrollment in enrollments %}
    <tr>
        <td>{{ enrollment.student.name }}</td>
        <td>{{ enrollment.course.code }}: {{ enrollment.course.title }}</td>
        <td>{{ enrollment.grade|default:"Pending" }}</td>
        <td>{{ enrollment.enrollment_date|date:"d-m-Y H:i" }}</td>
    </tr>
    {% endfor %}
</table>
```

**Key Concepts:**
- Access related objects: `enrollment.student.name`, `enrollment.course.code`
- Count related objects: `course.students.count`
- Use filters for formatting: `{{ value|default:"N/A" }}`, `{{ date|date:"d-m-Y" }}`

## Running the Assignment

### 1. Activate Virtual Environment

```bash
cd assignment2
source venv/bin/activate
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Sample Data

```bash
python manage.py shell
```

```python
from courses.models import Student, Course, Enrollment

# Create students
s1 = Student.objects.create(name="Raj Kumar", roll_no=1, email="raj@example.com")
s2 = Student.objects.create(name="Priya Singh", roll_no=2, email="priya@example.com")

# Create courses
c1 = Course.objects.create(title="Python Basics", code="PY101", credits=3)
c2 = Course.objects.create(title="Web Development", code="WEB201", credits=4)

# Create enrollments
Enrollment.objects.create(student=s1, course=c1, grade='A')
Enrollment.objects.create(student=s1, course=c2, grade='B')
Enrollment.objects.create(student=s2, course=c1, grade='A')

exit()
```

### 4. Run Tests

```bash
python test_assignment.py
```

### 5. Start Development Server

```bash
python manage.py runserver
```

### 6. Test in Browser

- Students: http://localhost:8000/students/
- Courses: http://localhost:8000/courses/
- Course Detail: http://localhost:8000/courses/1/
- Student Detail: http://localhost:8000/students/1/
- Enrollments: http://localhost:8000/enrollments/

## Key Concepts

### Model Relationships

**ForeignKey (One-to-Many):**
```python
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

# Access: enrollment.student, enrollment.course
# Reverse: student.enrollment_set.all(), course.enrollment_set.all()
```

**ManyToMany:**
```python
class Course(models.Model):
    students = models.ManyToManyField(Student, through='Enrollment')

# Access: course.students.all(), student.course_set.all()
```

**Through Model:**
```python
# Store extra data in the relationship
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1)  # Extra data
```

### QuerySet Operations

```python
# Filter
Student.objects.filter(roll_no=1)
Enrollment.objects.filter(grade='A')

# Ordering
Student.objects.all().order_by('roll_no')
Enrollment.objects.all().order_by('-enrollment_date')

# Count
course.students.count()
Course.objects.filter(credits=3).count()

# Accessing related objects
enrollment.student.name  # Through FK
enrollment.course.title
```

### Templates with Related Objects

```django
{% for enrollment in enrollments %}
    Student: {{ enrollment.student.name }}
    Course: {{ enrollment.course.code }}
    Grade: {{ enrollment.grade|default:"Pending" }}
    Date: {{ enrollment.enrollment_date|date:"d-m-Y" }}
{% endfor %}
```

## Test Cases (30 total)

The test suite covers:

1. **Model Tests (7 tests)**
   - Student, Course, Enrollment creation
   - Unique constraints
   - String representations
   - Many-to-many through relationship

2. **View Tests (8 tests)**
   - All views return 200 status
   - Correct templates used
   - Context variables present

3. **Integration Tests (6 tests)**
   - Navigation between pages
   - Counting students/courses
   - Queryset filtering and ordering
   - Related object access

4. **Advanced Tests (9 tests)**
   - Many-to-many relationships
   - Reverse relationships
   - Complex filtering
   - Date ordering

## Reference Solutions

When stuck, check:
- `courses/models_solution.py` - Complete models with relationships
- `courses/views_solution.py` - Complete views
- `courses/templates/courses/*_solution.html` - Complete templates

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `django.db.utils.OperationalError: no such table` | Migrations not applied | Run `python manage.py migrate` |
| `AttributeError: 'QuerySet' has no attribute 'student'` | Forgetting loop in template | Use `{% for enrollment in enrollments %}` |
| `RelatedObjectDoesNotExist` | Trying to access non-existent relationship | Use `.all()` or check existence |
| `Duplicate entry for unique_together` | Enrolling same student in same course twice | Check model constraint |
| `Reverse query: enrollment.student_set` wrong | Using wrong reverse name | Use `enrollment_set` or check related_name |

## Next Steps

1. Add Django admin interface for easy data management
2. Create forms for creating enrollments
3. Add filtering/searching by student name or course code
4. Calculate GPA from grades
5. Generate transcripts with course history

---

**Happy Learning!** 🎓

Created: February 17, 2026
Status: Ready for Student Implementation
