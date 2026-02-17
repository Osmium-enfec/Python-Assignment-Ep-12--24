"""
EPISODE 12 - ASSIGNMENT 2: Solution
Complete implementation of session-based authentication with cookies
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
        path = self._parse_path()
        
        if path == '/':
            self._handle_login_page()
        elif path == '/profile':
            self._handle_profile()
        elif path == '/logout':
            self._handle_logout()
        elif path == '/messages':
            self._handle_messages()
        else:
            self._render_json({'status': 'error', 'message': 'Not found'}, 404)
    
    def do_POST(self):
        """Handle POST requests"""
        path = self._parse_path()
        
        if path == '/login':
            self._handle_login_post()
        else:
            self._render_json({'status': 'error', 'message': 'Not found'}, 404)
    
    def _parse_path(self):
        """Parse URL path without query string"""
        parsed = urlparse(self.path)
        return parsed.path
    
    def _get_session_from_cookie(self):
        """Extract session ID from cookie"""
        cookie_header = self.headers.get('Cookie', '')
        
        if not cookie_header:
            return None
        
        cookies = SimpleCookie()
        try:
            cookies.load(cookie_header)
            session_id = cookies.get('session_id')
            if session_id:
                return session_id.value
        except Exception:
            pass
        
        return None
    
    def _create_session(self, username):
        """Create a new session"""
        session_id = str(uuid.uuid4())
        SESSIONS[session_id] = {
            'username': username,
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat()
        }
        return session_id
    
    def _set_session_cookie(self, session_id):
        """Set session cookie"""
        cookie = SimpleCookie()
        cookie['session_id'] = session_id
        cookie['session_id']['path'] = '/'
        cookie['session_id']['max-age'] = 3600  # 1 hour
        cookie['session_id']['httponly'] = True
        return cookie['session_id'].OutputString()
    
    def _clear_session_cookie(self):
        """Clear session cookie"""
        cookie = SimpleCookie()
        cookie['session_id'] = ''
        cookie['session_id']['path'] = '/'
        cookie['session_id']['max-age'] = 0
        return cookie['session_id'].OutputString()
    
    def _set_flash_message(self, session_id, message_type, message):
        """Set a flash message"""
        if session_id not in FLASH_MESSAGES:
            FLASH_MESSAGES[session_id] = []
        FLASH_MESSAGES[session_id].append({
            'type': message_type,
            'message': message
        })
    
    def _get_and_clear_flash_message(self, session_id):
        """Get and remove flash message"""
        if session_id in FLASH_MESSAGES and FLASH_MESSAGES[session_id]:
            message = FLASH_MESSAGES[session_id].pop(0)
            if not FLASH_MESSAGES[session_id]:
                del FLASH_MESSAGES[session_id]
            return message
        return None
    
    def _handle_login_page(self):
        """Show login page with flash messages"""
        session_id = self._get_session_from_cookie()
        
        # If already logged in, redirect to profile
        if session_id and session_id in SESSIONS:
            self.send_response(302)
            self.send_header('Location', '/profile')
            self.end_headers()
            return
        
        # Get flash messages if any
        flash = self._get_and_clear_flash_message(session_id) if session_id else None
        flash_html = ''
        
        if flash:
            flash_html = f'''
            <div class="alert alert-{flash['type']}">
                {flash['message']}
            </div>
            '''
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; }}
                form {{ max-width: 300px; }}
                input {{ display: block; margin: 10px 0; padding: 5px; width: 100%; }}
                button {{ padding: 8px 15px; cursor: pointer; }}
                .alert {{ padding: 10px; margin: 10px 0; border-radius: 4px; }}
                .alert-success {{ background: #d4edda; color: #155724; }}
                .alert-error {{ background: #f8d7da; color: #721c24; }}
            </style>
        </head>
        <body>
            <h1>Login</h1>
            {flash_html}
            <form method="POST" action="/login">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <p>Test user: username=<strong>admin</strong>, password=<strong>password123</strong></p>
        </body>
        </html>
        '''
        self._render_html(html)
    
    def _handle_profile(self):
        """Show user profile (requires authentication)"""
        session_id = self._get_session_from_cookie()
        
        if not session_id or session_id not in SESSIONS:
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
            return
        
        session = SESSIONS[session_id]
        username = session['username']
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Profile</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 50px; }}
                .profile {{ border: 1px solid #ddd; padding: 20px; max-width: 400px; }}
                a {{ display: inline-block; margin-top: 15px; padding: 8px 15px; background: #dc3545; color: white; text-decoration: none; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <h1>Welcome, {username}!</h1>
            <div class="profile">
                <h2>Profile Information</h2>
                <p><strong>Username:</strong> {username}</p>
                <p><strong>Session ID:</strong> {session_id[:8]}...</p>
                <p><strong>Created:</strong> {session['created_at']}</p>
                <a href="/logout">Logout</a>
            </div>
        </body>
        </html>
        '''
        self._render_html(html)
    
    def _handle_logout(self):
        """Handle logout"""
        session_id = self._get_session_from_cookie()
        
        if session_id and session_id in SESSIONS:
            del SESSIONS[session_id]
        
        self.send_response(302)
        self.send_header('Location', '/')
        self.send_header('Set-Cookie', self._clear_session_cookie())
        self.end_headers()
    
    def _handle_messages(self):
        """Demonstrate flash messaging"""
        session_id = self._get_session_from_cookie()
        
        if session_id and session_id in SESSIONS:
            # Set a flash message
            self._set_flash_message(session_id, 'success', 'This is a flash message! It will show once.')
        
        self.send_response(302)
        self.send_header('Location', '/profile')
        self.end_headers()
    
    def _handle_login_post(self):
        """Handle login POST request"""
        form_data = self._read_form()
        
        username = form_data.get('username', '')
        password = form_data.get('password', '')
        
        # Simple authentication (hardcoded for demo)
        if username == 'admin' and password == 'password123':
            # Create session
            session_id = self._create_session(username)
            
            # Redirect with session cookie
            self.send_response(302)
            self.send_header('Location', '/profile')
            self.send_header('Set-Cookie', self._set_session_cookie(session_id))
            self.end_headers()
        else:
            # Failed login
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
    
    def _render_html(self, content):
        """Send HTML response"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def _render_json(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def _read_form(self):
        """Read POST form data"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        body_string = body.decode('utf-8')
        parsed = parse_qs(body_string)
        return {k: v[0] for k, v in parsed.items()}
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8002), SessionHandler)
    print("Server running on http://localhost:8002")
    print("\nTest the following:")
    print("1. http://localhost:8002/               - Login page")
    print("2. http://localhost:8002/profile        - Protected page (redirects to login)")
    print("3. Login with username: admin, password: password123")
    print("4. http://localhost:8002/logout         - Logout")
    print("5. http://localhost:8002/messages       - Test flash messages")
    print("\nDefault credentials:")
    print("  Username: admin")
    print("  Password: password123")
    server.serve_forever()
