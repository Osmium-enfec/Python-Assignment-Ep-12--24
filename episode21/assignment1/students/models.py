from django.db import models

class Student(models.Model):
    """Student model for form exercises"""
    # Topic 4: Model to Form Conversion - These fields will automatically generate form fields
    roll_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    gpa = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    enrolled_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['roll_no']

    def __str__(self):
        return f"{self.name} ({self.roll_no})"
