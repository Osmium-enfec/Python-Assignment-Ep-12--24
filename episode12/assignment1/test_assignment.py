"""
EPISODE 12 - ASSIGNMENT 1: Test Suite
Tests for form data processing
"""

import unittest
import json
from urllib.parse import urlencode
from http.server import HTTPServer
import threading
import time
import requests


class TestFormHandler(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Start the server in a background thread"""
        from solution import FormHandler
        
        cls.server = HTTPServer(('localhost', 8001), FormHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.5)  # Give server time to start
        cls.base_url = 'http://localhost:8001'
    
    @classmethod
    def tearDownClass(cls):
        """Shutdown the server"""
        cls.server.shutdown()
    
    def test_valid_registration(self):
        """Test valid registration form"""
        data = {
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'securepass123',
            'age': '25'
        }
        response = requests.post(f'{self.base_url}/register', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['data']['username'], 'johndoe')
    
    def test_invalid_username_short(self):
        """Test username too short"""
        data = {
            'username': 'ab',
            'email': 'john@example.com',
            'password': 'securepass123',
            'age': '25'
        }
        response = requests.post(f'{self.base_url}/register', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['status'], 'error')
        self.assertTrue(any('Username must be 3-20' in error for error in result['errors']))
    
    def test_invalid_username_long(self):
        """Test username too long"""
        data = {
            'username': 'a' * 21,
            'email': 'john@example.com',
            'password': 'securepass123',
            'age': '25'
        }
        response = requests.post(f'{self.base_url}/register', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(any('Username must be 3-20' in error for error in result['errors']))
    
    def test_invalid_email(self):
        """Test email without @"""
        data = {
            'username': 'johndoe',
            'email': 'johnexample.com',
            'password': 'securepass123',
            'age': '25'
        }
        response = requests.post(f'{self.base_url}/register', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(any('Email must contain @' in error for error in result['errors']))
    
    def test_invalid_password_short(self):
        """Test password too short"""
        data = {
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'short',
            'age': '25'
        }
        response = requests.post(f'{self.base_url}/register', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(any('Password must be at least 8' in error for error in result['errors']))
    
    def test_invalid_age_not_number(self):
        """Test age that's not a number"""
        data = {
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'securepass123',
            'age': 'twenty'
        }
        response = requests.post(f'{self.base_url}/register', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(any('Age must be a valid number' in error for error in result['errors']))
    
    def test_invalid_age_too_young(self):
        """Test age too young"""
        data = {
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'securepass123',
            'age': '10'
        }
        response = requests.post(f'{self.base_url}/register', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(any('Age must be between 13 and 120' in error for error in result['errors']))
    
    def test_invalid_age_too_old(self):
        """Test age too old"""
        data = {
            'username': 'johndoe',
            'email': 'john@example.com',
            'password': 'securepass123',
            'age': '150'
        }
        response = requests.post(f'{self.base_url}/register', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(any('Age must be between 13 and 120' in error for error in result['errors']))
    
    def test_missing_required_fields(self):
        """Test missing required fields"""
        data = {
            'username': 'johndoe',
            'email': 'john@example.com'
        }
        response = requests.post(f'{self.base_url}/register', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(result['errors']) >= 2)
    
    def test_endpoint_not_found(self):
        """Test accessing invalid endpoint"""
        response = requests.post(f'{self.base_url}/invalid')
        result = response.json()
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(result['status'], 'error')
    
    def test_utf8_encoding(self):
        """Test UTF-8 encoded form data"""
        data = {
            'username': 'señor',
            'email': 'test@example.com',
            'password': 'securepass123',
            'age': '25'
        }
        response = requests.post(f'{self.base_url}/register', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data']['username'], 'señor')


if __name__ == '__main__':
    # Install requests if not available
    try:
        import requests
    except ImportError:
        print("Installing requests library...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'requests'])
    
    unittest.main()
