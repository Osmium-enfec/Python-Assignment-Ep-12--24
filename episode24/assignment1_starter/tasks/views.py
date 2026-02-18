from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# TODO: Create 5 views:
# 1. task_list - Display all tasks
# 2. task_create - Create new task (GET shows form, POST saves)
# 3. task_detail - Show single task details (use get_object_or_404)
# 4. task_update - Update task (GET shows form with data, POST saves)
# 5. task_delete - Delete task (GET shows confirmation, POST deletes)
#
# Use messages framework for success messages
# Use POST-Redirect-GET pattern for POST requests
# Use get_object_or_404 for safety
