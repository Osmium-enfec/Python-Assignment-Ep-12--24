from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from students.models import Student, Course, Grade


class StudentModelTests(TestCase):
    """Test Student model functionality"""
    
    def setUp(self):
        self.student = Student.objects.create(
            name='John Doe',
            email='john@example.com',
            roll_no='001',
            date_of_birth='2000-01-01',
            phone='1234567890',
            gpa=Decimal('3.7')
        )
    
    def test_student_creation(self):
        """Test student model creation"""
        self.assertEqual(self.student.name, 'John Doe')
        self.assertEqual(self.student.email, 'john@example.com')
        self.assertEqual(self.student.gpa, Decimal('3.7'))
    
    def test_gpa_grade_a(self):
        """Test GPA grade calculation for A"""
        self.assertEqual(self.student.gpa_grade, 'A')
    
    def test_gpa_grade_b(self):
        """Test GPA grade calculation for B"""
        student = Student.objects.create(
            name='Jane Doe',
            email='jane@example.com',
            roll_no='002',
            date_of_birth='2000-02-01',
            phone='0987654321',
            gpa=Decimal('2.5')
        )
        self.assertEqual(student.gpa_grade, 'B')
    
    def test_dean_list_qualification(self):
        """Test Dean's List qualification (GPA >= 3.5)"""
        self.assertTrue(self.student.is_dean_list)
    
    def test_not_dean_list(self):
        """Test non-qualification for Dean's List"""
        student = Student.objects.create(
            name='Bob Smith',
            email='bob@example.com',
            roll_no='003',
            date_of_birth='2000-03-01',
            phone='5555555555',
            gpa=Decimal('3.0')
        )
        self.assertFalse(student.is_dean_list)
    
    def test_at_risk_qualification(self):
        """Test at-risk status (GPA < 2.0)"""
        student = Student.objects.create(
            name='Charlie Brown',
            email='charlie@example.com',
            roll_no='004',
            date_of_birth='2000-04-01',
            phone='3333333333',
            gpa=Decimal('1.5')
        )
        self.assertTrue(student.is_at_risk)
    
    def test_student_string_representation(self):
        """Test student string representation"""
        expected = f"{self.student.name} ({self.student.roll_no})"
        self.assertEqual(str(self.student), expected)


class CourseModelTests(TestCase):
    """Test Course model functionality"""
    
    def setUp(self):
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Computer Science',
            credits=3
        )
    
    def test_course_creation(self):
        """Test course creation"""
        self.assertEqual(self.course.code, 'CS101')
        self.assertEqual(self.course.name, 'Introduction to Computer Science')
        self.assertEqual(self.course.credits, 3)
    
    def test_course_string_representation(self):
        """Test course string representation"""
        expected = f"{self.course.code}: {self.course.name}"
        self.assertEqual(str(self.course), expected)


class GradeModelTests(TestCase):
    """Test Grade model functionality"""
    
    def setUp(self):
        self.student = Student.objects.create(
            name='Test Student',
            email='test@example.com',
            roll_no='001',
            date_of_birth='2000-01-01',
            phone='1234567890',
            gpa=Decimal('3.0')
        )
        self.course = Course.objects.create(
            code='CS101',
            name='Intro to CS',
            credits=3
        )
        self.grade = Grade.objects.create(
            student=self.student,
            course=self.course,
            score=Decimal('85'),
            semester='fall',
            year=2024
        )
    
    def test_grade_creation(self):
        """Test grade creation"""
        self.assertEqual(self.grade.score, Decimal('85'))
        self.assertEqual(self.grade.letter_grade, 'B')
    
    def test_letter_grade_a(self):
        """Test letter grade A"""
        grade = Grade.objects.create(
            student=self.student,
            course=self.course,
            score=Decimal('92'),
            semester='spring',
            year=2024
        )
        self.assertEqual(grade.letter_grade, 'A')
    
    def test_letter_grade_f(self):
        """Test letter grade F"""
        grade = Grade.objects.create(
            student=self.student,
            course=self.course,
            score=Decimal('55'),
            semester='summer',
            year=2024
        )
        self.assertEqual(grade.letter_grade, 'F')
    
    def test_is_passing(self):
        """Test passing grade check"""
        self.assertTrue(self.grade.is_passing)
    
    def test_is_failing(self):
        """Test failing grade check"""
        grade = Grade.objects.create(
            student=self.student,
            course=self.course,
            score=Decimal('45'),
            semester='spring',
            year=2024
        )
        self.assertFalse(grade.is_passing)


class URLTests(TestCase):
    """Test URL routing"""
    
    def test_home_url(self):
        """Test home URL"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_list_url(self):
        """Test student list URL"""
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_grade_report_url(self):
        """Test grade report URL"""
        response = self.client.get(reverse('grade_report'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_detail_url(self):
        """Test student detail URL"""
        student = Student.objects.create(
            name='Test',
            email='test@example.com',
            roll_no='001',
            date_of_birth='2000-01-01',
            phone='1234567890'
        )
        response = self.client.get(reverse('student_detail', args=[student.pk]))
        self.assertEqual(response.status_code, 200)


class TemplateTests(TestCase):
    """Test template rendering and conditionals"""
    
    def setUp(self):
        self.student = Student.objects.create(
            name='Alice Smith',
            email='alice@example.com',
            roll_no='001',
            date_of_birth='2000-01-01',
            phone='1234567890',
            gpa=Decimal('3.8'),
            status='active'
        )
    
    def test_home_template(self):
        """Test home page rendering"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'students/home.html')
        self.assertIn('total_students', response.context)
    
    def test_student_list_template(self):
        """Test student list template"""
        response = self.client.get(reverse('student_list'))
        self.assertTemplateUsed(response, 'students/student_list.html')
        self.assertIn('students', response.context)
    
    def test_student_detail_template(self):
        """Test student detail template"""
        response = self.client.get(reverse('student_detail', args=[self.student.pk]))
        self.assertTemplateUsed(response, 'students/student_detail.html')
        self.assertEqual(response.context['student'], self.student)
    
    def test_dean_list_conditional_rendering(self):
        """Test Dean's List conditional in template"""
        response = self.client.get(reverse('student_list'))
        self.assertContains(response, "Dean's List", count=1)
    
    def test_student_detail_dean_list_alert(self):
        """Test Dean's List alert on detail page"""
        response = self.client.get(reverse('student_detail', args=[self.student.pk]))
        self.assertContains(response, "Excellent!")


class AdminTests(TestCase):
    """Test Django Admin functionality"""
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.student = Student.objects.create(
            name='Test Student',
            email='student@example.com',
            roll_no='001',
            date_of_birth='2000-01-01',
            phone='1234567890'
        )
    
    def test_admin_login(self):
        """Test admin login"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
    
    def test_student_admin_list(self):
        """Test student list in admin"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/students/student/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Student')
