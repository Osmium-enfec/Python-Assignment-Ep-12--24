"""
EPISODE 13 - ASSIGNMENT 2: Test Suite
Tests for routing, redirects, templates, and PRG pattern
"""

import unittest
import json
import os
import socket
from urllib.parse import urlencode
from http.server import ThreadingHTTPServer
import threading
import time
import requests
from solution import ServerHandler
import stores
import page


# Custom server class that allows address reuse
class ReuseAddrHTTPServer(ThreadingHTTPServer):
    allow_reuse_address = True


class TestPageTemplates(unittest.TestCase):
    """Test HTML template rendering"""
    
    def test_render_home_no_students(self):
        """Test home page with no students"""
        stats = {
            'total_students': 0,
            'average_grade': 0,
            'pass_rate': 0
        }
        html = page.render_home([], stats)
        
        self.assertIn('Dashboard', html)
        self.assertIn('0', html)
    
    def test_render_home_with_students(self):
        """Test home page with students"""
        students = [
            {'id': 101, 'name': 'John', 'grade': 85},
            {'id': 102, 'name': 'Jane', 'grade': 92}
        ]
        stats = {
            'total_students': 2,
            'average_grade': 88.5,
            'pass_rate': 100.0
        }
        html = page.render_home(students, stats)
        
        self.assertIn('2', html)
        self.assertIn('88.50', html)
        self.assertIn('100.0%', html)
    
    def test_render_add_form(self):
        """Test add form rendering"""
        html = page.render_add_form()
        
        self.assertIn('Add Student', html)
        self.assertIn('form', html)
        self.assertIn('POST', html)
        self.assertIn('/add', html)
    
    def test_render_student_list(self):
        """Test student list rendering"""
        students = [
            {'id': 101, 'name': 'John', 'grade': 85}
        ]
        html = page.render_student_list(students)
        
        self.assertIn('101', html)
        self.assertIn('John', html)
        self.assertIn('85', html)
    
    def test_base_template_includes_nav(self):
        """Test base template has navigation"""
        html = page.render_base('Test', 'Content')
        
        self.assertIn('Dashboard', html)
        self.assertIn('Students', html)
        self.assertIn('Add Student', html)


class TestStatistics(unittest.TestCase):
    """Test statistics calculation"""
    
    def test_calculate_stats_empty(self):
        """Test stats with no students"""
        from solution import ServerHandler
        
        handler = ServerHandler.__new__(ServerHandler)
        stats = handler._calculate_statistics([])
        
        self.assertEqual(stats['total_students'], 0)
        self.assertEqual(stats['average_grade'], 0)
        self.assertEqual(stats['pass_rate'], 0)
    
    def test_calculate_stats_with_students(self):
        """Test stats calculation"""
        from solution import ServerHandler
        
        students = [
            {'id': 101, 'name': 'John', 'grade': 60},  # Pass
            {'id': 102, 'name': 'Jane', 'grade': 90},  # Pass
            {'id': 103, 'name': 'Bob', 'grade': 50}    # Fail
        ]
        
        handler = ServerHandler.__new__(ServerHandler)
        stats = handler._calculate_statistics(students)
        
        self.assertEqual(stats['total_students'], 3)
        self.assertAlmostEqual(stats['average_grade'], 66.67, places=1)
        self.assertAlmostEqual(stats['pass_rate'], 66.67, places=1)


class TestServerHandler(unittest.TestCase):
    """Test server routing and PRG pattern"""
    
    @classmethod
    def setUpClass(cls):
        """Start server"""
        cls.server = ReuseAddrHTTPServer(('localhost', 8008), ServerHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.5)
        
        cls.base_url = 'http://localhost:8008'
        cls.session = requests.Session()
    
    @classmethod
    def tearDownClass(cls):
        """Shutdown server"""
        cls.server.shutdown()
    
    def setUp(self):
        """Clear data"""
        from solution import STUDENTS, FLASH_MESSAGES
        stores.delete_file()
        STUDENTS.clear()
        FLASH_MESSAGES.clear()
        self.session.cookies.clear()
    
    def tearDown(self):
        """Clean up"""
        from solution import STUDENTS, FLASH_MESSAGES
        stores.delete_file()
        STUDENTS.clear()
        FLASH_MESSAGES.clear()
    
    def test_home_page_loads(self):
        """Test home page loads"""
        response = self.session.get(f'{self.base_url}/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Dashboard', response.text)
        self.assertIn('Total Students', response.text)
    
    def test_student_list_page(self):
        """Test student list page"""
        response = self.session.get(f'{self.base_url}/students')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Students', response.text)
    
    def test_add_form_page(self):
        """Test add form page"""
        response = self.session.get(f'{self.base_url}/add')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Add Student', response.text)
        self.assertIn('form', response.text)
    
    def test_add_student_post_redirect(self):
        """Test POST /add redirects (PRG pattern)"""
        data = {
            'id': '101',
            'name': 'John Doe',
            'grade': '85'
        }
        response = self.session.post(
            f'{self.base_url}/add',
            data=urlencode(data),
            allow_redirects=False
        )
        
        # Should redirect with 302
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/students')
    
    def test_add_student_persists(self):
        """Test student is persisted after add"""
        data = {
            'id': '101',
            'name': 'John Doe',
            'grade': '85'
        }
        self.session.post(f'{self.base_url}/add', data=urlencode(data))
        
        # Check file
        self.assertTrue(os.path.exists('students_dashboard.json'))
        loaded = stores.load_students()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]['name'], 'John Doe')
    
    def test_edit_student_post_redirect(self):
        """Test POST /edit redirects"""
        # Add first
        data = {
            'id': '101',
            'name': 'John',
            'grade': '85'
        }
        self.session.post(f'{self.base_url}/add', data=urlencode(data))
        
        # Edit
        edit_data = {
            'id': '101',
            'name': 'Jane',
            'grade': '90'
        }
        response = self.session.post(
            f'{self.base_url}/edit',
            data=urlencode(edit_data),
            allow_redirects=False
        )
        
        self.assertEqual(response.status_code, 302)
    
    def test_delete_student(self):
        """Test student deletion"""
        # Add first
        data = {
            'id': '101',
            'name': 'John',
            'grade': '85'
        }
        self.session.post(f'{self.base_url}/add', data=urlencode(data))
        
        # Delete
        response = self.session.get(
            f'{self.base_url}/delete?id=101',
            allow_redirects=False
        )
        
        self.assertEqual(response.status_code, 302)
        
        # Verify deleted
        loaded = stores.load_students()
        self.assertEqual(len(loaded), 0)
    
    def test_invalid_page_404(self):
        """Test invalid page returns 404"""
        response = self.session.get(f'{self.base_url}/invalid')
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('Error', response.text)
    
    def test_statistics_update(self):
        """Test statistics update on home page"""
        # Add student
        data = {
            'id': '101',
            'name': 'John',
            'grade': '85'
        }
        self.session.post(f'{self.base_url}/add', data=urlencode(data))
        
        # Check home page
        response = self.session.get(f'{self.base_url}/')
        
        self.assertIn('1', response.text)  # Total students
        # Look for average (could be 85.00)
        self.assertTrue('85' in response.text)


if __name__ == '__main__':
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'requests', '-q'])
    
    unittest.main()
