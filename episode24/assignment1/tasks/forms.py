from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    """
    TaskForm with:
    - TextInput for title with form-control class
    - Textarea for description with form-control class
    - Select widget for priority with form-select class
    - CheckboxInput for completed with form-check-input class
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter task description'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
