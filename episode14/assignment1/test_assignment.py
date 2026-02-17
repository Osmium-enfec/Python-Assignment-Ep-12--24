"""
EPISODE 14 - ASSIGNMENT 1: Test Suite
Tests for template system and XSS security
"""

import unittest
import os
import sys
from http.server import HTTPServer
import threading
import time
import requests
from urllib.parse import urlencode

# Import solution
from solution import read_template, html_escape, render_template, TemplateHandler, BASE_DIR, get_templates_dir


class TestPathHandling(unittest.TestCase):
    """Test file path handling with os.path"""
    
    def test_base_dir_exists(self):
        """Test BASE_DIR points to valid directory"""
        self.assertTrue(os.path.isdir(BASE_DIR))
    
    def test_templates_dir_exists(self):
        """Test templates directory exists"""
        templates_dir = get_templates_dir()
        self.assertTrue(os.path.isdir(templates_dir))
    
    def test_template_files_exist(self):
        """Test template files exist"""
        templates = ['layout.html', 'message.html', 'user.html']
        templates_dir = get_templates_dir()
        
        for template in templates:
            path = os.path.join(templates_dir, template)
            self.assertTrue(os.path.exists(path))


class TestTemplateLoading(unittest.TestCase):
    """Test read_template function"""
    
    def test_read_existing_template(self):
        """Test reading existing template"""
        content = read_template('message.html')
        
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)
        self.assertIn('{{message}}', content)
    
    def test_read_layout_template(self):
        """Test reading layout template"""
        content = read_template('layout.html')
        
        self.assertIn('{{content}}', content)
        self.assertIn('<!DOCTYPE html>', content)
    
    def test_template_not_found(self):
        """Test FileNotFoundError for missing template"""
        with self.assertRaises(FileNotFoundError):
            read_template('nonexistent.html')


class TestHtmlEscaping(unittest.TestCase):
    """Test HTML escape function for XSS prevention"""
    
    def test_escape_ampersand(self):
        """Test & is escaped first"""
        result = html_escape('&')
        self.assertEqual(result, '&amp;')
    
    def test_escape_less_than(self):
        """Test < is escaped"""
        result = html_escape('<')
        self.assertEqual(result, '&lt;')
    
    def test_escape_greater_than(self):
        """Test > is escaped"""
        result = html_escape('>')
        self.assertEqual(result, '&gt;')
    
    def test_escape_quote(self):
        """Test \" is escaped"""
        result = html_escape('"')
        self.assertEqual(result, '&quot;')
    
    def test_escape_script_tag(self):
        """Test script tag is escaped (XSS prevention)"""
        result = html_escape('<script>alert("XSS")</script>')
        
        self.assertNotIn('<script>', result)
        self.assertNotIn('</script>', result)
        self.assertIn('&lt;script&gt;', result)
        self.assertIn('&lt;/script&gt;', result)
    
    def test_escape_ampersand_first(self):
        """Test & is escaped before other entities"""
        result = html_escape('&<>')
        # Should be &amp;&lt;&gt;, not &amp;amp;...
        self.assertEqual(result, '&amp;&lt;&gt;')
    
    def test_escape_none_value(self):
        """Test None is converted to empty string"""
        result = html_escape(None)
        self.assertEqual(result, '')
    
    def test_escape_integer(self):
        """Test integer is converted and escaped"""
        result = html_escape(42)
        self.assertEqual(result, '42')
    
    def test_escape_boolean(self):
        """Test boolean is converted"""
        result_true = html_escape(True)
        result_false = html_escape(False)
        
        self.assertEqual(result_true, 'True')
        self.assertEqual(result_false, 'False')
    
    def test_escape_safe_string(self):
        """Test safe strings pass through"""
        result = html_escape('Hello World')
        self.assertEqual(result, 'Hello World')


