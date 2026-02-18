# Episode 19: Static Files, Media Management, and Galleries - Starter Code Guide

## Overview
Episode 19 covers Django's static files system and media file management. Students progress from basic static file configuration and CSS/JavaScript integration (Assignment 1) to advanced media handling with image galleries and comments (Assignment 2).

**Total Tests:** 80+ (40+ per assignment)
- Assignment 1: 40 tests on static files, CSS, images, and media configuration
- Assignment 2: 40+ tests on galleries, images, comments, and media handling

---

## Assignment 1: Static Files and Image Management

### Topics Covered: 1-40

### What Students Implement

#### 1. **Static Files Configuration** (Topics 1-10)
```python
# settings.py - Topics 1-10

# Topic 1: STATIC_URL - URL path for static files
STATIC_URL = '/static/'

# Topic 2: STATIC_ROOT - Directory where staticfiles are collected
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Topic 3: STATICFILES_DIRS - Additional static file directories
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Topic 4: Debug mode affects static file serving
DEBUG = True  # Static files served automatically in development

# Topic 5: Production static file storage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Topic 6-10: Static file discovery and management
# Django collects all static files from:
# - App static directories (myapp/static/)
# - STATICFILES_DIRS directories
# - Library static files (admin, etc.)
```

**Topics Covered:**
- Topic 1: STATIC_URL setting (URL prefix for static files)
- Topic 2: STATIC_ROOT setting (collected files destination)
- Topic 3: STATICFILES_DIRS configuration
- Topic 4: Static serving in DEBUG mode
- Topic 5: STATICFILES_STORAGE backend
- Topic 6-10: Static file collection and discovery

#### 2. **CSS and JavaScript Integration** (Topics 11-20)
```html
<!-- base.html - Topics 11-20 -->

<!-- Topic 11: Bootstrap CSS CDN -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- Topic 12: Custom static CSS file -->
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">

<!-- Topic 13-15: Bootstrap utility classes and custom styling -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <!-- Topic 14: Responsive Bootstrap components -->
</nav>

<!-- Topic 18: Font Awesome icons CDN -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Topic 16: Bootstrap JavaScript CDN -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Topic 19: Custom static JavaScript file -->
<script src="{% static 'js/main.js' %}"></script>

<!-- Topic 20: Event handlers and interactivity -->
```

**Topics Covered:**
- Topic 11: Bootstrap CSS integration
- Topic 12: Custom CSS files with {% static %} tag
- Topic 13-15: Bootstrap utility classes for styling
- Topic 14: Responsive design with Bootstrap
- Topic 16-17: Bootstrap and Popper.js JavaScript
- Topic 18: Font Awesome icon library
- Topic 19-20: Custom JavaScript and event handling

#### 3. **Media Files Configuration** (Topics 21-30)
```python
# settings.py - Topics 21-30

# Topic 21: MEDIA_URL - URL path for user uploads
MEDIA_URL = '/media/'

# Topic 22: MEDIA_ROOT - Directory where uploads are stored
MEDIA_ROOT = BASE_DIR / 'media'

# Topic 23: Difference between STATIC and MEDIA
# STATIC_URL: /static/ - Framework and app files (not user-uploaded)
# MEDIA_URL: /media/ - User-uploaded files (dynamic content)

# Topic 24: Media directory structure
# media/
#   ├── products/  (Topic 27)
#   ├── user_uploads/
#   └── profiles/
```

```python
# urls.py - Topics 25-30

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [...]

# Topic 25-30: Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Topics Covered:**
- Topic 21: MEDIA_URL configuration
- Topic 22: MEDIA_ROOT directory
- Topic 23: Static vs Media distinction
- Topic 24: Media directory organization
- Topic 25-30: Media file serving in development

#### 4. **Product Model with Images** (Topics 31-40)
```python
from django.db import models

