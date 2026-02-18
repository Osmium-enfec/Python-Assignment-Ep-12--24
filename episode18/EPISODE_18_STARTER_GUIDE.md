# Episode 18: User Authentication and Permissions - Starter Code Guide

## Overview
Episode 18 covers Django's built-in authentication system and permission framework. Students progress from basic user registration and login (Assignment 1) to advanced permission-based access control and group management (Assignment 2).

**Total Tests:** 80+ (40 per assignment)
- Assignment 1: 40 tests on user registration, login, profiles, and basic authentication
- Assignment 2: 40 tests on permissions, groups, post visibility, and object-level access control

---

## Assignment 1: User Authentication Basics

### Topics Covered: 1-40

### What Students Implement

#### 1. **Authentication Configuration** (Topics 1-10)
```python
# settings.py - Topics 1-10

# Topic 7: LOGIN_URL - where to redirect for login
LOGIN_URL = 'accounts:login'

# Topic 8: LOGIN_REDIRECT_URL - where to redirect after successful login
LOGIN_REDIRECT_URL = 'accounts:dashboard'

# Topic 9: LOGOUT_REDIRECT_URL - where to redirect after logout
LOGOUT_REDIRECT_URL = 'accounts:login'

# Topic 10: AUTH_USER_MODEL - custom user model (default: django.contrib.auth.User)
# AUTH_USER_MODEL = 'accounts.CustomUser'
```

**Topics Covered:**
- Topic 1: User authentication concept
- Topic 2: User registration flow
- Topic 3: Password fields and widgets
- Topic 4: PasswordInput widget
- Topic 5: CSRF token in forms
- Topic 6: UserCreationForm
- Topic 7: LOGIN_URL setting
- Topic 8: LOGIN_REDIRECT_URL setting
- Topic 9: LOGOUT_REDIRECT_URL setting
- Topic 10: AUTH_USER_MODEL configuration

#### 2. **User Registration** (Topics 1-10, 28-35)
```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Topics 1-5, 28-35: User registration form
class UserRegistrationForm(UserCreationForm):
    """
    Topic 28-35: Extend UserCreationForm for registration
    - Topic 28: Handle username field
    - Topic 29: Handle email field
    - Topic 30: Handle password1 and password2
    - Topic 31: Validate password strength
    - Topic 32: Check email uniqueness
    - Topic 33: Display help text
    - Topic 34: Show validation errors
    - Topic 35: Create user and profile
    """
    
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def clean_email(self):
        """Topic 32: Validate email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use')
        return email
    
    def save(self, commit=True):
        """Topic 35: Create user and related profile"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create UserProfile
            UserProfile.objects.create(user=user)
        return user


def register(request):
    """Topics 28-35: Registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
```

#### 3. **User Login** (Topics 3-6, 21-30)
```python
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView

# Topics 3-6, 21-30: Login view
class CustomLoginView(LoginView):
    """
    Topic 21-30: Handle user login
    - Topic 21: Display login form
    - Topic 22: Form fields: username, password
    - Topic 23: Authenticate credentials
    - Topic 24: Create session for user
    - Topic 25: Redirect to LOGIN_REDIRECT_URL
    """
    
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Topic 25: Redirect after login"""
        return reverse('accounts:dashboard')
```

#### 4. **UserProfile Model** (Topics 11-23)
```python
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Topics 11-20: Extended user information"""
    
    # Topic 11-12: OneToOneField creates 1:1 relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Topic 13: Bio/description
    bio = models.TextField(blank=True)
    
    # Topic 14: Phone field
    phone = models.CharField(max_length=15, blank=True)
    
    # Topic 15: Avatar image
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    
    # Topic 16: Date of birth
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Topic 17-18: Email verification
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=32, blank=True)
    
    # Topic 19: Track login IP
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    # Topic 20: Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """Topic 21: String representation"""
        return f"{self.user.username} Profile"
    
    def is_complete(self):
        """Topic 23: Check if profile is complete"""
        return all([self.bio, self.phone, self.avatar, self.date_of_birth])
```

