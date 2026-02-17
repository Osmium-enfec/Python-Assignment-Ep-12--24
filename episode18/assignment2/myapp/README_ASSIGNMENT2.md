# Episode 18 - Assignment 2: Advanced Bootstrap with Bootswatch & Font Awesome

## Learning Objectives

After completing this assignment, you should understand:

1. **Bootstrap Components** - Cards, tables, badges, buttons, modals
2. **Bootswatch Themes** - Customizing Bootstrap with pre-built themes
3. **Font Awesome Icons** - Advanced icon usage and sizing
4. **Template Inheritance Patterns** - Multi-level template hierarchy
5. **Responsive Tables** - Making data tables mobile-friendly
6. **Card-Based Layouts** - Using cards for different content types
7. **Navigation Patterns** - Multi-level navigation structures
8. **CSS Customization** - Extending Bootstrap with custom CSS
9. **Static Files Organization** - Managing multiple CSS/JS files
10. **Frontend Performance** - Optimizing CDN usage and caching

## What You'll Build

A professional course management interface with:
- Bootswatch theme integration (choose from 26 themes)
- Course list with cards and filters
- Student enrollment display with tables
- Course details with rich information
- Dynamic badge styling
- Responsive data tables
- Font Awesome icons for actions (edit, delete, view)
- Professional color schemes
- Advanced responsive design

## Files Overview

```
assignment2/
├── students/
│   ├── templates/students/
│   │   ├── base.html                     ← Base template with Bootswatch
│   │   ├── base_solution.html            (Reference)
│   │   ├── student_list.html             ← Student list with tables
│   │   ├── student_list_solution.html    (Reference)
│   │   ├── course_list.html              ← Course cards with filters
│   │   ├── course_list_solution.html     (Reference)
│   │   ├── course_detail.html            ← Course detail with enrollments
│   │   ├── course_detail_solution.html   (Reference)
│   │   ├── student_detail.html           ← Student detail with courses
│   │   ├── student_detail_solution.html  (Reference)
│   │   ├── enrollment_list.html          ← Enrollment table
│   │   └── enrollment_list_solution.html (Reference)
│   ├── static/students/
│   │   ├── css/
│   │   │   ├── style.css                 ← Custom CSS
│   │   │   └── bootswatch-variables.css  ← Theme customization
│   │   └── js/
│   │       └── main.js                   ← Interactions and dynamic features
│   ├── models.py                         (From Episode 17)
│   └── views.py                          (From Episode 17)
├── myproject/
│   ├── settings.py                       (Already configured)
│   └── urls.py                           (Already configured)
└── manage.py
```

## Step-by-Step Instructions

### Step 1: Choose Bootswatch Theme

Visit https://bootswatch.com/ and choose a theme. Then update `base.html`:

```html
<!-- Instead of Bootstrap CDN, use Bootswatch -->
<link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/[THEME]/bootstrap.min.css" rel="stylesheet">

<!-- Available themes: darkly, flatly, journal, lumen, lux, materia, minty, morph, 
     pulse, quartz, sandstone, simplex, sketchy, slate, solar, spacelab, superhero, 
     united, vapor, yeti, zephyr -->
```

### Step 2: Update Base Template (base.html)

Edit `students/templates/students/base.html`:

```django
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Course Management{% endblock %}</title>
    
    <!-- Bootswatch Theme CSS from CDN (choose one theme) -->
    <link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/darkly/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'students/css/style.css' %}">
</head>
<body>
    <!-- TODO 1: Navbar with theme colors
         - Navigation to Student List, Course List, Enrollment List
         - Responsive hamburger menu
         - Search functionality
         - Icons for navigation items
    -->
    
    <!-- Main Content -->
    <div class="container-fluid mt-4 mb-4">
        <!-- Breadcrumb navigation (optional) -->
        {% block breadcrumb %}{% endblock %}
        
        {% block content %}{% endblock %}
    </div>
    
    <!-- TODO 2: Footer with theme styling
         - Social links with Font Awesome icons
         - Copyright information
         - Theme info
    -->
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script src="{% static 'students/js/main.js' %}"></script>
</body>
</html>
```