class Product(models.Model):
    """Topics 31-40: Product model with image field"""
    
    # Topic 33: Basic fields
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    # Topic 34-35: Decimal price field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Topic 36-37: ImageField with upload path
    image = models.ImageField(upload_to='products/')
    
    # Topic 38: Category field
    category = models.CharField(max_length=50)
    
    # Topic 39-40: Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
```

**Topics Covered:**
- Topic 31-35: Product model fields
- Topic 36: ImageField definition
- Topic 37: upload_to with dynamic path
- Topic 38: Category field
- Topic 39-40: Timestamp tracking

#### 5. **Template Display with Static Files** (Topics 1-40)
```html
<!-- list.html - Topics 1-40 -->

{% extends 'base.html' %}
{% load static %}

{% block content %}
    <!-- Topic 13-14: Bootstrap grid and cards -->
    <div class="row mt-4">
        {% for product in products %}
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card">
                    <!-- Topic 29-30: Display product image URL -->
                    {% if product.image %}
                        <img src="{{ product.image.url }}" 
                             class="card-img-top" 
                             alt="{{ product.name }}">
                    {% else %}
                        <div class="bg-light">No image</div>
                    {% endif %}
                    
                    <div class="card-body">
                        <h5 class="card-title">{{ product.name }}</h5>
                        
                        <!-- Topic 38: Show category -->
                        <span class="badge bg-primary">{{ product.category }}</span>
                        
                        <!-- Topic 15: Custom CSS price styling -->
                        <p class="price-highlight">${{ product.price }}</p>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
{% endblock %}
```

### Test Structure: 40 tests organized by topic

**Test Classes:**
- StaticFilesConfigurationTestCase (5 tests): Topics 1-5 (STATIC_URL, STATIC_ROOT, STATICFILES_DIRS)
- StaticFileAccessTestCase (5 tests): Topics 6-10 (serving static files)
- CSSIntegrationTestCase (5 tests): Topics 11-15 (Bootstrap, custom CSS)
- JavaScriptIntegrationTestCase (5 tests): Topics 16-20 (Bootstrap JS, Font Awesome, events)
- MediaFilesConfigurationTestCase (5 tests): Topics 21-25 (MEDIA_URL, MEDIA_ROOT, serving)
- ProductImageUploadTestCase (5 tests): Topics 26-30 (image uploads, URLs)
- ProductModelImageFieldTestCase (5 tests): Topics 31-35 (Product model fields)
- ProductImageFieldAdvancedTestCase (5 tests): Topics 36-40 (ImageField, upload_to, timestamps)

---

## Assignment 2: Galleries, Images, and Comments

### Topics Covered: 41-80

### What Students Implement

#### 1. **Gallery and Image Models** (Topics 31-50)
```python
from django.db import models
from django.contrib.auth.models import User

# Topic 31-50: Gallery model with relationships
class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Topic 49-50
    created_at = models.DateTimeField(auto_now_add=True)  # Topic 39
    updated_at = models.DateTimeField(auto_now=True)  # Topic 40
    is_published = models.BooleanField(default=False)  # Topic 41
    
    def __str__(self):
        return self.title
    
    def image_count(self):
        """Topic 43: Count related images"""
        return self.images.count()
    
    class Meta:
        ordering = ['-created_at']


# Topic 36-40: Image model with nested upload path
class Image(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200)
    
    # Topic 37-38: Dynamic upload path with date
    image = models.ImageField(upload_to='gallery/%Y/%m/%d/')
    
    caption = models.TextField(blank=True)
    order = models.IntegerField(default=0)  # Topic 51-60
    created_at = models.DateTimeField(auto_now_add=True)  # Topic 66
    updated_at = models.DateTimeField(auto_now=True)  # Topic 67
    
    def __str__(self):
        return f"{self.gallery.title} - {self.title}"
    
    class Meta:
        ordering = ['order', 'created_at']
        unique_together = [['gallery', 'image']]
