"""
EPISODE 12 - ASSIGNMENT 1: Solution
Complete implementation of form data processing
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json

class FormHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/register':
            try:
                # Read form data
                form_data = self._read_form()
                
                # Validate form data
                is_valid, errors = self._validate_form(form_data)
                
                if is_valid:
                    response = {
                        'status': 'success',
                        'message': 'Registration successful',
                        'data': form_data
                    }
                    self._send_response(200, response)
                else:
                    response = {
                        'status': 'error',
                        'message': 'Validation failed',
                        'errors': errors
                    }
                    self._send_response(400, response)
            except Exception as e:
                response = {
                    'status': 'error',
                    'message': f'Server error: {str(e)}'
                }
                self._send_response(500, response)
        else:
            response = {
                'status': 'error',
                'message': 'Endpoint not found'
            }
            self._send_response(404, response)
    
    def _read_form(self):
        """
        Helper method to read and parse form data
        
        Steps:
        1. Get content-length from headers (default to 0)
        2. Read exact bytes from self.rfile
        3. Decode bytes using UTF-8
        4. Parse with parse_qs()
        5. Flatten using dict comprehension
        
        Returns:
            dict: Form data with {key: value} format
        """
        # Read Content-Length header
        content_length = int(self.headers.get('Content-Length', 0))
        
        # Read exact bytes from request body
        body = self.rfile.read(content_length)
        
        # Decode bytes to string using UTF-8
        body_string = body.decode('utf-8')
        
        # Parse form data
        parsed = parse_qs(body_string)
        
        # Flatten the dict: {key: [value]} -> {key: value}
        form_data = {k: v[0] for k, v in parsed.items()}
        
        return form_data
    
    def _validate_form(self, form_data):
        """
        Validate form data
        
        Returns:
            tuple: (is_valid: bool, errors: list)
        """
        errors = []
        
        # Check username
        username = form_data.get('username', '')
        if not username:
            errors.append('Username is required')
        elif len(username) < 3 or len(username) > 20:
            errors.append('Username must be 3-20 characters')
        
        # Check email
        email = form_data.get('email', '')
        if not email:
            errors.append('Email is required')
        elif '@' not in email:
            errors.append('Email must contain @')
        
        # Check password
        password = form_data.get('password', '')
        if not password:
            errors.append('Password is required')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters')
        
        # Check age
        age_str = form_data.get('age', '')
        if not age_str:
            errors.append('Age is required')
        else:
            try:
                age = int(age_str)
                if age < 13 or age > 120:
                    errors.append('Age must be between 13 and 120')
            except ValueError:
                errors.append('Age must be a valid number')
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _send_response(self, status_code, response_dict):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response_json = json.dumps(response_dict)
        self.wfile.write(response_json.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), FormHandler)
    print("Server running on http://localhost:8000")
    print("\nTest with curl commands:")
    print("\n1. Valid registration:")
    print('curl -X POST -d "username=john&email=john@example.com&password=securepass123&age=25" http://localhost:8000/register')
    print("\n2. Invalid username (too short):")
    print('curl -X POST -d "username=ab&email=john@example.com&password=securepass123&age=25" http://localhost:8000/register')
    print("\n3. Invalid email (missing @):")
    print('curl -X POST -d "username=john&email=johnexample.com&password=securepass123&age=25" http://localhost:8000/register')
    print("\n4. Invalid password (too short):")
    print('curl -X POST -d "username=john&email=john@example.com&password=short&age=25" http://localhost:8000/register')
    server.serve_forever()
