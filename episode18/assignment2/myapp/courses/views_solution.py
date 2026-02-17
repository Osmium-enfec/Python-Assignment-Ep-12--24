from django.shortcuts import render
from .models import Student, Course, Enrollment

def student_list(request):
    """Display list of all students"""
    students = Student.objects.all().order_by('roll_no')
    context = {'students': students}
    return render(request, 'courses/student_list.html', context)

def course_list(request):
    """Display list of all courses"""
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses/course_list.html', context)

def course_detail(request, course_id):
    """Display course details with enrolled students"""
    course = Course.objects.get(id=course_id)
    enrollments = course.enrollment_set.all()
    context = {'course': course, 'enrollments': enrollments}
    return render(request, 'courses/course_detail.html', context)

def student_detail(request, student_id):
    """Display student details with enrolled courses"""
    student = Student.objects.get(id=student_id)
    enrollments = student.enrollment_set.all()
    context = {'student': student, 'enrollments': enrollments}
    return render(request, 'courses/student_detail.html', context)

def enrollment_list(request):
    """Display all enrollments"""
    enrollments = Enrollment.objects.all().order_by('-enrollment_date')
    context = {'enrollments': enrollments}
    return render(request, 'courses/enrollment_list.html', context)
