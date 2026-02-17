# Episode 18 - Assignment 1: Bootstrap Frontend Styling

## Learning Objectives

After completing this assignment, you should understand:

1. **Bootstrap Framework** - Responsive CSS framework for rapid UI development
2. **Bootstrap Grid System** - 12-column responsive layout
3. **Bootstrap Components** - Cards, buttons, badges, navbars
4. **Django Static Files** - CSS, JS, and images organization
5. **Template Inheritance** - Base templates and template blocks
6. **Font Awesome Icons** - Adding icons to UI elements
7. **Responsive Design** - Creating layouts that work on all devices
8. **CSS Utilities** - Using Bootstrap utility classes for styling
9. **Custom CSS** - Adding custom styling with CSS variables
10. **Dynamic Content** - Using JavaScript with Bootstrap

## What You'll Build

A professional-looking student management interface with:
- Bootstrap navbar with navigation
- Student list displayed as responsive cards
- Student detail page with information cards
- Bootstrap footer with current year
- Font Awesome icons throughout
- Responsive design for all devices
- Custom CSS styling

## Files Overview

```
assignment1/
├── students/
│   ├── templates/students/
│   │   ├── base.html                ← TODO 1-2: Create navbar and footer
│   │   ├── base_solution.html       (Reference)
│   │   ├── list.html                ← TODO 3: Bootstrap card layout
│   │   ├── list_bootstrap.html      (Reference)
│   │   ├── detail.html              ← TODO 4: Bootstrap detail layout
│   │   └── detail_bootstrap.html    (Reference)
│   ├── static/students/
│   │   ├── css/
│   │   │   └── style.css            ← TODO 1-2: Custom CSS with variables
│   │   └── js/
│   │       └── main.js              ← TODO 2: Dynamic year, interactions
│   ├── models.py                    (From Episode 17)
│   └── views.py                     (From Episode 17)
├── myproject/
│   ├── settings.py                  (Already configured)
│   └── urls.py                      (Already configured)
└── manage.py
```

## Step-by-Step Instructions

### Step 1: Understand Template Inheritance

In Django templates, we use `{% extends %}` to inherit from a base template:

```django
{% extends 'students/base.html' %}

{% block content %}
    Your content here
{% endblock %}
```

### Step 2: Create Base Template (base.html)

Edit `students/templates/students/base.html`:

```django
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Student Management{% endblock %}</title>
    
    <!-- Bootstrap CSS from CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Font Awesome CSS from CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{% static 'students/css/style.css' %}">
</head>
<body>
    <!-- TODO 1: Add Navbar Component
         - Use .navbar, .navbar-expand-lg, .navbar-dark, .bg-dark
         - Brand: "Student Management" with icon
         - Nav items with Font Awesome icons
         - Responsive hamburger menu
    -->
    
    <!-- Main Content -->
    <div class="container-fluid mt-4">
        {% block content %}{% endblock %}
    </div>
    
    <!-- TODO 2: Add Footer Component
         - Dark background with text-white
         - Copyright with dynamic year using JS
         - Contact information
         - Font Awesome social icons
    -->
    
    <!-- Bootstrap JS from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <!-- Custom JS -->
    <script src="{% static 'students/js/main.js' %}"></script>
</body>
</html>
```

### Step 3: Create List Template (list.html)

Edit `students/templates/students/list.html`:

```django
{% extends 'students/base.html' %}

{% block title %}Student List{% endblock %}

{% block content %}
<h1 class="mb-4"><i class="fas fa-list"></i> Student List</h1>

<!-- TODO 3: Bootstrap Card Grid Layout
     - Use .row and .col-md-6 (2 columns on medium screens)
     - Create .card for each student
     - Show: name, roll_no, email, fees_paid
     - Use .badge for fees status (bg-success or bg-danger)
     - Add Font Awesome icons for each field
     - Include View button with fa-eye icon
     - Add empty state with message if no students
-->

{% endblock %}
```

**Key Bootstrap Classes:**
- `.row` - Grid row container
- `.col-md-6` - Half width on medium screens
- `.card` - Container for content
- `.card-body` - Card content area
- `.card-footer` - Footer section
- `.badge` - Small status indicator
- `.btn` - Button styling
- `.text-primary`, `.text-success` - Text colors
- `.mb-4` - Bottom margin (m = margin, b = bottom, 4 = size)
- `.shadow-sm` - Subtle drop shadow
- `.h-100` - Full height

### Step 4: Create Detail Template (detail.html)

Edit `students/templates/students/detail.html`:

```django
{% extends 'students/base.html' %}

{% block title %}{{ student.name }} - Student Details{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8 mx-auto">
        <h1 class="mb-4"><i class="fas fa-user-circle"></i> Student Details</h1>
        
        <!-- TODO 4: Bootstrap Detail Card
             - Use .card with shadow
             - Card header with student name
             - Display fields with icons
             - Show badges for fees status
             - Format date with Django date filter
             - Add back button with fa-arrow-left icon
        -->
    </div>
</div>
{% endblock %}
```

### Step 5: Add Custom CSS (style.css)

Edit `students/static/students/css/style.css`:

```css
/* TODO 1: Define CSS Custom Properties and Styling
   - Define color variables in :root
   - Add hover effects for cards
   - Style navbar and footer
   - Add transitions for smooth animations
*/

:root {
    --primary-color: #007bff;
    --success-color: #28a745;
    --danger-color: #dc3545;
}

body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.hover-shadow {
    transition: box-shadow 0.3s ease;
}

.hover-shadow:hover {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
}
```

