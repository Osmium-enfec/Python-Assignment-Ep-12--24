# Episode 19: HTML Tables, Template Conditionals, and Django Admin Panel

## Complete Learning Path

### Part 1: Assignment 1 - HTML Tables & Template Conditionals
Learn to build dynamic data-driven pages with:
- Semantic HTML table structure
- Bootstrap table styling and responsiveness
- Django template conditionals (if/elif/else)
- Comparison and logical operators in templates
- Conditional row coloring and styling
- Status-based rendering

**Key Topics:** 40 core concepts
- HTML Tables (12)
- Bootstrap Table Styling (11)
- Django Template Conditionals (17)

**Deliverable:** Student Management System with interactive tables and grades

### Part 2: Assignment 2 - Django Admin Panel
Master the built-in admin interface:
- Model registration and customization
- list_display, search_fields, list_filter
- Fieldsets and form organization
- Custom admin actions (bulk operations)
- Admin permissions and staff accounts
- Change history and data validation
- Admin site customization

**Key Topics:** 40 core concepts
- Admin Panel Basics (16)
- Admin CRUD Operations (10)
- Admin Panel Features (14)

**Deliverable:** Fully customized admin panel with advanced features

## Core Learning Outcomes

### Students will be able to:
1. ✅ Create semantic HTML tables
2. ✅ Style tables with Bootstrap for responsive design
3. ✅ Implement complex conditional logic in templates
4. ✅ Color-code rows based on data values
5. ✅ Use Django admin for CRUD operations
6. ✅ Customize admin interface with ModelAdmin
7. ✅ Create bulk actions and filters
8. ✅ Manage permissions and staff accounts

## Episode 19 Statistics

| Metric | Count |
|--------|-------|
| Core Topics | 80 |
| Assignments | 2 |
| Models | 6 (3 per assignment) |
| Templates | 5 (Assignment 1) |
| Test Cases | 40+ |
| Lines of Code | 2,000+ |
| Documentation | 50 KB |

## File Structure

```
episode19/
├── assignment1/
│   └── myapp/
│       ├── manage.py
│       ├── requirements.txt
│       ├── README.md
│       ├── myproject/
│       ├── students/
│       │   ├── models.py (Student, Course, Grade)
│       │   ├── admin.py
│       │   ├── views.py
│       │   ├── templates/ (5 HTML files)
│       │   ├── static/ (CSS, JS)
│       │   └── migrations/
│       └── test_assignment.py (40+ tests)
│
├── assignment2/
│   └── myapp/
│       ├── manage.py
│       ├── requirements.txt
│       ├── README.md (Advanced Admin Guide)
│       ├── myproject/
│       ├── students/
│       │   ├── models.py (Department, Student, Course, Enrollment)
│       │   ├── admin.py (Advanced customization)
│       │   └── migrations/
│       └── test_assignment.py (Admin tests)
│
└── episode19_overview.md (This file)
```

## Quick Start

### Assignment 1
```bash
cd assignment1/myapp
python manage.py migrate
python manage.py runserver
# Visit http://localhost:8000
python manage.py test test_assignment -v 2
```

### Assignment 2
```bash
cd assignment2/myapp
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Admin: http://localhost:8000/admin
python manage.py test test_assignment -v 2
```

## Next Steps

After Episode 19:
- Episode 20: Form Validation and Custom Forms
- Episode 21: User Authentication and Permissions
- Episode 22: API Development with Django REST Framework
- Episode 23: Deployment and Production

---

**Episode 19 Complete - Advanced Django & Frontend Skills Mastered!**
