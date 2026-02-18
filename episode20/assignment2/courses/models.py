from django.db import models

class Course(models.Model):
    """Course model for modal and AJAX exercises"""
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)
    max_students = models.IntegerField(default=30)
    enrolled_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code}: {self.title}"
    
    def is_full(self):
        """Check if course is at capacity"""
        return self.enrolled_count >= self.max_students
    
    def available_seats(self):
        """Get available seats"""
        return self.max_students - self.enrolled_count


class Enrollment(models.Model):
    """Track course enrollments for delete confirmation"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    enrolled_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-enrolled_date']

    def __str__(self):
        return f"{self.student_name} - {self.course.code}"
