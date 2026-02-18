"""
Blog post models with permissions and ownership.

Topics 41-80: Permissions, groups, and object-level access control
"""
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

# Topic 41-50: Post model with ownership and status
class Post(models.Model):
    """
    TODO: Implement Post model with following fields:
    
    Fields (Topics 41-80):
    - title: CharField, max_length=200 (Topic 41)
    - content: TextField (Topic 42)
    - author: ForeignKey to User, on_delete=models.CASCADE (Topic 49)
      * Topic 49: Author is the post owner (permission control)
      * Related name 'posts' for reverse access
    - status: CharField with choices: draft, published, archived (Topic 51-60)
    - visibility: CharField with choices: private, friends, public (Topic 71-80)
      * Topic 71-75: Different visibility levels
    - created_at: DateTimeField, auto_now_add=True (Topic 61)
    - updated_at: DateTimeField, auto_now=True (Topic 62)
    - published_at: DateTimeField, blank=True, null=True (Topic 63)
    
    Methods:
    - __str__: Return post title (Topic 41)
    - is_published: Check if post is published (Topic 51-60)
    - can_view(user): Check if user can view post (Topic 71-80)
    
    Meta:
    - ordering: ['-created_at']
    - permissions: [('view_published_post', 'Can view published posts')] (Topic 76-80)
    """
    pass


# Topic 61-70: Comment model with author and permissions
class Comment(models.Model):
    """
    TODO: Implement Comment model with following fields:
    
    Fields (Topics 61-70):
    - post: ForeignKey to Post, on_delete=models.CASCADE, related_name='comments'
    - author: ForeignKey to User, on_delete=models.CASCADE (Topic 64)
    - content: TextField (Topic 65)
    - is_approved: BooleanField, default=False (Topic 68)
    - created_at: DateTimeField, auto_now_add=True (Topic 66)
    - updated_at: DateTimeField, auto_now=True (Topic 67)
    
    Methods:
    - __str__: Return comment preview (Topic 69-70)
    
    Meta:
    - ordering: ['-created_at']
    """
    pass
