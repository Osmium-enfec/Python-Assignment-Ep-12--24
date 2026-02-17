"""
EPISODE 14 - ASSIGNMENT 1: Solution
Complete implementation of secure template rendering
"""

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# BASE_DIR: Root directory of this file
# This pattern enables relative paths from project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_templates_dir():
    """
    Return path to templates directory using os.path.join
    
    Demonstrates:
    - os.path.join() for cross-platform path construction
    - Separation of concerns (templates in dedicated folder)
    """
    return os.path.join(BASE_DIR, 'templates')


def read_template(template_name):
    """
    Read template file from templates directory
    
    Demonstrates:
    - File path handling with os.path
    - UTF-8 encoding for international character support
    - Error handling for missing files
    """
    templates_dir = get_templates_dir()
    template_path = os.path.join(templates_dir, template_name)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template '{template_name}' not found at {template_path}")


def html_escape(value):
    """
    Escape HTML special characters for safe rendering
    
    CRITICAL for XSS prevention!
    Converts untrusted data to safe HTML representation.
    
    Security Rules:
    1. MUST escape '&' FIRST (because other entities contain &)
    2. Escape '<' and '>' to prevent tag injection
    3. Escape '"' to prevent attribute breaking
    4. Any untrusted data MUST be escaped
    
    XSS Attack Example:
    - Malicious input: <script>alert('hacked')</script>
    - After escape: &lt;script&gt;alert('hacked')&lt;/script&gt;
    - Rendered: Text, not executable code
    """
    # Convert to string first (handles None, int, bool, etc.)
    value_str = str(value) if value is not None else ''
    
    # IMPORTANT: Escape & first! Other entities contain &
    value_str = value_str.replace('&', '&amp;')
    
    # Escape angle brackets to prevent tag injection
    value_str = value_str.replace('<', '&lt;')
    value_str = value_str.replace('>', '&gt;')
    
    # Escape quotes to prevent attribute breaking
    value_str = value_str.replace('"', '&quot;')
    
    return value_str


def render_template(template_name, **context):
    """
    Render template by replacing placeholders with escaped context data
    
    Process:
    1. Load template file from templates directory
    2. For each context variable:
       - Escape the value (XSS prevention)
       - Replace {{key}} with escaped value
    3. Return rendered HTML
    
    Security:
    - All context values are escaped before rendering
    - Prevents XSS attacks even with malicious input
    - Untrusted data is safe to render
    - Use __raw_content for pre-rendered HTML to avoid double-escaping
    
    Example:
        # User input is escaped
        render_template('msg.html', message='<script>alert("xss")</script>')
        # Result: {{message}} → &lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;
        
        # Pre-rendered HTML content is not escaped (prevents double-escaping)
        html_fragment = render_template('fragment.html', ...)
        render_template('layout.html', __raw_content=html_fragment)
        # Result: {{content}} → [raw HTML, not escaped]
    """
    # Read template
    template_html = read_template(template_name)
    
    # Replace each placeholder with escaped value
    for key, value in context.items():
        # Check for raw content markers (don't escape pre-rendered HTML)
        if key.startswith('__raw_'):
            # This is pre-rendered HTML, don't escape
            actual_key = key[6:]  # Remove __raw_ prefix
            placeholder = f'{{{{{actual_key}}}}}'  # Creates {{actual_key}}
            template_html = template_html.replace(placeholder, str(value) if value is not None else '')
        else:
            # Escape value for safe HTML rendering
            escaped_value = html_escape(value)
            
            # Replace {{key}} with escaped value
            placeholder = f'{{{{{key}}}}}'  # Creates {{key}}
            template_html = template_html.replace(placeholder, escaped_value)
    
    return template_html


class TemplateHandler(BaseHTTPRequestHandler):
    """HTTP handler demonstrating secure template rendering"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            # Home page with message template
            message_html = render_template('message.html', 
                                          message='Welcome to the Template Engine!')
            # Wrap in layout (use __raw_content to prevent double-escaping)
            html = render_template('layout.html', __raw_content=message_html)
            self._send_html(html)
            
        elif self.path == '/user':
            # User page with parameter
            user_html = render_template('user.html', username='Guest')
            html = render_template('layout.html', __raw_content=user_html)
            self._send_html(html)
            
        elif self.path == '/test-xss':
            # Test XSS vulnerability protection
            payload = '<script>alert("XSS")</script>'
            message = f'Attempted XSS attack with: {payload}'
            message_html = render_template('message.html', message=message)
            html = render_template('layout.html', __raw_content=message_html)
            self._send_html(html)
            
        else:
            self._send_html('<h1>404 Not Found</h1>', 404)
    
    def do_POST(self):
        """Handle POST requests for testing"""
        if self.path == '/render':
            # Read user input
            form_data = self._read_form()
            message = form_data.get('message', '')
            
            # Render with user input (SAFE - html_escape() called automatically)
            message_html = render_template('message.html', message=message)
            # Use __raw_content to prevent double-escaping of pre-rendered HTML
            html = render_template('layout.html', __raw_content=message_html)
            self._send_html(html)
            
        else:
            self._send_html('<h1>404 Not Found</h1>', 404)
    
    def _read_form(self):
        """Read POST form data"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        body_string = body.decode('utf-8')
        parsed = parse_qs(body_string)
        return {k: v[0] for k, v in parsed.items()}
    
    def _send_html(self, html, status=200):
        """Send HTML response"""
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress logging"""
        pass


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8009), TemplateHandler)
    
    print("╔════════════════════════════════════════════╗")
    print("║  Template Engine with XSS Protection       ║")
    print("╚════════════════════════════════════════════╝")
    print("\nServer running on http://localhost:8009")
    print("\nFeatures:")
    print("  ✓ File path handling (os.path module)")
    print("  ✓ Template file loading from templates/")
    print("  ✓ Placeholder {{variable}} substitution")
    print("  ✓ HTML entity escaping (&, <, >, \")")
    print("  ✓ XSS attack prevention")
    print("  ✓ Type conversion (None, int, bool → string)")
    print("\nTest URLs:")
    print("  GET  http://localhost:8009/              - Home page")
    print("  GET  http://localhost:8009/user          - User page")
    print("  GET  http://localhost:8009/test-xss      - XSS test")
    print("  POST http://localhost:8009/render        - Form render (test with malicious input)")
    print("\nSecurity Test:")
    print('  Try: message=<script>alert("XSS")</script>')
    print("  Result: Escaped as &lt;script&gt;...&lt;/script&gt; (safe!)")
    print("\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown")
