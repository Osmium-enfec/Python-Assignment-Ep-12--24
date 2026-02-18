from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm

class TaskModelTests(TestCase):
    """
    Tests covering:
    - Topic 1: Understanding Copilot's role in model generation
    - Topic 2: String representation and model methods
    - Topic 3: Model field types and choices
    """

    def setUp(self):
        """Create test task"""
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            priority=3,
            completed=False
        )

    def test_task_str_representation(self):
        """Topic 2: Verify __str__ method works correctly"""
        expected_str = "Test Task (Priority: High)"
        self.assertEqual(str(self.task), expected_str)

    def test_task_creation(self):
        """Topic 1: Verify task can be created with default values"""
        task = Task.objects.create(title='Simple Task')
        self.assertEqual(task.title, 'Simple Task')
        self.assertEqual(task.priority, 2)
        self.assertFalse(task.completed)

    def test_task_priority_choices(self):
        """Topic 3: Verify priority choices are valid"""
        valid_priorities = [1, 2, 3, 4, 5]
        for priority in valid_priorities:
            task = Task.objects.create(title=f'Task {priority}', priority=priority)
            self.assertEqual(task.priority, priority)

    def test_task_timestamps(self):
        """Topic 4: Verify created_at and updated_at work correctly"""
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)
        self.assertLessEqual((self.task.updated_at - self.task.created_at).total_seconds(), 1)

    def test_task_ordering(self):
        """Topic 5: Verify tasks are ordered by priority and created_at"""
        task1 = Task.objects.create(title='Low Priority', priority=1)
        task2 = Task.objects.create(title='High Priority', priority=5)
        tasks = Task.objects.all()
        self.assertEqual(tasks.first(), task2)

