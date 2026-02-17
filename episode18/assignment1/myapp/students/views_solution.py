from django.shortcuts import render
from django.http import HttpResponse
from .models import Student

def student_list(request):
    """Display list of all students"""
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'students/list.html', context)

def student_detail(request, student_id):
    """Display details of a single student"""
    student = Student.objects.get(id=student_id)
    context = {'student': student}
    return render(request, 'students/detail.html', context)
