from django.db import models

class Student(models.Model):
    """Student model for course management"""
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField(unique=True)
    email = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.roll_no})"
    
    class Meta:
        ordering = ['roll_no']
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Course(models.Model):
    """Course model with many-to-many relationship to students"""
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credits = models.IntegerField()
    students = models.ManyToManyField(Student, through='Enrollment')
    
    def __str__(self):
        return f"{self.code}: {self.title}"
    
    class Meta:
        ordering = ['code']
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Enrollment(models.Model):
    """Enrollment model linking students to courses"""
    GRADES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GRADES, default='')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.course.code}"
    
    class Meta:
        ordering = ['-enrollment_date']
        unique_together = ('student', 'course')
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
