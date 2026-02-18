from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'enrollment_date', 'is_active']
    list_filter = ['is_active', 'enrollment_date']
    search_fields = ['email', 'first_name', 'last_name']