#### 5. **Protected Views** (Topics 7-9, 36-40)
```python
from django.contrib.auth.decorators import login_required

# Topic 7-9, 36-40: Protected dashboard view
@login_required(login_url='accounts:login')  # Topic 7: Require authentication
def dashboard(request):
    """Topics 7-9, 36-40: User dashboard"""
    # Topic 8: User accessible via request.user
    user = request.user
    
    # Topic 9: Access user profile
    profile = user.profile
    
    # Topic 36: User object in context
    context = {
        'user': user,
        'profile': profile,
    }
    
    return render(request, 'accounts/dashboard.html', context)
```

#### 6. **Templates with Authentication** (Topics 36-40)
```html
<!-- base.html - Topics 36-40 -->
{% if user.is_authenticated %}
    <!-- Topic 36-37: Display authenticated user info -->
    Welcome, {{ user.username }}!
    
    <!-- Topic 38: is_authenticated check -->
    <a href="{% url 'accounts:edit_profile' %}">Edit Profile</a>
    
    <form method="post" action="{% url 'accounts:logout' %}">
        {% csrf_token %}
        <button type="submit">Logout</button>
    </form>
{% else %}
    <!-- Topic 39: Anonymous user links -->
    <a href="{% url 'accounts:register' %}">Register</a>
    <a href="{% url 'accounts:login' %}">Login</a>
{% endif %}
```

### Test Structure: 40 tests organized by topic

**Test Classes:**
- UserRegistrationTestCase (5 tests): Topics 1-5 (register view, form display, fields)
- UserCreationTestCase (5 tests): Topics 6-10 (user creation, validation)
- UserProfileModelTestCase (10 tests): Topics 11-20 (profile model fields)
- UserLoginTestCase (5 tests): Topics 21-25 (login view, redirect)
- UserLogoutTestCase (5 tests): Topics 26-30 (logout, session clearing)
- PasswordChangeTestCase (5 tests): Topics 31-35 (password management)
- AuthenticationContextTestCase (5 tests): Topics 36-40 (template context, decorators)

---

## Assignment 2: Permissions and Access Control

### Topics Covered: 41-80

### What Students Implement

#### 1. **Post Model with Visibility** (Topics 41-50, 71-80)
```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    """Topics 41-80: Blog post with permissions"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('friends', 'Friends Only'),
        ('public', 'Public'),
    ]
    
    # Topic 41: Post title
    title = models.CharField(max_length=200)
    
    # Topic 42: Post content
    content = models.TextField()
    
    # Topic 49: Author (ForeignKey to User)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    
    # Topic 51-60: Publication status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # Topic 71-80: Visibility control
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default='public'
    )
    
    # Topic 61-62: Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def is_published(self):
        """Topic 51-60: Check if published"""
        return self.status == 'published'
    
    def can_view(self, user):
        """Topic 71-80: Check if user can view"""
        if self.status != 'published':
            return user == self.author
        
        if self.visibility == 'public':
            return True
        elif self.visibility == 'private':
            return user == self.author
        elif self.visibility == 'friends':
            return user == self.author or user.is_staff
        
        return False
    
    class Meta:
        ordering = ['-created_at']
        permissions = [
            ('view_published_post', 'Can view published posts'),
        ]
```

#### 2. **Comment Model** (Topics 61-70)
```python
class Comment(models.Model):
    """Topics 61-70: Post comments with moderation"""
    
    # Topic 61: ForeignKey to Post
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    # Topic 64: Comment author (user)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    # Topic 65: Comment content
    content = models.TextField()
    
    # Topic 66-67: Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Topic 68: Approval workflow
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        """Topic 69-70: Comment representation"""
        return f"Comment by {self.author} on {self.post}"
    
    class Meta:
        ordering = ['-created_at']
```

