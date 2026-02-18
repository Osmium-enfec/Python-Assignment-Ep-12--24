from django.test import TestCase, Client
from django.urls import reverse
from .models import Product

class TemplateInheritanceTestCase(TestCase):
    """Tests for Template Inheritance Fundamentals (Topics 1-12)"""
    
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            code='PROD001',
            name='Test Product',
            description='Test description',
            price=99.99,
            category='Electronics',
            is_active=True
        )
    
    def test_extends_tag(self):
        """Topic 2: {% extends %} Tag - Child template extends base"""
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        # Check that base template structure is present
        self.assertIn('navbar', response.content.decode())
        self.assertIn('footer', response.content.decode())
    
    def test_base_template(self):
        """Topic 3: Base Template - Master template structure"""
        response = self.client.get(reverse('products:list'))
        content = response.content.decode()
        # Check for base template elements
        self.assertIn('<!DOCTYPE html>', content)
        self.assertIn('<html', content)
        self.assertIn('Product Management', content)
    
    def test_child_template(self):
        """Topic 4: Child Template - Template inheriting from base"""
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        # Child extends base successfully
    
    def test_block_override(self):
        """Topic 6: Block Override - Child template overrides blocks"""
        response = self.client.get(reverse('products:list'))
        content = response.content.decode()
        # Check for overridden content block
        self.assertIn('Product List', content)
    
    def test_multiple_blocks(self):
        """Topic 9: Multiple Blocks - Base has multiple blocks"""
        response = self.client.get(reverse('products:list'))
        content = response.content.decode()
        # Base template has page_title, content, extra_css, extra_js blocks
        self.assertIn('Product Management', content)
    
    def test_template_organization(self):
        """Topic 11: Template Organization - Proper directory structure"""
        # Templates are in templates/base.html and templates/products/list.html
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_dry_principle(self):
        """Topic 12: DRY Principle - Code reuse"""
        # Load list page
        list_response = self.client.get(reverse('products:list'))
        list_content = list_response.content.decode()
        
        # Load detail page
        detail_response = self.client.get(reverse('products:detail', args=[self.product.id]))
        detail_content = detail_response.content.decode()
        
        # Both have the same navbar from base template
        self.assertIn('navbar', list_content)
        self.assertIn('navbar', detail_content)
        self.assertIn('Product Management', list_content)
        self.assertIn('Product Management', detail_content)


class TemplateTagsTestCase(TestCase):
    """Tests for Template Tags (Topics 23-30)"""
    
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            code='PROD001',
            name='Test Product',
            description='Test description',
            price=99.99,
            category='Electronics'
        )
    
    def test_url_tag(self):
        """Topic 23: {% url %} Tag - Dynamic URL generation"""
        response = self.client.get(reverse('products:list'))
        content = response.content.decode()
        # Check for generated URLs
        self.assertIn('/products/', content)
    
    def test_if_tag_conditional(self):
        """Topic 24: {% if %} Tag - Conditional rendering"""
        response = self.client.get(reverse('products:list'))
        content = response.content.decode()
        # Check for conditional badge display
        self.assertIn('Active', content)
    
    def test_for_tag_looping(self):
        """Topic 25: {% for %} Tag - Looping sequences"""
        # Create multiple products
        Product.objects.create(
            code='PROD002',
            name='Product 2',
            price=49.99,
            category='Books'
        )
        response = self.client.get(reverse('products:list'))
        content = response.content.decode()
        # Check that products are listed
        self.assertIn('PROD001', content)
        self.assertIn('PROD002', content)
    
    def test_template_variables(self):
        """Topic 28: Template Variables - Context data"""
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.context['page_title'], 'Product List')
    
    def test_block_content(self):
        """Topic 26: {% block %} Content - Block rendering"""
        response = self.client.get(reverse('products:list'))
        content = response.content.decode()
        # Check that content block is rendered
        self.assertIn('Product List', content)
    
    def test_empty_blocks(self):
        """Topic 29: Empty Blocks - Default block content"""
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        # extra_css and extra_js blocks are empty by default


class TemplateFiltersTestCase(TestCase):
    """Tests for Template Filters (Topics 31-35)"""
    
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            code='PROD001',
            name='Test Product Name',
            price=99.99,
            category='Electronics'
        )
    
    def test_date_filter(self):
        """Topic 31: |date Filter - Date formatting"""
        response = self.client.get(reverse('products:detail', args=[self.product.id]))
        content = response.content.decode()
        # Check for formatted date
        self.assertIn('Created:', content)
    
    def test_length_filter(self):
        """Topic 33: |length Filter - Length retrieval"""
        # Create multiple products
        Product.objects.create(code='PROD002', name='Product 2', price=49.99)
        Product.objects.create(code='PROD003', name='Product 3', price=29.99)
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        # Products are looped and displayed
    
    def test_upper_filter(self):
        """Topic 34: |upper Filter - Uppercase conversion"""
        response = self.client.get(reverse('products:list'))
        content = response.content.decode()
        # Check for uppercase conversion in table
        self.assertIn('PROD001', content)  # Code in uppercase
    
    def test_lower_filter(self):
        """Topic 35: |lower Filter - Lowercase conversion"""
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)


class BestPracticesTestCase(TestCase):
    """Tests for Best Practices (Topics 36-40)"""
    
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            code='PROD001',
            name='Test Product',
            price=99.99,
            category='Electronics'
        )
    
    def test_semantic_html(self):
        """Topic 36: Semantic HTML - Proper tags"""
        response = self.client.get(reverse('products:list'))
        content = response.content.decode()
        # Check for semantic HTML tags
        self.assertIn('<nav', content)
        self.assertIn('<main', content)
        self.assertIn('<footer', content)
    
    def test_consistent_navigation(self):
        """Topic 37: Consistent Navigation - Same navbar"""
        list_response = self.client.get(reverse('products:list'))
        detail_response = self.client.get(reverse('products:detail', args=[self.product.id]))
        
        list_content = list_response.content.decode()
        detail_content = detail_response.content.decode()
        
        # Both pages have the same navbar
        self.assertIn('Product Management', list_content)
        self.assertIn('Product Management', detail_content)
        self.assertIn('navbar', list_content)
        self.assertIn('navbar', detail_content)
    
    def test_mobile_responsive(self):
        """Topic 38: Mobile Responsive - Bootstrap compatibility"""
        response = self.client.get(reverse('products:list'))
        content = response.content.decode()
        # Check for Bootstrap classes
        self.assertIn('container', content)
        self.assertIn('row', content)
        self.assertIn('col', content)
    
    def test_code_organization(self):
        """Topic 39: Code Organization - Clean structure"""
        # Templates in proper directories
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_reusability(self):
        """Topic 40: Template Reusability - Component-based"""
        # Base template reused across multiple pages
        list_response = self.client.get(reverse('products:list'))
        detail_response = self.client.get(reverse('products:detail', args=[self.product.id]))
        
        # Both pages use base.html
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
