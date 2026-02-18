# Episode 23: Complete CRUD Operations - Starter Code Guide

## Overview
Episode 23 teaches complete Create, Read, Update, Delete (CRUD) operations in Django. Students work with a Student management system, progressing from basic operations (Assignment 1) to advanced UI presentation (Assignment 2).

**Total Tests:** 118/118
- Assignment 1: 70 tests
- Assignment 2: 48 tests

---

## Assignment 1: Basic CRUD Operations

### Topics Covered: 1-70

### What Students Implement

#### 1. **Student Model** (Topics 1-8)
```
8 fields with validation:
- name: CharField (max_length=200)
- email: EmailField (unique=True)
- enrollment_date: DateField (auto_now_add=True)
- age: IntegerField (optional)
- status: CharField with choices (active, inactive, graduated)
- gpa: DecimalField (0.0-4.0)
- major: CharField (optional)
- created_at: DateTimeField (auto_now_add=True)

Meta options:
- ordering: ['-enrollment_date']
- unique_together: [['email']]

Methods:
- __str__(): Display name with email
- is_active: Property checking if status='active'
```

#### 2. **StudentForm** (Topics 9-14)
ModelForm with 6 fields: name, email, age, status, gpa, major
- Bootstrap styling (form-control)
- Required field indicators
- Help text for guidance

#### 3. **Five CRUD Views** (Topics 15-70)

**a) student_index** (Topics 15-22)
- List all students with simple table/list display
- Show: name, email, status, major
- Action buttons: View, Edit, Delete

**b) student_add** (Topics 23-32)
- GET: Display empty form
- POST: Create new student
- Validation with error messages
- Success message with student name
- Redirect to index or detail

**c) student_view** (Topics 33-44)
- GET: Display student details
- 404 handling for invalid IDs
- All fields displayed
- Navigation buttons

**d) student_edit** (Topics 45-58)
- GET: Display form with current data
- POST: Update student
- Validation
- Success message
- Redirect to detail

**e) student_delete** (Topics 59-70)
- GET: Show confirmation
- POST: Delete student
- Success message
- Redirect to index

### Test Structure: 70 tests across 9 test classes
- StudentModelTests (10 tests): Model creation, validation, properties
- StudentFormTests (5 tests): Form validation, widgets
- StudentIndexViewTests (10 tests): Listing, display
- StudentAddViewTests (5 tests): Creation, validation, redirect
- StudentViewDetailTests (5 tests): Detail display, 404
- StudentEditViewTests (5 tests): Update operations
- StudentDeleteViewTests (5 tests): Deletion, confirmation
- StudentAdminTests (5 tests): Admin registration
- CRUDPatternTests (10 tests): Complete workflows

---

## Assignment 2: Advanced UI with Enhanced Features

### Topics Covered: 41-80 (New: 41-48 reuse model, 49-80 advanced UI)

### What Students Implement

#### 1. **Enhanced Student Model** (Topics 41-48)
Same as Assignment 1 - students may reuse or rebuild:
```
Same 8 fields and methods as A1
```

#### 2. **Enhanced StudentForm** (Topics 49-50)
- Same fields as A1
- Better Bootstrap styling
- Improved labels and help text
- Better error display

#### 3. **Five Enhanced CRUD Views** (Topics 51-70)

**a) student_index** (Topics 51-55)
- **Advanced Grid Layout**: Responsive card display (col-md-6, col-lg-4)
- **Status Badges**: Color-coded badges (active=green, inactive=gray, graduated=blue)
- **Card Information**:
  - Name prominently displayed
  - Email with icon
  - Major with icon
  - GPA with color-coding (>3.5=gold, >=3.0=green, <3.0=orange)
  - Enrollment date formatted
- **Action Buttons**: View, Edit, Delete with icons

**b) student_add** (Topics 56-60)
- Clean form in card layout
- Field groups for organization
- Required field indicators
- Bootstrap form styling
- Success/error messages
- Redirect to detail view

**c) student_view** (Topics 61-65)
- Detailed card layout
- All student information displayed professionally
- Status badge prominently
- GPA with color coding
- Email as mailto link
- Formatted dates
- Navigation buttons

**d) student_edit** (Topics 66-68)
- **Organized Field Groups**:
  1. Personal Information: name, email
  2. Academic Info: major, status, gpa
  3. Additional: age
- Each group in separate card section
- Field icons for better UX
- Bootstrap form styling
- Save/Cancel buttons

**e) student_delete** (Topics 69-70)
- Beautiful confirmation page
- Display student's key information
- Warning message about permanent deletion
- Confirm/Cancel buttons
- Clear emphasis on consequences

#### 4. **Admin Interface** (Topics 76-80)
StudentAdmin with:
- list_display: name, email, status, gpa, enrollment_date, major
- list_filter: status, enrollment_date, gpa
- search_fields: name, email, major
- ordering: -enrollment_date
- readonly_fields: created_at, enrollment_date
- Fieldsets for organized display

### Test Structure: 48 tests across 10 test classes
- StudentModelTests (8 tests)
- StudentFormTests (6 tests)
- StudentIndexViewTests (5 tests): Advanced card display
- StudentAddViewTests (5 tests): Enhanced form
- StudentViewDetailTests (5 tests): Detail card
- StudentEditViewTests (5 tests): Grouped fields
- StudentDeleteViewTests (5 tests): Confirmation
- AdminIntegrationTests (5 tests)
- AdvancedPatternTests (10 tests): Professional workflows

