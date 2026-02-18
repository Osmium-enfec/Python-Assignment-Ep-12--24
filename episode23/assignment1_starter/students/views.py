from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# TODO: Create 5 CRUD views (Topics 16-40):
#
# 1. student_index (GET - list all students)
#    - Display all students in a table
#    - Show: name, email, status, major
#    - Add buttons: View, Edit, Delete
#
# 2. student_add (GET/POST - create new student)
#    - GET: Display empty form
#    - POST: Save new student, show success message, redirect to index
#    - Use POST-Redirect-GET pattern
#
# 3. student_view (GET - view single student details)
#    - Display student details in a card
#    - Use get_object_or_404 for safety
#    - Add buttons: Edit, Delete, Back
#
# 4. student_edit (GET/POST - update student)
#    - GET: Display form with current data
#    - POST: Save changes, show success message, redirect to view
#    - Use form instance parameter
#
# 5. student_delete (GET/POST - delete student)
#    - GET: Show confirmation page with student info
#    - POST: Delete student, show success message, redirect to index
#    - Confirm before deletion
#
# Use messages framework for all feedback
# Use get_object_or_404 for safety
# Use POST-Redirect-GET pattern
