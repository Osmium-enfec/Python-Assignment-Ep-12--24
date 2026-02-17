"""
EPISODE 14 - ASSIGNMENT 2: Solution
Advanced Template Systems and Composition

Concepts:
- Template composition (layout + content)
- Dictionary iteration (building HTML from data)
- Safe rendering of lists
- Attribute vs content escaping
- Data persistence
"""

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlencode
import json
import threading
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Global students data
STUDENTS = []
STUDENTS_LOCK = threading.Lock()


def get_templates_dir():
    """Return path to templates directory"""
    return os.path.join(BASE_DIR, 'templates')


def read_template(template_name):
    """Read template file from templates directory"""
    templates_dir = get_templates_dir()
    template_path = os.path.join(templates_dir, template_name)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def html_escape(value):
    """
    Escape HTML special characters for safe content rendering
    
    Security: Escape & first!
    """
    value_str = str(value) if value is not None else ''
    
    value_str = value_str.replace('&', '&amp;')    # MUST be first!
    value_str = value_str.replace('<', '&lt;')
    value_str = value_str.replace('>', '&gt;')
    value_str = value_str.replace('"', '&quot;')
    
    return value_str


def render_template(template_name, **context):
    """
    Render template with context variables
    
    Raw HTML content: Use __raw_prefix to avoid double-escaping
    Example: render_template('layout.html', __raw_content=html_fragment)
    """
    template_html = read_template(template_name)
    
    for key, value in context.items():
        if key.startswith('__raw_'):
            actual_key = key[6:]  # Remove __raw_ prefix
            placeholder = f'{{{{{actual_key}}}}}'
            template_html = template_html.replace(placeholder, str(value) if value is not None else '')
        else:
            escaped_value = html_escape(value)
            placeholder = f'{{{{{key}}}}}'
            template_html = template_html.replace(placeholder, escaped_value)
    
    return template_html


def escape_attribute(value):
    """
    Escape values for use in HTML attributes (stricter than content escaping)
    
    Used in: onclick, href, data-attributes, style, class, etc.
    """
    value_str = str(value) if value is not None else ''
    
    # Escape &, <, >, ", and '
    value_str = value_str.replace('&', '&amp;')    # First!
    value_str = value_str.replace('<', '&lt;')
    value_str = value_str.replace('>', '&gt;')
    value_str = value_str.replace('"', '&quot;')
    value_str = value_str.replace("'", '&#x27;')   # Also escape single quotes in attributes
    
    return value_str


def student_row_html(student):
    """
    Build HTML table row for a single student
    
    Args:
        student: dict with keys: id, name, email, grade, status
    
    Returns:
        str - HTML <tr>...</tr> row
    
    Demonstrates:
    - Safe dict access with .get()
    - Type conversion (grade to int)
    - Conditional rendering (pass/fail)
    - HTML escaping for content
    - Attribute escaping for href
    """
    student_id = student.get('id', '')
    name = student.get('name', 'Unknown')
    email = student.get('email', '')
    grade = student.get('grade', '0')
    
    # Convert grade to int
    try:
        grade_int = int(grade)
    except (ValueError, TypeError):
        grade_int = 0
    
    # Determine status
    status = 'Pass' if grade_int >= 60 else 'Fail'
    status_class = 'pass' if grade_int >= 60 else 'fail'
    
    # Build row with escaped values
    # Escape all content
    escaped_id = html_escape(student_id)
    escaped_name = html_escape(name)
    escaped_email = html_escape(email)
    escaped_grade = html_escape(grade)
    escaped_status = html_escape(status)
    
    # Escape attribute values
    escaped_id_attr = escape_attribute(student_id)
    
    return f'''<tr>
        <td>{escaped_id}</td>
        <td>{escaped_name}</td>
        <td>{escaped_email}</td>
        <td>{escaped_grade}</td>
        <td><span class="{status_class}">{escaped_status}</span></td>
        <td>
            <a href="/students/edit?id={escaped_id_attr}">Edit</a>
            <a href="/students/delete?id={escaped_id_attr}" onclick="return confirm('Delete?')">Delete</a>
        </td>
    </tr>'''


def render_student_list(students):
    """
    Render list of students as HTML table
    
    Args:
        students: list of dicts (student records)
    
    Returns:
        str - HTML <table>...</table>
    
    Demonstrates:
    - Dictionary iteration (for student in students)
    - Safe data access (.get())
    - Building complex HTML from data
    - Security-conscious rendering
    """
    if not students:
        return '<p>No students found</p>'
    
    rows = []
    for student in students:
        row = student_row_html(student)
        rows.append(row)
    
    table = f'''<table class="student-table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Grade</th>
            <th>Status</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {''.join(rows)}
    </tbody>
</table>'''
    
    return table


def get_students():
    """Load students from JSON file"""
    file_path = os.path.join(BASE_DIR, 'students.json')
    
    if os.path.exists(file_path):
        try:
            with STUDENTS_LOCK:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    
    return []


def save_students(students):
    """Save students to JSON file"""
    file_path = os.path.join(BASE_DIR, 'students.json')
    
    with STUDENTS_LOCK:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(students, f, indent=2, ensure_ascii=False)


