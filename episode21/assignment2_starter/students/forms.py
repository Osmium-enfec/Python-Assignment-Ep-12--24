from django import forms
from django.core.exceptions import ValidationError

# TODO: Create CourseForm (Topics 41-80):
# ModelForm with fields: code, name, credit_hours, instructor_email, description, max_students, enrollment_fee, is_active
#
# Topics 41-56: Advanced validation
# - clean() method for form-level validation (Topic 43)
# - ValidationError exception (Topic 44)
# - Cross-field validation (Topic 45-46)
# - Unique field validation (Topic 47)
# - Database lookup validation (Topic 48)
# - Conditional field exclusion (Topic 49)
#
# Topics 50-60: Bootstrap integration and saving
# - form.save() with commit parameter (Topic 51-52)
# - Modifying data before save (Topic 53)
# - Widget customization with Bootstrap classes (Topic 61-62)
#
# Topics 62-70: Widget and field rendering
# - form-control and form-check-input classes
# - Alert components for errors
# - Error styling and display
