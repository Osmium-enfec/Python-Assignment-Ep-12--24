from django.contrib import admin
from .models import Project, Event, Analytics

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['project', 'event_type', 'user_id', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['project__name', 'user_id']

@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ['project', 'total_events', 'total_views', 'average_duration']
    readonly_fields = ['total_events', 'total_views', 'total_clicks', 'total_errors']
