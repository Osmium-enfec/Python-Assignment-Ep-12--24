from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from .models import Student

# Topic 1: View Function - Basic list view showing all students
def student_list(request):
    """
    Topic 27: View Function
    Topic 28: Request Parameter
    Topic 29: View Return
    Topic 32: Context Dictionary
    Topic 33: render() Function
    Topic 38: Model.objects.all()
    """
    students = Student.objects.all().order_by('roll_no')
    context = {'students': students}
    return render(request, 'students/list.html', context)

# Topic 2: View with URL parameters
def student_detail(request, student_id):
    """
    Topic 34: View Parameters - Captures student_id from URL
    Topic 36: get_object_or_404() - Returns 404 if student not found
    Topic 37: QuerySet - Result from database lookup
    """
    student = get_object_or_404(Student, id=student_id)
    context = {'student': student}
    return render(request, 'students/detail.html', context)

# Topic 3: View with filtering
def student_by_gpa(request, min_gpa):
    """
    Topic 34: View Parameters - Captures min_gpa from URL (float converter)
    Topic 39: Model.objects.filter() - Filters students by GPA
    Topic 40: Model.objects.get() - Would raise DoesNotExist if no match
    """
    students = Student.objects.filter(gpa__gte=min_gpa).order_by('-gpa')
    context = {
        'students': students,
        'min_gpa': min_gpa,
        'title': f'Students with GPA >= {min_gpa}'
    }
    return render(request, 'students/filtered_list.html', context)

# Topic 4: POST redirect pattern
def create_student(request):
    """
    Topic 30: HTTP Methods - GET shows form, POST processes submission
    Topic 31: Method Checking - if request.method == 'POST'
    Topic 35: Request Data - request.POST contains form data
    Topic 19: HttpResponseRedirect - Implicit via redirect()
    Topic 20: redirect() Shortcut - Redirects after successful POST
    Topic 25: Post-Redirect-Get - Pattern preventing form resubmission
    """
    if request.method == 'POST':
        student = Student.objects.create(
            roll_no=request.POST['roll_no'],
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST.get('phone', ''),
            gpa=float(request.POST.get('gpa', 0))
        )
        # Redirecting using reverse() - Topic 11: reverse() Function
        return redirect(reverse('students:detail', args=[student.id]))
    return render(request, 'students/create.html')

# Topic 5: URL reversal in view
def view_student_info(request, roll_no):
    """
    Topic 11: reverse() Function
    Topic 12: reverse() with Args
    Topic 13: reverse() with Kwargs
    Topic 14: Namespace Usage - Using 'students:view' pattern
    Topic 15: Template Tag {% url %} equivalent in Python
    """
    student = get_object_or_404(Student, roll_no=roll_no)
    # Building URL using reverse
    detail_url = reverse('students:detail', args=[student.id])
    context = {'student': student, 'detail_url': detail_url}
    return render(request, 'students/view_info.html', context)

# Topic 6: Redirect example
def redirect_to_list(request):
    """
    Topic 23: Redirect to Name - Using URL pattern name
    Topic 24: Redirect to URL - Using hardcoded URL path
    """
    return redirect('students:list')

# Topic 7: Delete with redirect
def delete_student(request, student_id):
    """
    Topic 20: redirect() Shortcut
    Topic 21: Redirect After POST
    Topic 25: Post-Redirect-Get
    Topic 26: Session Data - Messages after delete (can be enhanced)
    """
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('students:list')
    return render(request, 'students/delete_confirm.html', {'student': student})

# Topic 8: Edit student view
def edit_student(request, student_id):
    """
    Topic 31: Method Checking
    Topic 35: Request Data
    Topic 20: redirect() after successful update
    """
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.phone = request.POST.get('phone', '')
        student.gpa = float(request.POST.get('gpa', student.gpa))
        student.address = request.POST.get('address', '')
        student.save()
        return redirect(reverse('students:detail', args=[student.id]))
    
    context = {'student': student}
    return render(request, 'students/edit.html', context)

# Topic 9: Search/filter view
def search_students(request):
    """
    Topic 35: Request Data - GET parameters
    Topic 39: Model.objects.filter() - Dynamic filtering
    """
    query = request.GET.get('q', '')
    if query:
        students = Student.objects.filter(
            Q(name__icontains=query) | 
            Q(roll_no__icontains=query)
        )
    else:
        students = Student.objects.all()
    
    context = {'students': students, 'query': query}
    return render(request, 'students/search_results.html', context)

# Topic 10: Export student data (different return type)
def export_student_data(request, student_id):
    """
    Topic 29: View Return - Can return different types (JSON, CSV, etc)
    """
    from django.http import JsonResponse
    student = get_object_or_404(Student, id=student_id)
    data = {
        'id': student.id,
        'roll_no': student.roll_no,
        'name': student.name,
        'email': student.email,
        'gpa': student.gpa,
    }
    return JsonResponse(data)
