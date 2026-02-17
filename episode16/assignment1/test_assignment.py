"""
EPISODE 16 - ASSIGNMENT 1: DJANGO VIEWS - TESTS

Run with: python test_assignment.py
Tests verify your views and URL routing work correctly.
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.urls import resolve
from pathlib import Path

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.http import HttpResponse
from myproject import views


class ViewsExistTest(TestCase):
    """Test that views are properly defined"""
    
    def test_welcome_view_exists(self):
        """Test welcome view is defined"""
        self.assertTrue(
            hasattr(views, 'welcome'),
            "welcome view not found in myproject/views.py"
        )
    
    def test_about_view_exists(self):
        """Test about view is defined"""
        self.assertTrue(
            hasattr(views, 'about'),
            "about view not found in myproject/views.py"
        )
    
    def test_welcome_is_callable(self):
        """Test welcome view is callable"""
        self.assertTrue(
            callable(views.welcome),
            "welcome is not callable"
        )
    
    def test_about_is_callable(self):
        """Test about view is callable"""
        self.assertTrue(
            callable(views.about),
            "about is not callable"
        )


class ViewsReturnResponseTest(TestCase):
    """Test that views return proper HttpResponse objects"""
    
    def test_welcome_returns_response(self):
        """Test welcome view returns HttpResponse"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/')
        
        response = views.welcome(request)
        self.assertIsInstance(
            response,
            HttpResponse,
            "welcome view should return HttpResponse"
        )
    
    def test_about_returns_response(self):
        """Test about view returns HttpResponse"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/about/')
        
        response = views.about(request)
        self.assertIsInstance(
            response,
            HttpResponse,
            "about view should return HttpResponse"
        )
    
    def test_welcome_has_content(self):
        """Test welcome view returns non-empty content"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/')
        
        response = views.welcome(request)
        self.assertGreater(
            len(response.content),
            0,
            "welcome view should return content"
        )
    
    def test_about_has_content(self):
        """Test about view returns non-empty content"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/about/')
        
        response = views.about(request)
        self.assertGreater(
            len(response.content),
            0,
            "about view should return content"
        )


class URLRoutingTest(TestCase):
    """Test that URLs are properly configured"""
    
    def test_root_url_resolves(self):
        """Test that / URL resolves to welcome view"""
        try:
            match = resolve('/')
            self.assertEqual(
                match.func,
                views.welcome,
                "/ should route to welcome view"
            )
        except Exception as e:
            self.fail(f"/ URL does not resolve: {e}")
    
    def test_about_url_resolves(self):
        """Test that /about/ URL resolves to about view"""
        try:
            match = resolve('/about/')
            self.assertEqual(
                match.func,
                views.about,
                "/about/ should route to about view"
            )
        except Exception as e:
            self.fail(f"/about/ URL does not resolve: {e}")


class IntegrationTest(TestCase):
    """Test complete request-response cycle"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_welcome_page_loads(self):
        """Test welcome page returns 200 status"""
        response = self.client.get('/')
        self.assertEqual(
            response.status_code,
            200,
            f"welcome page returned {response.status_code} instead of 200"
        )
    
    def test_about_page_loads(self):
        """Test about page returns 200 status"""
        response = self.client.get('/about/')
        self.assertEqual(
            response.status_code,
            200,
            f"about page returned {response.status_code} instead of 200"
        )
    
    def test_welcome_page_has_html(self):
        """Test welcome page returns HTML content"""
        response = self.client.get('/')
        content = response.content.decode()
        self.assertGreater(
            len(content),
            0,
            "welcome page has no content"
        )
        # Should have some HTML tags
        self.assertTrue(
            '<' in content and '>' in content,
            "welcome page should contain HTML"
        )


if __name__ == '__main__':
    import unittest
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(ViewsExistTest))
    suite.addTests(loader.loadTestsFromTestCase(ViewsReturnResponseTest))
    suite.addTests(loader.loadTestsFromTestCase(URLRoutingTest))
    suite.addTests(loader.loadTestsFromTestCase(IntegrationTest))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
