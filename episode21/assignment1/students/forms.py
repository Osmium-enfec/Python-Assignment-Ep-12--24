from django import forms
from django.core.exceptions import ValidationError
from .models import Student

# Topic 1-3: Django Forms Module, ModelForm Class, Form Meta Class
class StudentForm(forms.ModelForm):
    """
    Topic 2: ModelForm Class - Creates a form from a Django model
    Topic 3: Form Meta Class - Specifies model and fields configuration
    Topic 4: Model to Form Conversion - Auto-generates form from model
    """
    
    # Topic 21: Field Labels - Custom label for roll_no
    roll_no = forms.CharField(
        max_length=20,
        label="Student Roll Number",  # Topic 21: Field Labels
        # Topic 22: Form Help Text
        help_text="Enter unique roll number (e.g., S001, S002)",
        # Topic 13: Widget Attributes and Classes
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter roll number'
        })
    )
    
    # Topic 15: CharField in Forms - Standard text field
    name = forms.CharField(
        max_length=100,
        label="Full Name",
        help_text="Enter student's full name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter full name'
        })
    )
    
    # Topic 16: EmailField in Forms - Validates email format
    email = forms.EmailField(
        label="Email Address",
        help_text="Enter valid email address",
        # Topic 8: EmailInput Widget - Specialized email input
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'student@example.com'
        })
    )
    
    # Topic 15: CharField for phone (optional)
    phone = forms.CharField(
        max_length=15,
        required=False,
        label="Phone Number",
        help_text="Enter phone number (optional)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+1-234-567-8900'
        })
    )
    
    # Topic 12: Textarea Widget - Multi-line text input
    address = forms.CharField(
        required=False,
        label="Address",
        help_text="Enter student's address (optional)",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter address'
        })
    )
    
    # Topic 20: IntegerField in Forms (using FloatField for GPA)
    gpa = forms.FloatField(
        initial=0.0,
        label="GPA",
        help_text="Enter GPA (0.0 - 4.0)",
        # Topic 7: TextInput Widget
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'min': '0',
            'max': '4',
            'step': '0.01',
            'placeholder': '3.5'
        })
    )
    
    # Topic 18: BooleanField in Forms - Checkbox
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label="Is Active Student",
        help_text="Check if student is currently enrolled",
        # Topic 10: CheckboxInput Widget
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    class Meta:
        # Topic 2: ModelForm - Specifies the model
        model = Student
        # Topic 5: Automatic Field Generation
        # Note: enrolled_date is excluded because it has auto_now_add=True (non-editable)
        fields = ['roll_no', 'name', 'email', 'phone', 'address', 'gpa', 'is_active']
        
        # Topic 13: Widget Attributes - Additional widget configuration
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
