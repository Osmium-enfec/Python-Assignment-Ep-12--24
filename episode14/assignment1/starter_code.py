"""
EPISODE 14 - ASSIGNMENT 1: Template System & HTML Security

TOPICS COVERED:
- File Path Concepts (Absolute vs Relative)
- os.path Module Basics (dirname, abspath, join)
- BASE_DIR Pattern for project root
- Template File Organization
- read_template() Function
- Placeholder Substitution Pattern
- Context Dictionaries
- String replace() Method
- Dictionary Unpacking with **kwargs
- HTML Special Characters
- HTML Entity Encoding
- XSS (Cross-Site Scripting) Attacks Prevention
- html_escape() Function
- Type Conversion in Templates

ASSIGNMENT:
Build a secure template rendering system with XSS protection.

STRUCTURE:
1. templates/ folder containing HTML templates
2. template_utils.py module with template functions
3. Server using secure template rendering

TEMPLATES NEEDED:
- layout.html - Base template with {{content}} placeholder
- message.html - Simple template with {{message}} placeholder
- user.html - Template with {{username}} placeholder

REQUIREMENTS:
- Use os.path for cross-platform path handling
- Load templates from templates/ folder
- Implement read_template() function
- Implement html_escape() function for XSS prevention
- Implement render_template() function
- Handle None values properly
- Test with malicious input (XSS attacks)
- All untrusted data must be escaped
"""

import os
import json

# TODO: Set BASE_DIR to this file's directory
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_templates_dir():
    """
    TODO: Return path to templates directory
    Use os.path.join with BASE_DIR and 'templates'
    """
    pass


def read_template(template_name):
    """
    TODO: Read template file from templates directory
    
    Steps:
    1. Get templates directory path
    2. Join with template_name
    3. Open file with encoding='utf-8'
    4. Read and return content
    5. Handle FileNotFoundError
    
    Args:
        template_name: Name of template file (e.g., 'layout.html')
    
    Returns:
        str: Full HTML content
    
    Raises:
        FileNotFoundError: If template doesn't exist
    """
    pass


def html_escape(value):
    """
    TODO: Escape HTML special characters for safe rendering
    
    Prevents XSS attacks by converting special characters to entities.
    IMPORTANT: Must escape '&' FIRST!
    
    Conversions:
    - & → &amp;
    - < → &lt;
    - > → &gt;
    - " → &quot;
    
    Args:
        value: Value to escape (can be any type)
    
    Returns:
        str: Escaped string safe for HTML
    """
    pass


def render_template(template_name, **context):
    """
    TODO: Render template by replacing placeholders with context data
    
    Steps:
    1. Read template file
    2. For each key-value pair in context:
        - Escape the value
        - Replace {{key}} with escaped value
    3. Return rendered HTML
    
    Args:
        template_name: Name of template file
        **context: Keyword arguments with template variables
    
    Returns:
        str: Rendered HTML with placeholders replaced
    
    Example:
        render_template('message.html', message='Hello World')
        # Replaces {{message}} with escaped 'Hello World'
    """
    pass


class TemplateHandler:
    """HTTP handler using secure template rendering"""
    
    def do_GET(self):
        """Handle GET requests"""
        # TODO: Implement GET handler
        # 1. Check path
        # 2. Render appropriate template
        # 3. Send HTML response
        pass
    
    def do_POST(self):
        """Handle POST requests"""
        # TODO: Implement POST handler for XSS testing
        # 1. Read form data
        # 2. Render template with user input
        # 3. Input MUST be escaped by render_template()
        pass
    
    def _read_form(self):
        """Read POST form data"""
        from urllib.parse import parse_qs
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        body_string = body.decode('utf-8')
        parsed = parse_qs(body_string)
        return {k: v[0] for k, v in parsed.items()}
    
    def _send_html(self, html):
        """Send HTML response"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress logging"""
        pass


if __name__ == '__main__':
    from http.server import HTTPServer
    
    print("Template Rendering Server on port 8009")
    print("Features:")
    print("  - Safe HTML escaping to prevent XSS")
    print("  - Cross-platform file path handling")
    print("  - Template composition with placeholders")
    print("\nTest with:")
    print("  GET http://localhost:8009/")
    print("  POST to test XSS: <script>alert('test')</script>")