class TestTemplateRendering(unittest.TestCase):
    """Test render_template function"""
    
    def test_render_simple_template(self):
        """Test rendering with simple substitution"""
        result = render_template('message.html', message='Hello')
        
        self.assertIn('Hello', result)
        self.assertNotIn('{{message}}', result)
    
    def test_render_with_escaping(self):
        """Test rendering escapes values"""
        result = render_template('message.html', message='<script>alert("XSS")</script>')
        
        self.assertNotIn('<script>', result)
        self.assertIn('&lt;script&gt;', result)
    
    def test_render_layout(self):
        """Test rendering layout template"""
        # When using layout.html with pre-rendered content, use __raw_content
        # to prevent double-escaping
        result = render_template('layout.html', __raw_content='<p>Test</p>')
        
        self.assertIn('<!DOCTYPE html>', result)
        self.assertIn('<p>Test</p>', result)
        self.assertNotIn('{{content}}', result)
    
    def test_render_user_template(self):
        """Test rendering user template"""
        result = render_template('user.html', username='Alice')
        
        self.assertIn('Welcome, Alice!', result)
        self.assertNotIn('{{username}}', result)
    
    def test_render_with_none_value(self):
        """Test rendering with None value"""
        result = render_template('message.html', message=None)
        
        self.assertNotIn('{{message}}', result)
        # Should have empty content where placeholder was
        self.assertIn('<p></p>', result)
    
    def test_render_multiple_placeholders(self):
        """Test rendering with multiple placeholders"""
        # Create test template content
        template_content = 'Name: {{name}}, Age: {{age}}'
        
        # Manually test rendering logic
        result = template_content
        result = result.replace('{{name}}', html_escape('Bob'))
        result = result.replace('{{age}}', html_escape('25'))
        
        self.assertEqual(result, 'Name: Bob, Age: 25')
    
    def test_render_xss_attack_blocked(self):
        """Test XSS attack is blocked"""
        xss_payload = '<img src=x onerror="alert(\'XSS\')">'
        result = render_template('message.html', message=xss_payload)
        
        # Should not contain unescaped tags
        self.assertNotIn('<img src=x', result)
        self.assertIn('&lt;img', result)


class TestTemplateHTTPServer(unittest.TestCase):
    """Test HTTP server with template rendering"""
    
    @classmethod
    def setUpClass(cls):
        """Start server"""
        cls.server = HTTPServer(('localhost', 8010), TemplateHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.5)
        cls.base_url = 'http://localhost:8010'
    
    @classmethod
    def tearDownClass(cls):
        """Shutdown server"""
        cls.server.shutdown()
    
    def test_home_page(self):
        """Test home page loads"""
        response = requests.get(f'{self.base_url}/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to the Template Engine', response.text)
        self.assertIn('<!DOCTYPE html>', response.text)
    
    def test_user_page(self):
        """Test user page"""
        response = requests.get(f'{self.base_url}/user')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome, Guest!', response.text)
    
    def test_xss_test_page(self):
        """Test XSS test page"""
        response = requests.get(f'{self.base_url}/test-xss')
        
        self.assertEqual(response.status_code, 200)
        # XSS payload should be escaped
        self.assertNotIn('<script>alert', response.text)
        self.assertIn('&lt;script&gt;', response.text)
    
    def test_post_with_safe_message(self):
        """Test POST with safe message"""
        data = {'message': 'Hello World'}
        response = requests.post(f'{self.base_url}/render', data=urlencode(data))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello World', response.text)
    
    def test_post_with_xss_attack(self):
        """Test POST with XSS attack payload"""
        data = {'message': '<script>alert("XSS")</script>'}
        response = requests.post(f'{self.base_url}/render', data=urlencode(data))
        
        self.assertEqual(response.status_code, 200)
        # XSS should be escaped
        self.assertNotIn('<script>', response.text)
        self.assertIn('&lt;script&gt;', response.text)
    
    def test_post_with_html_tags(self):
        """Test POST with HTML tags"""
        data = {'message': '<b>Bold</b>'}
        response = requests.post(f'{self.base_url}/render', data=urlencode(data))
        
        self.assertEqual(response.status_code, 200)
        # HTML should be escaped
        self.assertNotIn('<b>Bold</b>', response.text)
        self.assertIn('&lt;b&gt;Bold&lt;/b&gt;', response.text)
    
    def test_post_with_sql_injection(self):
        """Test POST with SQL injection attempt"""
        data = {'message': "'; DROP TABLE students; --"}
        response = requests.post(f'{self.base_url}/render', data=urlencode(data))
        
        self.assertEqual(response.status_code, 200)
        # The SQL injection should be safely rendered as text
        # Single quotes pass through (HTML doesn't require escaping them)
        # but it's displayed as text, not executed
        self.assertIn("DROP TABLE students", response.text)
    
    def test_404_not_found(self):
        """Test 404 for invalid path"""
        response = requests.get(f'{self.base_url}/invalid')
        
        self.assertEqual(response.status_code, 404)
    
    def test_html_special_chars_in_response(self):
        """Test HTML special characters in rendered output"""
        data = {'message': 'A&B<C>D"E'}
        response = requests.post(f'{self.base_url}/render', data=urlencode(data))
        
        self.assertEqual(response.status_code, 200)
        # All special chars should be escaped
        self.assertIn('A&amp;B&lt;C&gt;D&quot;E', response.text)


if __name__ == '__main__':
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'requests', '-q'])
    
    unittest.main()
