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
from courses.models import Student, Course, Enrollment
from django.urls import reverse


class StudentModelTests(TestCase):
    """Test Student model"""
    
    def setUp(self):
        """Create test students"""
        Student.objects.create(name="Raj Kumar", roll_no=1, email="raj@example.com")
        Student.objects.create(name="Priya Singh", roll_no=2, email="priya@example.com")
    
    def test_student_creation(self):
        """Test if student can be created"""
        self.assertEqual(Student.objects.count(), 2)
    
    def test_student_str(self):
        """Test student string representation"""
        student = Student.objects.first()
        self.assertIn("Raj Kumar", str(student))
    
    def test_unique_roll_no(self):
        """Test roll_no is unique"""
        with self.assertRaises(Exception):
            Student.objects.create(name="Duplicate", roll_no=1, email="dup@example.com")


class CourseModelTests(TestCase):
    """Test Course model"""
    
    def setUp(self):
        """Create test courses"""
        Course.objects.create(title="Python Basics", code="PY101", credits=3)
        Course.objects.create(title="Web Development", code="WEB201", credits=4)
    
    def test_course_creation(self):
        """Test course can be created"""
        self.assertEqual(Course.objects.count(), 2)
    
    def test_course_unique_code(self):
        """Test course code is unique"""
        with self.assertRaises(Exception):
            Course.objects.create(title="Duplicate", code="PY101", credits=3)
    
    def test_course_str(self):
        """Test course string representation"""
        course = Course.objects.first()
        self.assertIn("PY101", str(course))


