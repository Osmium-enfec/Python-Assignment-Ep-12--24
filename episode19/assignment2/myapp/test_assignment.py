from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from students.models import Department, Student, Course, Enrollment


class DepartmentModelTests(TestCase):
    """Test Department model"""
    
    def setUp(self):
        self.dept = Department.objects.create(
            name='Computer Science',
            code='CS',
            head='Dr. Smith',
            phone='1234567890'
        )
    
    def test_department_creation(self):
        self.assertEqual(self.dept.name, 'Computer Science')
        self.assertEqual(self.dept.code, 'CS')


class StudentModelTests(TestCase):
    """Test Student model with admin functionality"""
    
    def setUp(self):
        self.dept = Department.objects.create(
            name='Computer Science',
            code='CS',
            head='Dr. Smith',
            phone='1234567890'
        )
        self.student = Student.objects.create(
            name='John Doe',
            email='john@example.com',
            roll_no='001',
            date_of_birth=date(2000, 1, 1),
            phone='1234567890',
            department=self.dept,
            gpa=Decimal('3.5'),
            admission_date=date(2020, 9, 1)
        )
    
    def test_student_creation(self):
        self.assertEqual(self.student.name, 'John Doe')
        self.assertEqual(self.student.gpa, Decimal('3.5'))
    
    def test_student_string_representation(self):
        expected = f"{self.student.name} ({self.student.roll_no})"
        self.assertEqual(str(self.student), expected)


class AdminPanelTests(TestCase):
    """Test Django Admin Panel functionality"""
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.dept = Department.objects.create(
            name='Computer Science',
            code='CS',
            head='Dr. Smith',
            phone='1234567890'
        )
        self.student = Student.objects.create(
            name='Test Student',
            email='student@example.com',
            roll_no='001',
            date_of_birth=date(2000, 1, 1),
            phone='1234567890',
            department=self.dept,
            admission_date=date(2020, 9, 1)
        )
    
    def test_admin_login(self):
        """Test admin can login"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
    
    def test_department_admin_list(self):
        """Test department list in admin"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/students/department/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Computer Science')
    
    def test_student_admin_list(self):
        """Test student list in admin"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/students/student/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Student')
    
    def test_student_admin_add(self):
        """Test adding student through admin"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/students/student/add/')
        self.assertEqual(response.status_code, 200)
    
    def test_course_admin_list(self):
        """Test course list in admin"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/students/course/')
        self.assertEqual(response.status_code, 200)
    
    def test_enrollment_admin_list(self):
        """Test enrollment list in admin"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/students/enrollment/')
        self.assertEqual(response.status_code, 200)


class CourseModelTests(TestCase):
    """Test Course model"""
    
    def setUp(self):
        self.dept = Department.objects.create(
            name='Computer Science',
            code='CS',
            head='Dr. Smith',
            phone='1234567890'
        )
        self.course = Course.objects.create(
            code='CS101',
            name='Intro to Programming',
            department=self.dept,
            credits=3
        )
    
    def test_course_creation(self):
        self.assertEqual(self.course.code, 'CS101')
        self.assertTrue(self.course.is_active)


class EnrollmentModelTests(TestCase):
    """Test Enrollment model"""
    
    def setUp(self):
        self.dept = Department.objects.create(
            name='Computer Science',
            code='CS',
            head='Dr. Smith',
            phone='1234567890'
        )
        self.student = Student.objects.create(
            name='Test Student',
            email='test@example.com',
            roll_no='001',
            date_of_birth=date(2000, 1, 1),
            phone='1234567890',
            department=self.dept,
            admission_date=date(2020, 9, 1)
        )
        self.course = Course.objects.create(
            code='CS101',
            name='Intro to Programming',
            department=self.dept,
            credits=3
        )
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            semester='fall',
            year=2024,
            score=Decimal('85'),
            grade='B'
        )
    
    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.score, Decimal('85'))
        self.assertEqual(self.enrollment.grade, 'B')
    
    def test_enrollment_string_representation(self):
        expected = f"{self.student} - {self.course} (fall 2024)"
        self.assertEqual(str(self.enrollment), expected)
