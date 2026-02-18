# Episode 19 - Assignment 2: Django Admin Panel

## Overview
This assignment teaches advanced Django admin customization. Students learn to build a professional admin interface with custom fields, filters, search, bulk actions, and permissions.

## Learning Objectives
- ✅ Register models with Django admin using `@admin.register` decorator
- ✅ Configure `list_display` to customize admin list view columns
- ✅ Implement `search_fields` for full-text search functionality
- ✅ Add `list_filter` for sidebar filtering options
- ✅ Use `fieldsets` to organize form sections
- ✅ Mark fields as `readonly_fields`
- ✅ Create custom `admin actions` for bulk operations
- ✅ Set up `date_hierarchy` for date-based navigation
- ✅ Create custom admin permissions
- ✅ Customize admin site header and title
- ✅ Implement staff accounts with limited permissions
- ✅ Use `ModelAdmin` class for advanced configuration

## Core Topics Covered

### Django Admin Panel Basics (Topics 41-56)
41. Django Admin - Built-in administrative interface
42. Admin URL - `/admin/` endpoint
43. Superuser Account - Administrative account creation
44. createsuperuser Command - Creating admin users
45. Admin Credentials - Login authentication
46. Admin Login - Accessing the admin panel
47. Model Registration - `admin.site.register()`
48. Admin Decorator - `@admin.register()`
49. ModelAdmin Class - Customization base class
50. list_display - Column configuration
51. list_filter - Sidebar filters
52. search_fields - Search functionality
53. fields Property - Form field specification
54. readonly_fields - Non-editable fields
55. fieldsets Property - Form section organization
56. ordering Property - Default sort order

### Admin CRUD Operations (Topics 57-66)
57. Add Student - Creating records
58. List Students - Viewing records in table
59. Edit Student - Modifying records
60. Delete Student - Removing records
61. Bulk Delete - Multiple record deletion
62. Search Students - Full-text search
63. Filter Students - Sidebar filtering
64. Sort Results - Column-based sorting
65. Pagination - Multi-page navigation
66. Admin Actions - Bulk operations

### Admin Panel Features (Topics 67-80)
67. Permissions - Model-level access control
68. Staff Users - Non-superuser accounts
69. Change History - Automatic logging
70. Data Validation - Model-level validation
71. Inline Editing - Related record editing
72. Admin Site Customization - Header/title/index
73. Time Stamping - Auto-populated timestamps
74. Admin Documentation - Auto-generated docs
75. Foreign Key Display - Dropdown selection
76. Choice Fields - Dropdown options
77. Boolean Fields - Checkbox rendering
78. Date Fields - Calendar pickers
79. URL Reversal - Automatic URL generation
80. Related Records - Relationship management

## Project Structure

```
assignment2/myapp/
├── manage.py
├── requirements.txt
├── README.md
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
    ├── __init__.py
    ├── models.py (4 models)
    ├── admin.py (Advanced configuration)
    ├── apps.py
    ├── tests.py
    └── test_assignment.py (Admin tests)
```

## Database Models

### Department Model
- **Fields**: name, code, head, phone
- **Features**: Unique constraints, ordering

### Student Model
- **Fields**: name, email, roll_no, date_of_birth, phone, department (FK), status, gpa, admission_date, is_scholarship_holder, timestamps
- **Choices**: status (active, inactive, graduated, suspended)
- **Features**: Custom permissions, date ordering

### Course Model
- **Fields**: code, name, department (FK), level, credits, description, is_active
- **Choices**: level (100-400 for course levels)
- **Features**: Active filtering, department relationships

### Enrollment Model
- **Fields**: student (FK), course (FK), semester, year, score, grade, is_completed, enrollment_date
- **Choices**: semester (fall, spring, summer), grade (A-F, Incomplete)
- **Features**: Unique together constraint, date-based navigation

## Admin Configuration Features

### StudentAdmin Configuration
```python
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Display columns
    list_display = ('name', 'roll_no', 'department', 'status', 'gpa', 'is_scholarship_holder', 'admission_date')
    
    # Sidebar filters
    list_filter = ('status', 'department', 'is_scholarship_holder', 'admission_date')
    
    # Search fields
    search_fields = ('name', 'email', 'roll_no')
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at')
    
    # Date hierarchy
    date_hierarchy = 'admission_date'
    
    # Form organization
    fieldsets = (
        ('Personal Information', {...}),
        ('Academic Information', {...}),
        ('Important Dates', {...}),
    )
    
    # Bulk actions
    actions = ['mark_active', 'mark_inactive']
```

### DepartmentAdmin Configuration
- Simple but complete configuration
- Organized fieldsets
- Search and filtering

### CourseAdmin Configuration
- Level display with get_level_display()
- Department-based filtering
- Search by code and name

### EnrollmentAdmin Configuration
- Date hierarchy for semester navigation
- Semester and year filtering
- Bulk completion marking
- Score and grade management

## Admin Interface Features

### 1. List Display
Customize which columns appear in list view:
```python
list_display = ('name', 'roll_no', 'department', 'gpa', 'admission_date')
```

