from django import forms
from django.core.exceptions import ValidationError
from .models import Course

# Topic 41-48: Advanced Form Validation
class CourseForm(forms.ModelForm):
    """
    Topic 41: Advanced Form Validation
    Topic 42-46: Custom Validation Methods
    Topic 47-48: Database Validation
    """
    
    # Topic 43: Custom Clean Method for Fields
    code = forms.CharField(
        max_length=10,
        label="Course Code",
        help_text="Enter course code (e.g., CS101, MATH201)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CS101'
        })
    )
    
    # Topic 44: Field-level Validation
    credit_hours = forms.IntegerField(
        label="Credit Hours",
        help_text="Enter credit hours (1-4)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '4'
        })
    )
    
    name = forms.CharField(
        max_length=200,
        label="Course Name",
        help_text="Enter full course name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introduction to Computer Science'
        })
    )
    
    instructor_email = forms.EmailField(
        label="Instructor Email",
        help_text="Instructor's email address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'instructor@university.edu'
        })
    )
    
    description = forms.CharField(
        required=False,
        label="Description",
        help_text="Course description (optional)",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter course description'
        })
    )
    
    max_students = forms.IntegerField(
        label="Max Students",
        help_text="Maximum enrollment capacity",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        })
    )
    
    enrollment_fee = forms.DecimalField(
        label="Enrollment Fee",
        help_text="Course enrollment fee (USD)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0'
        })
    )
    
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label="Is Active",
        help_text="Is this course currently active?",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    # Topic 42: Form clean() Method - Custom Form-level Validation
    def clean(self):
        """Topic 42: Form-level validation across multiple fields"""
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        name = cleaned_data.get('name')
        credit_hours = cleaned_data.get('credit_hours')
        max_students = cleaned_data.get('max_students')
        
        # Topic 43: Custom validation logic
        if code and name:
            # Topic 45: Cross-field Validation
            if code.upper() == name[:len(code)].upper():
                raise ValidationError(
                    "Course code should not be the start of course name"
                )
        
        # Topic 44: Field-level Validation
        if credit_hours and credit_hours < 1:
            self.add_error('credit_hours', 'Credit hours must be at least 1')
        
        if credit_hours and credit_hours > 4:
            self.add_error('credit_hours', 'Credit hours cannot exceed 4')
        
        if max_students and max_students < 1:
            self.add_error('max_students', 'Maximum students must be at least 1')
        
        return cleaned_data
    
    # Topic 46: Field-level clean_<fieldname>() methods
    def clean_code(self):
        """Topic 46: Field-specific validation for code"""
        code = self.cleaned_data.get('code')
        if code:
            code = code.upper()
            # Validate format: letters followed by numbers
            if not any(c.isalpha() for c in code) or not any(c.isdigit() for c in code):
                raise ValidationError(
                    "Course code must contain both letters and numbers (e.g., CS101)"
                )
        return code
    
    def clean_name(self):
        """Field-specific validation for name"""
        name = self.cleaned_data.get('name')
        if name and len(name) < 3:
            raise ValidationError("Course name must be at least 3 characters")
        return name
    
    def clean_enrollment_fee(self):
        """Field-specific validation for enrollment fee"""
        fee = self.cleaned_data.get('enrollment_fee')
        if fee and fee < 0:
            raise ValidationError("Enrollment fee cannot be negative")
        if fee and fee > 10000:
            raise ValidationError("Enrollment fee seems too high")
        return fee
    
    class Meta:
        model = Course
        # Topic 49-50: Form Field Configuration
        fields = ['code', 'name', 'credit_hours', 'instructor_email', 'description', 'max_students', 'enrollment_fee', 'is_active']
        
        # Topic 52-53: Widget Configuration in Meta
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
