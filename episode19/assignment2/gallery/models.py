"""
Gallery models with images and comments.

Topics 31-80: Media files, comments, and relationships
"""
from django.db import models
from django.contrib.auth.models import User

# Topic 31-50: Gallery model with multiple images
class Gallery(models.Model):
    """
    TODO: Implement Gallery model with following fields:
    
    Fields (Topics 31-50):
    - title: CharField, max_length=200 (Topic 33)
    - description: TextField (Topic 34)
    - created_by: ForeignKey to User (Topic 49-50)
    - created_at: DateTimeField, auto_now_add=True (Topic 39)
    - updated_at: DateTimeField, auto_now=True (Topic 40)
    - is_published: BooleanField, default=False (Topic 41)
    
    Methods:
    - __str__: Return gallery title (Topic 39)
    - image_count: Return number of images (Topic 43)
    
    Meta:
    - ordering: ['-created_at']
    """
    pass


# Topic 36-40: Image model with ForeignKey relationship
class Image(models.Model):
    """
    TODO: Implement Image model with following fields:
    
    Fields (Topics 36-40):
    - gallery: ForeignKey to Gallery, on_delete=models.CASCADE (Topic 49)
    - title: CharField, max_length=200 (Topic 36-37)
    - image: ImageField, upload_to='gallery/%Y/%m/%d/' (Topic 37-38)
    - caption: TextField, blank=True (Topic 34)
    - order: IntegerField, default=0 (Topic 51-60)
    - created_at: DateTimeField, auto_now_add=True (Topic 39)
    - updated_at: DateTimeField, auto_now=True (Topic 40)
    
    Methods:
    - __str__: Return image title (Topic 39)
    
    Meta:
    - ordering: ['order', 'created_at']
    - unique_together: [['gallery', 'image']]
    """
    pass


# Topic 61-70: Comment model with relationships
class Comment(models.Model):
    """
    TODO: Implement Comment model with following fields:
    
    Fields (Topics 61-70):
    - image: ForeignKey to Image, on_delete=models.CASCADE (Topic 49)
    - author: CharField, max_length=100 (Topic 62)
    - email: EmailField (Topic 63)
    - text: TextField (Topic 64)
    - rating: IntegerField, choices, default=5 (Topic 65)
    - created_at: DateTimeField, auto_now_add=True (Topic 66)
    - updated_at: DateTimeField, auto_now=True (Topic 67)
    - is_approved: BooleanField, default=False (Topic 68)
    
    Methods:
    - __str__: Return comment summary (Topic 69)
    - get_rating_stars: Return star rating (Topic 70)
    
    Meta:
    - ordering: ['-created_at']
    """
    pass
