"""
EPISODE 13 - ASSIGNMENT 1: Solution
Complete implementation of variable scopes and data persistence
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
from threading import Lock
import signal
import sys
from datetime import datetime
import stores

# Global variables (using LEGB rule)
STUDENTS = []
LOG_LOCK = Lock()

def log_message(format_string, *args):
    """
    Custom logging function with variable arguments (demonstrating *args)
    
    The *args allows any number of arguments to be passed
    LEGB Rule: This function uses 'global LOG_LOCK' (Global scope)
    """
    with LOG_LOCK:
        # Format the message with *args
        if args:
            message = format_string % args
        else:
            message = format_string
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")


def create_validator():
    """
    Factory function using closure pattern
    Demonstrates Enclosing scope and nonlocal keyword
    
    LEGB Rule: create_validator() creates an Enclosing scope
    Inner functions (validate_student) access this scope with nonlocal
    """
    # Enclosing scope variable - accessible to inner function
    student_ids = set()
    
    def validate_student(student_data):
        """
        Inner function that uses enclosing scope variable
        Uses 'nonlocal' to modify enclosing scope variable
        """
        nonlocal student_ids
        
        errors = []
        
        # Validate ID
        try:
            student_id = int(student_data.get('id', ''))
            if student_id in student_ids:
                errors.append('Student ID already exists')
            elif student_id < 1:
                errors.append('Student ID must be positive')
        except ValueError:
            errors.append('Student ID must be a number')
        
        # Validate name
        name = student_data.get('name', '')
        if not name or len(name) < 2 or len(name) > 50:
            errors.append('Name must be 2-50 characters')
        
        # Validate grade
        try:
            grade = float(student_data.get('grade', ''))
            if grade < 0 or grade > 100:
                errors.append('Grade must be 0-100')
        except ValueError:
            errors.append('Grade must be a number')
        
        if not errors and 'id' in student_data:
            # Register the ID in enclosing scope
            student_ids.add(int(student_data['id']))
        
        return len(errors) == 0, errors
    
    return validate_student


class StudentHandler(BaseHTTPRequestHandler):
    """Handler for student management requests"""
    
    # Class-level validator (shared across instances)
    validator = create_validator()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/add-student':
            global STUDENTS  # Declare we're using global variable
            
            try:
                form_data = self._read_form()
                
                # Validate using closure validator
                is_valid, errors = StudentHandler.validator(form_data)
                
                if is_valid:
                    # Create student object
                    student = {
                        'id': int(form_data['id']),
                        'name': form_data['name'],
                        'grade': float(form_data['grade'])
                    }
                    
                    # Modify global STUDENTS list
                    STUDENTS.append(student)
                    
                    # Persist to file
                    success = stores.save_students(STUDENTS)
                    
                    if success:
                        log_message("Added student: %s (ID: %d, Grade: %.2f)", 
                                   student['name'], student['id'], student['grade'])
                        response = {
                            'status': 'success',
                            'message': f"Student {student['name']} added successfully",
                            'student': student
                        }
                        self._send_json_response(response, 200)
                    else:
                        response = {
                            'status': 'error',
                            'message': 'Failed to save student data'
                        }
                        self._send_json_response(response, 500)
                else:
                    response = {
                        'status': 'error',
                        'message': 'Validation failed',
                        'errors': errors
                    }
                    self._send_json_response(response, 400)
                    
            except Exception as e:
                log_message("Error processing request: %s", str(e))
                response = {
                    'status': 'error',
                    'message': f'Server error: {str(e)}'
                }
                self._send_json_response(response, 500)
        else:
            self._send_json_response({'status': 'error', 'message': 'Not found'}, 404)
    
    def _read_form(self):
        """Read POST form data"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        body_string = body.decode('utf-8')
        parsed = parse_qs(body_string)
        return {k: v[0] for k, v in parsed.items()}
    
    def _send_json_response(self, data, status_code=200):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def handle_shutdown(signum, frame):
    """Handle graceful shutdown"""
    log_message("Shutdown signal received. Saving data...")
    stores.save_students(STUDENTS)
    sys.exit(0)


if __name__ == '__main__':
    # Load existing students from file
    STUDENTS = stores.load_students()
    log_message("Loaded %d students from file", len(STUDENTS))
    
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    # Create ThreadingHTTPServer for handling multiple requests
    server = ThreadingHTTPServer(('localhost', 8005), StudentHandler)
    
    log_message("Student Management Server started on http://localhost:8005")
    log_message("Available endpoints: POST /add-student")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        handle_shutdown(None, None)
