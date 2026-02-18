from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json

# TODO: Create views (Topics 41-80):
#
# 1. course_list (GET):
#    - Display all courses
#    - Show action buttons (view, edit, delete)
#    - Include Bootstrap modals on page
#    - Topics 41-60: Modal components and rendering
#    - Template: courses/list.html
#
# 2. course_view (GET):
#    - Display course details in modal
#    - Topics 41-80: Modal content and pre-filling
#    - Return HTML or JSON for AJAX
#    - Topics 62-68: AJAX and JSON responses
#
# 3. course_delete_confirm (GET):
#    - Show delete confirmation modal
#    - Display course details to be deleted
#    - Topics 61-80: Modal interactions and delete buttons
#    - Topics 74: Confirmation dialogs
#
# 4. course_delete (POST):
#    - Delete course after confirmation
#    - Topics 19-26: Redirect after POST
#    - Redirect to list
#
# 5. course_data (GET):
#    - Return course data as JSON
#    - Topics 62-68: AJAX and JsonResponse
#    - Used by AJAX requests to populate modals
