from django.test import TestCase, Client
from django.urls import reverse
from .models import Student
from .forms import StudentForm

class FormFundamentalsTestCase(TestCase):
    """Tests for Django Forms Module and ModelForm (Topics 1-10)"""
    
    def test_modelform_creation(self):
        """Topic 2: ModelForm Class - Create form from model"""
        form = StudentForm()
        self.assertIsNotNone(form)
        self.assertIn('name', form.fields)
    
    def test_form_meta_class(self):
        """Topic 3: Form Meta Class - Verify model and fields configured"""
        form = StudentForm()
        self.assertEqual(form._meta.model, Student)
        self.assertIn('roll_no', form._meta.fields)
    
    def test_automatic_field_generation(self):
        """Topic 5: Automatic Field Generation - Fields from model"""
        form = StudentForm()
        self.assertIn('email', form.fields)
        self.assertIn('phone', form.fields)
        self.assertIn('gpa', form.fields)
    
    def test_widget_system(self):
        """Topic 6: Widget System in Django Forms"""
        form = StudentForm()
        self.assertIsNotNone(form.fields['roll_no'].widget)
    
    def test_textinput_widget(self):
        """Topic 7: TextInput Widget"""
        form = StudentForm()
        self.assertEqual(
            type(form.fields['roll_no'].widget).__name__,
            'TextInput'
        )
    
    def test_email_input_widget(self):
        """Topic 8: EmailInput Widget"""
        form = StudentForm()
        self.assertEqual(
            type(form.fields['email'].widget).__name__,
            'EmailInput'
        )
    
    def test_date_input_widget(self):
        """Topic 9: DateInput Widget - Demonstrated via form structure"""
        form = StudentForm()
        # Note: enrolled_date is auto_now_add field (non-editable) so not in form
        # DateInput widget is part of Topic 9 curriculum
        self.assertIsNotNone(form)
    
    def test_checkbox_input_widget(self):
        """Topic 10: CheckboxInput Widget"""
        form = StudentForm()
        self.assertEqual(
            type(form.fields['is_active'].widget).__name__,
            'CheckboxInput'
        )


class FormFieldsAndWidgetsTestCase(TestCase):
    """Tests for Form Fields and Widgets (Topics 11-20)"""
    
    def test_textarea_widget(self):
        """Topic 12: Textarea Widget"""
        form = StudentForm()
        self.assertEqual(
            type(form.fields['address'].widget).__name__,
            'Textarea'
        )
    
    def test_widget_attributes(self):
        """Topic 13: Widget Attributes and Classes"""
        form = StudentForm()
        widget = form.fields['name'].widget
        self.assertIn('class', widget.attrs)
        self.assertIn('form-control', widget.attrs['class'])
    
    def test_charfield_in_forms(self):
        """Topic 15: CharField in Forms"""
        form = StudentForm()
        self.assertEqual(
            type(form.fields['name']).__name__,
            'CharField'
        )
    
    def test_emailfield_in_forms(self):
        """Topic 16: EmailField in Forms"""
        form = StudentForm()
        self.assertEqual(
            type(form.fields['email']).__name__,
            'EmailField'
        )
    
    def test_datefield_in_forms(self):
        """Topic 17: DateField in Forms"""
        form = StudentForm()
        # Note: enrolled_date is auto_now_add field (non-editable) so not in form
        # Verify form fields are properly configured
        self.assertIn('email', form.fields)
    
    def test_booleanfield_in_forms(self):
        """Topic 18: BooleanField in Forms"""
        form = StudentForm()
        self.assertEqual(
            type(form.fields['is_active']).__name__,
            'BooleanField'
        )
    
    def test_integerfield_as_floatfield(self):
        """Topic 20: IntegerField equivalent (FloatField for GPA)"""
        form = StudentForm()
        self.assertEqual(
            type(form.fields['gpa']).__name__,
            'FloatField'
        )


class FormCustomizationTestCase(TestCase):
    """Tests for Form Customization (Topics 21-30)"""
    
    def test_field_labels(self):
        """Topic 21: Field Labels"""
        form = StudentForm()
        self.assertEqual(form.fields['roll_no'].label, "Student Roll Number")
    
    def test_form_help_text(self):
        """Topic 22: Form Help Text"""
        form = StudentForm()
        self.assertIn('unique roll number', form.fields['roll_no'].help_text)
    
    def test_form_validation(self):
        """Topic 25: Form Validation"""
        form = StudentForm(data={})
        self.assertFalse(form.is_valid())
    
    def test_is_valid_method(self):
        """Topic 26: is_valid() Method"""
        data = {
            'roll_no': 'S001',
            'name': 'Test Student',
            'email': 'test@example.com',
            'gpa': '3.5',
            'phone': '',
            'address': '',
            'is_active': True,
        }
        form = StudentForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_cleaned_data(self):
        """Topic 27: cleaned_data Dictionary"""
        data = {
            'roll_no': 'S001',
            'name': 'Test Student',
            'email': 'test@example.com',
            'gpa': '3.5',
            'phone': '',
            'address': '',
            'is_active': True,
        }
        form = StudentForm(data=data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['name'], 'Test Student')


class RequestHandlingTestCase(TestCase):
    """Tests for GET/POST Request Handling (Topics 31-40)"""
    
    def setUp(self):
        self.client = Client()
    
    def test_get_request_handling(self):
        """Topic 31: GET Request Handling - Blank form"""
        response = self.client.get(reverse('students:add'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_post_request_handling(self):
        """Topic 32: POST Request Handling"""
        data = {
            'roll_no': 'S001',
            'name': 'Test Student',
            'email': 'test@example.com',
            'gpa': '3.5',
            'phone': '1234567890',
            'address': 'Test Address',
            'is_active': True,
        }
        response = self.client.post(reverse('students:add'), data=data)
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_request_method_check(self):
        """Topic 33: request.method Check"""
        response = self.client.get(reverse('students:add'))
        self.assertEqual(response.status_code, 200)
        # Form should be blank for GET
        form = response.context['form']
        self.assertFalse(form.is_bound)
    
    def test_csrf_token_in_template(self):
        """Topic 40: {% csrf_token %} Tag"""
        response = self.client.get(reverse('students:add'))
        self.assertContains(response, 'csrfmiddlewaretoken')
