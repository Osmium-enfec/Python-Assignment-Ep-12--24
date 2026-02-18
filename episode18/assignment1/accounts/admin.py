"""
Admin configuration for accounts app.

Topics 1-40: Admin interface for users and profiles
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

# TODO: Topic 21-25: Register User and UserProfile in admin

# UserInline for editing profile alongside user
# - Topic 22: InlineModelAdmin for related objects
# - Display fields: user, is_verified, bio

# CustomUserAdmin extending UserAdmin
# - Topic 23: Add custom fields to user admin
# - Fieldsets for better organization
# - Readonly fields: created_at, last_login
# - Search fields: username, email, first_name

# Topic 24-25: Register UserProfile in admin
# - Display fields: user, is_verified, phone, created_at
# - Readonly fields: verification_code, created_at
# - List filter: is_verified, created_at
