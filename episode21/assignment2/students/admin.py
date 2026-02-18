from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credit_hours', 'max_students', 'is_active', 'created_at')
    list_filter = ('is_active', 'credit_hours', 'created_at')
    search_fields = ('code', 'name', 'instructor_email')
    readonly_fields = ('created_at',)