class EnrollmentModelTests(TestCase):
    """Test Enrollment model"""
    
    def setUp(self):
        """Create test data"""
        self.student = Student.objects.create(name="Test", roll_no=1, email="test@example.com")
        self.course = Course.objects.create(title="Test Course", code="TEST101", credits=3)
    
    def test_enrollment_creation(self):
        """Test enrollment can be created"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            grade='A'
        )
        self.assertEqual(str(enrollment), "Test - TEST101")
    
    def test_enrollment_unique_together(self):
        """Test unique constraint on student-course pair"""
        Enrollment.objects.create(student=self.student, course=self.course)
        with self.assertRaises(Exception):
            Enrollment.objects.create(student=self.student, course=self.course)
    
    def test_many_to_many_through_enrollment(self):
        """Test many-to-many relationship through Enrollment"""
        Enrollment.objects.create(student=self.student, course=self.course)
        self.assertIn(self.student, self.course.students.all())


class StudentListViewTests(TestCase):
    """Test student_list view"""
    
    def setUp(self):
        """Create test data"""
        self.client = Client()
        Student.objects.create(name="S1", roll_no=1, email="s1@example.com")
        Student.objects.create(name="S2", roll_no=2, email="s2@example.com")
    
    def test_student_list_url(self):
        """Test student list URL exists"""
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)
    
    def test_student_list_template(self):
        """Test correct template is used"""
        response = self.client.get('/students/')
        self.assertTemplateUsed(response, 'courses/student_list.html')
    
    def test_student_list_context(self):
        """Test context contains students"""
        response = self.client.get('/students/')
        self.assertIn('students', response.context)
        self.assertEqual(len(response.context['students']), 2)
    
    def test_student_list_content(self):
        """Test student names in response"""
        response = self.client.get('/students/')
        self.assertContains(response, 'S1')
        self.assertContains(response, 'S2')


class CourseListViewTests(TestCase):
    """Test course_list view"""
    
    def setUp(self):
        """Create test courses"""
        self.client = Client()
        Course.objects.create(title="Python", code="PY101", credits=3)
        Course.objects.create(title="Web", code="WEB201", credits=4)
    
    def test_course_list_url(self):
        """Test course list URL exists"""
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
    
    def test_course_list_template(self):
        """Test correct template is used"""
        response = self.client.get('/courses/')
        self.assertTemplateUsed(response, 'courses/course_list.html')
    
    def test_course_list_context(self):
        """Test context contains courses"""
        response = self.client.get('/courses/')
        self.assertIn('courses', response.context)
        self.assertEqual(len(response.context['courses']), 2)


class StudentDetailViewTests(TestCase):
    """Test student_detail view"""
    
    def setUp(self):
        """Create test data"""
        self.client = Client()
        self.student = Student.objects.create(name="Test", roll_no=1, email="test@example.com")
        self.course = Course.objects.create(title="Course", code="C101", credits=3)
        Enrollment.objects.create(student=self.student, course=self.course, grade='A')
    
    def test_student_detail_url(self):
        """Test student detail URL exists"""
        response = self.client.get(f'/students/{self.student.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_student_detail_template(self):
        """Test correct template is used"""
        response = self.client.get(f'/students/{self.student.id}/')
        self.assertTemplateUsed(response, 'courses/student_detail.html')
    
    def test_student_detail_context(self):
        """Test context contains student and enrollments"""
        response = self.client.get(f'/students/{self.student.id}/')
        self.assertEqual(response.context['student'].id, self.student.id)
        self.assertIn('enrollments', response.context)


class CourseDetailViewTests(TestCase):
    """Test course_detail view"""
    
    def setUp(self):
        """Create test data"""
        self.client = Client()
        self.course = Course.objects.create(title="Course", code="C101", credits=3)
        self.student1 = Student.objects.create(name="S1", roll_no=1, email="s1@example.com")
        self.student2 = Student.objects.create(name="S2", roll_no=2, email="s2@example.com")
        Enrollment.objects.create(student=self.student1, course=self.course, grade='A')
        Enrollment.objects.create(student=self.student2, course=self.course, grade='B')
    
    def test_course_detail_url(self):
        """Test course detail URL exists"""
        response = self.client.get(f'/courses/{self.course.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_course_detail_template(self):
        """Test correct template is used"""
        response = self.client.get(f'/courses/{self.course.id}/')
        self.assertTemplateUsed(response, 'courses/course_detail.html')
    
    def test_course_detail_enrollments(self):
        """Test enrolled students shown"""
        response = self.client.get(f'/courses/{self.course.id}/')
        self.assertEqual(len(response.context['enrollments']), 2)


class EnrollmentListViewTests(TestCase):
    """Test enrollment_list view"""
    
    def setUp(self):
        """Create test enrollments"""
        self.client = Client()
        s1 = Student.objects.create(name="S1", roll_no=1, email="s1@example.com")
        c1 = Course.objects.create(title="C1", code="C101", credits=3)
        Enrollment.objects.create(student=s1, course=c1, grade='A')
    
    def test_enrollment_list_url(self):
        """Test enrollment list URL exists"""
        response = self.client.get('/enrollments/')
        self.assertEqual(response.status_code, 200)
    
    def test_enrollment_list_template(self):
        """Test correct template is used"""
        response = self.client.get('/enrollments/')
        self.assertTemplateUsed(response, 'courses/enrollment_list.html')
    
    def test_enrollment_list_context(self):
        """Test context contains enrollments"""
        response = self.client.get('/enrollments/')
        self.assertEqual(len(response.context['enrollments']), 1)


class IntegrationTests(TestCase):
    """Integration tests for course management"""
    
    def setUp(self):
        """Create comprehensive test data"""
        self.client = Client()
        
        # Create students
        self.students = []
        for i in range(3):
            s = Student.objects.create(
                name=f"Student {i+1}",
                roll_no=i+1,
                email=f"s{i+1}@example.com"
            )
            self.students.append(s)
        
        # Create courses
        self.courses = []
        for i in range(2):
            c = Course.objects.create(
                title=f"Course {i+1}",
                code=f"C{i+1}01",
                credits=3+i
            )
            self.courses.append(c)
        
        # Create enrollments
        Enrollment.objects.create(student=self.students[0], course=self.courses[0], grade='A')
        Enrollment.objects.create(student=self.students[0], course=self.courses[1], grade='B')
        Enrollment.objects.create(student=self.students[1], course=self.courses[0], grade='C')
    
    def test_student_course_count(self):
        """Test counting student enrollments"""
        student = self.students[0]
        enrollments = Enrollment.objects.filter(student=student)
        self.assertEqual(enrollments.count(), 2)
    
    def test_course_student_count(self):
        """Test counting course enrollments"""
        course = self.courses[0]
        enrollments = Enrollment.objects.filter(course=course)
        self.assertEqual(enrollments.count(), 2)
    
    def test_navigation_student_to_courses(self):
        """Test viewing student's courses"""
        student = self.students[0]
        response = self.client.get(f'/students/{student.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['enrollments']), 2)
    
    def test_navigation_course_to_students(self):
        """Test viewing course's students"""
        course = self.courses[0]
        response = self.client.get(f'/courses/{course.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['enrollments']), 2)
    
    def test_queryset_filtering(self):
        """Test queryset operations"""
        # Filter students by enrollment
        students_in_course = self.courses[0].students.all()
        self.assertEqual(students_in_course.count(), 2)
    
    def test_queryset_ordering(self):
        """Test queryset ordering"""
        students = Student.objects.all()
        self.assertEqual(students[0].roll_no, 1)


if __name__ == '__main__':
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=True)
    failures = test_runner.run_tests(['__main__'])
    sys.exit(bool(failures))