### Step 6: Add JavaScript (main.js)

Edit `students/static/students/js/main.js`:

```javascript
// TODO 2: Add Dynamic Content
// Display current year in footer
document.addEventListener('DOMContentLoaded', function() {
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
});
```

## Bootstrap Classes Reference

### Layout
- `.container` - Fixed-width responsive container
- `.container-fluid` - Full-width container
- `.row` - Horizontal group of columns
- `.col-*` - Column (1-12 width)

### Responsive Breakpoints
- `.col-md-6` - Half width on medium screens (768px+)
- `.col-lg-8` - 2/3 width on large screens (992px+)
- `.d-md-none` - Hide on medium screens and up
- `.d-none d-md-block` - Show only on medium screens and up

### Spacing
- `.m-*` - Margin (m3 = 1rem, m5 = 3rem)
- `.mb-4` - Margin bottom 1.5rem
- `.mt-4` - Margin top 1.5rem
- `.p-*` - Padding
- `.mx-auto` - Horizontal auto margin (center)

### Colors
- `.text-primary` - Primary color text
- `.text-success` - Green text
- `.text-danger` - Red text
- `.bg-dark` - Dark background
- `.bg-light` - Light background

### Shadows
- `.shadow` - Large shadow
- `.shadow-sm` - Small shadow
- `.shadow-lg` - Extra large shadow

## Font Awesome Icons

Common icons to use:
- `fa-list` - List
- `fa-user-graduate` - Student
- `fa-users` - Multiple users
- `fa-user-circle` - User profile
- `fa-eye` - View
- `fa-edit` - Edit
- `fa-trash` - Delete
- `fa-check` - Success
- `fa-times` - Error
- `fa-home` - Home
- `fa-envelope` - Email
- `fa-id-card` - ID
- `fa-money-bill` - Money/Fees
- `fa-calendar` - Date
- `fa-arrow-left` - Back

Usage:
```html
<i class="fas fa-user-graduate"></i>  <!-- Solid icon -->
<i class="fa-2x"></i>                <!-- 2x size -->
<i class="text-primary"></i>         <!-- Primary color -->
```

## Key Concepts

### Static Files in Django

1. **File Location**
   ```
   app/static/app/css/style.css
   app/static/app/js/main.js
   ```

2. **Loading in Template**
   ```django
   {% load static %}
   <link rel="stylesheet" href="{% static 'app/css/style.css' %}">
   ```

3. **In Development**
   - Django serves static files automatically when DEBUG=True

4. **In Production**
   - Run: `python manage.py collectstatic`
   - Web server serves from STATIC_ROOT

### Template Inheritance

1. **Base Template** defines blocks
2. **Child Templates** extend base and override blocks
3. **DRY** - Don't Repeat Yourself

```django
<!-- base.html -->
{% block content %}{% endblock %}

<!-- list.html -->
{% extends 'base.html' %}
{% block content %}
    Student list here
{% endblock %}
```

### Bootstrap Grid

- 12-column system
- Responsive at different breakpoints
- Automatic wrapping

```html
<!-- 2 equal columns -->
<div class="row">
    <div class="col-md-6">Column 1</div>
    <div class="col-md-6">Column 2</div>
</div>

<!-- 3 equal columns -->
<div class="row">
    <div class="col-md-4">Col 1</div>
    <div class="col-md-4">Col 2</div>
    <div class="col-md-4">Col 3</div>
</div>
```

## Running Your Application

### 1. Ensure Static Files Configuration

Edit `myproject/settings.py`:

```python
STATIC_URL = '/static/'

# If needed
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### 2. Collect Static Files (Optional in Development)

```bash
python manage.py collectstatic --noinput
```

### 3. Run Development Server

```bash
python manage.py runserver
```

### 4. Visit in Browser

- Students: http://localhost:8000/students/
- Student Detail: http://localhost:8000/students/1/

## Reference Solutions

When stuck, check:
- `base_solution.html` - Complete navbar and footer
- `list_bootstrap.html` - Card-based list layout
- `detail_bootstrap.html` - Styled detail view
- `style.css` - Custom CSS with variables
- `main.js` - JavaScript functionality

## Testing Your Frontend

### Visual Testing
1. Open http://localhost:8000/students/
2. Check navbar appears with responsive menu
3. Check cards display correctly
4. Check footer shows current year
5. Click View button to test detail page
6. Test on mobile (Chrome DevTools F12)

### Responsive Testing
1. Press F12 in browser
2. Click device toggle (mobile icon)
3. Test different screen sizes
4. Verify layout adapts

## Common Bootstrap Patterns

### Card Grid
```html
<div class="row">
    {% for item in items %}
    <div class="col-md-6 col-lg-4">
        <div class="card h-100">
            <div class="card-body">
                <!-- Content -->
            </div>
        </div>
    </div>
    {% endfor %}
</div>
```

### Centered Content
```html
<div class="row">
    <div class="col-lg-8 mx-auto">
        <!-- Content -->
    </div>
</div>
```

### Navbar
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="/">Brand</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link" href="#">Link</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

## Next Steps

1. Explore other Bootstrap components (modals, forms, alerts)
2. Try Bootswatch themes (swap CDN URL)
3. Add more Font Awesome icons
4. Create custom color scheme
5. Add animations and transitions

---

**Happy Styling!** 🎨

Created: February 17, 2026
3. Create relationships between models (ForeignKey)
4. Add forms for creating/updating students (Episode 18)

---

**Happy Learning!** 🎓

Created: February 17, 2026
Status: Ready for Student Implementation
