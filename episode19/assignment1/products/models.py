"""
Product model for storing product information with images.

Topics 31-40: Media file handling in models
"""
from django.db import models

# Topic 31-40: Product model with image field
class Product(models.Model):
    """
    TODO: Implement Product model with following fields:
    
    Fields (Topics 31-40):
    - name: CharField, max_length=100 (Topic 33)
    - description: TextField (Topic 34)
    - price: DecimalField, max_digits=10, decimal_places=2 (Topic 35)
    - image: ImageField, upload_to='products/' (Topic 36-37)
      * Topic 36: ImageField definition
      * Topic 37: upload_to parameter with dynamic path
    - category: CharField, max_length=50 (Topic 38)
    - created_at: DateTimeField, auto_now_add=True (Topic 39)
    - updated_at: DateTimeField, auto_now=True (Topic 40)
    
    Methods:
    - __str__: Return product name (Topic 39)
    
    Meta:
    - ordering: ['-created_at']
    """
    pass
