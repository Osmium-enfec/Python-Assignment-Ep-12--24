from django.contrib import admin
from .models import Department, Student, Course, Enrollment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin configuration for Department model"""
    list_display = ('name', 'code', 'head', 'phone')
    search_fields = ('name', 'code')
    ordering = ['name']
    
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'code')
        }),
        ('Contact Information', {
            'fields': ('head', 'phone')
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Advanced admin configuration for Student model"""
    list_display = ('name', 'roll_no', 'department', 'status', 'gpa', 'is_scholarship_holder', 'admission_date')
    list_filter = ('status', 'department', 'is_scholarship_holder', 'admission_date')
    search_fields = ('name', 'email', 'roll_no')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'admission_date'
    ordering = ['-admission_date']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'date_of_birth')
        }),
        ('Academic Information', {
            'fields': ('roll_no', 'department', 'gpa', 'status', 'is_scholarship_holder')
        }),
        ('Important Dates', {
            'fields': ('admission_date', 'created_at', 'updated_at'),
        }),
    )
    
    actions = ['mark_active', 'mark_inactive']
    
    def mark_active(self, request, queryset):
        """Bulk action to mark students as active"""
        count = queryset.update(status='active')
        self.message_user(request, f'{count} students marked as active.')
    mark_active.short_description = "Mark selected students as active"
    
    def mark_inactive(self, request, queryset):
        """Bulk action to mark students as inactive"""
        count = queryset.update(status='inactive')
        self.message_user(request, f'{count} students marked as inactive.')
    mark_inactive.short_description = "Mark selected students as inactive"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for Course model"""
    list_display = ('code', 'name', 'department', 'get_level_display', 'credits', 'is_active')
    list_filter = ('department', 'level', 'is_active')
    search_fields = ('code', 'name')
    ordering = ['code']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('code', 'name', 'department')
        }),
        ('Course Details', {
            'fields': ('level', 'credits', 'is_active')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )
    
    def get_level_display(self, obj):
        return obj.get_level_display()
    get_level_display.short_description = 'Level'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin configuration for Enrollment model"""
    list_display = ('student', 'course', 'semester', 'year', 'score', 'grade', 'is_completed')
    list_filter = ('semester', 'year', 'course__department', 'is_completed')
    search_fields = ('student__name', 'course__code')
    readonly_fields = ('enrollment_date',)
    date_hierarchy = 'enrollment_date'
    
    fieldsets = (
        ('Enrollment Information', {
            'fields': ('student', 'course', 'semester', 'year')
        }),
        ('Performance', {
            'fields': ('score', 'grade', 'is_completed')
        }),
        ('Metadata', {
            'fields': ('enrollment_date',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_completed']
    
    def mark_completed(self, request, queryset):
        """Mark selected enrollments as completed"""
        count = queryset.update(is_completed=True)
        self.message_user(request, f'{count} enrollments marked as completed.')
    mark_completed.short_description = "Mark selected enrollments as completed"


# Customize admin site
admin.site.site_header = "Student Management Admin"
admin.site.site_title = "Student Admin Portal"
admin.site.index_title = "Welcome to Student Management System - Episode 19"
