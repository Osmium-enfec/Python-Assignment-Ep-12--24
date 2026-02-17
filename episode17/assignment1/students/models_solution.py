from django.db import models

class Student(models.Model):
    """Student model representing database table"""
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField(unique=True)
    email = models.CharField(max_length=100)
    fees_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.roll_no})"
    
    class Meta:
        ordering = ['roll_no']
        verbose_name = "Student"
        verbose_name_plural = "Students"
