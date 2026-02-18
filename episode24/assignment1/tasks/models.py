from django.db import models

class Task(models.Model):
    """
    Task model with fields:
    - title: CharField
    - description: TextField
    - priority: IntegerField (1-5)
    - completed: BooleanField
    - created_at: DateTimeField auto_now_add
    - updated_at: DateTimeField auto_now
    """
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Urgent'),
        (5, 'Critical'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"{self.title} (Priority: {self.get_priority_display()})"
