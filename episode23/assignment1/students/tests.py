from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import date
from .models import Student
from .forms import StudentForm


class CRUDFoundationTestCase(TestCase):
    """Topics 1-15: CRUD Operations Foundation"""

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            email='john@example.com',
            first_name='John',
            last_name='Doe',
            phone='555-1234',
            enrollment_date=date(2024, 1, 15),
            is_active=True
        )

    def test_crud_operations_overview(self):
        """Topic 1: CRUD operations are available"""
        self.assertTrue(hasattr(Student, 'objects'))
        self.assertEqual(Student.objects.count(), 1)

    def test_create_operation_pattern(self):
        """Topic 2: Create operation works with POST"""
        response = self.client.post(reverse('students:add'), {
            'email': 'jane@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone': '555-5678',
            'enrollment_date': '2024-02-01',
            'is_active': True
        })
        self.assertEqual(Student.objects.count(), 2)

    def test_read_operation_list(self):
        """Topic 3: Read operation displays list"""
        response = self.client.get(reverse('students:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'john@example.com')

    def test_update_operation_pattern(self):
        """Topic 4: Update operation modifies existing object"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.post(url, {
            'email': 'john.new@example.com',
            'first_name': 'John',
            'last_name': 'Updated',
            'phone': '555-9999',
            'enrollment_date': '2024-01-15',
            'is_active': True
        })
        self.student.refresh_from_db()
        self.assertEqual(self.student.last_name, 'Updated')

    def test_delete_operation_pattern(self):
        """Topic 5: Delete operation removes object"""
        student_id = self.student.id
        response = self.client.post(
            reverse('students:delete', kwargs={'student_id': student_id})
        )
        self.assertFalse(Student.objects.filter(id=student_id).exists())

    def test_get_object_or_404_function(self):
        """Topic 6: get_object_or_404 used for retrieval"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_single_object_retrieval(self):
        """Topic 7: Single object retrieval by ID"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, self.student.email)

    def test_404_error_handling(self):
        """Topic 8: 404 error on invalid ID"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': 99999})
        )
        self.assertEqual(response.status_code, 404)

    def test_detail_view_pattern(self):
        """Topic 9: Detail view displays single object"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view.html')

    def test_instance_parameter_in_forms(self):
        """Topic 10: Form accepts instance parameter"""
        form = StudentForm(instance=self.student)
        self.assertEqual(form.instance.email, 'john@example.com')

    def test_pre_populated_form_fields(self):
        """Topic 11: Form fields pre-populated with instance data"""
        form = StudentForm(instance=self.student)
        self.assertEqual(form['email'].value(), 'john@example.com')

    def test_editing_existing_objects(self):
        """Topic 12: Can edit existing objects"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.student.email, str(response.content))

    def test_form_modification_workflow(self):
        """Topic 13: Form modification workflow works"""
        form = StudentForm(instance=self.student)
        self.assertIsNotNone(form.instance)

    def test_update_vs_create_distinction(self):
        """Topic 14: Update differs from create"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        old_count = Student.objects.count()
        self.client.post(url, {
            'email': 'updated@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '555-1234',
            'enrollment_date': '2024-01-15',
            'is_active': True
        })
        self.assertEqual(Student.objects.count(), old_count)

    def test_redirect_after_update(self):
        """Topic 15: Redirect after successful update"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.post(url, {
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '555-1234',
            'enrollment_date': '2024-01-15',
            'is_active': True
        })
        self.assertRedirects(response, reverse('students:index'))


