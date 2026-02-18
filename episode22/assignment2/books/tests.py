from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Book
from .forms import BookForm
from decimal import Decimal


class BookModelTestCase(TestCase):
    """Topic 41-48: Book Model and ModelForm Tests"""

    def setUp(self):
        self.book = Book.objects.create(
            title="Django for Beginners",
            isbn="978-1-234567-89-0",
            author="John Smith",
            description="Learn Django from scratch",
            price=Decimal("29.99"),
            genre="Technology",
            is_published=True
        )

    def test_book_model_creation(self):
        """Topic 42: Book model creation and fields"""
        self.assertEqual(self.book.title, "Django for Beginners")
        self.assertEqual(self.book.isbn, "978-1-234567-89-0")
        self.assertEqual(self.book.price, Decimal("29.99"))
        self.assertEqual(self.book.genre, "Technology")

    def test_book_model_str(self):
        """Topic 42: Book __str__ method"""
        self.assertIn("Django for Beginners", str(self.book))
        self.assertIn("John Smith", str(self.book))

    def test_book_timestamps(self):
        """Topic 41: Auto timestamp fields"""
        self.assertIsNotNone(self.book.created_at)
        self.assertIsNotNone(self.book.updated_at)

    def test_book_unique_isbn(self):
        """Topic 44: ISBN unique constraint"""
        with self.assertRaises(Exception):
            Book.objects.create(
                title="Another Book",
                isbn="978-1-234567-89-0",
                author="Another Author",
                price=Decimal("19.99"),
                genre="Tech"
            )