---

## File Structure

### Provided (For Both Assignments)
```
manage.py
myapp/
  __init__.py
  settings.py (fully configured)
  urls.py (skeleton)
  wsgi.py
templates/
  base.html (Bootstrap navbar/footer)
students/
  __init__.py
```

### TODO: Students Create
```
students/
  models.py (Student model)
  forms.py (StudentForm)
  views.py (5 CRUD views)
  urls.py (5 URL patterns)
  admin.py (StudentAdmin)
  tests.py (test classes + methods)
templates/students/
  student_index.html
  student_add.html
  student_view.html
  student_edit.html
  student_confirm_delete.html
```

---

## Key Learning Objectives

### Episode 23 A1: Basic CRUD
1. Model design with validation
2. Simple form creation
3. Basic view patterns (index, create, view, update, delete)
4. Django ORM operations
5. URL routing
6. Basic templates
7. 404 error handling
8. Database integrity
9. Admin registration
10. Complete CRUD workflow

### Episode 23 A2: Advanced UI
1. All A1 skills retained
2. Advanced form styling with Bootstrap
3. Professional card-based layouts
4. Status badges and color coding
5. Icon usage (Font Awesome)
6. Responsive grid layouts
7. Field grouping in forms
8. Enhanced error display
9. Professional user feedback
10. Real-world UI patterns

---

## Getting Started

### Setup Instructions
1. Navigate to `episode23/assignment1_starter/` or `assignment2_starter/`
2. Run: `python manage.py migrate`
3. Run: `python manage.py runserver`
4. Implement TODO items in order
5. Run tests: `python manage.py test`

### Implementation Order
1. **First**: models.py (Student model with all fields)
2. **Second**: forms.py (StudentForm with Bootstrap)
3. **Third**: views.py (5 CRUD views with proper redirect)
4. **Fourth**: urls.py (5 URL patterns)
5. **Fifth**: admin.py (StudentAdmin registration)
6. **Sixth**: Templates (HTML files with Bootstrap)
7. **Seventh**: tests.py (Fill in test implementations)

### Common Patterns to Implement

**Create Operation:**
```python
if request.method == 'POST':
    form = StudentForm(request.POST)
    if form.is_valid():
        student = form.save()
        messages.success(request, f"Student {student.name} created!")
        return redirect('students:view', student.id)
else:
    form = StudentForm()
return render(request, 'students/student_add.html', {'form': form})
```

**Read Operation:**
```python
student = get_object_or_404(Student, id=student_id)
return render(request, 'students/student_view.html', {'student': student})
```

**Update Operation:**
```python
student = get_object_or_404(Student, id=student_id)
if request.method == 'POST':
    form = StudentForm(request.POST, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, f"Student {student.name} updated!")
        return redirect('students:view', student.id)
else:
    form = StudentForm(instance=student)
return render(request, 'students/student_edit.html', {'student': student, 'form': form})
```

**Delete Operation:**
```python
student = get_object_or_404(Student, id=student_id)
if request.method == 'POST':
    name = student.name
    student.delete()
    messages.success(request, f"Student {name} deleted!")
    return redirect('students:index')
return render(request, 'students/student_confirm_delete.html', {'student': student})
```

---

## Advanced Considerations (A2)

### Card Display in Templates
```html
<!-- Student Card Grid -->
<div class="row">
{% for student in students %}
    <div class="col-md-6 col-lg-4">
        <div class="card h-100">
            <!-- Card content -->
        </div>
    </div>
{% endfor %}
</div>
```

### Status Badge Colors
- active: `<span class="badge bg-success">Active</span>`
- inactive: `<span class="badge bg-secondary">Inactive</span>`
- graduated: `<span class="badge bg-info">Graduated</span>`

### GPA Color Coding
- >3.5: Yellow/Gold (excellent)
- >=3.0 & <=3.5: Green (good)
- <3.0: Orange (needs improvement)

### Form Field Groups
```html
<div class="card mb-3">
    <div class="card-header">Personal Information</div>
    <div class="card-body">
        <!-- Fields for name, email -->
    </div>
</div>
```

---

## Test Commands

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test students.tests.StudentModelTests

# Run specific test method
python manage.py test students.tests.StudentModelTests.test_student_creation

# Run with verbose output
python manage.py test -v 2
```

---

## Debugging Tips

1. **Model Issues**: Check migration - `python manage.py makemigrations && python manage.py migrate`
2. **Form Issues**: Print form.errors in view to see validation problems
3. **Template Issues**: Check template name spelling in render() call
4. **URL Issues**: Use `reverse()` to test URL pattern generation
5. **View Issues**: Add print statements or use Django debugger
6. **Test Issues**: Run single test to isolate failures

---

## Success Criteria

### Assignment 1: All 70 tests pass ✓
### Assignment 2: All 48 tests pass ✓

Both assignments should result in:
- Fully functional CRUD interface
- Clean, organized code
- Professional-looking templates
- Comprehensive test coverage
- Proper error handling
- User-friendly feedback messages
