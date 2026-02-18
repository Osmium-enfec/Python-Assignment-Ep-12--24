# Episode 19 - Assignment 1: HTML Tables and Template Conditionals

## Overview
This assignment teaches HTML table structure, Bootstrap table styling, and Django template conditionals. Students build a student management system with data displayed in responsive Bootstrap tables and conditional rendering based on student performance.

## Learning Objectives
- ✅ Create semantic HTML tables with `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`
- ✅ Apply Bootstrap table classes: `.table`, `.table-striped`, `.table-hover`, `.table-bordered`
- ✅ Use Django template conditionals: `{% if %}`, `{% elif %}`, `{% else %}`, `{% endif %}`
- ✅ Implement comparison operators: `==`, `!=`, `>`, `<`, `>=`, `<=`
- ✅ Use logical operators: `and`, `or`, `not` in templates
- ✅ Check for empty values and existence in templates
- ✅ Color-code table rows based on conditionals
- ✅ Display status badges with conditional logic
- ✅ Build multi-table page with related data

## Core Topics Covered

### HTML Tables (Topics 1-12)
1. HTML Table Definition and semantic structure
2. `<table>` element - Table container
3. `<thead>` - Table header section
4. `<tbody>` - Table body section
5. `<tr>` - Table rows
6. `<th>` - Header cells with scope
7. `<td>` - Data cells
8. `<tfoot>` - Optional footer
9. `scope` attribute for accessibility
10. `colspan` - Spanning columns
11. `rowspan` - Spanning rows
12. `<caption>` - Table title

### Bootstrap Table Styling (Topics 13-23)
13. `.table` - Base Bootstrap table class
14. `.table-striped` - Alternating row colors
15. `.table-hover` - Row highlighting on hover
16. `.table-dark` - Dark theme
17. `.table-bordered` - Cell borders
18. `.table-responsive` - Mobile horizontal scroll
19. `.align-middle` - Vertical centering
20. Header and row styling
21. Cell alignment utilities
22. Status indication with colors
23. Responsive integration

### Django Template Conditionals (Topics 24-40)
24. `{% if condition %}` block
25. `{% endif %}` closing tag
26. `{% else %}` clause
27. `{% elif %}` additional condition
28. Equality operator `==`
29. Inequality operator `!=`
30. Greater than `>`
31. Less than `<`
32. Greater or equal `>=`
33. Less or equal `<=`
34. Logical `and` operator
35. Logical `or` operator
36. Logical `not` operator
37. `in` operator for lists
38. Boolean context evaluation
39. Empty value checking
40. Variable existence checking

## Project Structure

```
assignment1/myapp/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── students/
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    ├── templates/students/
    │   ├── base.html
    │   ├── home.html
    │   ├── student_list.html
    │   ├── student_detail.html
    │   └── grade_report.html
    ├── static/students/
    │   ├── css/style.css
    │   └── js/main.js
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── admin.py
    ├── apps.py
    └── tests.py
```

## Database Models

### Student Model
- **Fields**: name, email, roll_no, date_of_birth, phone, status, gpa, created_at
- **Properties**:
  - `gpa_grade` - Converts GPA to letter grade (A, B, C, D, F)
  - `is_dean_list` - True if GPA ≥ 3.5
  - `is_at_risk` - True if GPA < 2.0

### Course Model
- **Fields**: code, name, credits

### Grade Model
- **Fields**: student (FK), course (FK), score, semester, year
- **Properties**:
  - `letter_grade` - Converts score to letter grade
  - `is_passing` - True if score ≥ 60

## Templates and Conditionals

### home.html
- Displays dashboard with statistics cards
- Shows nested conditionals for student status
- Uses `if/elif/else` for activity levels

### student_list.html
- Table with conditional row colors:
  - Green row: Dean's List students (GPA ≥ 3.5)
  - Red row: At-risk students (GPA < 2.0)
  - Gray row: Graduated students
- Badges showing status and GPA grade
- Conditional icons and color-coded values

### student_detail.html
- Displays student profile with alerts:
  - Success alert: Dean's List qualification
  - Danger alert: Academic risk warning
  - Info alert: Good standing message
- Grades table with color-coded rows:
  - Green: Score ≥ 90
  - Blue: Score 80-89
  - Yellow: Score 60-79
  - Red: Score < 60
- Summary section with conditional messages

### grade_report.html
- Filter form with semester and year selection
- Statistics cards showing totals, passing, failing
- Full grade table with row coloring by score
- Conditional messages for no results

## Key Template Conditionals Examples

