from django.db import models

# TODO: Create 3 models:
#
# 1. Project model (Topics 41-43):
#    - name (CharField, max_length=200)
#    - description (TextField, blank=True)
#    - created_at (DateTimeField, auto_now_add=True)
#    - updated_at (DateTimeField, auto_now=True)
#    - is_active (BooleanField, default=True)
#    - Meta: ordering by -created_at, with indexes
#
# 2. Event model (Topics 44-46):
#    - project (ForeignKey to Project, on_delete=CASCADE)
#    - event_type (CharField with choices: view, click, submit, error)
#    - user_id (CharField, blank=True)
#    - url (URLField, blank=True)
#    - timestamp (DateTimeField, auto_now_add=True)
#    - duration_ms (IntegerField, default=0)
#    - Meta: ordering by -timestamp, with indexes
#
# 3. Analytics model (Topics 47-49):
#    - project (OneToOneField to Project, on_delete=CASCADE)
#    - total_events (IntegerField, default=0)
#    - total_views (IntegerField, default=0)
#    - total_clicks (IntegerField, default=0)
#    - total_errors (IntegerField, default=0)
#    - average_duration (FloatField, default=0.0)
#    - last_updated (DateTimeField, auto_now=True)