### Step 3: Student List Template (student_list.html)

Edit `students/templates/students/student_list.html`:

```django
{% extends 'students/base.html' %}

{% block title %}Students{% endblock %}

{% block content %}
<h1 class="mb-4"><i class="fas fa-users"></i> All Students</h1>

<!-- TODO 3: Responsive Data Table
     - Table with striped rows
     - Columns: Roll No, Name, Email, Fees Status
     - Buttons for View/Edit/Delete with icons
     - Empty state if no students
     - Responsive table wrapper for mobile
-->

<div class="table-responsive">
    <table class="table table-hover">
        <thead class="table-dark">
            <tr>
                <th>Roll No</th>
                <th>Name</th>
                <th>Email</th>
                <th>Fees Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <!-- TODO 3a: Loop through students
                 - Show roll_no, name, email
                 - Badge for fees_paid (green if yes, red if no)
                 - Action buttons with Font Awesome icons
            -->
        </tbody>
    </table>
</div>

{% endblock %}
```

### Step 4: Course List Template (course_list.html)

Edit `students/templates/students/course_list.html`:

```django
{% extends 'students/base.html' %}

{% block title %}Courses{% endblock %}

{% block content %}
<h1 class="mb-4"><i class="fas fa-book"></i> Available Courses</h1>

<!-- TODO 4: Course Card Grid
     - Card layout with 3 columns (col-lg-4)
     - Course name with icon
     - Instructor information
     - Student count badge
     - Duration or credits
     - View button with icon
     - Filter options by instructor (bonus)
-->

<div class="row">
    <!-- TODO 4a: Loop through courses
         - Use col-md-6 col-lg-4 for responsive grid
         - Card with header (course name) and body
         - Icons for different info (fa-chalkboard, fa-users, fa-clock)
         - Badge for enrollment count
    -->
</div>

{% endblock %}
```

### Step 5: Course Detail Template (course_detail.html)

Edit `students/templates/students/course_detail.html`:

```django
{% extends 'students/base.html' %}

{% block title %}{{ course.name }} - Course Details{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <h1 class="mb-4"><i class="fas fa-book-open"></i> {{ course.name }}</h1>
        
        <!-- TODO 5: Course Information Card
             - Course name, instructor, credits
             - Description
             - Student count with badge
             - Enrollment table showing students
        -->
    </div>
    
    <div class="col-lg-4">
        <!-- TODO 5a: Sidebar with course stats
             - Total enrollments
             - Credits
             - Action buttons
        -->
    </div>
</div>

{% endblock %}
```

### Step 6: Enrollment List Template (enrollment_list.html)

Edit `students/templates/students/enrollment_list.html`:

```django
{% extends 'students/base.html' %}

{% block title %}Enrollments{% endblock %}

{% block content %}
<h1 class="mb-4"><i class="fas fa-clipboard-list"></i> All Enrollments</h1>

<!-- TODO 6: Enrollment Data Table
     - Columns: Student, Course, Enrollment Date, Grade
     - Sort by date descending
     - Status badge (active/completed)
     - Action buttons
     - Pagination (bonus)
-->

<div class="table-responsive">
    <table class="table table-striped table-hover">
        <thead class="table-primary">
            <tr>
                <th>Student</th>
                <th>Course</th>
                <th>Enrollment Date</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <!-- TODO 6a: Loop through enrollments
                 - Student name and ID
                 - Course name
                 - Date with format
                 - Status badge
                 - View/Delete buttons
            -->
        </tbody>
    </table>
</div>

{% endblock %}
```

### Step 7: Student Detail Template (student_detail.html)

Edit `students/templates/students/student_detail.html`:

