from django.test import TestCase, Client
from django.urls import reverse
from .models import Student

class URLRoutingTestCase(TestCase):
    """Tests for URL routing and patterns (Topics 1-10)"""
    
    def setUp(self):
        """Topic 38: Model.objects.all() - Creating test data"""
        self.client = Client()
        self.student = Student.objects.create(
            roll_no='S001',
            name='Student 1',
            email='test@example.com',
            phone='9999999999',
            gpa=3.8
        )
    
    def test_url_routing_list(self):
        """Topic 1: URL Routing - Basic path mapping"""
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)
    
    def test_path_function_detail(self):
        """Topic 2: path() Function - Dynamic URL routing"""
        response = self.client.get(f'/students/{self.student.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_url_parameters_integer(self):
        """Topic 3 & 4: URL Parameters with int Converter"""
        url = reverse('students:detail', args=[self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.student.name)
    
    def test_str_converter_roll_no(self):
        """Topic 5: str Converter - String parameter in URL"""
        url = reverse('students:by_roll', args=[self.student.roll_no])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_url_name_reverse(self):
        """Topic 6: URL Name - Named URL patterns"""
        url = reverse('students:list')
        self.assertEqual(url, '/students/')
    
    def test_url_inclusion(self):
        """Topic 10: URL Inclusion - app URLs nested in project"""
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)


class URLReversalTestCase(TestCase):
    """Tests for reverse() function (Topics 11-18)"""
    
    def setUp(self):
        self.student = Student.objects.create(
            roll_no='S002',
            name='Student 2',
            email='student2@test.com',
            gpa=3.5
        )
    
    def test_reverse_function(self):
        """Topic 11: reverse() Function"""
        url = reverse('students:list')
        self.assertTrue(url.startswith('/students'))
    
    def test_reverse_with_args(self):
        """Topic 12: reverse() with Args"""
        url = reverse('students:detail', args=[self.student.id])
        self.assertEqual(url, f'/students/{self.student.id}/')
    
    def test_reverse_with_kwargs(self):
        """Topic 13 & 14: reverse() with Kwargs and Namespace"""
        url = reverse('students:by_roll', args=[self.student.roll_no])
        self.assertIn(self.student.roll_no, url)
    
    def test_template_url_tag(self):
        """Topic 15: Template Tag {% url %} - Used in templates"""
        response = self.client.get(reverse('students:detail', args=[self.student.id]))
        self.assertContains(response, f'/students/{self.student.id}/')
    
    def test_url_maintainability(self):
        """Topic 17 & 18: Flexibility and Maintainability"""
        # URLs can change without breaking template/view code
        url1 = reverse('students:list')
        url2 = reverse('students:list')
        self.assertEqual(url1, url2)


class RedirectTestCase(TestCase):
    """Tests for HTTP redirects (Topics 19-26)"""
    
    def setUp(self):
        self.student = Student.objects.create(
            roll_no='S003',
            name='Student 3',
            email='student3@test.com',
            gpa=3.2
        )
    
    def test_redirect_to_name(self):
        """Topic 23: Redirect to Name - Using view name"""
        response = self.client.get(reverse('students:redirect_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('students:list'))
    
    def test_post_redirect_get_pattern(self):
        """Topic 25: Post-Redirect-Get - After form submission"""
        response = self.client.post(
            reverse('students:create'),
            {
                'roll_no': 'S004',
                'name': 'New Student',
                'email': 'new@test.com',
                'gpa': '3.6'
            }
        )
        self.assertEqual(response.status_code, 302)


class ViewFunctionTestCase(TestCase):
    """Tests for view functions (Topics 27-35)"""
    
    def setUp(self):
        self.student = Student.objects.create(
            roll_no='S005',
            name='Student 5',
            email='student5@test.com',
            phone='1111111111',
            gpa=3.9
        )
    
    def test_view_function_request_parameter(self):
        """Topic 27 & 28: View Function and Request Parameter"""
        response = self.client.get(reverse('students:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_return_types(self):
        """Topic 29: View Return - Different response types"""
        # HTML response
        response = self.client.get(reverse('students:detail', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        
        # JSON response
        response = self.client.get(reverse('students:export', args=[self.student.id]))
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def test_http_methods_get(self):
        """Topic 30: HTTP Methods - GET"""
        response = self.client.get(reverse('students:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_http_methods_post(self):
        """Topic 30 & 31: HTTP Methods - POST and Method Checking"""
        response = self.client.post(
            reverse('students:create'),
            {
                'roll_no': 'S006',
                'name': 'Test Student',
                'email': 'test@test.com',
                'gpa': '3.7'
            }
        )
        self.assertEqual(response.status_code, 302)
    
    def test_context_dictionary(self):
        """Topic 32: Context Dictionary - Data passed to template"""
        response = self.client.get(reverse('students:list'))
        self.assertIn('students', response.context)
    
    def test_view_parameters(self):
        """Topic 34: View Parameters - URL parameters captured"""
        response = self.client.get(reverse('students:detail', args=[self.student.id]))
        self.assertEqual(response.context['student'].id, self.student.id)
    
    def test_request_data_post(self):
        """Topic 35: Request Data - POST data processing"""
        response = self.client.post(
            reverse('students:create'),
            {
                'roll_no': 'S007',
                'name': 'Created Student',
                'email': 'created@test.com',
                'gpa': '3.5'
            }
        )
        new_student = Student.objects.get(roll_no='S007')
        self.assertEqual(new_student.name, 'Created Student')


class ObjectRetrievalTestCase(TestCase):
    """Tests for object retrieval (Topics 36-40)"""
    
    def setUp(self):
        self.student = Student.objects.create(
            roll_no='S008',
            name='Student 8',
            email='student8@test.com',
            gpa=3.3
        )
    
    def test_get_object_or_404(self):
        """Topic 36: get_object_or_404() - Returns 404 if not found"""
        response = self.client.get(reverse('students:detail', args=[999]))
        self.assertEqual(response.status_code, 404)
    
    def test_queryset(self):
        """Topic 37: QuerySet - Database query results"""
        response = self.client.get(reverse('students:list'))
        students = response.context['students']
        self.assertIn(self.student, students)
    
    def test_model_objects_all(self):
        """Topic 38: Model.objects.all() - All instances"""
        Student.objects.create(roll_no='S009', name='Student 9', email='s9@test.com')
        response = self.client.get(reverse('students:list'))
        self.assertEqual(len(response.context['students']), 2)
    
    def test_model_objects_filter(self):
        """Topic 39: Model.objects.filter() - Filtered instances"""
        Student.objects.create(roll_no='S010', name='Student 10', email='s10@test.com', gpa=3.6)
        response = self.client.get(reverse('students:by_gpa', args=['3.5']))
        students = response.context['students']
        self.assertTrue(all(s.gpa >= 3.5 for s in students))
    
    def test_model_objects_get(self):
        """Topic 40: Model.objects.get() - Single instance by criteria"""
        response = self.client.get(reverse('students:by_roll', args=[self.student.roll_no]))
        self.assertEqual(response.context['student'].roll_no, self.student.roll_no)