#### 3. **Groups and Permissions** (Topics 1-40, 76-80)
```python
from django.contrib.auth.models import Group, Permission

# Topic 1-40, 76-80: Setup groups in management command or admin

def setup_groups():
    """Setup permission groups"""
    
    # Topic 10-20: Create Editors group
    editors, created = Group.objects.get_or_create(name='Editors')
    if created:
        # Add permissions
        add_post = Permission.objects.get(codename='add_post')
        change_post = Permission.objects.get(codename='change_post')
        editors.permissions.add(add_post, change_post)
    
    # Topic 21-30: Create Moderators group
    moderators, created = Group.objects.get_or_create(name='Moderators')
    if created:
        change_comment = Permission.objects.get(codename='change_comment')
        delete_comment = Permission.objects.get(codename='delete_comment')
        moderators.permissions.add(change_comment, delete_comment)
    
    # Topic 31-40: Create Viewers group (read-only)
    viewers, created = Group.objects.get_or_create(name='Viewers')
    if created:
        view_post = Permission.objects.get(codename='view_post')
        viewers.permissions.add(view_post)
```

#### 4. **Permission Checking in Views** (Topics 76-80)
```python
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import HttpResponseForbidden

# Topic 76-80: Permission-based view access

@login_required
def post_create(request):
    """Topic 76: Create post (requires add_post permission)"""
    if not request.user.has_perm('posts.add_post'):
        return HttpResponseForbidden("You don't have permission to create posts")
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'posts/create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """Topics 77-80: Edit post with ownership check"""
    post = get_object_or_404(Post, id=post_id)
    
    # Topic 79-80: Check if user is author
    if post.author != request.user:
        return HttpResponseForbidden("You can't edit this post")
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/edit.html', {'form': form})


@permission_required('posts.delete_post', raise_exception=True)
def post_delete(request, post_id):
    """Topic 78: Delete requires permission"""
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('posts:list')
```

#### 5. **Visibility Filtering in Views** (Topics 71-75)
```python
def post_list(request):
    """Topics 71-75: Filter posts by visibility"""
    
    if request.user.is_authenticated:
        # Topic 75: Show user's own posts + public posts
        posts = Post.objects.filter(
            models.Q(author=request.user) |
            models.Q(visibility='public', status='published')
        )
    else:
        # Topic 73: Anonymous users see only public published posts
        posts = Post.objects.filter(
            visibility='public',
            status='published'
        )
    
    return render(request, 'posts/list.html', {'posts': posts})


def post_detail(request, post_id):
    """Topics 71-75: Check visibility before showing"""
    post = get_object_or_404(Post, id=post_id)
    
    # Topic 72: Use can_view method
    if not post.can_view(request.user):
        return HttpResponseForbidden("You don't have permission to view this post")
    
    context = {
        'post': post,
        'comments': post.comments.filter(is_approved=True) if post.is_published() else []
    }
    
    return render(request, 'posts/detail.html', context)
```

### Test Structure: 40+ tests organized by topic

**Test Classes:**
- PostModelTestCase (9 tests): Topics 41-50 (post model fields)
- CommentModelTestCase (7 tests): Topics 61-70 (comment model, approval)
- GroupsAndPermissionsTestCase (8 tests): Topics 1-40 (groups setup)
- PostVisibilityTestCase (5 tests): Topics 71-75 (visibility filtering)
- PostPermissionsTestCase (5 tests): Topics 76-80 (permission decorators)
- CommentPermissionsTestCase (5 tests): Topics 61-70 (comment permissions)
- ViewAccessControlTestCase (5 tests): Topics 1-40 (view-level access)

---

## Key Learning Objectives

### Episode 18 A1: Authentication Basics
1. Django's built-in User model
2. User registration with UserCreationForm
3. Login and logout flows
4. UserProfile model with OneToOneField
5. @login_required decorator
6. User authentication context in templates
7. request.user object
8. Settings: LOGIN_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
9. Password hashing and validation
10. Session management

### Episode 18 A2: Permissions & Access Control
1. All A1 concepts retained
2. Django Permission system
3. Group-based permissions
4. User.has_perm() method
5. @permission_required decorator
6. Object-level access control
7. ForeignKey relationships to User
8. Post visibility levels (public, friends, private)
9. Status workflows (draft, published, archived)
10. Post ownership and author checks

---

## File Structure