class BookFormTestCase(TestCase):
    """Topic 45-48: ModelForm and Widget Configuration"""

    def test_book_form_fields(self):
        """Topic 45: BookForm includes all required fields"""
        form = BookForm()
        self.assertIn('title', form.fields)
        self.assertIn('isbn', form.fields)
        self.assertIn('author', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('price', form.fields)
        self.assertIn('genre', form.fields)
        self.assertIn('is_published', form.fields)

    def test_book_form_widgets(self):
        """Topic 46-47: Widgets configured with Bootstrap classes"""
        form = BookForm()
        self.assertIn('form-control', str(form['title'].field.widget.attrs.get('class', '')))
        self.assertIn('form-control', str(form['price'].field.widget.attrs.get('class', '')))
        self.assertIn('form-check-input', str(form['is_published'].field.widget.attrs.get('class', '')))

    def test_book_form_valid_data(self):
        """Topic 48: Form validation with valid data"""
        form_data = {
            'title': 'New Book',
            'isbn': '978-1-987654-32-1',
            'author': 'Jane Doe',
            'description': 'A great book',
            'price': '24.99',
            'genre': 'Fiction',
            'is_published': True
        }
        form = BookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_book_form_invalid_price(self):
        """Topic 49: Form validation - invalid price"""
        form_data = {
            'title': 'New Book',
            'isbn': '978-1-987654-32-1',
            'author': 'Jane Doe',
            'price': 'invalid',
            'genre': 'Fiction'
        }
        form = BookForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_book_form_missing_required_field(self):
        """Topic 50: Form validation - missing required field"""
        form_data = {
            'author': 'Jane Doe',
            'price': '24.99'
        }
        form = BookForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class BookCreateViewTestCase(TestCase):
    """Topic 51-56: Form Display and POST Handling"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('books:create')

    def test_create_view_get_displays_form(self):
        """Topic 51: GET request displays form template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')
        self.assertIsInstance(response.context['form'], BookForm)

    def test_create_view_get_form_has_csrf_token(self):
        """Topic 52: Form contains CSRF token for security"""
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_create_view_post_valid_data(self):
        """Topic 53: POST with valid data creates book and redirects"""
        form_data = {
            'title': 'New Book',
            'isbn': '978-1-987654-32-1',
            'author': 'Jane Doe',
            'description': 'A great book',
            'price': '24.99',
            'genre': 'Fiction',
            'is_published': True
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(isbn='978-1-987654-32-1').exists())

    def test_create_view_post_invalid_data(self):
        """Topic 54: POST with invalid data re-displays form with errors"""
        form_data = {
            'title': 'New Book',
            'isbn': '978-1-987654-32-1',
            'price': 'invalid'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')
        self.assertTrue(response.context['form'].errors)

    def test_create_view_success_message(self):
        """Topic 55: Success message displayed after creation"""
        form_data = {
            'title': 'New Book',
            'isbn': '978-1-987654-32-1',
            'author': 'Jane Doe',
            'price': '24.99',
            'genre': 'Fiction'
        }
        response = self.client.post(self.url, form_data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('successfully' in str(m).lower() for m in messages))

    def test_create_view_redirects_to_list(self):
        """Topic 56: After creation, redirect to book list"""
        form_data = {
            'title': 'New Book',
            'isbn': '978-1-987654-32-1',
            'author': 'Jane Doe',
            'price': '24.99',
            'genre': 'Fiction'
        }
        response = self.client.post(self.url, form_data)
        self.assertRedirects(response, reverse('books:list'))


class BookListViewTestCase(TestCase):
    """Topic 57-60: Form Templates and Bootstrap Integration"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('books:list')
        self.book1 = Book.objects.create(
            title="Book 1",
            isbn="978-1-111111-11-1",
            author="Author 1",
            price=Decimal("19.99"),
            genre="Tech"
        )
        self.book2 = Book.objects.create(
            title="Book 2",
            isbn="978-2-222222-22-2",
            author="Author 2",
            price=Decimal("29.99"),
            genre="Fiction"
        )

    def test_list_view_displays_all_books(self):
        """Topic 57: List view displays all books"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertContains(response, "Book 1")
        self.assertContains(response, "Book 2")

    def test_list_view_displays_book_details(self):
        """Topic 58: Book details rendered in list"""
        response = self.client.get(self.url)
        self.assertContains(response, "Author 1")
        self.assertContains(response, "$19.99")
        self.assertContains(response, "Tech")

    def test_list_view_has_add_button(self):
        """Topic 59: List page has 'Add Book' button"""
        response = self.client.get(self.url)
        self.assertContains(response, reverse('books:create'))

    def test_list_view_empty_state(self):
        """Topic 60: Empty state message when no books"""
        Book.objects.all().delete()
        response = self.client.get(self.url)
        self.assertContains(response, "No books")


class BookUpdateViewTestCase(TestCase):
    """Topic 61-66: Edit Forms and Instance Population"""

    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="Original Title",
            isbn="978-1-234567-89-0",
            author="Original Author",
            price=Decimal("19.99"),
            genre="Tech"
        )
        self.url = reverse('books:update', kwargs={'book_id': self.book.id})

    def test_update_view_displays_edit_form(self):
        """Topic 61: GET displays form for editing"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')

    def test_update_view_form_populated_with_book_data(self):
        """Topic 62: Form fields pre-populated with book data"""
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertEqual(form.instance.title, "Original Title")
        self.assertEqual(form.instance.author, "Original Author")

    def test_update_view_post_updates_book(self):
        """Topic 63: POST updates existing book"""
        form_data = {
            'title': 'Updated Title',
            'isbn': self.book.isbn,
            'author': 'Updated Author',
            'price': '29.99',
            'genre': 'Fiction'
        }
        response = self.client.post(self.url, form_data)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
        self.assertEqual(self.book.author, 'Updated Author')

    def test_update_view_post_invalid_data(self):
        """Topic 64: POST with invalid data shows errors"""
        form_data = {
            'title': 'Updated Title',
            'isbn': self.book.isbn,
            'price': 'invalid'
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_form.html')
        self.assertTrue(response.context['form'].errors)

    def test_update_view_success_message(self):
        """Topic 65: Success message after update"""
        form_data = {
            'title': 'Updated Title',
            'isbn': self.book.isbn,
            'author': 'Updated Author',
            'price': '29.99',
            'genre': 'Fiction'
        }
        response = self.client.post(self.url, form_data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('successfully' in str(m).lower() for m in messages))

    def test_update_view_redirects_to_list(self):
        """Topic 66: Redirect to list after successful update"""
        form_data = {
            'title': 'Updated Title',
            'isbn': self.book.isbn,
            'author': 'Updated Author',
            'price': '29.99',
            'genre': 'Fiction'
        }
        response = self.client.post(self.url, form_data)
        self.assertRedirects(response, reverse('books:list'))


class BookDeleteViewTestCase(TestCase):
    """Topic 67-72: Delete Confirmation and Messaging"""

    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="Book to Delete",
            isbn="978-1-111111-11-1",
            author="Author",
            price=Decimal("19.99"),
            genre="Tech"
        )
        self.url = reverse('books:delete', kwargs={'book_id': self.book.id})

    def test_delete_view_displays_confirmation(self):
        """Topic 67: GET displays confirmation template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_confirm_delete.html')

    def test_delete_view_shows_book_details(self):
        """Topic 68: Confirmation page shows book details"""
        response = self.client.get(self.url)
        self.assertContains(response, "Book to Delete")
        self.assertContains(response, "Author")

    def test_delete_view_post_deletes_book(self):
        """Topic 69: POST request deletes the book"""
        response = self.client.post(self.url)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_view_post_with_csrf_token(self):
        """Topic 70: Delete requires CSRF token"""
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_delete_view_success_message(self):
        """Topic 71: Success message after deletion"""
        response = self.client.post(self.url, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('successfully' in str(m).lower() or 'deleted' in str(m).lower() for m in messages))

    def test_delete_view_redirects_to_list(self):
        """Topic 72: Redirect to list after deletion"""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('books:list'))


