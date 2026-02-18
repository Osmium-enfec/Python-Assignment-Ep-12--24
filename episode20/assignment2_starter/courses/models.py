from django.db import models

# TODO: Create Course model (Topics 41-80):
# Fields:
# - code (CharField, max_length=20, unique=True)
# - title (CharField, max_length=200)
# - description (TextField)
# - instructor (CharField, max_length=100)
# - credits (IntegerField, default=3)
# - max_students (IntegerField, default=30)
# - enrolled_count (IntegerField, default=0)
# - created_at (DateTimeField, auto_now_add=True)
# - updated_at (DateTimeField, auto_now=True)
#
# Meta:
# - ordering = ['code']
#
# Methods:
# - __str__: return "{code}: {title}"
# - is_full(): return enrolled_count >= max_students
# - available_seats(): return max_students - enrolled_count

# TODO: Create Enrollment model (Topics 41-80):
# For tracking delete confirmations and modal interactions
# Fields:
# - course (ForeignKey to Course, on_delete=CASCADE)
# - student_name (CharField, max_length=100)
# - enrolled_date (DateTimeField, auto_now_add=True)
#
# Meta:
# - ordering = ['-enrolled_date']
#
# Methods:
# - __str__: return "{student_name} - {course.code}"
