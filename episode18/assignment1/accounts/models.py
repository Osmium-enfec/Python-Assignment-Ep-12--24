"""
User profile model for storing additional user information.

Topics 11-20: User profiles and extended user data
"""
from django.db import models
from django.contrib.auth.models import User

# Topic 11-20: UserProfile model with extended user data
class UserProfile(models.Model):
    """
    TODO: Implement UserProfile model with following fields:
    
    Fields (Topics 11-20):
    - user: OneToOneField to User, on_delete=models.CASCADE (Topic 11)
      * Topic 11: OneToOneField creates 1:1 relationship
      * Related name 'profile' for reverse access (Topic 12)
    - bio: TextField, blank=True (Topic 13)
    - phone: CharField, max_length=15, blank=True (Topic 14)
    - avatar: ImageField, upload_to='avatars/', blank=True (Topic 15)
    - date_of_birth: DateField, blank=True, null=True (Topic 16)
    - is_verified: BooleanField, default=False (Topic 17)
    - verification_code: CharField, max_length=32, blank=True (Topic 18)
    - last_login_ip: GenericIPAddressField, blank=True, null=True (Topic 19)
    - created_at: DateTimeField, auto_now_add=True (Topic 20)
    
    Methods:
    - __str__: Return user's username (Topic 21)
    - get_full_name: Return user's full name (Topic 22)
    - is_complete: Check if profile is complete (Topic 23)
    
    Meta:
    - verbose_name_plural: 'User Profiles'
    """
    pass
