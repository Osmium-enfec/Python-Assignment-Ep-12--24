"""
EPISODE 16 - ASSIGNMENT 2: MULTIPLE VIEWS - TESTS

Run with: python test_assignment.py
Tests verify your views and URL routing work correctly.
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.urls import resolve
from pathlib import Path
import json

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.http import HttpResponse, JsonResponse
from myproject import views


class ViewsExistTest(TestCase):
    """Test that all views are properly defined"""
    
    def test_home_view_exists(self):
        """Test home view is defined"""
        self.assertTrue(
            hasattr(views, 'home'),
            "home view not found in myproject/views.py"
        )
    
    def test_blog_list_view_exists(self):
        """Test blog_list view is defined"""
        self.assertTrue(
            hasattr(views, 'blog_list'),
            "blog_list view not found in myproject/views.py"
        )
    
    def test_blog_detail_view_exists(self):
        """Test blog_detail view is defined"""
        self.assertTrue(
            hasattr(views, 'blog_detail'),
            "blog_detail view not found in myproject/views.py"
        )
    
    def test_contact_view_exists(self):
        """Test contact view is defined"""
        self.assertTrue(
            hasattr(views, 'contact'),
            "contact view not found in myproject/views.py"
        )
    
    def test_api_response_view_exists(self):
        """Test api_response view is defined"""
        self.assertTrue(
            hasattr(views, 'api_response'),
            "api_response view not found in myproject/views.py"
        )


class ViewsReturnResponseTest(TestCase):
    """Test that views return proper response objects"""
    
    def test_home_returns_response(self):
        """Test home view returns HttpResponse"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/')
        
        response = views.home(request)
        self.assertIsNotNone(response)
        self.assertTrue(
            hasattr(response, 'content'),
            "home view should return an HTTP response"
        )
    
    def test_blog_list_returns_response(self):
        """Test blog_list view returns HttpResponse"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/blog/')
        
        response = views.blog_list(request)
        self.assertIsNotNone(response)
        self.assertTrue(
            hasattr(response, 'content'),
            "blog_list view should return an HTTP response"
        )
    
    def test_blog_detail_returns_response(self):
        """Test blog_detail view returns HttpResponse"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/blog/1/')
        
        response = views.blog_detail(request, 1)
        self.assertIsNotNone(response)
        self.assertTrue(
            hasattr(response, 'content'),
            "blog_detail view should return an HTTP response"
        )
    
    def test_contact_returns_response(self):
        """Test contact view returns HttpResponse"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/contact/')
        
        response = views.contact(request)
        self.assertIsNotNone(response)
        self.assertTrue(
            hasattr(response, 'content'),
            "contact view should return an HTTP response"
        )
    
    def test_api_response_returns_json(self):
        """Test api_response view returns JsonResponse"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/api/data/')
        
        response = views.api_response(request)
        self.assertIsNotNone(response)
        self.assertTrue(
            hasattr(response, 'content'),
            "api_response view should return a response"
        )


class URLRoutingTest(TestCase):
    """Test that URLs are properly configured"""
    
    def test_home_url_resolves(self):
        """Test that / URL resolves to home view"""
        try:
            match = resolve('/')
            self.assertEqual(
                match.func,
                views.home,
                "/ should route to home view"
            )
        except Exception as e:
            self.fail(f"/ URL does not resolve: {e}")
    
    def test_blog_list_url_resolves(self):
        """Test that /blog/ URL resolves to blog_list view"""
        try:
            match = resolve('/blog/')
            self.assertEqual(
                match.func,
                views.blog_list,
                "/blog/ should route to blog_list view"
            )
        except Exception as e:
            self.fail(f"/blog/ URL does not resolve: {e}")
    
    def test_blog_detail_url_resolves(self):
        """Test that /blog/<id>/ URL resolves with parameter"""
        try:
            match = resolve('/blog/1/')
            self.assertEqual(
                match.func,
                views.blog_detail,
                "/blog/<id>/ should route to blog_detail view"
            )
            self.assertEqual(
                match.kwargs.get('post_id'),
                1,
                "post_id parameter should be captured"
            )
        except Exception as e:
            self.fail(f"/blog/<id>/ URL does not resolve: {e}")
    
    def test_contact_url_resolves(self):
        """Test that /contact/ URL resolves to contact view"""
        try:
            match = resolve('/contact/')
            self.assertEqual(
                match.func,
                views.contact,
                "/contact/ should route to contact view"
            )
        except Exception as e:
            self.fail(f"/contact/ URL does not resolve: {e}")
    
    def test_api_url_resolves(self):
        """Test that /api/data/ URL resolves to api_response view"""
        try:
            match = resolve('/api/data/')
            self.assertEqual(
                match.func,
                views.api_response,
                "/api/data/ should route to api_response view"
            )
        except Exception as e:
            self.fail(f"/api/data/ URL does not resolve: {e}")


class IntegrationTest(TestCase):
    """Test complete request-response cycle"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
    
    def test_home_page_loads(self):
        """Test home page returns 200 status"""
        response = self.client.get('/')
        self.assertEqual(
            response.status_code,
            200,
            f"home page returned {response.status_code} instead of 200"
        )
    
    def test_blog_list_page_loads(self):
        """Test blog list page returns 200 status"""
        response = self.client.get('/blog/')
        self.assertEqual(
            response.status_code,
            200,
            f"blog list page returned {response.status_code} instead of 200"
        )
    
    def test_blog_detail_page_loads(self):
        """Test blog detail page returns 200 status"""
        response = self.client.get('/blog/1/')
        self.assertEqual(
            response.status_code,
            200,
            f"blog detail page returned {response.status_code} instead of 200"
        )
    
    def test_contact_page_loads(self):
        """Test contact page returns 200 status"""
        response = self.client.get('/contact/')
        self.assertEqual(
            response.status_code,
            200,
            f"contact page returned {response.status_code} instead of 200"
        )
    
    def test_api_endpoint_works(self):
        """Test API endpoint returns 200 status"""
        response = self.client.get('/api/data/')
        self.assertEqual(
            response.status_code,
            200,
            f"API endpoint returned {response.status_code} instead of 200"
        )
    
    def test_api_returns_json(self):
        """Test API endpoint returns valid JSON"""
        response = self.client.get('/api/data/')
        try:
            data = json.loads(response.content)
            self.assertIsInstance(data, dict)
        except json.JSONDecodeError:
            self.fail("API endpoint should return valid JSON")


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