```

#### 2. **Comment Model with Relationships** (Topics 61-70)
```python
# Topic 61-70: Comment model with ratings

RATING_CHOICES = [
    (1, '⭐'),
    (2, '⭐⭐'),
    (3, '⭐⭐⭐'),
    (4, '⭐⭐⭐⭐'),
    (5, '⭐⭐⭐⭐⭐'),
]

class Comment(models.Model):
    # Topic 61: ForeignKey to Image
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')
    
    # Topic 62-65: Comment fields with validation
    author = models.CharField(max_length=100)  # Topic 62
    email = models.EmailField()  # Topic 63
    text = models.TextField()  # Topic 64
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)  # Topic 65
    
    # Topic 66-67: Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Topic 66
    updated_at = models.DateTimeField(auto_now=True)  # Topic 67
    
    # Topic 68: Approval workflow
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Comment by {self.author} on {self.image.title}"  # Topic 69
    
    def get_rating_stars(self):
        """Topic 70: Return star representation"""
        return '★' * self.rating
    
    class Meta:
        ordering = ['-created_at']
```

#### 3. **Views with Media Handling** (Topics 41-80)
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Gallery, Image, Comment
from .forms import CommentForm

def gallery_list(request):
    """Topics 1-50: Display all published galleries"""
    galleries = Gallery.objects.filter(is_published=True)
    return render(request, 'gallery/list.html', {'galleries': galleries})

def gallery_detail(request, gallery_id):
    """Topics 31-50: Display gallery with all images"""
    gallery = get_object_or_404(Gallery, id=gallery_id)
    images = gallery.images.all()
    return render(request, 'gallery/detail.html', {
        'gallery': gallery,
        'images': images
    })

def image_view(request, image_id):
    """Topics 36-50: Display image with comments section"""
    image = get_object_or_404(Image, id=image_id)
    
    # Topic 61-70: Get approved comments only
    comments = image.comments.filter(is_approved=True)
    
    context = {
        'image': image,
        'gallery': image.gallery,
        'comments': comments,
        'comment_form': CommentForm()
    }
    return render(request, 'gallery/image.html', context)

def image_comments(request, image_id):
    """Topics 61-70: Handle comment submission"""
    image = get_object_or_404(Image, id=image_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Topic 61-70: Save comment
            comment = form.save(commit=False)
            comment.image = image
            comment.save()
            
            # Topic 68: Comment awaiting approval
            return redirect('gallery:image_view', image_id=image_id)
    
    return redirect('gallery:image_view', image_id=image_id)

def approve_comment(request, comment_id):
    """Topics 68-70: Approve pending comments"""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    return redirect('gallery:image_view', image_id=comment.image.id)
```

#### 4. **Templates with Galleries and Comments** (Topics 41-80)
```html
<!-- list.html - Topics 41-80 -->
{% extends 'base.html' %}

{% block content %}
    <h1>Image Galleries</h1>
    
    <!-- Topic 11-14: Bootstrap grid for galleries -->
    <div class="row">
        {% for gallery in galleries %}
            <div class="col-md-4 mb-4">
                <div class="card gallery-card">
                    <!-- Topic 37: Display first image thumbnail -->
                    {% if gallery.images.first.image %}
                        <img src="{{ gallery.images.first.image.url }}" 
                             class="card-img-top" 
                             alt="{{ gallery.title }}">
                    {% endif %}
                    
                    <div class="card-body">
                        <h5 class="card-title">{{ gallery.title }}</h5>
                        
                        <!-- Topic 43: Show image count -->
                        <p>{{ gallery.image_count }} images</p>
                        
                        <a href="{% url 'gallery:detail' gallery.id %}" 
                           class="btn btn-primary">View</a>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
{% endblock %}

<!-- image.html - Topics 61-70 -->
{% extends 'base.html' %}

{% block content %}
    <div class="row">
        <div class="col-lg-8">
            <!-- Topic 37-40: Full image display -->
            <img src="{{ image.image.url }}" class="img-fluid" alt="{{ image.title }}">
        </div>
        
        <div class="col-lg-4">
            <!-- Topic 61-70: Comments section -->
            <h3>Comments ({{ comments.count }})</h3>
            
            {% for comment in comments %}
                <div class="comment-item">
                    <strong>{{ comment.author }}</strong>
                    
                    <!-- Topic 70: Display star rating -->
                    <span class="rating">{{ comment.get_rating_stars }}</span>
                    
                    <p>{{ comment.text }}</p>
                    <small>{{ comment.created_at|date:"M d, Y" }}</small>
                </div>
            {% endfor %}
            
            <!-- Topic 61-70: Comment submission form -->
            <form method="post" action="{% url 'gallery:image_comments' image.id %}">
                {% csrf_token %}
                {{ comment_form.as_p }}
                <button type="submit" class="btn btn-primary">Post Comment</button>
            </form>
        </div>
    </div>
{% endblock %}
```

