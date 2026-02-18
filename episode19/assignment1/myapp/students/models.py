from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    """Student model for Episode 19 - Tables and Conditionals"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_no = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    status = models.CharField(
        max_length=10,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('graduated', 'Graduated'),
        ],
        default='active'
    )
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f"{self.name} ({self.roll_no})"
    
    @property
    def gpa_grade(self):
        """Determine letter grade based on GPA"""
        if self.gpa >= 3.5:
            return 'A'
        elif self.gpa >= 3.0:
            return 'A-'
        elif self.gpa >= 2.7:
            return 'B+'
        elif self.gpa >= 2.3:
            return 'B'
        elif self.gpa >= 2.0:
            return 'B-'
        elif self.gpa >= 1.7:
            return 'C+'
        elif self.gpa >= 1.3:
            return 'C'
        else:
            return 'F'
    
    @property
    def is_dean_list(self):
        """Check if student qualifies for Dean's List (GPA >= 3.5)"""
        return self.gpa >= 3.5
    
    @property
    def is_at_risk(self):
        """Check if student is at academic risk (GPA < 2.0)"""
        return self.gpa < 2.0


class Course(models.Model):
    """Course model for grading"""
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code}: {self.name}"


class Grade(models.Model):
    """Grade model linking students to courses"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    semester = models.CharField(
        max_length=10,
        choices=[
            ('fall', 'Fall'),
            ('spring', 'Spring'),
            ('summer', 'Summer'),
        ]
    )
    year = models.IntegerField()
    
    class Meta:
        ordering = ['-year', '-semester']
        unique_together = ['student', 'course', 'semester', 'year']
    
    def __str__(self):
        return f"{self.student} - {self.course} ({self.semester} {self.year})"
    
    @property
    def letter_grade(self):
        """Convert numeric score to letter grade"""
        if self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'
    
    @property
    def is_passing(self):
        """Check if score is passing (>= 60)"""
        return self.score >= 60
