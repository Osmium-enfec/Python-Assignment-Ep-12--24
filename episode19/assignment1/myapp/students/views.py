from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Student, Grade

def home(request):
    """Home page with student statistics"""
    context = {
        'total_students': Student.objects.count(),
        'active_students': Student.objects.filter(status='active').count(),
        'dean_list_count': Student.objects.filter(gpa__gte=3.5).count(),
    }
    return render(request, 'students/home.html', context)


def student_list(request):
    """Display all students in a Bootstrap table with conditionals"""
    students = Student.objects.all()
    context = {
        'students': students,
        'total': students.count(),
        'active': students.filter(status='active').count(),
    }
    return render(request, 'students/student_list.html', context)


def student_detail(request, pk):
    """Display individual student details with grades table"""
    student = Student.objects.get(pk=pk)
    grades = Grade.objects.filter(student=student)
    
    context = {
        'student': student,
        'grades': grades,
        'passing_grades': grades.filter(score__gte=60).count(),
        'total_grades': grades.count(),
    }
    return render(request, 'students/student_detail.html', context)


def grade_report(request):
    """Display grade report with filtering"""
    semester = request.GET.get('semester', None)
    year = request.GET.get('year', None)
    
    grades = Grade.objects.all()
    
    if semester:
        grades = grades.filter(semester=semester)
    if year:
        grades = grades.filter(year=year)
    
    context = {
        'grades': grades,
        'semester': semester,
        'year': year,
        'total_grades': grades.count(),
        'passing': grades.filter(score__gte=60).count(),
    }
    return render(request, 'students/grade_report.html', context)
