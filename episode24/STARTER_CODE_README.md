# Episode 24 Starter Code Guide

## Overview

This directory contains **starter code** for Episode 24: AI-Assisted Development with GitHub Copilot.

Two folders are provided:
- `assignment1_starter/` - Topics 1-40: Copilot Fundamentals
- `assignment2_starter/` - Topics 41-80: Query Optimization & Professional Workflows

## Structure

### Assignment 1 Starter (`assignment1_starter/`)

**What's Provided:**
- ✅ `manage.py` - Django management script
- ✅ `myapp/settings.py` - Configured Django settings
- ✅ `myapp/urls.py` - Main URL config (with TODO)
- ✅ `myapp/wsgi.py` - WSGI application
- ✅ `templates/base.html` - HTML skeleton (with TODO)
- ✅ `tasks/__init__.py` - Empty init file

**What You Need to Create:**
- ❌ `tasks/models.py` - Task model with 6 fields (see TODO comments)
- ❌ `tasks/forms.py` - TaskForm with Bootstrap widgets
- ❌ `tasks/views.py` - 5 CRUD views (list, create, detail, update, delete)
- ❌ `tasks/urls.py` - URL patterns with app_name
- ❌ `tasks/admin.py` - TaskAdmin registration
- ❌ `tasks/tests.py` - 32 test functions with topics
- ❌ `templates/task_list.html` - Task table template
- ❌ `templates/task_form.html` - Create/Update form template
- ❌ `templates/task_detail.html` - Task detail template
- ❌ `templates/task_confirm_delete.html` - Delete confirmation template

**Topics Covered (1-30):**
- Topics 1-5: Models, string representation, field types, ordering
- Topics 6-9: Forms, validation, widgets, ModelForm
- Topics 10-14: Views, templates, context data, GET requests
- Topics 15-20: Messages framework, error handling, deletions
- Topics 21-30: Detail views, updates, CRUD patterns, URL naming

### Assignment 2 Starter (`assignment2_starter/`)

**What's Provided:**
- ✅ `manage.py` - Django management script
- ✅ `myapp/settings.py` - Configured Django settings
- ✅ `myapp/urls.py` - Main URL config (with TODO)
- ✅ `myapp/wsgi.py` - WSGI application
- ✅ `templates/base.html` - HTML skeleton (with TODO)
- ✅ `analytics/__init__.py` - Empty init file

**What You Need to Create:**
- ❌ `analytics/models.py` - 3 models: Project, Event, Analytics
- ❌ `analytics/forms.py` - ProjectForm & EventForm with validation
- ❌ `analytics/views.py` - 7 optimized views with query optimization
- ❌ `analytics/urls.py` - URL patterns with app_name
- ❌ `analytics/admin.py` - 3 admin registrations
- ❌ `analytics/tests.py` - 41 test functions with topics
- ❌ `templates/analytics_dashboard.html` - Dashboard with stats
- ❌ `templates/project_list.html` - Project cards
- ❌ `templates/project_detail.html` - Project details with events
- ❌ `templates/project_form.html` - Create/Update form
- ❌ `templates/event_form.html` - Event logging form
- ❌ `templates/event_bulk_form.html` - Bulk event creation

**Topics Covered (41-80):**
- Topics 41-49: Models, relationships (FK, OneToOne), Meta options
- Topics 50-57: Query optimization (select_related, prefetch_related, aggregates)
- Topics 58-65: Form validation, widgets, view patterns, messages
- Topics 66-73: Bulk operations, performance, indexing, efficiency
- Topics 74-80: Error handling, data integrity, security, documentation, testing

## Getting Started

### For Assignment 1:

1. **Create Task Model** (`tasks/models.py`)
   - Look at the TODO comments for field specifications
   - Add PRIORITY_CHOICES
   - Add Meta class with ordering
   - Add __str__ method

2. **Create TaskForm** (`tasks/forms.py`)
   - Create ModelForm inheriting from forms.ModelForm
   - Add widgets for Bootstrap styling (form-control, form-check-input)
   - Specify fields and widgets in Meta class

3. **Create Views** (`tasks/views.py`)
   - Implement 5 views: list, create, detail, update, delete
   - Use get_object_or_404 for safety
   - Use messages framework for feedback
   - Follow POST-Redirect-GET pattern

4. **Add URL Routing** (`tasks/urls.py`)
   - Map URLs to views
   - Use namespacing with app_name = 'tasks'

5. **Register in Admin** (`tasks/admin.py`)
   - Use @admin.register decorator
   - Add list_display, list_filter, search_fields

6. **Create Templates** (5 templates)
   - Extend base.html
   - Use Bootstrap 5 classes
   - Display data and forms

7. **Write Tests** (`tasks/tests.py`)
   - Each test function has a topic number
   - Implement tests following the test class structure
   - Test models, forms, views, patterns

