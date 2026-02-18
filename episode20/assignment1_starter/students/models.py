from django.db import models

# TODO: Create Student model (Topics 38-40):
# Fields:
# - roll_no (CharField, max_length=20, unique=True)
# - name (CharField, max_length=100)
# - email (EmailField)
# - phone (CharField, max_length=15, blank=True)
# - address (TextField, blank=True)
# - gpa (FloatField, default=0.0)
# - created_at (DateTimeField, auto_now_add=True)
# - updated_at (DateTimeField, auto_now=True)
#
# Meta:
# - ordering = ['roll_no']
#
# Methods:
# - __str__: return "{name} ({roll_no})"