```django
{% extends 'students/base.html' %}

{% block title %}{{ student.name }} - Student Profile{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-4">
        <!-- TODO 7: Student Profile Card
             - Photo placeholder (if needed)
             - Student info (name, roll_no, email)
             - Enrollment count badge
        -->
    </div>
    
    <div class="col-lg-8">
        <!-- TODO 7a: Enrolled Courses Table
             - Courses student is enrolled in
             - Progress or status
             - Grade/Score if available
        -->
    </div>
</div>

{% endblock %}
```

### Step 8: Custom CSS (style.css)

Edit `students/static/students/css/style.css`:

```css
/* TODO 8: Custom Styling
   - Define CSS variables that work with any Bootswatch theme
   - Card hover effects
   - Table row hover effects
   - Button animations
   - Responsive adjustments
*/

:root {
    --transition-duration: 0.3s ease;
}

.card {
    transition: transform var(--transition-duration), box-shadow var(--transition-duration);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.table tbody tr:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

.badge {
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
}

/* Action buttons styling */
.btn-sm {
    transition: all var(--transition-duration);
}

.btn-sm:hover {
    transform: scale(1.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .table {
        font-size: 0.9rem;
    }
    
    .btn-sm {
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
    }
}
```

### Step 9: JavaScript (main.js)

Edit `students/static/students/js/main.js`:

```javascript
// TODO 9: Dynamic Functionality
// - Initialize Bootstrap tooltips
// - Handle delete confirmations
// - Sort table columns (bonus)
// - Search/filter functionality (bonus)

document.addEventListener('DOMContentLoaded', function() {
    // Display current year in footer
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure?')) {
                e.preventDefault();
            }
        });
    });
});
```

## Bootstrap Tables Reference

### Basic Table
```html
<table class="table">
    <thead>
        <tr><th>Column</th></tr>
    </thead>
    <tbody>
        <tr><td>Data</td></tr>
    </tbody>
</table>
```

### Table Variants
- `.table-striped` - Alternating row colors
- `.table-hover` - Highlight on hover
- `.table-sm` - Smaller cells
- `.table-dark` - Dark background
- `.table-primary`, `.table-success` - Themed colors

### Responsive Tables
```html
<div class="table-responsive">
    <table class="table"><!-- Content --></table>
</div>
```

## Bootswatch Themes Overview

Popular themes:
- **darkly** - Dark background, light text (great for eyes)
- **flatly** - Flat design, minimal shadows
- **journal** - Clean, professional
- **lumen** - Light, modern
- **lux** - Premium look
- **materia** - Material design
- **pulse** - Colorful, energetic
- **superhero** - Dark with bright accents
- **yeti** - Clean, minimal

Try different themes by changing the CDN URL:
```html
<!-- Darkly Theme -->
<link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/darkly/bootstrap.min.css">

<!-- Flatly Theme -->
<link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/flatly/bootstrap.min.css">

<!-- Lux Theme -->
<link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/lux/bootstrap.min.css">
```

## Font Awesome Icons for Tables

**Action Icons:**
- `fa-eye` - View
- `fa-edit` - Edit
- `fa-trash` - Delete
- `fa-download` - Download
- `fa-share` - Share
- `fa-print` - Print

**Status Icons:**
- `fa-check-circle` - Success
- `fa-times-circle` - Error
- `fa-info-circle` - Info
- `fa-warning` - Warning
- `fa-star` - Rating/Important

**Data Icons:**
- `fa-users` - Students/People
- `fa-book` - Courses
- `fa-clipboard` - Enrollment
- `fa-chart-bar` - Statistics
- `fa-calendar` - Date

Example Usage:
```html
<a href="#" class="btn btn-sm btn-primary">
    <i class="fas fa-eye"></i> View
</a>

<a href="#" class="btn btn-sm btn-warning">
    <i class="fas fa-edit"></i> Edit
</a>

<a href="#" class="btn btn-sm btn-danger btn-delete">
    <i class="fas fa-trash"></i> Delete
</a>
```