class StudentListHandler(BaseHTTPRequestHandler):
    """HTTP handler for student list management with templates"""
    
    def do_GET(self):
        """Handle GET requests"""
        students = get_students()
        
        if self.path == '/':
            # Home page - show all students
            table_html = render_student_list(students)
            
            content = f'''
            <h2>Student List</h2>
            <p><a href="/add">Add New Student</a></p>
            {table_html}
            '''
            
            html = render_template('layout.html', __raw_content=content)
            self._send_html(html)
        
        elif self.path == '/add':
            # Add student form
            content = '''
            <h2>Add New Student</h2>
            <form method="POST" action="/students/add">
                <div>
                    <label>Name:</label>
                    <input type="text" name="name" required>
                </div>
                <div>
                    <label>Email:</label>
                    <input type="email" name="email" required>
                </div>
                <div>
                    <label>Grade:</label>
                    <input type="number" name="grade" min="0" max="100" required>
                </div>
                <button type="submit">Add Student</button>
                <a href="/">Cancel</a>
            </form>
            '''
            
            html = render_template('layout.html', __raw_content=content)
            self._send_html(html)
        
        elif self.path.startswith('/students/edit'):
            # Edit student form
            query = self.path.split('?')[1] if '?' in self.path else ''
            params = parse_qs(query)
            student_id = params.get('id', [None])[0]
            
            # Find student
            student = None
            for s in students:
                if s.get('id') == student_id:
                    student = s
                    break
            
            if not student:
                self._send_html('<h1>404 Student Not Found</h1>', 404)
                return
            
            # Escape for HTML attributes
            student_id_attr = escape_attribute(student.get('id', ''))
            name_val = html_escape(student.get('name', ''))
            email_val = html_escape(student.get('email', ''))
            grade_val = html_escape(student.get('grade', ''))
            
            content = f'''
            <h2>Edit Student</h2>
            <form method="POST" action="/students/update">
                <input type="hidden" name="id" value="{student_id_attr}">
                <div>
                    <label>Name:</label>
                    <input type="text" name="name" value="{name_val}" required>
                </div>
                <div>
                    <label>Email:</label>
                    <input type="email" name="email" value="{email_val}" required>
                </div>
                <div>
                    <label>Grade:</label>
                    <input type="number" name="grade" value="{grade_val}" min="0" max="100" required>
                </div>
                <button type="submit">Save Changes</button>
                <a href="/">Cancel</a>
            </form>
            '''
            
            html = render_template('layout.html', __raw_content=content)
            self._send_html(html)
        
        else:
            self._send_html('<h1>404 Not Found</h1>', 404)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/students/add':
            # Add new student
            form_data = self._read_form()
            
            name = form_data.get('name', '').strip()
            email = form_data.get('email', '').strip()
            grade = form_data.get('grade', '0').strip()
            
            # Validate
            if not name or not email or not grade:
                self._send_html('<h1>400 Bad Request</h1>', 400)
                return
            
            # Create new student
            students = get_students()
            new_student = {
                'id': str(uuid.uuid4())[:8],
                'name': name,
                'email': email,
                'grade': grade
            }
            
            students.append(new_student)
            save_students(students)
            
            # Redirect to home
            self._redirect('/')
        
        elif self.path == '/students/update':
            # Update student
            form_data = self._read_form()
            
            student_id = form_data.get('id', '').strip()
            name = form_data.get('name', '').strip()
            email = form_data.get('email', '').strip()
            grade = form_data.get('grade', '0').strip()
            
            if not student_id or not name or not email or not grade:
                self._send_html('<h1>400 Bad Request</h1>', 400)
                return
            
            # Find and update student
            students = get_students()
            for student in students:
                if student.get('id') == student_id:
                    student['name'] = name
                    student['email'] = email
                    student['grade'] = grade
                    break
            
            save_students(students)
            self._redirect('/')
        
        elif self.path.startswith('/students/delete'):
            # Delete student
            query = self.path.split('?')[1] if '?' in self.path else ''
            params = parse_qs(query)
            student_id = params.get('id', [None])[0]
            
            if not student_id:
                self._send_html('<h1>400 Bad Request</h1>', 400)
                return
            
            # Remove student
            students = get_students()
            students = [s for s in students if s.get('id') != student_id]
            save_students(students)
            
            self._redirect('/')
        
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
    
    def _redirect(self, path):
        """Send redirect response"""
        self.send_response(302)
        self.send_header('Location', path)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress logging"""
        pass


if __name__ == '__main__':
    server = HTTPServer(('localhost', 8011), StudentListHandler)
    
    print("╔════════════════════════════════════════════╗")
    print("║  Student Management with Templates         ║")
    print("╚════════════════════════════════════════════╝")
    print("\nServer running on http://localhost:8011")
    print("\nFeatures:")
    print("  ✓ Template composition and inheritance")
    print("  ✓ Dictionary iteration for building tables")
    print("  ✓ Safe rendering of lists")
    print("  ✓ HTML table generation from data")
    print("  ✓ Attribute escaping for security")
    print("  ✓ CRUD operations (Create, Read, Update, Delete)")
    print("\nEndpoints:")
    print("  GET  /              - Student list")
    print("  GET  /add           - Add student form")
    print("  POST /students/add  - Create new student")
    print("  GET  /students/edit?id=1 - Edit form")
    print("  POST /students/update - Save changes")
    print("  POST /students/delete - Remove student")
    print("\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown")
