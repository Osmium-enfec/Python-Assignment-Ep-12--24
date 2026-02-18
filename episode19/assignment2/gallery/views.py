"""
Views for gallery management.

Topics 1-80: Handling galleries, images, and comments
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Gallery, Image, Comment
from .forms import Image as ImageForm, Comment as CommentForm

# TODO: Implement views (Topics 1-80)

# def gallery_list(request):
#     """
#     Topic 1-10: Display all galleries with pagination
#     - Retrieve all published galleries
#     - Display thumbnail from first image (Topic 37)
#     - Render list.html template
#     """
#     pass

# def gallery_detail(request, gallery_id):
#     """
#     Topic 31-50: Display gallery with all images
#     - Retrieve specific gallery
#     - Get all images in gallery (Topic 49)
#     - Display images in grid layout (Topic 11-20)
#     """
#     pass

# def image_view(request, image_id):
#     """
#     Topic 36-50: Display single image detail
#     - Retrieve image and related gallery (Topic 37-40)
#     - Display image comments (Topic 61-70)
#     - Show comment form (Topic 61-70)
#     """
#     pass

# def image_comments(request, image_id):
#     """
#     Topic 61-70: Handle comment submission
#     - Handle GET: display comments
#     - Handle POST: save new comment (Topic 61-70)
#     - Validate comment (Topic 62-65)
#     - Redirect to image_view after success
#     """
#     pass

# def approve_comment(request, comment_id):
#     """
#     Topic 68-70: Approve pending comments
#     - Retrieve comment
#     - Mark is_approved=True (Topic 68)
#     - Redirect to gallery
#     """
#     pass

# @login_required
# def upload_images(request):
#     """
#     Topic 37-40: Handle batch image upload
#     - Display upload form (Topic 37)
#     - Handle GET: render upload.html
#     - Handle POST: save multiple images (Topic 37-40)
#     - Validate images (Topic 38)
#     - Redirect after success
#     """
#     pass
