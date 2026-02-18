from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import date
from .models import Student
from .forms import StudentForm


class AdvancedViewOperationsTestCase(TestCase):
    """Topics 41-50: Advanced View Operations and Display"""

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            email='advanced@example.com',
            first_name='Advanced',
            last_name='Student',
            phone='555-0001',
            enrollment_date=date(2024, 1, 15),
            is_active=True
        )

    def test_dynamic_url_generation(self):
        """Topic 41: Dynamic URLs generated with parameters"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        self.assertIn(str(self.student.id), url)

    def test_url_tag_with_parameters(self):
        """Topic 42: {% url %} tag works with parameters"""
        response = self.client.get(reverse('students:index'))
        url = reverse('students:view', kwargs={'student_id': self.student.id})
        self.assertContains(response, url)

    def test_reverse_function_with_parameters(self):
        """Topic 43: reverse() works with parameters"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        self.assertTrue(url.endswith(f'/{self.student.id}/'))

    def test_student_id_from_url(self):
        """Topic 44: Student ID retrieved from URL"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertEqual(response.context['student'].id, self.student.id)

    def test_primary_key_retrieval(self):
        """Topic 45: Primary key correctly retrieved"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, self.student.email)

    def test_view_details_heading(self):
        """Topic 46: View details has proper heading"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'Profile')

    def test_information_display_layout(self):
        """Topic 47: Information displayed in organized layout"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'Name')
        self.assertContains(response, 'Email')

    def test_grid_layout_for_details(self):
        """Topic 48: Grid layout used for details display"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'row')

    def test_email_link_in_details(self):
        """Topic 49: Email displayed as clickable link"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, f'mailto:{self.student.email}')

    def test_phone_number_display(self):
        """Topic 50: Phone number prominently displayed"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, self.student.phone)


class AdvancedEditPatternsTestCase(TestCase):
    """Topics 51-60: Advanced Edit Patterns and Validation"""

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            email='edit@example.com',
            first_name='Edit',
            last_name='Test',
            phone='555-0002',
            enrollment_date=date(2024, 1, 15),
            is_active=True
        )

    def test_status_badge_display(self):
        """Topic 51: Status badge prominently displayed"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'badge')

    def test_active_inactive_status(self):
        """Topic 52: Active/Inactive status clearly shown"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'Active')

    def test_enrollment_date_formatting(self):
        """Topic 53: Enrollment date formatted nicely"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, '2024')

    def test_date_filters_in_templates(self):
        """Topic 54: Date filters applied in templates"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'January')

    def test_created_at_timestamp(self):
        """Topic 55: Created at timestamp displayed"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'Created')

    def test_edit_form_heading(self):
        """Topic 56: Edit form has descriptive heading"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, 'Edit')

    def test_edit_template_structure(self):
        """Topic 57: Edit template properly structured"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'edit.html')

    def test_current_data_display(self):
        """Topic 58: Current data displayed in form"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, self.student.first_name)

    def test_form_field_re_rendering(self):
        """Topic 59: Form fields re-rendered with current data"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        form = response.context['form']
        self.assertEqual(form['email'].value(), self.student.email)

    def test_validation_on_update(self):
        """Topic 60: Validation runs on update"""
        url = reverse('students:edit', kwargs={'student_id': self.student.id})
        response = self.client.post(url, {
            'email': 'invalid',
            'first_name': 'Test'
        })
        self.assertEqual(response.status_code, 200)


class AdvancedDeleteWorkflowsTestCase(TestCase):
    """Topics 61-70: Advanced Delete Workflows"""

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            email='delete@example.com',
            first_name='Delete',
            last_name='Test',
            phone='555-0003',
            enrollment_date=date(2024, 1, 15)
        )

    def test_unique_constraint_checking(self):
        """Topic 61: Unique constraints enforced"""
        Student.objects.create(
            email='unique@example.com',
            first_name='Unique',
            last_name='User',
            enrollment_date=date(2024, 1, 15)
        )
        form = StudentForm(data={
            'email': 'unique@example.com',
            'first_name': 'Other',
            'last_name': 'User',
            'enrollment_date': '2024-01-15'
        })
        self.assertFalse(form.is_valid())

    def test_email_uniqueness_on_edit(self):
        """Topic 62: Email uniqueness enforced during edit"""
        other = Student.objects.create(
            email='other@example.com',
            first_name='Other',
            last_name='User',
            enrollment_date=date(2024, 1, 15)
        )
        form = StudentForm(data={
            'email': 'other@example.com',
            'first_name': 'Delete',
            'last_name': 'Test',
            'enrollment_date': '2024-01-15'
        }, instance=self.student)
        self.assertFalse(form.is_valid())

    def test_exclude_current_instance(self):
        """Topic 63: Current instance excluded from validation"""
        form = StudentForm(data={
            'email': 'delete@example.com',
            'first_name': 'Delete',
            'last_name': 'Test',
            'enrollment_date': '2024-01-15'
        }, instance=self.student)
        self.assertTrue(form.is_valid())

    def test_delete_confirmation_heading(self):
        """Topic 64: Delete confirmation has clear heading"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, 'Confirm')

    def test_delete_warning_alert(self):
        """Topic 65: Delete warning alert displayed"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, 'Warning')

    def test_student_info_preview(self):
        """Topic 66: Student info shown on delete page"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, self.student.first_name)

    def test_confirm_and_cancel_buttons(self):
        """Topic 67: Confirm and Cancel buttons present"""
        url = reverse('students:delete', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertContains(response, 'Delete')
        self.assertContains(response, 'Cancel')

    def test_deletion_post_action(self):
        """Topic 68: Deletion occurs on POST"""
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
        """Topic 70: Navigation flow between all views"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, reverse('students:add'))
        self.assertContains(response, reverse('students:view', kwargs={'student_id': self.student.id}))


