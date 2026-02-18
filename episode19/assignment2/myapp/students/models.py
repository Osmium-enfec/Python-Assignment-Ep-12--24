from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Department(models.Model):
    """Department model"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    head = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return f"{self.code}: {self.name}"


class Student(models.Model):
    """Student model for Assignment 2 - Admin Panel"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_no = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    admission_date = models.DateField()
    is_scholarship_holder = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-admission_date']
        verbose_name_plural = 'Students'
        permissions = [
            ('can_export_students', 'Can export student list'),
            ('can_view_gpa', 'Can view GPA information'),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.roll_no})"


class Course(models.Model):
    """Course model for Assignment 2"""
    LEVEL_CHOICES = [
        (100, 'Introductory'),
        (200, 'Intermediate'),
        (300, 'Advanced'),
        (400, 'Graduate'),
    ]
    
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.IntegerField(choices=LEVEL_CHOICES, default=100)
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return f"{self.code}: {self.name}"


class Enrollment(models.Model):
    """Enrollment linking students to courses"""
    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
        ('I', 'Incomplete'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(
        max_length=10,
        choices=[('fall', 'Fall'), ('spring', 'Spring'), ('summer', 'Summer')]
    )
    year = models.IntegerField()
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, null=True, blank=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-year', '-semester']
        unique_together = ['student', 'course', 'semester', 'year']
        verbose_name_plural = 'Enrollments'
    
    def __str__(self):
        return f"{self.student} - {self.course} ({self.semester} {self.year})"
