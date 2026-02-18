from django.db import models

# TODO: Create Book model (Topics 41-48):
# Fields:
# - title (CharField, max_length=200)
# - isbn (CharField, max_length=20, unique=True)
# - author (CharField, max_length=200)
# - description (TextField, blank=True)
# - price (DecimalField, max_digits=10, decimal_places=2)
# - genre (CharField, max_length=50)
# - is_published (BooleanField, default=True)
# - created_at (DateTimeField, auto_now_add=True)
# - updated_at (DateTimeField, auto_now=True)
#
# Meta:
# - ordering = ['-created_at']
#
# Methods:
# - __str__: return "{title} by {author}"
