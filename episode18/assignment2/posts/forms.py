"""
Forms for post management with permissions.

Topics 41-80: Post creation and comment forms
"""
from django import forms
from .models import Post, Comment

# TODO: Topic 41-50: Implement PostForm
# - Fields: title, content, status, visibility
# - Widgets: Textarea for content, Select for status/visibility
# - Help text for status: "Draft = not visible, Published = visible per visibility setting"

# TODO: Topic 61-70: Implement CommentForm
# - Fields: content
# - Widget: Textarea with placeholder
# - Validation: content must be at least 5 characters
