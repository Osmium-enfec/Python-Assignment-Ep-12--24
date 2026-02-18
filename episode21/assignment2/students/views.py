from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Course
from .forms import CourseForm

# Topic 54-55: Form Display in Views
def course_list(request):
    """
    Topic 54: Form Display in Templates
    Display all courses
    """
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'students/course_list.html', context)

# Topic 56-61: Form Submission and Validation Handling
def add_course(request):
    """
    Topic 56-61: Complete form handling with validation
    Topic 62: Form Errors Display
    Topic 63-64: Bootstrap Form Styling
    """
    
    if request.method == 'POST':
        # Topic 56: Form with POST Data
        form = CourseForm(request.POST)
        
        # Topic 57: is_valid() Check
        if form.is_valid():
            # Topic 58: cleaned_data Access
            cleaned_data = form.cleaned_data
            
            # Topic 59: Form Save
            course = form.save()
            
            # Topic 65-66: Success Messages
            messages.success(
                request,
                f'Course {course.code} - {course.name} created successfully!'
            )
            return redirect('students:course_list')
        else:
            # Topic 62: Form Errors Handling
            messages.error(request, 'Please correct the errors below.')
    else:
        # Topic 60: Blank Form Instance
        form = CourseForm()
    
    context = {'form': form}
    return render(request, 'students/add_course.html', context)

# Topic 61: Edit Operations with Validation
def edit_course(request, course_id):
    """
    Topic 61: Form Edit Pattern with validation
    Topic 67-68: Pre-populated Forms
    """
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(
                request,
                f'Course {course.code} updated successfully!'
            )
            return redirect('students:course_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Topic 67: Instance Parameter for Pre-population
        form = CourseForm(instance=course)
    
    context = {'form': form, 'course': course}
    return render(request, 'students/edit_course.html', context)

# Topic 69-70: Delete Operations
def delete_course(request, course_id):
    """
    Topic 69: Delete Confirmation
    Topic 70: Delete with Redirect
    """
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        course_name = f"{course.code} - {course.name}"
        course.delete()
        # Topic 71-73: Success Messages after Delete
        messages.success(request, f'Course {course_name} deleted successfully!')
        return redirect('students:course_list')
    
    context = {'course': course}
    return render(request, 'students/delete_course.html', context)

# Topic 74-76: Form Validation Showcase
def validate_course(request):
    """
    Topic 74-76: Validate form without saving
    Topic 77: Error Summary Display
    """
    if request.method == 'POST':
        form = CourseForm(request.POST)
        
        # Topic 74: Check Validation without Saving
        if form.is_valid():
            # Topic 75: Access Valid Data
            messages.success(request, 'Form validation passed!')
        else:
            # Topic 76-77: Display Validation Errors
            messages.error(request, 'Form validation failed. See errors below.')
        
        context = {'form': form}
        return render(request, 'students/validate_course.html', context)
    else:
        form = CourseForm()
    
    context = {'form': form}
    return render(request, 'students/validate_course.html', context)
