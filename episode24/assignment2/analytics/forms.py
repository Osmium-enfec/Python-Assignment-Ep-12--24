from django import forms
from .models import Project, Event

class ProjectForm(forms.ModelForm):
    """
    ProjectForm with Bootstrap styling
    Topic 60: Professional form design patterns
    """
    class Meta:
        model = Project
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Project description'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EventForm(forms.ModelForm):
    """
    EventForm for logging events
    Topic 61: Event data validation
    """
    class Meta:
        model = Event
        fields = ['project', 'event_type', 'user_id', 'url', 'duration_ms']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'user_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User ID'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL'}),
            'duration_ms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration (ms)'}),
        }

    def clean_duration_ms(self):
        """Topic 62: Custom field validation"""
        duration = self.cleaned_data.get('duration_ms')
        if duration < 0:
            raise forms.ValidationError('Duration cannot be negative')
        return duration