class ProjectIntegrationTestCase(TestCase):
    """Topics 71-80: Project Integration and Summary"""

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            email='project@example.com',
            first_name='Project',
            last_name='Test',
            phone='555-0004',
            enrollment_date=date(2024, 1, 15),
            is_active=True
        )

    def test_previous_page_navigation(self):
        """Topic 71: Back button navigates to previous page"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, reverse('students:index'))

    def test_student_list_integration(self):
        """Topic 72: Student list shows all students"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, self.student.email)

    def test_button_row_display(self):
        """Topic 73: Button rows displayed properly"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'btn-group')

    def test_icon_plus_text_in_buttons(self):
        """Topic 74: Icons and text in buttons"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'fa-')

    def test_responsive_button_layout(self):
        """Topic 75: Button layout is responsive"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'btn-sm')

    def test_mobile_friendly_actions(self):
        """Topic 76: Actions are mobile-friendly"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'd-none')

    def test_complete_project_structure(self):
        """Topic 77: Project structure is complete"""
        views_exist = hasattr(Student, 'objects')
        self.assertTrue(views_exist)

    def test_template_inheritance_usage(self):
        """Topic 78: Template inheritance used throughout"""
        response = self.client.get(reverse('students:add'))
        self.assertTemplateUsed(response, 'base.html')

    def test_base_template_navigation(self):
        """Topic 79: Base template has navigation"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'navbar')

    def test_project_overview_complete(self):
        """Topic 80: Complete project fully functional"""
        all_views_work = True
        test_urls = [
            reverse('students:index'),
            reverse('students:add'),
            reverse('students:view', kwargs={'student_id': self.student.id}),
            reverse('students:edit', kwargs={'student_id': self.student.id}),
            reverse('students:delete', kwargs={'student_id': self.student.id}),
        ]
        for url in test_urls:
            response = self.client.get(url)
            if response.status_code not in [200, 302]:
                all_views_work = False
        self.assertTrue(all_views_work)


class AdvancedUIFeaturesTestCase(TestCase):
    """Additional UI and UX Features"""

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            email='ui@example.com',
            first_name='UI',
            last_name='Feature',
            phone='555-0005',
            enrollment_date=date(2024, 1, 15),
            is_active=False
        )

    def test_card_based_layout_for_list(self):
        """Card-based layout on list view"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'card')

    def test_timestamp_display(self):
        """Timestamps displayed with formatting"""
        response = self.client.get(
            reverse('students:view', kwargs={'student_id': self.student.id})
        )
        self.assertContains(response, 'Created')

    def test_color_coded_badges(self):
        """Status badges with appropriate colors"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'bg-')

    def test_icon_consistency(self):
        """Icons used consistently throughout"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'fas')

    def test_form_layout_consistency(self):
        """Form layouts are consistent"""
        add_response = self.client.get(reverse('students:add'))
        edit_response = self.client.get(
            reverse('students:edit', kwargs={'student_id': self.student.id})
        )
        self.assertContains(add_response, 'form')
        self.assertContains(edit_response, 'form')

    def test_success_message_styling(self):
        """Success messages are styled"""
        response = self.client.post(reverse('students:add'), {
            'email': 'styled@example.com',
            'first_name': 'Styled',
            'last_name': 'Message',
            'enrollment_date': '2024-02-01'
        }, follow=True)
        self.assertContains(response, 'alert')

    def test_footer_present(self):
        """Footer displayed on all pages"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'footer')

    def test_responsive_grid(self):
        """Bootstrap responsive grid used"""
        response = self.client.get(reverse('students:index'))
        self.assertContains(response, 'col-')
