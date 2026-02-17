# Episode 18 - Quick Setup & Getting Started

## What You're Learning

Episode 18 teaches you to build **professional-looking web interfaces** using Bootstrap CSS framework, Font Awesome icons, and modern frontend design patterns. This is about making your Django apps look polished and user-friendly.

## Assignment Overview

### Assignment 1: Basic Bootstrap Styling (Beginner)
**Focus:** Learn Bootstrap fundamentals
- ✅ Template inheritance patterns
- ✅ Responsive card layouts
- ✅ Bootstrap grid system
- ✅ Font Awesome icons
- ✅ Custom CSS styling

**Time:** 1-2 hours

### Assignment 2: Advanced Bootswatch & Tables (Intermediate)
**Focus:** Professional data presentation
- ✅ Bootswatch theme integration (choose from 26 themes)
- ✅ Responsive data tables
- ✅ Multi-page navigation
- ✅ Badge and status indicators
- ✅ Advanced JavaScript

**Time:** 1-2 hours

## Quick Start - Assignment 1

### 1. Open Terminal & Navigate
```bash
cd /Users/enfec/Desktop/Python\ Assignment\ Ep\ 12-24/Python-Assignment-Ep-12--24/episode18/assignment1/myapp
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 3. Run Development Server
```bash
python manage.py runserver
```

### 4. Open Browser
Visit: http://localhost:8000/students/

You'll see a simple list of students. Your job: **Make it look professional with Bootstrap!**

## What to Do

### Step 1: Edit Base Template
📄 File: `students/templates/students/base.html`

**Add Navbar:**
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">
            <i class="fas fa-graduation-cap"></i> Student Manager
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'student_list' %}">
                        <i class="fas fa-list"></i> Students
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

**Add Footer:**
```html
<footer class="bg-dark text-white mt-5 py-4">
    <div class="container-fluid text-center">
        <p class="mb-0">
            <i class="fas fa-copyright"></i> <span id="year"></span> Student Manager
        </p>
    </div>
</footer>
```

### Step 2: Edit List Template
📄 File: `students/templates/students/list.html`

**Change from:**
```html
<!DOCTYPE html>
<html>
```

**To:**
```html
{% extends 'students/base.html' %}
{% block content %}
<h1 class="mb-4"><i class="fas fa-list"></i> Students</h1>

<div class="row">
    {% for student in students %}
    <div class="col-md-6 col-lg-4 mb-4">
        <div class="card h-100">
            <div class="card-body">
                <h5 class="card-title">
                    <i class="fas fa-user-graduate"></i> {{ student.name }}
                </h5>
                <p class="card-text">Roll: {{ student.roll_no }}</p>
                {% if student.fees_paid %}
                    <span class="badge bg-success"><i class="fas fa-check"></i> Paid</span>
                {% else %}
                    <span class="badge bg-danger"><i class="fas fa-times"></i> Pending</span>
                {% endif %}
            </div>
            <div class="card-footer bg-light">
                <a href="{% url 'student_detail' student.id %}" class="btn btn-sm btn-primary">
                    <i class="fas fa-eye"></i> View
                </a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

### Step 3: Edit Detail Template
📄 File: `students/templates/students/detail.html`

**Change from HTML to:**
```html
{% extends 'students/base.html' %}
{% block title %}{{ student.name }}{% endblock %}
{% block content %}
<div class="row">
    <div class="col-lg-8 mx-auto">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0"><i class="fas fa-id-card"></i> Student Details</h4>
            </div>
            <div class="card-body">
                <p><strong><i class="fas fa-user"></i> Name:</strong> {{ student.name }}</p>
                <p><strong><i class="fas fa-code"></i> Roll No:</strong> {{ student.roll_no }}</p>
                <p><strong><i class="fas fa-envelope"></i> Email:</strong> {{ student.email }}</p>
                <p>
                    <strong><i class="fas fa-money-bill"></i> Fees:</strong>
                    {% if student.fees_paid %}
                        <span class="badge bg-success">Paid</span>
                    {% else %}
                        <span class="badge bg-danger">Pending</span>
                    {% endif %}
                </p>
                <p><strong><i class="fas fa-calendar"></i> Date:</strong> {{ student.created_at|date:"d-m-Y" }}</p>
            </div>
            <div class="card-footer">
                <a href="{% url 'student_list' %}" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i> Back
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Step 4: Add CSS
📄 File: `students/static/students/css/style.css`

```css
:root {
    --primary-color: #007bff;
}

body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

main {
    flex: 1;
}

.card {
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15) !important;
}

footer {
    margin-top: auto;
}
```

### Step 5: Add JavaScript
📄 File: `students/static/students/js/main.js`

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const yearSpan = document.getElementById('year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
});
```

## View Your Result

**Refresh browser:** http://localhost:8000/students/

You should now see:
- 📱 Responsive navbar with gradient
- 🎨 Beautiful card layout
- ⭐ Font Awesome icons throughout
- 📱 Mobile-friendly design
- ✨ Smooth hover effects

## Assignment 2 Quick Start

