"""
EPISODE 12 - ASSIGNMENT 2: Cookie Management & Session System

TOPICS COVERED:
- Cookie Fundamentals
- Cookie Management with http.cookies
- Cookie Expiration and Clearing
- Flash Messaging System
- Session Management
- Advanced URL Parsing and Validation
- Path Parameter Extraction
- State Management Across Requests

ASSIGNMENT:
Create a simple session-based authentication system with the following features:

ENDPOINTS:
1. GET /                      - Show login page with flash messages
2. POST /login                - Login handler (creates session + cookie)
3. GET /profile               - Show user profile (requires session)
4. GET /logout                - Logout handler (clears session cookie)
5. GET /messages              - Flash messaging system demonstration

REQUIREMENTS:
1. Implement a simple session store (dictionary with user data)
2. Create cookies with session IDs
3. Implement flash message system (one-time display)
4. Parse URLs correctly to identify endpoints
5. Validate session cookies and user sessions
6. Handle cookie expiration
7. Demonstrate cookie clearing on logout

FEATURES:
- Simple username/password authentication
- Session persistence via cookies
- Flash messages (success, error)
- Protected endpoints requiring authentication
- Clean session management on logout
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from http.cookies import SimpleCookie
import json
import uuid
from datetime import datetime

# Simple in-memory session store
SESSIONS = {}
FLASH_MESSAGES = {}


class SessionHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        """Handle GET requests"""
        # TODO: Parse URL and route to appropriate handler
        # Parse the path
        # 1. If path == '/' -> render login page
        # 2. If path == '/profile' -> check session and render profile
        # 3. If path == '/logout' -> clear session
        # 4. Otherwise -> 404
        pass
    
    def do_POST(self):
        """Handle POST requests"""
        # TODO: Implement POST handlers
        # 1. If path == '/login' -> authenticate and create session
        pass
    
    def _parse_path(self):
        """
        Parse the URL path
        
        TODO: Implement path parsing
        Returns the path without query string
        """
        pass
    
    def _get_session_from_cookie(self):
        """
        Extract session ID from cookie
        
        TODO: Implement cookie reading
        1. Get Cookie header
        2. Parse with SimpleCookie
        3. Extract session_id value
        4. Return session_id or None
        """
        pass
    
    def _create_session(self, username):
        """
        Create a new session
        
        TODO: Implement session creation
        1. Generate unique session ID (use uuid)
        2. Store user data in SESSIONS dict
        3. Return session_id
        """
        pass
    
    def _set_session_cookie(self, session_id):
        """
        Set session cookie in response
        
        TODO: Implement cookie setting
        1. Create SimpleCookie
        2. Set 'session_id' cookie value
        3. Set cookie attributes (max-age, path, httponly)
        4. Return Set-Cookie header value
        """
        pass
    
    def _clear_session_cookie(self):
        """
        Clear session cookie
        
        TODO: Implement cookie clearing
        1. Create SimpleCookie
        2. Set 'session_id' to empty
        3. Set max-age to 0
        4. Return Set-Cookie header value
        """
        pass
    
    def _set_flash_message(self, session_id, message_type, message):
        """
        Set a flash message for next request
        
        TODO: Store flash message in FLASH_MESSAGES
        message_type: 'success', 'error', 'info'
        """
        pass
    
    def _get_and_clear_flash_message(self, session_id):
        """
        Get flash message and remove it
        
        TODO: Get flash message from FLASH_MESSAGES and delete it
        """
        pass
    
    def _render_html(self, content):
        """Send HTML response"""
        # TODO: Implement HTML response
        pass
    
    def _render_json(self, data, status_code=200):
        """Send JSON response"""
        # TODO: Implement JSON response
        pass
    
    def _read_form(self):
        """Read POST form data"""
        # TODO: Implement form reading (similar to assignment 1)
        pass


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8002), SessionHandler)
    print("Server running on http://localhost:8002")
    print("\nTest the following:")
    print("1. http://localhost:8002/               - Login page")
    print("2. http://localhost:8002/profile        - Protected page (should redirect to login)")
    print("3. POST to /login with username=test&password=test")
    print("4. http://localhost:8002/logout         - Logout")
    server.serve_forever()