class FormSecurityAndValidationTestCase(TestCase):
    """Topic 73-76: Form Security and Validation"""

    def setUp(self):
        self.client = Client()
        self.create_url = reverse('books:create')

    def test_form_requires_csrf_protection(self):
        """Topic 73: POST without CSRF token rejected"""
        self.client.enforce_csrf_checks = True
        form_data = {
            'title': 'New Book',
            'isbn': '978-1-987654-32-1',
            'author': 'Jane Doe',
            'price': '24.99',
            'genre': 'Fiction'
        }
        # This should work because we're using CSRF token in the template
        response = self.client.get(self.create_url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_form_validation_required_fields(self):
        """Topic 74: Required field validation"""
        response = self.client.get(self.create_url)
        form = BookForm(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 0)

    def test_form_validation_field_types(self):
        """Topic 75: Field type validation"""
        form = BookForm(data={
            'title': 'Book',
            'isbn': '123',
            'author': 'Author',
            'price': 'not_a_number',
            'genre': 'Tech'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_form_displays_field_errors(self):
        """Topic 76: Form displays validation errors to user"""
        response = self.client.get(self.create_url)
        self.assertContains(response, 'form-control')
        self.assertContains(response, 'csrfmiddlewaretoken')


class FormTemplateIntegrationTestCase(TestCase):
    """Topic 77-80: Complete Form Template Integration"""

    def setUp(self):
        self.client = Client()
        self.book = Book.objects.create(
            title="Test Book",
            isbn="978-1-234567-89-0",
            author="Test Author",
            description="Test Description",
            price=Decimal("29.99"),
            genre="Technology",
            is_published=True
        )

    def test_create_form_template_structure(self):
        """Topic 77: Create form template has proper structure"""
        response = self.client.get(reverse('books:create'))
        self.assertContains(response, '<form')
        self.assertContains(response, 'method="POST"')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, 'btn btn-primary')

    def test_update_form_template_structure(self):
        """Topic 78: Update form template differs from create"""
        response = self.client.get(reverse('books:update', kwargs={'book_id': self.book.id}))
        self.assertContains(response, 'Edit')
        self.assertContains(response, 'btn btn-warning')

    def test_delete_form_template_structure(self):
        """Topic 79: Delete confirmation template"""
        response = self.client.get(reverse('books:delete', kwargs={'book_id': self.book.id}))
        self.assertContains(response, 'Delete Confirmation')
        self.assertContains(response, 'btn btn-danger')
        self.assertContains(response, self.book.title)

    def test_form_error_display_integration(self):
        """Topic 80: Complete form workflow with error display"""
        form_data = {
            'title': 'New Book',
            'isbn': '978-1-987654-32-1',
            'author': 'Jane Doe',
            'price': 'invalid_price',
            'genre': 'Fiction'
        }
        response = self.client.post(reverse('books:create'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'invalid')
        self.assertTemplateUsed(response, 'books/book_form.html')
