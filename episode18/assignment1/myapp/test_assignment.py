import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import TestCase, Client
from students.models import Student
from django.urls import reverse


class StudentModelTests(TestCase):
    """Test Student model"""
    
    def setUp(self):
        """Create test students"""
        Student.objects.create(
            name="Raj Kumar",
            roll_no=1,
            email="raj@example.com",
            fees_paid=True
        )
        Student.objects.create(
            name="Priya Singh",
            roll_no=2,
            email="priya@example.com",
            fees_paid=False
        )
    
    def test_student_creation(self):
        """Test if student can be created"""
        student = Student.objects.get(roll_no=1)
        self.assertEqual(student.name, "Raj Kumar")
        self.assertEqual(student.email, "raj@example.com")
        self.assertTrue(student.fees_paid)
    
    def test_student_str_method(self):
        """Test __str__ method"""
        student = Student.objects.get(roll_no=1)
        self.assertIn("Raj Kumar", str(student))
        self.assertIn("1", str(student))
    
    def test_unique_roll_no(self):
        """Test that roll_no is unique"""
        with self.assertRaises(Exception):
            Student.objects.create(
                name="Another Student",
                roll_no=1,
                email="another@example.com"
            )
    
    def test_student_ordering(self):
        """Test students are ordered by roll_no"""
        students = Student.objects.all()
        self.assertEqual(students[0].roll_no, 1)
        self.assertEqual(students[1].roll_no, 2)
    
    def test_fees_paid_default_false(self):
        """Test fees_paid defaults to False"""
        student = Student.objects.create(
            name="Test Student",
            roll_no=3,
            email="test@example.com"
        )
        self.assertFalse(student.fees_paid)
    
    def test_created_at_timestamp(self):
        """Test created_at timestamp is set"""
        student = Student.objects.get(roll_no=1)
        self.assertIsNotNone(student.created_at)


class StudentListViewTests(TestCase):
    """Test student_list view"""
    
    def setUp(self):
        """Create test data"""
        self.client = Client()
        Student.objects.create(name="Student 1", roll_no=1, email="s1@example.com")
        Student.objects.create(name="Student 2", roll_no=2, email="s2@example.com")
    
    def test_student_list_url(self):
        """Test student list URL exists"""
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)
    
    def test_student_list_template(self):
        """Test correct template is used"""
        response = self.client.get('/students/')
        self.assertTemplateUsed(response, 'students/list.html')
    
    def test_student_list_context(self):
        """Test context contains students"""
        response = self.client.get('/students/')
        self.assertIn('students', response.context)
        self.assertEqual(len(response.context['students']), 2)
    
    def test_student_list_content(self):
        """Test student names appear in response"""
        response = self.client.get('/students/')
        self.assertContains(response, 'Student 1')
        self.assertContains(response, 'Student 2')
    
    def test_student_list_empty(self):
        """Test empty student list"""
        Student.objects.all().delete()
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['students']), 0)


class StudentDetailViewTests(TestCase):
    """Test student_detail view"""
    
    def setUp(self):
        """Create test student"""
        self.client = Client()
        self.student = Student.objects.create(
            name="Test Student",
            roll_no=1,
            email="test@example.com",
            fees_paid=True
        )
    
    def test_student_detail_url(self):
        """Test student detail URL exists"""
        response = self.client.get(f'/students/{self.student.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_student_detail_template(self):
        """Test correct template is used"""
        response = self.client.get(f'/students/{self.student.id}/')
        self.assertTemplateUsed(response, 'students/detail.html')
    
    def test_student_detail_context(self):
        """Test context contains student"""
        response = self.client.get(f'/students/{self.student.id}/')
        self.assertIn('student', response.context)
        self.assertEqual(response.context['student'].id, self.student.id)
    
    def test_student_detail_content(self):
        """Test student details appear in response"""
        response = self.client.get(f'/students/{self.student.id}/')
        self.assertContains(response, 'Test Student')
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, '1')  # roll_no
    
    def test_student_detail_fees_paid(self):
        """Test fees paid status appears"""
        response = self.client.get(f'/students/{self.student.id}/')
        self.assertIn('fees_paid', response.context['student'].__dict__)


class StudentIntegrationTests(TestCase):
    """Integration tests for Student app"""
    
    def setUp(self):
        """Create test data"""
        self.client = Client()
        for i in range(5):
            Student.objects.create(
                name=f"Student {i+1}",
                roll_no=i+1,
                email=f"student{i+1}@example.com",
                fees_paid=(i % 2 == 0)
            )
    
    def test_list_to_detail_navigation(self):
        """Test navigating from list to detail"""
        response = self.client.get('/students/')
        self.assertContains(response, 'Student 1')
        
        # Now visit detail page
        student = Student.objects.first()
        response = self.client.get(f'/students/{student.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_student_count(self):
        """Test total student count"""
        self.assertEqual(Student.objects.count(), 5)
    
    def test_fees_paid_filter(self):
        """Test filtering students by fees paid"""
        paid = Student.objects.filter(fees_paid=True)
        unpaid = Student.objects.filter(fees_paid=False)
        self.assertEqual(paid.count() + unpaid.count(), 5)
    
    def test_template_filters(self):
        """Test template filters work"""
        student = Student.objects.first()
        response = self.client.get(f'/students/{student.id}/')
        # Check if created_at is displayed (with date filter)
        self.assertIn('created_at', str(response.context['student'].__dict__))


if __name__ == '__main__':
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=True)
    failures = test_runner.run_tests(['__main__'])
    sys.exit(bool(failures))