### 2. Search Functionality
Enable full-text search on specified fields:
```python
search_fields = ('name', 'email', 'roll_no')
```

### 3. Sidebar Filters
Add filtering options:
```python
list_filter = ('status', 'department', 'is_scholarship_holder', 'admission_date')
```

### 4. Fieldsets
Organize form into sections:
```python
fieldsets = (
    ('Personal Information', {
        'fields': ('name', 'email', 'phone', 'date_of_birth')
    }),
    ('Academic Information', {
        'fields': ('roll_no', 'department', 'gpa', 'status', 'is_scholarship_holder')
    }),
    ('Important Dates', {
        'fields': ('admission_date', 'created_at', 'updated_at'),
        'classes': ('collapse',)
    }),
)
```

### 5. Read-Only Fields
Display but prevent editing:
```python
readonly_fields = ('created_at', 'updated_at')
```

### 6. Bulk Actions
Custom operations on multiple records:
```python
def mark_active(self, request, queryset):
    count = queryset.update(status='active')
    self.message_user(request, f'{count} students marked as active.')
mark_active.short_description = "Mark selected as active"

actions = ['mark_active']
```

### 7. Date Hierarchy
Navigate by date field:
```python
date_hierarchy = 'admission_date'
```

### 8. Ordering
Default sort order:
```python
ordering = ['-admission_date']
```

## Admin Site Customization

```python
# Customize site header
admin.site.site_header = "Student Management Admin"

# Customize site title
admin.site.site_title = "Student Admin Portal"

# Customize index title
admin.site.index_title = "Welcome to Student Management System"
```

## Running Assignment 2

```bash
cd assignment2/myapp

# Create database
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123

# Start server
python manage.py runserver

# Access admin at http://localhost:8000/admin/

# Run tests
python manage.py test test_assignment -v 2
```

## Admin Features to Explore

### List View
1. View all records in table format
2. Click column headers to sort
3. Use search box to find records
4. Use filters on sidebar
5. Use date hierarchy for navigation
6. Select multiple records for bulk actions

### Add Record
1. Fill in form fields
2. See organized fieldsets
3. Select related records from dropdowns
4. Choose from choice fields
5. Get inline validation errors

### Edit Record
1. View current values
2. See read-only fields (cannot edit)
3. Edit all editable fields
4. See timestamp fields
5. Track changes in history

### Delete Record
1. Confirm deletion
2. See cascading relationships
3. Understand deletion impact

## Testing Admin Functionality

```bash
# Run specific admin tests
python manage.py test test_assignment.AdminPanelTests -v 2

# Run all tests
python manage.py test test_assignment -v 2
```

## Custom Permissions Example

Models can define custom permissions:
```python
class Student(models.Model):
    class Meta:
        permissions = [
            ('can_export_students', 'Can export student list'),
            ('can_view_gpa', 'Can view GPA information'),
        ]
```

## Assignment Tasks

### Basic Requirements
1. ✅ Create 4 models with relationships
2. ✅ Register all models with admin
3. ✅ Configure list_display for each model
4. ✅ Implement search_fields for searchable models
5. ✅ Add list_filter for filtering options
6. ✅ Organize forms with fieldsets
7. ✅ Mark appropriate fields as readonly
8. ✅ Create custom admin actions

### Advanced Requirements
- Create staff accounts with limited permissions
- Implement inline editing for related records
- Add custom admin methods for display
- Create admin filters for custom logic
- Implement change history tracking
- Export data functionality
- Dashboard with statistics

## Expected Results

- ✅ 20+ admin tests passing
- ✅ Fully functional admin interface
- ✅ All CRUD operations working
- ✅ Search and filtering functional
- ✅ Bulk actions executing properly
- ✅ Custom permissions respected

## Common Admin Configurations

```python
# Basic admin registration
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass

# Intermediate configuration
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status')
    search_fields = ('name', 'email')

# Advanced configuration
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'gpa')
    list_filter = ('status', 'admission_date')
    search_fields = ('name', 'email', 'roll_no')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'admission_date'
    fieldsets = (...)
    actions = ['mark_active']
```

## Resources

- Django Admin Documentation: https://docs.djangoproject.com/en/5.1/ref/contrib/admin/
- ModelAdmin API Reference: https://docs.djangoproject.com/en/5.1/ref/contrib/admin/#modeladmin-options
- Django Permissions: https://docs.djangoproject.com/en/5.1/topics/auth/default/#permissions-and-authorization

## Learning Outcomes

By completing this assignment, you will understand:
- ✅ Django admin interface architecture
- ✅ Model registration and customization
- ✅ List display and filtering options
- ✅ Form organization with fieldsets
- ✅ Bulk actions and custom operations
- ✅ Admin permissions and access control
- ✅ Staff account management
- ✅ Change history and data validation
- ✅ Professional admin interface design
- ✅ Admin site customization

---

**Episode 19 - Assignment 2 Complete!**
Topics: Admin Basics (16) | CRUD Operations (10) | Features (14)