### For Assignment 2:

1. **Create 3 Models** (`analytics/models.py`)
   - Project: name, description, timestamps, is_active
   - Event: ForeignKey to Project, event_type choices, duration_ms
   - Analytics: OneToOneField to Project, aggregated data fields
   - Add Meta.indexes for performance

2. **Create Forms** (`analytics/forms.py`)
   - ProjectForm: name, description, is_active
   - EventForm: project, event_type, user_id, url, duration_ms
   - Add custom validation for duration_ms >= 0

3. **Create Optimized Views** (`analytics/views.py`)
   - Use select_related('analytics') for one-to-one relationships
   - Use prefetch_related('events') for reverse relationships
   - Use aggregate() for Count, Avg, filtered queries
   - Use bulk_create() for multiple events

4. **Add URL Routing** (`analytics/urls.py`)
   - 7 URL patterns with app_name = 'analytics'
   - See TODO comment for pattern list

5. **Register in Admin** (`analytics/admin.py`)
   - Register all 3 models
   - Add appropriate admin options

6. **Create Templates** (7 templates)
   - Dashboard with stats cards
   - Project list and detail views
   - Forms for create/update/events

7. **Write Tests** (`analytics/tests.py`)
   - 41 test functions across 9 test classes
   - Test relationships, optimization, aggregation, forms, views

## Key Patterns to Implement

### Assignment 1 - Basic CRUD
```python
# Views follow this pattern:
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Created successfully!')
            return redirect('tasks:list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Deleted successfully!')
        return redirect('tasks:list')
    return render(request, 'task_confirm_delete.html', {'task': task})
```

### Assignment 2 - Query Optimization
```python
# Use select_related for one-to-one/foreign key
projects = Project.objects.select_related('analytics').all()

# Use prefetch_related for reverse relationships
projects = Project.objects.prefetch_related('events').all()

# Use aggregate for calculations
stats = Event.objects.aggregate(
    total=Count('id'),
    views=Count('id', filter=Q(event_type='view')),
    avg_duration=Avg('duration_ms')
)

# Use bulk_create for efficiency
events = [
    Event(project=p, event_type='view'),
    Event(project=p, event_type='click'),
]
Event.objects.bulk_create(events)
```

## Testing

Run tests with:
```bash
cd assignment1_starter
python manage.py test tasks.tests --verbosity=2

cd ../assignment2_starter
python manage.py test analytics.tests --verbosity=2
```

Expected results:
- Assignment 1: 32/32 tests passing
- Assignment 2: 41/41 tests passing

## TODO Checklist

### Assignment 1
- [ ] Create Task model
- [ ] Create TaskForm
- [ ] Write 5 views
- [ ] Add URL patterns
- [ ] Register in admin
- [ ] Create 4 templates
- [ ] Implement 32 tests
- [ ] All tests passing ✅

### Assignment 2
- [ ] Create Project, Event, Analytics models
- [ ] Create ProjectForm, EventForm
- [ ] Write 7 optimized views
- [ ] Add URL patterns
- [ ] Register all 3 models in admin
- [ ] Create 7 templates
- [ ] Implement 41 tests
- [ ] All tests passing ✅

## Files Included

```
episode24/
├── assignment1_starter/
│   ├── manage.py
│   ├── myapp/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── models.py (TODO)
│   │   ├── forms.py (TODO)
│   │   ├── views.py (TODO)
│   │   ├── urls.py (TODO)
│   │   ├── admin.py (TODO)
│   │   └── tests.py (TODO)
│   └── templates/
│       └── base.html (skeleton)
│
├── assignment2_starter/
│   ├── manage.py
│   ├── myapp/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── models.py (TODO)
│   │   ├── forms.py (TODO)
│   │   ├── views.py (TODO)
│   │   ├── urls.py (TODO)
│   │   ├── admin.py (TODO)
│   │   └── tests.py (TODO)
│   └── templates/
│       └── base.html (skeleton)
│
└── STARTER_CODE_README.md (this file)
```

## Tips

1. **Use Copilot**: These starter files are designed to work with GitHub Copilot. The TODO comments guide Copilot to generate appropriate code.

2. **Topic Coverage**: Each test function is mapped to a topic. Implement code to make tests pass.

3. **Bootstrap**: Use Bootstrap 5 classes (form-control, form-select, form-check-input) for consistent styling.

4. **Messages Framework**: Always provide user feedback with messages.success(), messages.error(), etc.

5. **Query Optimization**: In Assignment 2, focus on reducing database queries with select_related/prefetch_related.

6. **Testing**: Write tests as you implement features, not after.

---

**Total Topics**: 80
**Total Tests**: 73 (32 + 41)
**All Tests Should Pass**: ✅
