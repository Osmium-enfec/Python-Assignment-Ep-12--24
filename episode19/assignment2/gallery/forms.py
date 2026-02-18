"""
Forms for gallery management.

Topics 1-40: Form handling with image uploads
"""
from django import forms
from .models import Gallery, Image, Comment

# TODO: Topic 37: Create ModelForm for Image
# - Include fields: title, image, caption, gallery
# - Widget for image: ClearableFileInput
# - Help text for image: "Max size: 5MB. Formats: JPG, PNG, GIF"

# TODO: Topic 61-70: Create ModelForm for Comment
# - Include fields: author, email, text, rating
# - Widget for rating: RadioSelect with choices 1-5
# - Help text for email: "Your email will not be published"
# - Validation: text must be at least 10 characters
