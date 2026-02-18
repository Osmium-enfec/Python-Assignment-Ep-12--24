from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Student
from .forms import StudentForm

# Topic 31-34: GET/POST Request Handling and Method Checking
def student_list(request):
    """
    Topic 31: GET Request Handling - Display list of students
    """
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'students/list.html', context)

# Topic 35-40: Creating Form Instances and CSRF Protection
def add_student(request):
    """
    Topic 33: request.method Check - Differentiate GET vs POST
    Topic 34: GET and POST Differentiation
    Topic 35: Creating Blank Form Instance - GET request
    Topic 36: Creating Form with POST Data - POST request
    Topic 37: Form Submission Processing
    Topic 39: CSRF Token Security (automatic in Django)
    Topic 40: {% csrf_token %} Tag (in template)
    """
    
    if request.method == 'POST':
        # Topic 36: Creating Form with POST Data
        form = StudentForm(request.POST)
        
        # Topic 25-26: Form Validation using is_valid()
        if form.is_valid():
            # Topic 50: Form Save Method - Save to database
            student = form.save()
            # Topic 74-75: messages.success() Function
            messages.success(request, f'Student {student.name} added successfully!')
            return redirect('students:list')
        else:
            # Topic 76: messages.error() Function (optional)
            messages.error(request, 'Please correct the errors below.')
    else:
        # Topic 35: Creating Blank Form Instance for GET request
        form = StudentForm()
    
    # Topic 67: Passing Form to Template
    context = {'form': form}
    return render(request, 'students/add.html', context)

# Topic 78-80: Edit Form Pattern with Instance
def edit_student(request, student_id):
    """
    Topic 78: Form Edit Pattern
    Topic 79: Instance in Form Constructor - Pre-populate form
    Topic 80: Update vs Add Operations
    """
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.name} updated successfully!')
            return redirect('students:list')
    else:
        # Topic 79: Instance Parameter - Pre-fills form with existing data
        form = StudentForm(instance=student)
    
    context = {'form': form, 'student': student}
    return render(request, 'students/edit.html', context)

# Topic 72-73: Redirect After Success
def delete_student(request, student_id):
    """
    Topic 72: Redirect Function
    Topic 73: Redirect After Success
    """
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f'Student {name} deleted successfully!')
        # Topic 72: Redirect Function with reverse
        return redirect(reverse('students:list'))
    
    context = {'student': student}
    return render(request, 'students/delete_confirm.html', context)
