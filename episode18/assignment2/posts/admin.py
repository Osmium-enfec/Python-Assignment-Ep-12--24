"""
Admin configuration for posts app.

Topics 41-80: Advanced admin with permissions
"""
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment

# TODO: Topic 51-70: Setup groups and permissions in admin
# - Create groups: Editors, Moderators, Viewers
# - Editors: can_add_post, can_change_post, can_delete_own_post (Topic 76-80)
# - Moderators: can_approve_comments (Topic 68-70)
# - Viewers: can_view_published_post (Topic 71-75)

# TODO: Topic 41-50: Register Post model
# - Display fields: title, author, status, visibility, created_at
# - Readonly fields: created_at, updated_at
# - List filter: status, visibility, author
# - Search fields: title, content
# - Ordering: -created_at

# TODO: Topic 61-70: Register Comment model
# - Display fields: author, post, is_approved, created_at
# - Readonly fields: created_at, updated_at
# - List filter: is_approved, post
# - Search fields: content, author__username
