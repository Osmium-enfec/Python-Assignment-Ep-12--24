from django.db import models
from django.utils import timezone

class Project(models.Model):
    """
    Project model for analytics tracking
    Demonstrates: query optimization, indexing, performance
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return self.name

class Event(models.Model):
    """
    Event model with ForeignKey to Project
    Demonstrates: relationships, query optimization, aggregation
    """
    EVENT_TYPES = [
        ('view', 'Page View'),
        ('click', 'Click'),
        ('submit', 'Form Submit'),
        ('error', 'Error'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    user_id = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration_ms = models.IntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['project', '-timestamp']),
            models.Index(fields=['event_type', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.project.name} - {self.event_type}"

class Analytics(models.Model):
    """
    Aggregated analytics data
    Demonstrates: data aggregation, caching patterns, optimization
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='analytics')
    total_events = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    total_clicks = models.IntegerField(default=0)
    total_errors = models.IntegerField(default=0)
    average_duration = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Analytics"

    def __str__(self):
        return f"Analytics for {self.project.name}"
