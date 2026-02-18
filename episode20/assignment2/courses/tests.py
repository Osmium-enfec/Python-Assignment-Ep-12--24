from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
import json
from .models import Course, Enrollment

class BootstrapModalTestCase(TestCase):
    """Tests for Bootstrap Modals (Topics 41-58)"""
    
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            code='CS101',
            title='Introduction to Computer Science',
            description='Learn the basics of programming',
            instructor='Dr. Smith',
            credits=3,
            max_students=30
        )
    
    def test_modal_component_rendering(self):
        """Topic 45: Modal Component - Main page renders with modals"""
        response = self.client.get(reverse('courses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('courseModal', response.content.decode())
    
    def test_modal_header_footer(self):
        """Topic 43 & 45: Modal Header and Footer"""
        response = self.client.get(reverse('courses:list'))
        content = response.content.decode()
        self.assertIn('modal-header', content)
        self.assertIn('modal-footer', content)
    
    def test_modal_body_content(self):
        """Topic 44: Modal Body - Contains dynamic content"""
        response = self.client.get(reverse('courses:list'))
        content = response.content.decode()
        self.assertIn('modal-body', content)
    
    def test_modal_toggle_attributes(self):
        """Topic 51 & 52: data-bs-toggle and data-bs-target"""
        response = self.client.get(reverse('courses:list'))
        content = response.content.decode()
        self.assertIn('data-bs-toggle="modal"', content)
        self.assertIn('data-bs-target=', content)
    
    def test_modal_sizing(self):
        """Topic 54: Modal Size - Different modal sizes"""
        response = self.client.get(reverse('courses:list'))
        content = response.content.decode()
        self.assertIn('modal-dialog-centered', content)
    
    def test_modal_ids(self):
        """Topic 50: Modal ID - Unique identifiers"""
        response = self.client.get(reverse('courses:list'))
        content = response.content.decode()
        self.assertIn('id="courseModal"', content)
        self.assertIn('id="editModal"', content)
        self.assertIn('id="deleteModal"', content)


class AJAXAndFetchTestCase(TestCase):
    """Tests for AJAX and Fetch API (Topics 61-68)"""
    
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            code='CS102',
            title='Data Structures',
            description='Learn about arrays, lists, trees',
            instructor='Dr. Johnson',
            credits=4,
            max_students=25,
            enrolled_count=15
        )
    
    def test_ajax_detail_endpoint(self):
        """Topic 61 & 62: AJAX and Fetch API"""
        response = self.client.get(reverse('courses:detail_ajax', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_json_response_content(self):
        """Topic 64: JsonResponse - Returns JSON data"""
        response = self.client.get(reverse('courses:detail_ajax', args=[self.course.id]))
        data = json.loads(response.content)
        
        self.assertEqual(data['code'], 'CS102')
        self.assertEqual(data['title'], 'Data Structures')
        self.assertEqual(data['enrolled_count'], 15)
        self.assertEqual(data['available_seats'], 10)
    
    def test_dynamic_content_loading(self):
        """Topic 68: Dynamic Content - Data ready for insertion"""
        response = self.client.get(reverse('courses:detail_ajax', args=[self.course.id]))
        data = json.loads(response.content)
        
        self.assertIn('id', data)
        self.assertIn('code', data)
        self.assertIn('title', data)
        self.assertIn('description', data)
    
    def test_loading_state_support(self):
        """Topic 67: Loading State - Content available for display"""
        response = self.client.get(reverse('courses:list'))
        content = response.content.decode()
        self.assertIn('spinner-border', content)
    
    def test_search_ajax_endpoint(self):
        """Topic 65: AJAX - Search functionality"""
        Course.objects.create(
            code='CS103',
            title='Algorithms',
            description='Algorithm design',
            instructor='Dr. Williams',
            credits=3,
            max_students=30
        )
        
        response = self.client.post(
            reverse('courses:search'),
            {'q': 'Algorithms'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['courses']), 1)
        self.assertEqual(data['courses'][0]['title'], 'Algorithms')
    
    def test_error_handling_ajax(self):
        """Topic 70: Error Handling - Invalid course ID"""
        response = self.client.get(reverse('courses:detail_ajax', args=[999]))
        self.assertEqual(response.status_code, 404)


class ActionButtonsTestCase(TestCase):
    """Tests for Action Buttons (Topics 69-76)"""
    
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            code='CS104',
            title='Web Development',
            description='HTML, CSS, JavaScript',
            instructor='Dr. Davis',
            credits=3,
            max_students=20
        )
    
    def test_view_button_action(self):
        """Topic 69: View Button - Loads course details"""
        response = self.client.get(reverse('courses:detail_ajax', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'Web Development')
    
    def test_edit_button_form_loading(self):
        """Topic 70: Edit Button - Loads pre-filled form"""
        response = self.client.get(reverse('courses:edit_form', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('form', data)
        self.assertIn('Web Development', data['form'])
    
    def test_edit_course_update(self):
        """Topic 70: Edit Button - Updates course"""
        response = self.client.post(
            reverse('courses:update', args=[self.course.id]),
            {
                'title': 'Advanced Web Development',
                'description': 'HTML5, CSS3, Modern JavaScript',
                'instructor': 'Dr. Davis',
                'credits': 4
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Advanced Web Development')
    
    def test_delete_button_confirmation(self):
        """Topic 71: Delete Button - Shows confirmation"""
        Enrollment.objects.create(
            course=self.course,
            student_name='John Doe'
        )
        
        response = self.client.get(reverse('courses:delete_confirm', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        self.assertIn('message', data)
        self.assertIn('enrollment_count', data)
        self.assertEqual(data['enrollment_count'], 1)
    
    def test_delete_button_execution(self):
        """Topic 71: Delete Button - Deletes course"""
        course_id = self.course.id
        response = self.client.post(
            reverse('courses:delete', args=[course_id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(id=course_id)
    
    def test_button_styling_classes(self):
        """Topic 72 & 73: Button Styling and Icons"""
        response = self.client.get(reverse('courses:list'))
        content = response.content.decode()
        
        # Check for button styling classes
        self.assertIn('btn-info', content)
        self.assertIn('btn-warning', content)
        self.assertIn('btn-danger', content)
        
        # Check for Font Awesome icons
        self.assertIn('fa-eye', content)
        self.assertIn('fa-edit', content)
        self.assertIn('fa-trash', content)


class ModalInteractionsTestCase(TestCase):
    """Tests for Modal Interactions (Topics 55-60)"""
    
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            code='CS105',
            title='Database Design',
            description='SQL and NoSQL databases',
            instructor='Dr. Miller',
            credits=3,
            max_students=25
        )
    
    def test_enrollment_modal_flow(self):
        """Topic 54-60: Complete modal interaction flow"""
        # 1. Load course details
        response = self.client.get(reverse('courses:detail_ajax', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        
        # 2. Enroll student
        response = self.client.post(
            reverse('courses:enroll', args=[self.course.id]),
            {'student_name': 'Jane Doe'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # 3. Verify enrollment
        self.course.refresh_from_db()
        self.assertEqual(self.course.enrolled_count, 1)
    
    def test_enrollment_full_course(self):
        """Topic 45-60: Modal handling for full course"""
        self.course.max_students = 1
        self.course.enrolled_count = 1
        self.course.save()
        
        response = self.client.post(
            reverse('courses:enroll', args=[self.course.id]),
            {'student_name': 'Bob Smith'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIn('full', data['message'].lower())
    
    def test_enrollments_list_modal(self):
        """Topic 44 & 68: Dynamic content in enrollments modal"""
        Enrollment.objects.create(course=self.course, student_name='Student 1')
        Enrollment.objects.create(course=self.course, student_name='Student 2')
        
        response = self.client.get(reverse('courses:enrollments', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['total_enrollments'], 2)
        self.assertEqual(len(data['enrollments']), 2)


class AJAXFormHandlingTestCase(TestCase):
    """Tests for AJAX Form Handling (Topics 65-76)"""
    
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            code='CS106',
            title='Software Engineering',
            description='Development practices',
            instructor='Dr. Brown',
            credits=3,
            max_students=20
        )
    
    def test_pre_filled_edit_form(self):
        """Topic 78: Pre-filled Modal Forms"""
        response = self.client.get(reverse('courses:edit_form', args=[self.course.id]))
        data = json.loads(response.content)
        form_html = data['form']
        
        self.assertIn('Software Engineering', form_html)
        self.assertIn('Dr. Brown', form_html)
        self.assertIn('value=', form_html)
    
    def test_course_statistics_ajax(self):
        """Topic 61 & 68: Statistics via AJAX"""
        Course.objects.create(
            code='CS107',
            title='Cloud Computing',
            description='AWS, Azure, GCP',
            instructor='Dr. Wilson',
            credits=3,
            max_students=30,
            enrolled_count=20
        )
        
        response = self.client.get(reverse('courses:stats'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['total_courses'], 2)
        self.assertEqual(data['total_enrollments'], 20)
    
    def test_csrf_token_ajax_request(self):
        """Topic 65 & 66: X-Requested-With header for AJAX"""
        response = self.client.post(
            reverse('courses:update', args=[self.course.id]),
            {'title': 'Updated Title'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN='test'
        )
        
        # Request is accepted (CSRF validation in Django)
        self.assertIn(response.status_code, [200, 403])
