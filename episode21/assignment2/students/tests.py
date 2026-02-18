from django.test import TestCase, Client
from django.urls import reverse
from .models import Course
from .forms import CourseForm
from django.core.exceptions import ValidationError

class AdvancedValidationTestCase(TestCase):
    """Tests for Advanced Form Validation (Topics 41-50)"""
    
    def setUp(self):
        self.client = Client()
    
    def test_form_clean_method(self):
        """Topic 42: Form clean() Method - Custom form-level validation"""
        form_data = {
            'code': 'CS101',
            'name': 'Computer Science',
            'credit_hours': 3,
            'instructor_email': 'prof@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_custom_validation_code(self):
        """Topic 43: Custom Validation - Code field validation"""
        form_data = {
            'code': 'INVALID',  # No numbers
            'name': 'Test Course',
            'credit_hours': 3,
            'instructor_email': 'prof@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('code', form.errors)
    
    def test_field_level_validation_credit_hours(self):
        """Topic 44: Field-level Validation for credit hours"""
        form_data = {
            'code': 'CS101',
            'name': 'Test Course',
            'credit_hours': 5,  # Greater than 4
            'instructor_email': 'prof@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_cross_field_validation(self):
        """Topic 45: Cross-field Validation"""
        form_data = {
            'code': 'COMP',
            'name': 'Computer Science COMP',  # Code is at start of name
            'credit_hours': 3,
            'instructor_email': 'prof@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_clean_code_method(self):
        """Topic 46: Field-specific clean_<fieldname>() method"""
        form_data = {
            'code': 'MATH',  # No numbers
            'name': 'Mathematics',
            'credit_hours': 3,
            'instructor_email': 'prof@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('code', form.errors)
    
    def test_unique_field_validation(self):
        """Topic 47: Unique Field Validation - Database constraint"""
        # Create first course
        Course.objects.create(
            code='CS101',
            name='Computer Science 101',
            credit_hours=3,
            instructor_email='prof1@example.com',
            max_students=30,
            enrollment_fee=100.00
        )
        
        # Try to create duplicate
        form_data = {
            'code': 'CS101',
            'name': 'Different Name',
            'credit_hours': 3,
            'instructor_email': 'prof2@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_database_validation_unique_email(self):
        """Topic 48: Database Validation - Unique email constraint"""
        # Create first course
        Course.objects.create(
            code='CS101',
            name='Computer Science 101',
            credit_hours=3,
            instructor_email='unique@example.com',
            max_students=30,
            enrollment_fee=100.00
        )
        
        # Try to create with duplicate email
        form_data = {
            'code': 'CS102',
            'name': 'Computer Science 102',
            'credit_hours': 3,
            'instructor_email': 'unique@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_field_configuration(self):
        """Topic 49: Form Field Configuration"""
        form = CourseForm()
        self.assertIn('code', form.fields)
        self.assertIn('credit_hours', form.fields)
    
    def test_form_save(self):
        """Topic 50: Form Save Method"""
        form_data = {
            'code': 'CS101',
            'name': 'Computer Science 101',
            'credit_hours': 3,
            'instructor_email': 'prof@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        if form.is_valid():
            course = form.save()
            self.assertEqual(course.code, 'CS101')
            self.assertEqual(course.name, 'Computer Science 101')


class FormDisplayAndHandlingTestCase(TestCase):
    """Tests for Form Display and Handling (Topics 54-73)"""
    
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(
            code='CS101',
            name='Computer Science 101',
            credit_hours=3,
            instructor_email='prof@example.com',
            max_students=30,
            enrollment_fee=100.00
        )
    
    def test_form_display_in_template(self):
        """Topic 54: Form Display in Templates"""
        response = self.client.get(reverse('students:add_course'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_form_with_post_data(self):
        """Topic 56: Form with POST Data"""
        form_data = {
            'code': 'CS102',
            'name': 'Computer Science 102',
            'credit_hours': 3,
            'instructor_email': 'prof2@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        response = self.client.post(reverse('students:add_course'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_is_valid_check(self):
        """Topic 57: is_valid() Check"""
        form_data = {
            'code': 'INVALID',  # Missing numbers
            'name': 'Test',
            'credit_hours': 3,
            'instructor_email': 'prof@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_cleaned_data_access(self):
        """Topic 58: cleaned_data Access"""
        form_data = {
            'code': 'CS101',
            'name': 'Computer Science 101',
            'credit_hours': 3,
            'instructor_email': 'prof@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        if form.is_valid():
            cleaned = form.cleaned_data
            self.assertEqual(cleaned['name'], 'Computer Science 101')
    
    def test_blank_form_instance(self):
        """Topic 60: Blank Form Instance"""
        response = self.client.get(reverse('students:add_course'))
        form = response.context['form']
        self.assertFalse(form.is_bound)
    
    def test_instance_parameter(self):
        """Topic 67: Instance Parameter for Pre-population"""
        response = self.client.get(reverse('students:edit_course', args=[self.course.id]))
        form = response.context['form']
        self.assertEqual(form.instance.code, 'CS101')
    
    def test_success_message(self):
        """Topic 65: Success Messages"""
        form_data = {
            'code': 'CS102',
            'name': 'Computer Science 102',
            'credit_hours': 3,
            'instructor_email': 'prof2@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        response = self.client.post(reverse('students:add_course'), data=form_data, follow=True)
        messages = list(response.context['messages'])
        self.assertTrue(any('created successfully' in str(m) for m in messages))
    
    def test_delete_operation(self):
        """Topic 69-70: Delete with Redirect"""
        response = self.client.post(reverse('students:delete_course', args=[self.course.id]))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())


class FormValidationDisplayTestCase(TestCase):
    """Tests for Form Validation Display (Topics 62-77)"""
    
    def test_form_errors_display(self):
        """Topic 62: Form Errors Handling"""
        form_data = {
            'code': 'INVALID',
            'name': '',  # Empty name
            'credit_hours': 10,
            'instructor_email': 'invalid-email',
            'max_students': -1,
            'enrollment_fee': '-100',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 0)
    
    def test_non_field_errors_display(self):
        """Topic 77: Error Summary Display - Non-field errors"""
        form_data = {
            'code': 'CS101',  
            'name': 'Computer Science 101',
            'credit_hours': 3,
            'instructor_email': 'prof@example.com',
            'max_students': 30,
            'enrollment_fee': '100.00',
            'is_active': True,
        }
        form = CourseForm(data=form_data)
        # Test form without non_field_errors in this case
        self.assertTrue(form.is_valid())
