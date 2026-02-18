from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Topic 1-5: Django Admin for Forms (Topic 64 related - Admin interface)
    list_display = ('roll_no', 'name', 'email', 'gpa', 'is_active', 'enrolled_date')
    list_filter = ('is_active', 'enrolled_date')
    search_fields = ('roll_no', 'name', 'email')
    readonly_fields = ('enrolled_date',)
