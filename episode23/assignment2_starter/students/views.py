from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# TODO: Create 5 enhanced views (Topics 51-70):
#
# 1. student_index (Topics 51-55):
#    - Display all students in advanced card layout
#    - Show: name, email, status, major, gpa
#    - Status badge with colors (active=green, inactive=gray, graduated=blue)
#    - GPA highlighted if > 3.5
#    - Add buttons: View Details, Edit, Delete
#
# 2. student_add (Topics 56-60):
#    - Enhanced form with validation feedback
#    - Show field requirements
#    - Success message with name
#    - Redirect to detail view (not index)
#
# 3. student_view (Topics 61-65):
#    - Enhanced detail card with all fields
#    - Status badge
#    - Enrollment date formatted
#    - GPA with color coding
#    - Additional info sections
#
# 4. student_edit (Topics 66-68):
#    - Form with current data
#    - Separate sections for different field groups
#    - Save button and Cancel button
#    - Show what changed on success
#
# 5. student_delete (Topics 69-70):
#    - Beautiful confirmation page
#    - Show student's important info
#    - Warning message about deletion
#    - Confirm and Cancel buttons
#
# All views:
# - Use get_object_or_404 for safety
# - Use messages for feedback
# - Use POST-Redirect-GET pattern
# - Show student name in messages