class TaskFormTests(TestCase):
    """
    Tests covering:
    - Topic 6: Form validation
    - Topic 7: ModelForm field widgets
    - Topic 8: Form rendering in templates
    """

    def test_form_valid_data(self):
        """Topic 6: Valid form data should pass validation"""
        form_data = {
            'title': 'New Task',
            'description': 'Task description',
            'priority': 2,
            'completed': False
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_title(self):
        """Topic 6: Form should fail without title"""
        form_data = {
            'description': 'Task description',
            'priority': 2,
            'completed': False
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_widget_classes(self):
        """Topic 7: Verify Bootstrap widget classes are applied"""
        form = TaskForm()
        self.assertIn('form-control', str(form['title']))
        self.assertIn('form-control', str(form['description']))
        self.assertIn('form-select', str(form['priority']))
        self.assertIn('form-check-input', str(form['completed']))

    def test_form_save(self):
        """Topic 8: Form should save to database correctly"""
        form_data = {
            'title': 'Database Task',
            'description': 'Testing form save',
            'priority': 4,
            'completed': False
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
        task = form.save()
        self.assertEqual(Task.objects.filter(title='Database Task').count(), 1)

    def test_form_with_instance(self):
        """Topic 9: Form should load existing task data"""
        task = Task.objects.create(title='Existing Task', priority=3)
        form = TaskForm(instance=task)
        self.assertEqual(form.initial['title'], 'Existing Task')
        self.assertEqual(form.initial['priority'], 3)

class TaskListViewTests(TestCase):
    """
    Tests covering:
    - Topic 10: Views and request handling
    - Topic 11: Template rendering
    - Topic 12: GET requests and data passing
    """

    def setUp(self):
        """Create test tasks"""
        self.client = Client()
        self.url = reverse('tasks:list')
        self.task1 = Task.objects.create(title='Task 1', priority=1)
        self.task2 = Task.objects.create(title='Task 2', priority=5)

    def test_list_view_status_code(self):
        """Topic 10: List view should return 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_view_template(self):
        """Topic 11: List view should use task_list.html template"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'task_list.html')

    def test_list_view_context_data(self):
        """Topic 12: Context should contain tasks"""
        response = self.client.get(self.url)
        self.assertIn('tasks', response.context)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 2)

    def test_list_view_task_ordering(self):
        """Topic 13: Tasks should be ordered by priority (highest first)"""
        response = self.client.get(self.url)
        tasks = response.context['tasks']
        self.assertEqual(tasks[0].priority, 5)
        self.assertEqual(tasks[1].priority, 1)

    def test_list_view_empty(self):
        """Topic 14: Empty list should display message"""
        Task.objects.all().delete()
        response = self.client.get(self.url)
        self.assertContains(response, 'No tasks yet')

class TaskCreateViewTests(TestCase):
    """
    Tests covering:
    - Topic 15: POST-Redirect-GET pattern
    - Topic 16: Form validation in views
    - Topic 17: Messages framework
    """

    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('tasks:create')

    def test_create_view_get(self):
        """Topic 15: GET request should display form"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_form.html')
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_create_task_post_valid(self):
        """Topic 16: Valid POST should create task and redirect"""
        form_data = {
            'title': 'New Task',
            'description': 'New description',
            'priority': 3,
            'completed': False
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

    def test_create_task_post_invalid(self):
        """Topic 16: Invalid POST should redisplay form"""
        form_data = {
            'title': '',
            'description': 'Missing title',
            'priority': 3,
            'completed': False
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid())

    def test_create_task_message(self):
        """Topic 17: Success message should be displayed"""
        form_data = {
            'title': 'Task with Message',
            'description': 'Test message',
            'priority': 2,
            'completed': False
        }
        response = self.client.post(self.url, form_data, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn('created successfully', str(messages[0]))

class TaskDetailViewTests(TestCase):
    """
    Tests covering:
    - Topic 18: get_object_or_404 safety
    - Topic 19: 404 error handling
    - Topic 20: Template context data
    """

    def setUp(self):
        """Create test task"""
        self.client = Client()
        self.task = Task.objects.create(
            title='Detail Task',
            description='Test detail',
            priority=3
        )
        self.url = reverse('tasks:detail', args=[self.task.id])

    def test_detail_view_success(self):
        """Topic 18: Valid task ID should display details"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'], self.task)

    def test_detail_view_404(self):
        """Topic 19: Invalid task ID should return 404"""
        url = reverse('tasks:detail', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template(self):
        """Topic 20: Detail view should use task_detail.html"""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'task_detail.html')

    def test_detail_view_shows_task_content(self):
        """Topic 21: Task details should be visible on page"""
        response = self.client.get(self.url)
        self.assertContains(response, self.task.title)
        self.assertContains(response, self.task.description)

class TaskUpdateViewTests(TestCase):
    """
    Tests covering:
    - Topic 22: Instance parameter in forms
    - Topic 23: Pre-populated form data
    - Topic 24: Update validation
    """

    def setUp(self):
        """Create test task"""
        self.client = Client()
        self.task = Task.objects.create(
            title='Original Title',
            description='Original Description',
            priority=2
        )
        self.url = reverse('tasks:update', args=[self.task.id])

    def test_update_view_get(self):
        """Topic 22: Form should pre-populate with existing data"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.instance, self.task)

    def test_update_task_valid(self):
        """Topic 23: Valid update should save changes"""
        form_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'priority': 4,
            'completed': True
        }
        response = self.client.post(self.url, form_data)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Title')
        self.assertEqual(self.task.priority, 4)
        self.assertTrue(self.task.completed)

    def test_update_task_message(self):
        """Topic 24: Update success message should display"""
        form_data = {
            'title': 'Updated',
            'description': 'Test',
            'priority': 3,
            'completed': False
        }
        response = self.client.post(self.url, form_data, follow=True)
        messages = list(response.context['messages'])
        self.assertIn('updated successfully', str(messages[0]))

class TaskDeleteViewTests(TestCase):
    """
    Tests covering:
    - Topic 25: DELETE confirmation pattern
    - Topic 26: POST-based deletion
    - Topic 27: Deletion safety
    """

    def setUp(self):
        """Create test task"""
        self.client = Client()
        self.task = Task.objects.create(title='Delete Me', priority=2)
        self.url = reverse('tasks:delete', args=[self.task.id])

    def test_delete_view_get(self):
        """Topic 25: GET should show confirmation"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_confirm_delete.html')

    def test_delete_task_post(self):
        """Topic 26: POST should delete task"""
        response = self.client.post(self.url)
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_task_message(self):
        """Topic 27: Delete success message should display"""
        response = self.client.post(self.url, follow=True)
        messages = list(response.context['messages'])
        self.assertIn('deleted successfully', str(messages[0]))

class CopilotPatternRecognitionTests(TestCase):
    """
    Tests covering:
    - Topic 28: CRUD pattern completeness
    - Topic 29: View naming conventions
    - Topic 30: URL naming and reversibility
    """

    def test_crud_patterns_exist(self):
        """Topic 28: All CRUD operations should be available"""
        # Create
        task = Task.objects.create(title='CRUD Test', priority=2)
        self.assertIsNotNone(task.id)
        
        # Read
        retrieved = Task.objects.get(id=task.id)
        self.assertEqual(retrieved.title, 'CRUD Test')
        
        # Update
        retrieved.priority = 4
        retrieved.save()
        self.assertEqual(Task.objects.get(id=task.id).priority, 4)
        
        # Delete
        task.delete()
        self.assertEqual(Task.objects.filter(id=task.id).count(), 0)

    def test_url_reverse_works(self):
        """Topic 29: URL reversibility for all views"""
        self.assertIsNotNone(reverse('tasks:list'))
        self.assertIsNotNone(reverse('tasks:create'))
        
        task = Task.objects.create(title='URL Test', priority=2)
        self.assertIsNotNone(reverse('tasks:detail', args=[task.id]))
        self.assertIsNotNone(reverse('tasks:update', args=[task.id]))
        self.assertIsNotNone(reverse('tasks:delete', args=[task.id]))

    def test_view_names_match_patterns(self):
        """Topic 30: View function names should match their purpose"""
        from tasks import views
        self.assertTrue(hasattr(views, 'task_list'))
        self.assertTrue(hasattr(views, 'task_create'))
        self.assertTrue(hasattr(views, 'task_detail'))
        self.assertTrue(hasattr(views, 'task_update'))
        self.assertTrue(hasattr(views, 'task_delete'))