```django
<!-- Simple if -->
{% if student.is_dean_list %}
    <span class="badge bg-warning">Dean's List</span>
{% endif %}

<!-- if/else -->
{% if student.is_at_risk %}
    <div class="alert alert-danger">At Risk!</div>
{% else %}
    <div class="alert alert-success">Good Standing</div>
{% endif %}

<!-- if/elif/else -->
{% if student.status == 'active' %}
    <span class="badge bg-success">Active</span>
{% elif student.status == 'graduated' %}
    <span class="badge bg-info">Graduated</span>
{% else %}
    <span class="badge bg-secondary">Inactive</span>
{% endif %}

<!-- Comparison operators -->
{% if student.gpa >= 3.5 %}
    Dean's List Qualified
{% elif student.gpa >= 3.0 %}
    Good Standing
{% else %}
    Academic Warning
{% endif %}

<!-- Logical operators -->
{% if student.status == 'active' and student.gpa < 2.0 %}
    <span class="badge bg-danger">Active but At Risk</span>
{% endif %}

<!-- not operator -->
{% if not student.is_dean_list %}
    <p>Student does not qualify for Dean's List</p>
{% endif %}

<!-- Empty check -->
{% if grades %}
    <table class="table">...</table>
{% else %}
    <p>No grades found</p>
{% endif %}

<!-- in operator -->
{% if student.status in passing_statuses %}
    <p>Student may graduate</p>
{% endif %}
```

## Bootstrap Table Examples

```html
<!-- Basic table with striped rows -->
<table class="table table-striped">
    <thead class="table-dark">
        <tr>
            <th scope="col">Name</th>
            <th scope="col">GPA</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>John Doe</td>
            <td>3.7</td>
        </tr>
    </tbody>
</table>

<!-- Responsive table -->
<div class="table-responsive">
    <table class="table table-hover table-bordered">
        ...
    </table>
</div>

<!-- Conditional row colors -->
<tr class="{% if student.gpa >= 3.5 %}table-success{% elif student.gpa < 2.0 %}table-danger{% endif %}">
    <td>{{ student.name }}</td>
</tr>
```

## Running the Assignment

```bash
cd assignment1/myapp
python manage.py migrate          # Create database
python manage.py createsuperuser  # Create admin account
python manage.py runserver        # Start development server
python manage.py test             # Run tests
```

## Admin Panel Access
- URL: `http://localhost:8000/admin/`
- Login with superuser credentials
- View, add, edit, delete students, courses, and grades

## Assignment Tasks

### Basic Requirements
1. ✅ Create Student model with GPA and status fields
2. ✅ Create Course and Grade models for relationships
3. ✅ Build student list page with Bootstrap table
4. ✅ Implement conditional row coloring based on GPA
5. ✅ Create student detail page with grades table
6. ✅ Add conditional alerts for Dean's List and at-risk
7. ✅ Build grade report with filtering
8. ✅ Use template conditionals throughout

### Advanced Requirements
- Add custom admin configuration with `list_display`, `search_fields`, `list_filter`
- Implement table sorting with JavaScript
- Add print functionality for tables
- Create dashboard with statistics
- Add semester/year filtering
- Implement bulk operations in admin

## Testing

```bash
python manage.py test test_assignment -v 2
```

Tests cover:
- Model creation and properties (GPA grades, Dean's List, at-risk)
- URL routing
- Template rendering
- Conditional logic
- Admin functionality

## Expected Results

- ✅ 40+ tests passing
- ✅ All conditionals render correctly
- ✅ Tables display properly on all screen sizes
- ✅ Row colors update based on conditions
- ✅ Admin panel fully functional

## Common Mistakes to Avoid

1. ❌ Forgetting `{% endif %}` for conditionals
2. ❌ Using Python syntax (`and` is correct, `&&` is wrong)
3. ❌ Not using `scope` attribute on `<th>` elements
4. ❌ Missing responsive wrapper for tables
5. ❌ Using table.table-striped instead of .table-striped
6. ❌ Forgetting to close `<tbody>` and `<thead>`
7. ❌ Not handling empty results in templates
8. ❌ Using incorrect comparison operators in conditionals

## Resources

- Django Template Documentation: https://docs.djangoproject.com/en/5.1/topics/templates/
- Bootstrap Tables: https://getbootstrap.com/docs/5.3/content/tables/
- HTML Table Specification: https://html.spec.whatwg.org/multipage/tables.html
- MDN Table Guide: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table

## Learning Outcomes

By completing this assignment, you will understand:
- ✅ Semantic HTML structure for tables
- ✅ Bootstrap table styling and responsive design
- ✅ Django template conditionals and operators
- ✅ Conditional rendering and dynamic styling
- ✅ Building complex data-driven pages
- ✅ Admin panel customization
- ✅ Working with related models in templates

---

**Episode 19 - Assignment 1 Complete!**
Topics: HTML Tables (12) | Bootstrap Styling (11) | Template Conditionals (17)
