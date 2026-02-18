from django import forms

# TODO: Create 2 forms (Topics 58-62):
#
# 1. ProjectForm (ModelForm):
#    - Fields: name, description, is_active
#    - Widgets with Bootstrap classes (form-control, form-check-input)
#
# 2. EventForm (ModelForm):
#    - Fields: project, event_type, user_id, url, duration_ms
#    - Widgets with Bootstrap classes
#    - Custom validation: duration_ms must be >= 0
