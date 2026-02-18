from django.db import models

# TODO: Create Product model (Topics 11, 17-22):
# Fields:
# - code (CharField, max_length=20, unique=True)
# - name (CharField, max_length=200)
# - description (TextField, blank=True)
# - price (DecimalField, max_digits=10, decimal_places=2)
# - category (CharField, max_length=50)
# - is_active (BooleanField, default=True)
# - created_at (DateTimeField, auto_now_add=True)
# - updated_at (DateTimeField, auto_now=True)
#
# Meta:
# - ordering = ['code']
#
# Methods:
# - __str__: return "{code} - {name}"
