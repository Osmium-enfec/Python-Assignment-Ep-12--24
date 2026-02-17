"""
EPISODE 12 - ASSIGNMENT 2: Test Suite
Tests for session-based authentication with cookies
"""

import unittest
from urllib.parse import urlencode
from http.server import HTTPServer
import threading
import time
import requests


class TestSessionHandler(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Start the server in a background thread"""
        from solution import SessionHandler, SESSIONS, FLASH_MESSAGES
        
        # Clear any existing sessions
        SESSIONS.clear()
        FLASH_MESSAGES.clear()
        
        cls.server = HTTPServer(('localhost', 8003), SessionHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.5)
        cls.base_url = 'http://localhost:8003'
        cls.session = requests.Session()
    
    def tearDown(self):
        """Clear sessions after each test"""
        from solution import SESSIONS, FLASH_MESSAGES
        SESSIONS.clear()
        FLASH_MESSAGES.clear()
        self.session.cookies.clear()
    
    @classmethod
    def tearDownClass(cls):
        """Shutdown the server"""
        cls.server.shutdown()
    
    def test_login_page_loads(self):
        """Test login page loads successfully"""
        response = self.session.get(f'{self.base_url}/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login', response.text)
        self.assertIn('Username', response.text)
    
    def test_profile_redirect_without_session(self):
        """Test accessing profile without session redirects to login"""
        response = self.session.get(f'{self.base_url}/profile', allow_redirects=False)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/')
    
    def test_successful_login(self):
        """Test successful login"""
        data = {
            'username': 'admin',
            'password': 'password123'
        }
        response = self.session.post(f'{self.base_url}/login', data=urlencode(data), allow_redirects=False)
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('Set-Cookie', response.headers)
        self.assertIn('session_id', response.headers['Set-Cookie'])
    
    def test_failed_login(self):
        """Test failed login"""
        data = {
            'username': 'admin',
            'password': 'wrongpassword'
        }
        response = self.session.post(f'{self.base_url}/login', data=urlencode(data), allow_redirects=False)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/')
    
    def test_session_persistence(self):
        """Test session persists across requests"""
        # Login
        data = {
            'username': 'admin',
            'password': 'password123'
        }
        login_response = self.session.post(f'{self.base_url}/login', data=urlencode(data))
        
        # Access profile
        profile_response = self.session.get(f'{self.base_url}/profile')
        
        self.assertEqual(profile_response.status_code, 200)
        self.assertIn('Welcome, admin!', profile_response.text)
    
    def test_profile_shows_user_info(self):
        """Test profile page shows correct user information"""
        # Login
        data = {
            'username': 'admin',
            'password': 'password123'
        }
        self.session.post(f'{self.base_url}/login', data=urlencode(data))
        
        # Access profile
        response = self.session.get(f'{self.base_url}/profile')
        
        self.assertIn('admin', response.text)
        self.assertIn('Profile Information', response.text)
        self.assertIn('Session ID', response.text)
    
    def test_logout_clears_session(self):
        """Test logout clears session"""
        # Login
        data = {
            'username': 'admin',
            'password': 'password123'
        }
        self.session.post(f'{self.base_url}/login', data=urlencode(data))
        
        # Logout
        logout_response = self.session.get(f'{self.base_url}/logout', allow_redirects=False)
        
        self.assertEqual(logout_response.status_code, 302)
        self.assertIn('Set-Cookie', logout_response.headers)
        
        # Try to access profile - should redirect
        profile_response = self.session.get(f'{self.base_url}/profile', allow_redirects=False)
        self.assertEqual(profile_response.status_code, 302)
    
    def test_invalid_endpoint(self):
        """Test accessing invalid endpoint"""
        response = self.session.get(f'{self.base_url}/invalid')
        
        self.assertEqual(response.status_code, 404)
    
    def test_login_page_redirect_when_authenticated(self):
        """Test login page redirects to profile when already authenticated"""
        # Login
        data = {
            'username': 'admin',
            'password': 'password123'
        }
        self.session.post(f'{self.base_url}/login', data=urlencode(data))
        
        # Visit login page
        response = self.session.get(f'{self.base_url}/', allow_redirects=False)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/profile')
    
    def test_cookie_has_security_attributes(self):
        """Test session cookie has proper security attributes"""
        data = {
            'username': 'admin',
            'password': 'password123'
        }
        response = self.session.post(f'{self.base_url}/login', data=urlencode(data), allow_redirects=False)
        
        cookie_header = response.headers['Set-Cookie']
        self.assertIn('httponly', cookie_header.lower())
        self.assertIn('path', cookie_header.lower())


if __name__ == '__main__':
    try:
        import requests
    except ImportError:
        print("Installing requests library...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'requests'])
    
    unittest.main()
