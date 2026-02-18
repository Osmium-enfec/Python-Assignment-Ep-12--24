from django.db import models

# TODO: Create a Task model with the following fields:
# - title (CharField, max_length=200)
# - description (TextField, blank=True)
# - priority (IntegerField with choices: 1-Low, 2-Medium, 3-High, 4-Urgent, 5-Critical)
# - completed (BooleanField, default=False)
# - created_at (DateTimeField, auto_now_add=True)
# - updated_at (DateTimeField, auto_now=True)
#
# Add a Meta class with ordering
# Add a __str__ method that returns the title with priority
