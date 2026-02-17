# Episode 17 - Complete Setup Summary

## ✅ Successfully Created

### Episode 17 Structure
```
episode17/
├── EPISODE_17_GUIDE.md                 ← Comprehensive learning guide
├── assignment1/                        ← Basic Student Database
│   ├── README.md                       ← Assignment 1 instructions
│   ├── test_assignment.py              ← 22 comprehensive tests
│   ├── requirements.txt                ← Django==5.0
│   ├── manage.py                       ← Django CLI
│   ├── myproject/                      ← Django project
│   │   ├── settings.py                 ✓ Configured with 'students' app
│   │   ├── urls.py                     ✓ Routes configured
│   │   └── ...
│   ├── students/                       ← Django app
│   │   ├── models.py                   📝 TODO: Student model
│   │   ├── models_solution.py          ✓ Complete solution
│   │   ├── views.py                    📝 TODO: student_list, student_detail views
│   │   ├── views_solution.py           ✓ Complete solution
│   │   ├── templates/students/
│   │   │   ├── list.html               📝 TODO: Display students
│   │   │   ├── list_solution.html      ✓ Complete solution
│   │   │   ├── detail.html             📝 TODO: Display student info
│   │   │   └── detail_solution.html    ✓ Complete solution
│   │   └── migrations/                 ← Auto-created by migrations
│   └── venv/                           ✓ Python 3.14 with Django 5.0
│
└── assignment2/                        ← Advanced Course Management
    ├── README.md                       ← Assignment 2 instructions
    ├── test_assignment.py              ← 30 comprehensive tests
    ├── requirements.txt                ← Django==5.0
    ├── manage.py                       ← Django CLI
    ├── myproject/                      ← Django project
    │   ├── settings.py                 ✓ Configured with 'courses' app
    │   ├── urls.py                     ✓ Routes configured
    │   └── ...
    ├── courses/                        ← Django app
    │   ├── models.py                   📝 TODO: Student, Course, Enrollment models
    │   ├── models_solution.py          ✓ Complete solution
    │   ├── views.py                    📝 TODO: 5 views
    │   ├── views_solution.py           ✓ Complete solution
    │   ├── templates/courses/
    │   │   ├── student_list.html       📝 TODO
    │   │   ├── student_list_solution.html ✓
    │   │   ├── course_list.html        📝 TODO
    │   │   ├── course_list_solution.html ✓
    │   │   ├── course_detail.html      📝 TODO
    │   │   ├── course_detail_solution.html ✓
    │   │   ├── student_detail.html     📝 TODO
    │   │   ├── student_detail_solution.html ✓
    │   │   ├── enrollment_list.html    📝 TODO
    │   │   └── enrollment_list_solution.html ✓
    │   └── migrations/                 ← Auto-created by migrations
    └── venv/                           ✓ Python 3.14 with Django 5.0
```

---

## 📚 Core Concepts Covered

### Assignment 1: Beginner
- **Single Model:** Student (name, roll_no, email, fees_paid, created_at)
- **Migrations:** Creating and applying schema changes
- **Queries:** .all(), .get() basic operations
- **Views:** Fetching data and passing to templates
- **Templates:** Loops, conditionals, URL reversal
- **Tests:** 22 comprehensive test cases

### Assignment 2: Advanced
- **Multiple Models:** Student, Course, Enrollment
- **Relationships:** ForeignKey (one-to-many), ManyToMany with through model
- **Queries:** Filtering, ordering, counting related objects
- **Views:** 5 views handling different pages
- **Templates:** Nested loops, accessing related objects, filters
- **Tests:** 30 comprehensive test cases (including relationship tests)

---

## 🎯 Quick Start

### Assignment 1

```bash
cd episode17/assignment1
source venv/bin/activate

# Step 1: Edit models.py - Define Student model
# Step 2: Run migrations
python manage.py makemigrations
python manage.py migrate

# Step 3: Edit views.py - Create views
# Step 4: Edit templates - Create HTML

# Step 5: Test
python test_assignment.py

# Step 6: Run server (optional)
python manage.py runserver
# Visit: http://localhost:8000/students/
```

### Assignment 2

```bash
cd episode17/assignment2
source venv/bin/activate

# Step 1: Edit models.py - Define 3 models with relationships
# Step 2: Run migrations
python manage.py makemigrations
python manage.py migrate

# Step 3: Edit views.py - Create 5 views
# Step 4: Edit templates - Create HTML for all pages

# Step 5: Test
python test_assignment.py

# Step 6: Run server (optional)
python manage.py runserver
```

---

## 📋 Checklist for Students

### Assignment 1 - Student Model

- [ ] Define `Student` model in `students/models.py`
  - [ ] CharField for name (max_length=100)
  - [ ] IntegerField for roll_no (unique=True)
  - [ ] CharField for email (max_length=100)
  - [ ] BooleanField for fees_paid (default=False)
  - [ ] DateTimeField for created_at (auto_now_add=True)
  - [ ] Add `__str__()` method
  - [ ] Add `Meta` class with ordering