class OperationsSafetyTestCase(TestCase):
    """Topics 16-30: Operations Safety and UI"""

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            enrollment_date=date(2024, 1, 15)
        )

    def test_successful_update_feedback(self):
        """Topic 16: Success feedback after update"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.post(url, {
            'email': 'test@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'enrollment_date': '2024-01-15'
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('updated' in str(m).lower() for m in messages))

    def test_delete_confirmation_pattern(self):
        """Topic 17: Delete confirmation page"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete.html')

    def test_destructive_operation_safety(self):
        """Topic 18: Destructive operations are safe"""
        response = self.client.get(
            reverse('students:delete', kwargs={'student_id': self.student.id})
        )
        self.assertTrue(Student.objects.filter(id=self.student.id).exists())

    def test_post_for_deletion(self):
        """Topic 19: POST required for deletion"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertTrue(Student.objects.filter(id=self.student.id).exists())

    def test_data_loss_prevention(self):
        """Topic 20: Data loss prevented with confirmation"""
        original_count = Student.objects.count()
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        self.client.get(url)
        self.assertEqual(Student.objects.count(), original_count)

    def test_confirmation_templates(self):
        """Topic 21: Confirmation templates exist"""
        response = self.client.get(
            reverse('students:delete', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'Delete Confirmation')

    def test_delete_redirect_path(self):
        """Topic 22: Redirect to list after delete"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('students:index'))

    def test_success_messages_for_operations(self):
        """Topic 23: Success messages for all operations"""
        response = self.client.post(reverse('students:add'), {
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'enrollment_date': '2024-02-01'
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('successfully' in str(m).lower() for m in messages))

    def test_messages_success_usage(self):
        """Topic 24: messages.success() is used"""
        response = self.client.post(reverse('students:add'), {
            'email': 'another@example.com',
            'first_name': 'Another',
            'last_name': 'User',
            'enrollment_date': '2024-02-01'
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(len(messages) > 0)

    def test_messages_error_usage(self):
        """Topic 25: Form errors are displayed"""
        response = self.client.post(reverse('students:add'), {
            'email': 'invalid-email',
            'first_name': 'Test'
        })
        self.assertEqual(response.status_code, 200)

    def test_message_display_in_templates(self):
        """Topic 26: Messages display in templates"""
        response = self.client.post(reverse('students:add'), {
            'email': 'msg@example.com',
            'first_name': 'Message',
            'last_name': 'Test',
            'enrollment_date': '2024-02-01'
        }, follow=True)
        self.assertContains(response, 'alert')

    def test_bootstrap_alert_integration(self):
        """Topic 27: Bootstrap alerts for messages"""
        response = self.client.post(reverse('students:add'), {
            'email': 'bootstrap@example.com',
            'first_name': 'Bootstrap',
            'last_name': 'Alert',
            'enrollment_date': '2024-02-01'
        }, follow=True)
        self.assertContains(response, 'alert')

    def test_font_awesome_icons(self):
        """Topic 28: Font Awesome icons present"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'fa-')

    def test_icon_placement_in_ui(self):
        """Topic 29: Icons properly placed in UI"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'fas fa-')

    def test_user_action_buttons(self):
        """Topic 30: User action buttons present"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'btn')


class ViewOperationsTestCase(TestCase):
    """Topics 31-50: View Operations and Parameters"""

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            email='view@example.com',
            first_name='View',
            last_name='Test',
            phone='555-1111',
            enrollment_date=date(2024, 1, 15),
            is_active=True
        )

    def test_button_styling_bootstrap(self):
        """Topic 31: Button styling with Bootstrap"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'btn-')

    def test_primary_secondary_danger_buttons(self):
        """Topic 32: Button types present"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'btn-primary')
        self.assertContains(response, 'btn-info')
        self.assertContains(response, 'btn-danger')

    def test_button_groups_alignment(self):
        """Topic 33: Buttons aligned properly"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'btn')

    def test_edit_button_implementation(self):
        """Topic 34: Edit button links to edit view"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, reverse('students:edit', kwargs={'student_id': self.student.id}))

    def test_view_button_implementation(self):
        """Topic 35: View button links to detail view"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, reverse('students:view', kwargs={'student_id': self.student.id}))

    def test_delete_button_implementation(self):
        """Topic 36: Delete button links to delete view"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, reverse('students:delete', kwargs={'student_id': self.student.id}))

    def test_add_button_implementation(self):
        """Topic 37: Add button on list page"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, reverse('students:add'))

    def test_back_cancel_buttons(self):
        """Topic 38: Back/Cancel buttons present"""
        response = self.client.get(reverse('students:add'))
        self.assertContains(response, 'Cancel')

    def test_action_button_organization(self):
        """Topic 39: Action buttons organized properly"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'btn-info')
        self.assertContains(response, 'btn-warning')
        self.assertContains(response, 'btn-danger')

    def test_url_parameters_in_views(self):
        """Topic 40: URL parameters passed to views"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertEqual(response.context['student'].id, self.student.id)

    def test_dynamic_url_generation(self):
        """Topic 41: Dynamic URLs generated from parameters"""
        response = self.client.get(reverse('students:index'))
        edit_url = reverse('students:edit', kwargs={'student_id': self.student.id})
        self.assertContains(response, edit_url)

    def test_url_tag_with_parameters(self):
        """Topic 42: {% url %} tag with parameters works"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, f'/students/view/{self.student.id}/')

    def test_reverse_function_with_parameters(self):
        """Topic 43: reverse() function with parameters"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        self.assertIn(str(self.student.id), url)

    def test_student_id_from_url(self):
        """Topic 44: Student ID retrieved from URL"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertEqual(response.context['student'].id, self.student.id)

    def test_primary_key_retrieval(self):
        """Topic 45: Primary key retrieved correctly"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, self.student.email)

    def test_view_details_heading(self):
        """Topic 46: Detail view has proper heading"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'Student Details')

    def test_information_display_layout(self):
        """Topic 47: Information displayed in layout"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Phone')

    def test_grid_layout_for_details(self):
        """Topic 48: Grid layout used for details"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'row')

    def test_email_link_in_details(self):
        """Topic 49: Email displayed in details"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, self.student.email)

    def test_phone_number_display(self):
        """Topic 50: Phone number displayed"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, self.student.phone)


class EditDeleteWorkflowsTestCase(TestCase):
    """Topics 51-70: Edit and Delete Workflows"""

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            email='workflow@example.com',
            first_name='Workflow',
            last_name='Test',
            phone='555-2222',
            enrollment_date=date(2024, 1, 15),
            is_active=True
        )

    def test_status_badge_display(self):
        """Topic 51: Status badge displayed"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'badge')

    def test_active_inactive_status(self):
        """Topic 52: Active/Inactive status shown"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'Active')

    def test_enrollment_date_formatting(self):
        """Topic 53: Enrollment date formatted"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'Jan')

    def test_date_filters_in_templates(self):
        """Topic 54: Date filters applied in templates"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, ', 2024')

    def test_created_at_timestamp(self):
        """Topic 55: Created at timestamp exists"""
        self.assertIsNotNone(self.student.created_at)

    def test_edit_form_heading(self):
        """Topic 56: Edit form has proper heading"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, 'Edit')

    def test_edit_template_structure(self):
        """Topic 57: Edit template properly structured"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'edit.html')

    def test_current_data_display(self):
        """Topic 58: Current data displayed in edit form"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, self.student.email)

    def test_form_field_re_rendering(self):
        """Topic 59: Form fields re-rendered with data"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, self.student.first_name)

    def test_validation_on_update(self):
        """Topic 60: Validation occurs on update"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.post(url, {
            'email': 'invalid',
            'first_name': 'Test'
        })
        self.assertEqual(response.status_code, 200)

    def test_unique_constraint_checking(self):
        """Topic 61: Unique constraints checked"""
        Student.objects.create(
            email='unique@example.com',
            first_name='Unique',
            last_name='Test',
            enrollment_date=date(2024, 1, 15)
        )
        form = StudentForm(data={
            'email': 'unique@example.com',
            'first_name': 'Test',
            'last_name': 'Test',
            'enrollment_date': '2024-01-15'
        })
        self.assertFalse(form.is_valid())

    def test_email_uniqueness_on_edit(self):
        """Topic 62: Email uniqueness enforced on edit"""
        other_student = Student.objects.create(
            email='other@example.com',
            first_name='Other',
            last_name='User',
            enrollment_date=date(2024, 1, 15)
        )
        form = StudentForm(data={
            'email': 'other@example.com',
            'first_name': 'Workflow',
            'last_name': 'Test',
            'enrollment_date': '2024-01-15'
        }, instance=self.student)
        self.assertFalse(form.is_valid())

    def test_exclude_current_instance(self):
        """Topic 63: Current instance excluded from validation"""
        form = StudentForm(data={
            'email': 'workflow@example.com',
            'first_name': 'Workflow',
            'last_name': 'Test',
            'enrollment_date': '2024-01-15'
        }, instance=self.student)
        self.assertTrue(form.is_valid())

    def test_delete_confirmation_heading(self):
        """Topic 64: Delete confirmation has heading"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, 'Delete Confirmation')

    def test_delete_warning_alert(self):
        """Topic 65: Delete warning alert displayed"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, 'alert')

    def test_student_info_preview(self):
        """Topic 66: Student info shown on delete confirmation"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, self.student.email)

    def test_confirm_and_cancel_buttons(self):
        """Topic 67: Confirm and cancel buttons present"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, 'Delete')
        self.assertContains(response, 'Cancel')

    def test_deletion_post_action(self):
        """Topic 68: Post-deletion action occurs"""
        student_id = self.student.id
        self.client.post(
            reverse('students:delete', kwargs={'student_id': student_id})
        )
        self.assertFalse(Student.objects.filter(id=student_id).exists())

    def test_list_redirection(self):
        """Topic 69: Redirect to list after delete"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('students:index'))

    def test_navigation_flow(self):
        """Topic 70: Navigation flow between views"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, reverse('students:add'))
        self.assertContains(response, reverse('students:view', kwargs={'student_id': self.student.id}))
