from django.db import models

# TODO: Create Student model (same as A1, Topics 41-48):
# Fields:
# - name (CharField, max_length=200)
# - email (EmailField, unique=True)
# - enrollment_date (DateField, auto_now_add=True)
# - age (IntegerField, blank=True, null=True)
# - status (CharField with choices: active, inactive, graduated)
# - gpa (DecimalField, max_digits=3, decimal_places=2, default=0.0)
# - major (CharField, max_length=100, blank=True)
# - created_at (DateTimeField, auto_now_add=True)
#
# Meta:
# - ordering = ['-enrollment_date']
# - unique_together = [['email']]
#
# Methods:
# - __str__: return full name with email
# - is_active: property returning True if status='active'