### Test Structure: 40+ tests organized by topic

**Test Classes:**
- GalleryModelTestCase (8 tests): Topics 31-50 (Gallery model, relationships)
- ImageModelTestCase (12 tests): Topics 36-40 (Image model, ImageField)
- CommentModelTestCase (14 tests): Topics 61-70 (Comment model, ratings)
- StaticFilesConfigurationTestCase (4 tests): Topics 1-10 (configuration)
- CSSAndJavaScriptTestCase (4 tests): Topics 11-20 (CSS, JS)
- MediaFilesConfigurationTestCase (3 tests): Topics 21-30 (media setup)
- GalleryViewsTestCase (4 tests): Topics 1-50 (rendering views)
- CommentViewsTestCase (6 tests): Topics 61-70 (comment workflows)

---

## Key Learning Objectives

### Episode 19 A1: Static Files & Images
1. Understanding Django's static files system
2. STATIC_URL, STATIC_ROOT, STATICFILES_DIRS configuration
3. {% static %} template tag usage
4. Bootstrap CSS framework integration
5. Custom CSS styling with static files
6. Font Awesome icon library
7. Custom JavaScript with static files
8. MEDIA_URL and MEDIA_ROOT configuration
9. ImageField in models
10. Dynamic upload paths with upload_to

### Episode 19 A2: Galleries & Comments
1. All A1 concepts retained
2. ForeignKey relationships between Gallery, Image, and Comment
3. Nested model relationships (Gallery → Image → Comment)
4. upload_to with date-based paths (gallery/%Y/%m/%d/)
5. Choices field for ratings
6. Comment moderation workflow (is_approved)
7. Related manager usage (.images.all(), .comments.filter())
8. Template tag filters for display (date, default)
9. Cascade deletion with on_delete=models.CASCADE
10. Query optimization with related_name

---

## File Structure

### Assignment 1
```
assignment1_starter/
├── manage.py (provided)
├── myapp/
│   ├── settings.py (provided with STATIC/MEDIA config)
│   ├── urls.py (with media serving)
│   ├── wsgi.py (provided)
│   └── __init__.py
├── products/
│   ├── models.py (TODO - Product model)
│   ├── views.py (TODO - list, detail, upload views)
│   ├── urls.py (TODO - URL patterns)
│   ├── admin.py (TODO)
│   ├── forms.py (TODO - ProductForm)
│   ├── tests.py (40 test stubs)
│   └── __init__.py
├── static/
│   ├── css/
│   │   └── style.css (provided)
│   └── js/
│       └── main.js (provided)
└── templates/
    ├── base.html (provided)
    └── products/
        ├── list.html (TODO)
        ├── detail.html (TODO)
        └── upload.html (TODO)
```

