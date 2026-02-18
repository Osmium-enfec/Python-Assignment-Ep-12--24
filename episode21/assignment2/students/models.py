from django.db import models

class Course(models.Model):
    """Course model for advanced validation exercises"""
    # Topic 43-48: Database Validation Fields
    code = models.CharField(max_length=10, unique=True)  # Topic 47: Unique Field
    name = models.CharField(max_length=200)
    credit_hours = models.IntegerField(default=3)
    instructor_email = models.EmailField(unique=True)  # Topic 47: Unique Email
    description = models.TextField(blank=True)
    max_students = models.IntegerField(default=30)
    enrollment_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"