```bash
cd ../assignment2/myapp
source venv/bin/activate
python manage.py runserver
```

Visit: http://localhost:8000/students/

### What's Different in Assignment 2?

1. **Bootswatch Themes** - 26 professional themes to choose from
2. **Data Tables** - Display student/course data in tables
3. **Complex Layouts** - Sidebar + main content
4. **Advanced Icons** - More Font Awesome usage

### Choose a Bootswatch Theme

Edit `base.html` and change:
```html
<!-- Original -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">

<!-- To Darkly theme -->
<link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/darkly/bootstrap.min.css">

<!-- Other themes: flatly, lux, morph, superhero, yeti, etc. -->
```

## Bootstrap Classes You Need

### Layout
- `.row` - Container for columns
- `.col-md-6` - Half width on medium screens
- `.col-lg-4` - One-third width on large screens
- `.container-fluid` - Full width

### Components
- `.card` - Content container
- `.table` - Data table
- `.badge` - Small label
- `.btn` - Button
- `.navbar` - Navigation bar

### Spacing
- `.mb-4` - Margin bottom 1.5rem
- `.mt-3` - Margin top 1rem
- `.px-3` - Padding left & right 1rem
- `.mx-auto` - Center horizontally

### Colors
- `.bg-primary` - Blue background
- `.bg-success` - Green background
- `.bg-danger` - Red background
- `.text-muted` - Gray text
- `.text-white` - White text

## Font Awesome Icons to Use

```html
<!-- Most common -->
<i class="fas fa-graduation-cap"></i>  <!-- Student -->
<i class="fas fa-users"></i>           <!-- People -->
<i class="fas fa-book"></i>            <!-- Course -->
<i class="fas fa-user-graduate"></i>   <!-- Graduate -->
<i class="fas fa-check"></i>           <!-- Success -->
<i class="fas fa-times"></i>           <!-- Error -->
<i class="fas fa-eye"></i>             <!-- View -->
<i class="fas fa-edit"></i>            <!-- Edit -->
<i class="fas fa-trash"></i>           <!-- Delete -->
```

## Troubleshooting

### "Bootstrap not styling my HTML"
✅ Make sure Bootstrap CDN link is in `<head>`
✅ Check for typos in class names
✅ Clear browser cache (Ctrl+Shift+Delete)

### "Icons not showing"
✅ Verify Font Awesome CDN link is correct
✅ Use `fas` prefix (fa-solid)
✅ Check icon name on fontawesome.com

### "Layout broken on mobile"
✅ Add `<meta name="viewport">` tag
✅ Use responsive classes (col-md-6, col-lg-4)
✅ Test in actual mobile device

## Testing Your Work

### On Desktop
- [ ] Navbar visible with hamburger menu
- [ ] Cards stack in nice grid
- [ ] Hover effects work
- [ ] All icons display
- [ ] Colors look good

### On Mobile (F12 > Toggle device toolbar)
- [ ] Layout stacks vertically
- [ ] Navbar collapses
- [ ] Text readable
- [ ] Buttons clickable
- [ ] No horizontal scroll

## Reference Solutions

If you get stuck:
- `base_solution.html` - Complete base template
- `list_bootstrap.html` / `list_solution.html` - Complete list
- `detail_bootstrap.html` / `detail_solution.html` - Complete detail
- `style.css` - Complete CSS
- `main.js` - Complete JavaScript

## Tips for Success

### Start Simple
1. Get navbar working first
2. Then convert list view
3. Then convert detail view
4. Finally, add CSS and JavaScript

### Test Frequently
- Refresh browser after each change
- Check console for errors (F12 → Console)
- Test on mobile size

### Use Reference Solutions
- Look at `_solution.html` files when stuck
- Copy patterns, don't copy entire file
- Understand what each class does

### Customize
- Change colors: Edit CSS variables
- Change theme: Edit CDN URL
- Add more icons: Visit fontawesome.com
- Add animations: Add CSS transitions

## Learning Resources

### Bootstrap
- Official Docs: https://getbootstrap.com/docs/5.3/
- Grid System: https://getbootstrap.com/docs/5.3/layout/grid/
- Components: https://getbootstrap.com/docs/5.3/components/

### Bootswatch
- Themes: https://bootswatch.com/
- Preview: Try each theme online

### Font Awesome
- Icon Search: https://fontawesome.com/icons
- Cheatsheet: https://fontawesome.com/cheatsheet

## Time Estimate

- **Assignment 1:** 1-2 hours
- **Assignment 2:** 1-2 hours
- **Total:** 2-4 hours for full Episode 18

## What's Next?

After Episode 18, you'll have:
✅ Beautiful, professional UI
✅ Mobile-responsive design
✅ Modern web development skills
✅ Foundation for advanced JavaScript

Next episodes will add:
- REST APIs
- User authentication
- Real-time features
- JavaScript frameworks

---

**Happy Styling!** 🎨

If you get stuck, check:
1. Reference solution files
2. Bootstrap documentation
3. Browser console for errors (F12)
4. README files for detailed instructions

You've got this! 💪