### Assignment 2
```
assignment2_starter/
├── manage.py (provided)
├── myapp/
│   ├── settings.py (provided with STATIC/MEDIA config)
│   ├── urls.py (with media serving)
│   ├── wsgi.py (provided)
│   └── __init__.py
├── gallery/
│   ├── models.py (TODO - Gallery, Image, Comment)
│   ├── views.py (TODO - list, detail, comments)
│   ├── urls.py (TODO - URL patterns)
│   ├── admin.py (TODO - admin registration)
│   ├── forms.py (TODO - ImageForm, CommentForm)
│   ├── tests.py (40+ test stubs)
│   └── __init__.py
├── static/
│   ├── css/
│   │   ├── style.css (provided)
│   │   └── gallery.css (provided)
│   └── js/
│       └── gallery.js (provided)
└── templates/
    ├── base.html (provided)
    └── gallery/
        ├── list.html (TODO)
        ├── detail.html (TODO)
        └── image.html (TODO)
```

---

## Implementation Patterns

### Static File Loading
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}" alt="Logo">
<script src="{% static 'js/main.js' %}"></script>
```

### Static File in CSS
```css
/* Use relative paths from static directory */
background-image: url('../images/pattern.png');
```

### ImageField in Model
```python
class Product(models.Model):
    image = models.ImageField(upload_to='products/')
    # File saved to: media/products/filename.jpg
    # URL: /media/products/filename.jpg
    # Access in template: {{ product.image.url }}
```

### Upload Path with Dates
```python
class Image(models.Model):
    image = models.ImageField(upload_to='gallery/%Y/%m/%d/')
    # File saved to: media/gallery/2024/02/18/filename.jpg
    # Automatically creates date-based directories
```

### Displaying Images in Templates
```html
{% if product.image %}
    <img src="{{ product.image.url }}" alt="{{ product.name }}">
{% else %}
    <p>No image available</p>
{% endif %}
```

### Comment Moderation
```python
# Filter only approved comments
approved_comments = Comment.objects.filter(is_approved=True)

# Check if comment needs approval
if comment.is_approved:
    display_comment(comment)
else:
    show_pending_message()
```

### Star Rating Display
```python
def get_rating_stars(self):
    return '★' * self.rating  # Returns ⭐⭐⭐⭐⭐ for rating=5

# In template
{{ comment.get_rating_stars }}  # Displays actual stars
```

---

## Success Criteria

### Assignment 1: All 40 tests pass ✓
- Static files properly configured (STATIC_URL, STATIC_ROOT)
- CSS and JavaScript loading correctly
- Bootstrap utilities applied properly
- Media files configuration correct
- ImageField saving files to correct paths
- Product image URL generated properly
- All 8 test classes passing

### Assignment 2: All 40 tests pass ✓
- Gallery, Image, and Comment models created
- ForeignKey relationships working
- Comment approval workflow functional
- Images displaying in gallery views
- Comments displaying with ratings
- Upload paths creating date-based directories
- Cascade deletion working properly

---

## Debugging Tips

1. **Images not displaying**: Check MEDIA_URL, MEDIA_ROOT, DEBUG=True
2. **Static files not found**: Run `python manage.py collectstatic`
3. **{% static %} not working**: Verify `{% load static %}` at top of template
4. **Upload path incorrect**: Check upload_to parameter format
5. **ForeignKey error**: Verify on_delete parameter and related_name
6. **Comments not showing**: Check is_approved filter in template
7. **Image URL wrong**: Use {{ image.image.url }} not {{ image.image }}

---

## Resources

- Static Files: https://docs.djangoproject.com/en/5.1/howto/static-files/
- ImageField: https://docs.djangoproject.com/en/5.1/ref/models/fields/#imagefield
- Media Files: https://docs.djangoproject.com/en/5.1/topics/files/
- Template Tags: https://docs.djangoproject.com/en/5.1/topics/templates/
- Bootstrap: https://getbootstrap.com/docs/5.3/
- Font Awesome: https://fontawesome.com/docs/web/setup/get-started
