from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Course, Enrollment

# Topic 1-8: Bootstrap Modals and AJAX

def course_list(request):
    """
    Topic 45: Modal Component - Main page displaying courses with modal triggers
    Topic 69-71: Action Buttons - View, Edit, Delete buttons triggering modals
    """
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses/list.html', context)

@require_http_methods(["GET"])
def course_detail_ajax(request, course_id):
    """
    Topic 62-63: Fetch API and fetch() Method
    Topic 64: JsonResponse - Return JSON for AJAX requests
    Topic 61: AJAX - Asynchronous data loading
    Topic 68: Dynamic Content - Data loaded into modal
    """
    course = get_object_or_404(Course, id=course_id)
    data = {
        'id': course.id,
        'code': course.code,
        'title': course.title,
        'description': course.description,
        'instructor': course.instructor,
        'credits': course.credits,
        'enrolled_count': course.enrolled_count,
        'max_students': course.max_students,
        'available_seats': course.available_seats(),
        'is_full': course.is_full(),
    }
    return JsonResponse(data)

@require_http_methods(["GET"])
def course_edit_form(request, course_id):
    """
    Topic 78: Pre-filled Modal Forms - Return HTML form pre-filled with data
    Topic 64: JsonResponse with HTML content
    """
    course = get_object_or_404(Course, id=course_id)
    html_form = f"""
    <form id="editForm" method="POST">
        <div class="mb-3">
            <label for="title" class="form-label">Title</label>
            <input type="text" class="form-control" id="title" name="title" value="{course.title}" required>
        </div>
        <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea class="form-control" id="description" name="description" required>{course.description}</textarea>
        </div>
        <div class="mb-3">
            <label for="instructor" class="form-label">Instructor</label>
            <input type="text" class="form-control" id="instructor" name="instructor" value="{course.instructor}" required>
        </div>
        <div class="mb-3">
            <label for="credits" class="form-label">Credits</label>
            <input type="number" class="form-control" id="credits" name="credits" value="{course.credits}" required>
        </div>
    </form>
    """
    return JsonResponse({'form': html_form})

@require_http_methods(["POST"])
def update_course_ajax(request, course_id):
    """
    Topic 65: AJAX - Handle AJAX POST request
    Topic 69: Fetch API with POST method
    """
    course = get_object_or_404(Course, id=course_id)
    course.title = request.POST.get('title', course.title)
    course.description = request.POST.get('description', course.description)
    course.instructor = request.POST.get('instructor', course.instructor)
    course.credits = int(request.POST.get('credits', course.credits))
    course.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Course updated successfully',
        'course': {
            'id': course.id,
            'title': course.title,
            'code': course.code
        }
    })

@require_http_methods(["GET"])
def course_enrollments(request, course_id):
    """
    Topic 63: fetch() Method - Load related data
    Topic 68: Dynamic Content - Display enrollments in modal
    """
    course = get_object_or_404(Course, id=course_id)
    enrollments = course.enrollment_set.all()
    
    data = {
        'course_code': course.code,
        'course_title': course.title,
        'enrollments': [
            {
                'id': e.id,
                'student_name': e.student_name,
                'enrolled_date': e.enrolled_date.strftime('%Y-%m-%d %H:%M')
            }
            for e in enrollments
        ],
        'total_enrollments': enrollments.count()
    }
    return JsonResponse(data)

@require_http_methods(["POST"])
def enroll_student(request, course_id):
    """
    Topic 65: AJAX - Handle enrollment via AJAX
    Topic 74: Button Action - Enrollment button
    """
    course = get_object_or_404(Course, id=course_id)
    
    if course.is_full():
        return JsonResponse({
            'success': False,
            'message': 'Course is full'
        })
    
    student_name = request.POST.get('student_name', 'Anonymous')
    enrollment = Enrollment.objects.create(course=course, student_name=student_name)
    course.enrolled_count += 1
    course.save()
    
    return JsonResponse({
        'success': True,
        'message': f'Successfully enrolled {student_name}',
        'available_seats': course.available_seats()
    })

@require_http_methods(["GET"])
def delete_course_confirm(request, course_id):
    """
    Topic 75: Confirmation Dialog - Get confirmation data
    Topic 63: Dynamic data loading for confirmation
    """
    course = get_object_or_404(Course, id=course_id)
    enrollment_count = course.enrollment_set.count()
    
    data = {
        'course_code': course.code,
        'course_title': course.title,
        'enrollment_count': enrollment_count,
        'message': f'This course has {enrollment_count} enrollments. Are you sure?'
    }
    return JsonResponse(data)

@require_http_methods(["POST"])
def delete_course(request, course_id):
    """
    Topic 75: Delete confirmation and action
    Topic 71: Delete Button functionality
    """
    course = get_object_or_404(Course, id=course_id)
    course_code = course.code
    course.delete()
    
    return JsonResponse({
        'success': True,
        'message': f'Course {course_code} deleted successfully'
    })

@require_http_methods(["GET"])
def course_stats(request):
    """
    Topic 63: Multiple AJAX data fetching
    """
    courses = Course.objects.all()
    total_courses = courses.count()
    total_enrollments = sum(e.enrolled_count for e in courses) if courses.exists() else 0
    total_capacity = sum(e.max_students for e in courses) if courses.exists() else 0
    
    data = {
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'total_capacity': total_capacity,
        'average_per_course': round(total_enrollments / total_courses, 1) if total_courses > 0 else 0
    }
    return JsonResponse(data)

@require_http_methods(["POST"])
def search_courses(request):
    """
    Topic 65: AJAX search functionality
    """
    query = request.POST.get('q', '')
    courses = Course.objects.filter(
        title__icontains=query
    ) | Course.objects.filter(
        code__icontains=query
    )
    
    data = {
        'courses': [
            {
                'id': c.id,
                'code': c.code,
                'title': c.title,
                'available_seats': c.available_seats()
            }
            for c in courses
        ]
    }
    return JsonResponse(data)
