from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Student, Course, Department, Enrollment

def admin_dashboard(request):
    """Admin dashboard view"""
    context = {
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
        'total_departments': Department.objects.count(),
    }
    return render(request, 'students/admin_dashboard.html', context)
