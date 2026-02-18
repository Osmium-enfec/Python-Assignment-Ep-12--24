from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, Avg

# TODO: Create 7 views (Topics 56-69):
#
# 1. project_list (Topic 56):
#    - Use select_related('analytics')
#    - Display all projects
#
# 2. project_detail (Topic 57):
#    - Use select_related('analytics')
#    - Show project details and recent events
#    - Calculate event statistics
#
# 3. analytics_dashboard (Topic 58):
#    - Calculate aggregate statistics using aggregate()
#    - Count total events by type
#    - Average duration
#
# 4. project_create (Topic 59):
#    - Create new project and initialize Analytics
#    - Redirect after creation
#
# 5. project_update (Topic 64):
#    - Update project details
#    - Use form with instance parameter
#
# 6. event_create (Topic 65):
#    - Create single event
#
# 7. event_bulk_create (Topic 66):
#    - Use bulk_create for multiple events
