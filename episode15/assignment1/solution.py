"""
EPISODE 15 - Complete Student Management CRUD Application
Assignment 1: Basic CRUD with forms and data persistence
"""

import http.server
import urllib.parse
import json
import os
from datetime import datetime
from threading import Thread
import signal
import sys

import stores
import page


STUDENTS = {}


def parse_form_data(content):
    """Parse form data from POST request"""
    try:
        parsed = urllib.parse.parse_qs(content.decode('utf-8'))
        form_data = {}
        for key, values in parsed.items():
            form_data[key] = values[0] if values else ""
        return form_data
    except Exception as e:
        print(f"Error parsing form data: {e}")
        return {}


def validate_student_data(form_data, roll_no=None):
    """Validate student data"""
    errors = []
    
    # Check required fields
    if not form_data.get('roll_no', '').strip():
        errors.append("Roll number is required")
    if not form_data.get('name', '').strip():
        errors.append("Name is required")
    if not form_data.get('grade', '').strip():
        errors.append("Grade is required")
    
    # Check attendance
    try:
        attendance = int(form_data.get('attendance', 0))
        if attendance < 0 or attendance > 100:
            errors.append("Attendance must be between 0 and 100")
    except ValueError:
        errors.append("Attendance must be a valid number")
    
    # Check for duplicate roll number (only when adding new)
    new_roll_no = form_data.get('roll_no', '').strip()
    if new_roll_no != roll_no and new_roll_no in STUDENTS:
        errors.append("Roll number already exists")
    
    return errors


class StudentHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for student management"""
    
    def do_GET(self):
        """Handle GET requests"""
        path = self.path.split('?')[0]
        
        # Test-only endpoint to reset state
        if path == '/__test_reset__':
            global STUDENTS
            STUDENTS.clear()
            if os.path.exists('students_data.json'):
                try:
                    os.remove('students_data.json')
                except:
                    pass
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body>Reset complete</body></html>')
            return
        
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(page.render_home(STUDENTS).encode('utf-8'))
        
        elif path == '/add':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(page.render_add_form().encode('utf-8'))
        
        elif path.startswith('/view/'):
            roll_no = path.replace('/view/', '')
            if roll_no in STUDENTS:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(page.render_view_student(roll_no, STUDENTS[roll_no]).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(page.render_error("Student not found").encode('utf-8'))
        
        elif path.startswith('/edit/'):
            roll_no = path.replace('/edit/', '')
            if roll_no in STUDENTS:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(page.render_edit_form(roll_no, STUDENTS[roll_no]).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(page.render_error("Student not found").encode('utf-8'))
        
        elif path.startswith('/delete/'):
            roll_no = path.replace('/delete/', '')
            if roll_no in STUDENTS:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(page.render_delete_confirmation(roll_no, STUDENTS[roll_no]).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(page.render_error("Student not found").encode('utf-8'))
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(page.render_error("Page not found").encode('utf-8'))
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        form_data = parse_form_data(body)
        path = self.path
        
        if path == '/add':
            # Validate data
            errors = validate_student_data(form_data)
            if errors:
                self.send_response(400)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                error_html = page.render_add_form()
                # Inject error message
                error_msg = "<div class='error'>" + "<br>".join([page.html_escape(e) for e in errors]) + "</div>"
                error_html = error_html.replace("<h1>Add New Student</h1>", f"<h1>Add New Student</h1>{error_msg}")
                self.wfile.write(error_html.encode('utf-8'))
            else:
                # Add student
                roll_no = form_data.get('roll_no', '').strip()
                STUDENTS[roll_no] = {
                    'name': form_data.get('name', '').strip(),
                    'grade': form_data.get('grade', '').strip(),
                    'attendance': int(form_data.get('attendance', 0)),
                    'fees_paid': 'fees_paid' in form_data,
                    'added_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                stores.save_students(STUDENTS)
                
                # Redirect to home
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
        
        elif path.startswith('/edit/'):
            roll_no = path.replace('/edit/', '')
            if roll_no not in STUDENTS:
                self.send_response(404)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(page.render_error("Student not found").encode('utf-8'))
            else:
                # Validate data
                errors = validate_student_data(form_data, roll_no)
                if errors:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    error_html = page.render_edit_form(roll_no, STUDENTS[roll_no])
                    # Inject error message
                    error_msg = "<div class='error'>" + "<br>".join([page.html_escape(e) for e in errors]) + "</div>"
                    error_html = error_html.replace("<h1>Edit Student</h1>", f"<h1>Edit Student</h1>{error_msg}")
                    self.wfile.write(error_html.encode('utf-8'))
                else:
                    # Update student
                    STUDENTS[roll_no]['name'] = form_data.get('name', '').strip()
                    STUDENTS[roll_no]['grade'] = form_data.get('grade', '').strip()
                    STUDENTS[roll_no]['attendance'] = int(form_data.get('attendance', 0))
                    STUDENTS[roll_no]['fees_paid'] = 'fees_paid' in form_data
                    stores.save_students(STUDENTS)
                    
                    # Redirect to home
                    self.send_response(302)
                    self.send_header('Location', '/')
                    self.end_headers()
        
        elif path.startswith('/delete/'):
            roll_no = path.replace('/delete/', '')
            if roll_no not in STUDENTS:
                self.send_response(404)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(page.render_error("Student not found").encode('utf-8'))
            else:
                if form_data.get('confirm') == 'yes':
                    # Delete student
                    del STUDENTS[roll_no]
                    stores.save_students(STUDENTS)
                    
                    # Redirect to home
                    self.send_response(302)
                    self.send_header('Location', '/')
                    self.end_headers()
                else:
                    # Show confirmation again
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(page.render_delete_confirmation(roll_no, STUDENTS[roll_no]).encode('utf-8'))
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(page.render_error("Page not found").encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def start_server(port=5000):
    """Start the HTTP server"""
    global STUDENTS
    
    # Load existing students from file
    STUDENTS = stores.load_students()
    
    # Create server
    server = http.server.ThreadingHTTPServer(('127.0.0.1', port), StudentHandler)
    print(f"Server running at http://127.0.0.1:{port}")
    
    # Handle graceful shutdown (only in main thread)
    import threading
    if threading.current_thread() is threading.main_thread():
        def signal_handler(sig, frame):
            print("\nShutting down...")
            server.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    start_server(5000)
