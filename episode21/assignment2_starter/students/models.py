from django.db import models

# TODO: Create Course model (Topics 41-80):
# Fields:
# - code (CharField, max_length=10, unique=True)
# - name (CharField, max_length=200)
# - credit_hours (IntegerField, default=3)
# - instructor_email (EmailField, unique=True)
# - description (TextField, blank=True)
# - max_students (IntegerField, default=30)
# - enrollment_fee (DecimalField, max_digits=8, decimal_places=2, default=0)
# - is_active (BooleanField, default=True)
# - created_at (DateTimeField, auto_now_add=True)
#
# Meta:
# - ordering = ['code']
#
# Methods:
# - __str__: return "{code} - {name}"