### Assignment 1
```
assignment1_starter/
├── manage.py (provided)
├── myapp/
│   ├── settings.py (provided with AUTH settings)
│   ├── urls.py (with auth URL inclusion)
│   ├── wsgi.py (provided)
│   └── __init__.py
├── accounts/
│   ├── models.py (TODO - UserProfile model)
│   ├── views.py (TODO - register, login, profile views)
│   ├── urls.py (TODO - auth URL patterns)
│   ├── admin.py (TODO - admin registration)
│   ├── forms.py (TODO - registration, login forms)
│   ├── tests.py (40 test stubs)
│   └── __init__.py
├── static/
│   └── css/
│       └── style.css (provided)
└── templates/
    ├── base.html (provided)
    └── registration/
        ├── register.html (TODO)
        ├── login.html (TODO)
        └── accounts/
            ├── dashboard.html (TODO)
            └── edit_profile.html (TODO)
```

### Assignment 2
```
assignment2_starter/
├── manage.py (provided)
├── myapp/
│   ├── settings.py (provided)
│   ├── urls.py (with posts URL inclusion)
│   ├── wsgi.py (provided)
│   └── __init__.py
├── posts/
│   ├── models.py (TODO - Post, Comment models)
│   ├── views.py (TODO - permission-based views)
│   ├── urls.py (TODO - post URL patterns)
│   ├── admin.py (TODO - admin with groups)
│   ├── forms.py (TODO - post, comment forms)
│   ├── tests.py (40+ test stubs)
│   └── __init__.py
├── static/
│   └── css/
│       └── style.css (provided)
└── templates/
    ├── base.html (provided)
    └── posts/
        ├── list.html (TODO)
        ├── detail.html (TODO)
        └── forms.html (TODO)
```

---

## Implementation Patterns

### User Registration
```python
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Email already in use')
        return self.cleaned_data['email']
    
    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            UserProfile.objects.create(user=user)
        return user
```

### Login Template
```html
{% if user.is_authenticated %}
    Welcome, {{ user.username }}
{% else %}
    <a href="{% url 'accounts:login' %}">Login</a>
{% endif %}
```

### Permission Checking
```python
@login_required
def post_create(request):
    if not request.user.has_perm('posts.add_post'):
        raise PermissionDenied
    # ... create post logic
```

### Visibility Filtering
```python
posts = Post.objects.filter(
    models.Q(author=request.user) |
    models.Q(visibility='public', status='published')
)
```

### OneToOneField Access
```python
user = request.user
profile = user.profile  # OneToOneField with related_name='profile'
```

---

## Success Criteria

### Assignment 1: All 40 tests pass ✓
- User registration form working with validation
- Login and logout flows functioning
- UserProfile model with OneToOneField
- @login_required decorator protecting views
- User context available in templates
- Session management working correctly

### Assignment 2: All 40 tests pass ✓
- Post and Comment models created
- Permission system configured with groups
- Visibility filtering working (public/friends/private)
- Permission decorators enforcing access
- Object-level ownership checks working
- Post status workflow (draft/published/archived)
- Comments require approval

---

## Debugging Tips

1. **User not logged in after registration**: Check LOGIN_REDIRECT_URL
2. **Permission denied errors**: Verify user has group assignment
3. **Posts not showing**: Check visibility and status in database
4. **OneToOneField error**: Ensure profile created when user registered
5. **@login_required not working**: Check LOGIN_URL setting
6. **Comments not displaying**: Check is_approved filter

---

## Resources

- Authentication: https://docs.djangoproject.com/en/5.1/topics/auth/
- Permissions: https://docs.djangoproject.com/en/5.1/topics/auth/default/#permissions-and-authorization
- Decorators: https://docs.djangoproject.com/en/5.1/topics/auth/default/#the-permission-and-authorization-system
- UserCreationForm: https://docs.djangoproject.com/en/5.1/topics/auth/default/#django.contrib.auth.forms.UserCreationForm
- OneToOneField: https://docs.djangoproject.com/en/5.1/ref/models/fields/#onetoonefield
