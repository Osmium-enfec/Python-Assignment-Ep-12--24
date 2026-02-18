from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# TODO: Create views (Topics 41-80):
#
# 1. course_add (GET/POST):
#    - GET: Display blank CourseForm
#    - POST: Validate and save new course
#    - Topics 43-56: Form validation, clean methods, ValidationError
#    - Topics 66-67: Passing form to template context
#    - Topics 72-74: Messages framework, redirect after success
#    - Topic 49: CSRF token in template
#    - Show success message with course code
#
# 2. course_edit (GET/POST):
#    - GET: Display pre-filled CourseForm
#    - POST: Validate and update course
#    - Topic 79: Instance in form constructor for pre-filling
#    - Topic 80: Update vs Add operations
#    - Topics 51-52: Form save with commit parameter
#    - Topics 53: Modifying data before save
#    - Topic 75: messages.success() after update
#    - Show success message with updated info