## Key Concepts

### Responsive Tables
```html
<div class="table-responsive">
    <table class="table">
        <!-- Table becomes scrollable on small screens -->
    </table>
</div>
```

### Badges for Status
```html
<!-- Display badges for status info -->
<span class="badge bg-success"><i class="fas fa-check"></i> Enrolled</span>
<span class="badge bg-warning"><i class="fas fa-hourglass"></i> Pending</span>
<span class="badge bg-danger"><i class="fas fa-times"></i> Inactive</span>
```

### Card Components
```html
<div class="card">
    <div class="card-header">
        <h5 class="card-title">Title</h5>
    </div>
    <div class="card-body">
        Content here
    </div>
    <div class="card-footer">
        <small class="text-muted">Footer</small>
    </div>
</div>
```

### Two-Column Layout
```html
<div class="row">
    <div class="col-lg-8">
        <!-- Main content (2/3 width on large screens) -->
    </div>
    <div class="col-lg-4">
        <!-- Sidebar (1/3 width on large screens) -->
    </div>
</div>
```

## Running Your Application

### 1. Activate Virtual Environment

```bash
cd assignment2
source venv/bin/activate
```

### 2. Run Development Server

```bash
python manage.py runserver
```

### 3. Visit in Browser

- Students: http://localhost:8000/students/
- Courses: http://localhost:8000/courses/
- Enrollments: http://localhost:8000/enrollments/

## Reference Solutions

When stuck, check:
- `base_solution.html` - Complete navbar with theme
- `student_list_solution.html` - Table layout
- `course_list_solution.html` - Card grid layout
- `course_detail_solution.html` - Detail view with table
- `enrollment_list_solution.html` - Enrollment table
- `student_detail_solution.html` - Profile with courses
- `style.css` - Custom styling
- `main.js` - Dynamic functionality

## Testing Your Frontend

### Visual Testing Checklist
- [ ] Navbar appears with all links
- [ ] Theme colors applied throughout
- [ ] Cards display with hover effects
- [ ] Tables are responsive (test on mobile)
- [ ] Badges show correct status
- [ ] Buttons have icons and hover effects
- [ ] Footer shows current year
- [ ] All pages have breadcrumbs

### Responsive Testing
1. Press F12 in browser
2. Click device toggle (mobile icon)
3. Test on:
   - Mobile (375px)
   - Tablet (768px)
   - Desktop (1200px)
4. Verify:
   - Navbar collapses on mobile
   - Tables become scrollable
   - Cards stack vertically
   - Text remains readable

### Performance Check
- Open DevTools Network tab
- Verify CSS loads from CDN
- Check Font Awesome loads
- File sizes should be minimal

## Advanced Features (Bonus)

### 1. Table Search
```javascript
document.getElementById('search').addEventListener('keyup', function() {
    const value = this.value.toLowerCase();
    document.querySelectorAll('table tbody tr').forEach(row => {
        row.style.display = row.textContent.toLowerCase().includes(value) ? '' : 'none';
    });
});
```

### 2. Delete Confirmation Modal
```html
<div class="modal fade" id="deleteModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Confirm Delete</h5>
            </div>
            <div class="modal-body">
                Are you sure?
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-danger">Delete</button>
            </div>
        </div>
    </div>
</div>
```

### 3. Sort Table Columns
```javascript
document.querySelectorAll('th').forEach(header => {
    header.style.cursor = 'pointer';
    header.addEventListener('click', function() {
        // Implement column sorting
    });
});
```

## Next Steps

1. Explore Bootswatch theme variations
2. Try different Font Awesome icon sets
3. Add pagination to tables
4. Implement search/filter functionality
5. Create responsive navigation drawer
6. Add animations with CSS transitions
7. Implement dark mode toggle
8. Create print-friendly stylesheets

---

**Build Professional UIs!** 🎨

Created: February 17, 2026
