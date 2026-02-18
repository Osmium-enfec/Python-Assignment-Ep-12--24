"""
Admin configuration for gallery app.

Topics 31-80: Advanced admin with related models
"""
from django.contrib import admin
from .models import Gallery, Image, Comment

# TODO: Topic 33-40: Register Gallery model in admin
# - Display fields: title, created_by, created_at, is_published
# - Readonly fields: created_at, updated_at
# - Search fields: title, description
# - List filter: is_published, created_at

# TODO: Topic 36-40: Register Image model with inline admin
# - Display fields: title, image, order, created_at
# - Readonly fields: created_at, updated_at
# - List filter: gallery, created_at
# - Ordering: order, created_at

# TODO: Topic 61-70: Register Comment model in admin
# - Display fields: author, image, rating, is_approved, created_at
# - Readonly fields: created_at, updated_at, email
# - List filter: is_approved, rating, created_at
# - Search fields: author, email, text
# - Actions: approve_comments, disapprove_comments
