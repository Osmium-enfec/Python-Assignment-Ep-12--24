"""
EPISODE 12 - ASSIGNMENT 1: Form Data Processing & HTTP Request Handling

TOPICS COVERED:
- HTTP Content-Length Header
- Request Body Reading and Processing
- Form Data Encoding/Decoding (UTF-8)
- Form Data Parsing with parse_qs()
- Dictionary Comprehensions
- Helper Functions and Code Organization
- Error Handling in Request Processing

ASSIGNMENT:
Create a simple HTTP server that handles form submissions. The server should:
1. Accept POST requests to /register endpoint
2. Read the Content-Length header
3. Read the request body from self.rfile
4. Parse form data using parse_qs()
5. Extract form fields and validate them
6. Return appropriate responses

FORM FIELDS EXPECTED:
- username: should be 3-20 characters
- email: should contain @
- password: should be at least 8 characters
- age: should be a valid number between 13-120

REQUIREMENTS:
- Implement _read_form() helper method to read and parse form data
- Use dictionary comprehension to flatten parse_qs() output
- Handle encoding/decoding properly with UTF-8
- Validate all form fields
- Return JSON response with success/error messages
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json

class FormHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        """Handle POST requests"""
        # TODO: Implement POST handler
        # 1. Check if path is /register
        # 2. Read Content-Length header (use get with default)
        # 3. Call _read_form() to get form data
        # 4. Validate form fields
        # 5. Send appropriate response
        pass
    
    def _read_form(self):
        """
        Helper method to read and parse form data
        
        TODO: Implement this method
        1. Get content-length from self.headers
        2. Read exact bytes from self.rfile
        3. Decode bytes to string using UTF-8
        4. Parse using parse_qs()
        5. Use dict comprehension to flatten {key: [value]} to {key: value}
        6. Return flattened dictionary
        
        Returns:
            dict: Form data with {key: value} format
        """
        pass
    
    def _validate_form(self, form_data):
        """
        Validate form data
        
        TODO: Implement validation
        - username: 3-20 chars
        - email: must contain @
        - password: at least 8 chars
        - age: valid number between 13-120
        
        Returns:
            tuple: (is_valid: bool, errors: list)
        """
        pass
    
    def _send_response(self, status_code, response_dict):
        """Send JSON response"""
        # TODO: Implement response sending
        # 1. Set status and headers
        # 2. Encode response as JSON
        # 3. Send to client
        pass


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), FormHandler)
    print("Server running on http://localhost:8000")
    print("Test with: curl -X POST -d 'username=john&email=john@example.com&password=securepass123&age=25' http://localhost:8000/register")
    server.serve_forever()
