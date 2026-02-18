from django.contrib import admin
from .models import Student, Course, Grade

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin configuration for Student model"""
    list_display = ('name', 'roll_no', 'email', 'status', 'gpa', 'gpa_grade')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'roll_no')
    readonly_fields = ('created_at',)
    ordering = ['name']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'date_of_birth')
        }),
        ('Academic Information', {
            'fields': ('roll_no', 'gpa', 'status')
        }),
        ('System Info', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for Course model"""
    list_display = ('code', 'name', 'credits')
    search_fields = ('code', 'name')
    ordering = ['code']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    """Admin configuration for Grade model"""
    list_display = ('student', 'course', 'score', 'letter_grade', 'semester', 'year')
    list_filter = ('semester', 'year', 'course')
    search_fields = ('student__name', 'course__code')
    ordering = ['-year', '-semester']
