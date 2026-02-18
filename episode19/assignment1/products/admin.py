"""
Admin configuration for products app.

Topics 31-40: Admin display of media files
"""
from django.contrib import admin
from .models import Product

# TODO: Register Product model in admin
# - Display fields: name, category, price, image, created_at (Topics 31-35)
# - Readonly fields: created_at, updated_at (Topic 39)
# - Search fields: name, description (Topic 33-34)
# - List filter: category, created_at (Topic 38-39)