- [ ] Run migrations
  - [ ] `python manage.py makemigrations`
  - [ ] `python manage.py migrate`

- [ ] Create `student_list` view in `students/views.py`
  - [ ] Fetch all students
  - [ ] Pass to template

- [ ] Create `student_detail` view in `students/views.py`
  - [ ] Take student_id parameter
  - [ ] Fetch single student
  - [ ] Pass to template

- [ ] Create `students/templates/students/list.html` template
  - [ ] Display table of students
  - [ ] Show: Roll No, Name, Email, Fees Paid
  - [ ] Add link to detail view

- [ ] Create `students/templates/students/detail.html` template
  - [ ] Show student details
  - [ ] Use date filter for created_at
  - [ ] Add link back to list

- [ ] Run tests: `python test_assignment.py`
  - [ ] All 22 tests pass

### Assignment 2 - Course Management System

- [ ] Define `Student` model (name, roll_no, email)
  - [ ] Add `__str__()` and Meta class

- [ ] Define `Course` model
  - [ ] CharField for title (max_length=100)
  - [ ] CharField for code (max_length=10, unique=True)
  - [ ] IntegerField for credits
  - [ ] ManyToManyField to Student through Enrollment
  - [ ] Add `__str__()` and Meta class

- [ ] Define `Enrollment` model
  - [ ] ForeignKey to Student (on_delete=models.CASCADE)
  - [ ] ForeignKey to Course (on_delete=models.CASCADE)
  - [ ] CharField for grade with choices
  - [ ] DateTimeField for enrollment_date (auto_now_add=True)
  - [ ] Add `__str__()` and Meta class

- [ ] Run migrations
  - [ ] `python manage.py makemigrations`
  - [ ] `python manage.py migrate`

- [ ] Create 5 views in `courses/views.py`
  - [ ] `student_list` - display all students
  - [ ] `course_list` - display all courses
  - [ ] `course_detail` - show course with enrolled students
  - [ ] `student_detail` - show student with enrolled courses
  - [ ] `enrollment_list` - show all enrollments

- [ ] Create templates in `courses/templates/courses/`
  - [ ] `student_list.html` - table of students
  - [ ] `course_list.html` - table of courses
  - [ ] `course_detail.html` - course info + students table
  - [ ] `student_detail.html` - student info + courses table
  - [ ] `enrollment_list.html` - enrollments with dates

- [ ] Run tests: `python test_assignment.py`
  - [ ] All 30 tests pass

---

## 🔗 Model Relationships in Assignment 2

```
Student (1) ──────────┐
                      │ (Through Enrollment)
                      ├──── Many-to-Many ──────┐
                      │                        │
                   Enrollment              Course (1)
                   (Intermediate)              │
                      │                        │
                (student FK)              (course FK)
                (course FK)
                (grade: Choice)
                (enrollment_date)
```

**Key Points:**
- Student can enroll in multiple courses
- Course can have multiple students
- Enrollment stores the grade and date
- Access via: `course.enrollment_set.all()` or `student.enrollment_set.all()`

---

## 📖 Reference Materials

### Inside Each Assignment

- **README.md** - Detailed learning guide with step-by-step instructions
- **\*_solution.py files** - Complete working solutions
- **\*_solution.html files** - Complete working templates
- **test_assignment.py** - 22 or 30 tests covering all functionality

### Episode 17 Main Guide

- **EPISODE_17_GUIDE.md** - Comprehensive overview of Django concepts

---

## 🚀 Next Steps (Episode 18)

Episode 18 will build on Episode 17 with:
- **Forms** - User input collection and validation
- **CRUD Operations** - Create, Update, Delete using forms
- **Form Validation** - Built-in and custom validators
- **Model Forms** - Auto-generated forms from models
- **POST Requests** - Handling form submissions safely

---

## 💡 Tips for Success

1. **Start with Assignment 1** - It's foundational
2. **Read the README** in each assignment carefully
3. **Study the _solution.py files** when stuck
4. **Run tests frequently** - They guide your implementation
5. **Use the shell** to test queries: `python manage.py shell`
6. **Check migrations** if you have database errors
7. **Reference the guide** (EPISODE_17_GUIDE.md) for concepts

---

## ✨ Key Learning Outcomes

After completing Episode 17, students will:

✅ Understand Django apps and project structure
✅ Define database models using ORM
✅ Create and apply migrations
✅ Write views that fetch and filter data
✅ Build templates that display database records
✅ Implement model relationships (ForeignKey, ManyToMany)
✅ Access related objects in views and templates
✅ Query databases efficiently with QuerySets
✅ Build real web applications with persistent data
✅ Pass comprehensive test suites

---

## 🆘 Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| "No such table" | Run `python manage.py migrate` |
| "TemplateDoesNotExist" | Check template path: `app/templates/app/template.html` |
| "Tests fail with AttributeError" | Make sure model fields exist with correct names |
| "Reverse relationship not working" | Check model relationships are defined correctly |
| "Can't access related object in template" | Use correct reverse name: `model_set` for ForeignKey |

---

**Episode 17 Ready! Start Learning Django ORM! 🎓**

Created: February 17, 2026
