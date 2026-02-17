"""
EPISODE 13 - ASSIGNMENT 2: Solution
Complete implementation with HTTP routing, PRG pattern, and templates
"""

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from http.cookies import SimpleCookie
import json
import uuid
from datetime import datetime
import stores
import page

# Global variables
STUDENTS = []
FLASH_MESSAGES = {}


class ServerHandler(BaseHTTPRequestHandler):
    """Main server handler with routing"""
    
    def do_GET(self):
        """Handle GET requests with routing"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        # Get flash message if exists
        session_id = self._get_session_from_cookie()
        flash_msg = self._get_and_clear_flash(session_id)
        flash_html = ''
        
        if flash_msg:
            flash_type = 'success' if flash_msg['type'] == 'success' else 'error'
            flash_html = f'<div class="alert alert-{flash_type}">{flash_msg["message"]}</div>'
        
        try:
            if path == '/':
                self._handle_home(flash_html)
            elif path == '/students':
                self._handle_student_list(flash_html)
            elif path == '/add':
                self._handle_add_form(flash_html)
            elif path == '/edit':
                student_id = query_params.get('id', [None])[0]
                self._handle_edit_form(student_id, flash_html)
            elif path == '/delete':
                student_id = query_params.get('id', [None])[0]
                self._handle_delete(student_id, session_id)
            else:
                self._render_html(page.render_error('Page not found'), 404)
        except Exception as e:
            self._render_html(page.render_error(f'Error: {str(e)}'), 500)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        session_id = self._get_session_from_cookie() or str(uuid.uuid4())
        
        try:
            if path == '/add':
                self._handle_add_post(session_id)
            elif path == '/edit':
                self._handle_edit_post(session_id)
            else:
                self._render_html(page.render_error('Not found'), 404)
        except Exception as e:
            self._render_html(page.render_error(f'Error: {str(e)}'), 500)
    
    def _handle_home(self, flash_html=''):
        """Handle GET / - Dashboard"""
        global STUDENTS
        
        stats = self._calculate_statistics(STUDENTS)
        html = page.render_home(STUDENTS, stats)
        
        # Inject flash message if present
        if flash_html:
            html = html.replace('<h1>Dashboard</h1>', f'{flash_html}<h1>Dashboard</h1>')
        
        self._render_html(html)
    
    def _handle_student_list(self, flash_html=''):
        """Handle GET /students"""
        global STUDENTS
        
        html = page.render_student_list(STUDENTS, flash_html)
        self._render_html(html)
    
    def _handle_add_form(self, flash_html=''):
        """Handle GET /add"""
        html = page.render_add_form(flash_html)
        self._render_html(html)
    
    def _handle_edit_form(self, student_id, flash_html=''):
        """Handle GET /edit?id=X"""
        global STUDENTS
        
        if not student_id:
            self._redirect('/students')
            return
        
        try:
            sid = int(student_id)
            student = next((s for s in STUDENTS if s['id'] == sid), None)
            
            if not student:
                self._set_flash_message('error', f'Student {student_id} not found')
                self._redirect('/students')
                return
            
            html = page.render_edit_form(student, flash_html)
            self._render_html(html)
        except ValueError:
            self._redirect('/students')
    
    def _handle_add_post(self, session_id):
        """Handle POST /add - Add student (PRG pattern)"""
        global STUDENTS
        
        form_data = self._read_form()
        
        # Validate
        errors = []
        student_id = None
        try:
            student_id = int(form_data.get('id', ''))
            if student_id <= 0:
                errors.append('ID must be positive')
            elif any(s['id'] == student_id for s in STUDENTS):
                errors.append('ID already exists')
        except ValueError:
            errors.append('Invalid ID')
        
        name = form_data.get('name', '')
        if not name or len(name) < 2 or len(name) > 50:
            errors.append('Name must be 2-50 characters')
        
        try:
            grade = float(form_data.get('grade', ''))
            if grade < 0 or grade > 100:
                errors.append('Grade must be 0-100')
        except ValueError:
            errors.append('Invalid grade')
        
        if errors:
            self._set_flash_message('error', 'Validation failed: ' + ', '.join(errors))
            self._redirect('/add', session_id)
            return
        
        # Add student
        student = {
            'id': student_id,
            'name': name,
            'grade': grade
        }
        STUDENTS.append(student)
        
        # Persist
        stores.save_students(STUDENTS)
        
        # Set flash and redirect (PRG pattern)
        self._set_flash_message('success', f'Student {name} added successfully')
        self._redirect('/students', session_id)
    
    def _handle_edit_post(self, session_id):
        """Handle POST /edit - Update student (PRG pattern)"""
        global STUDENTS
        
        form_data = self._read_form()
        
        try:
            student_id = int(form_data.get('id', ''))
            student = next((s for s in STUDENTS if s['id'] == student_id), None)
            
            if not student:
                self._set_flash_message('error', 'Student not found')
                self._redirect('/students', session_id)
                return
            
            # Validate and update
            name = form_data.get('name', '')
            if not name or len(name) < 2 or len(name) > 50:
                self._set_flash_message('error', 'Invalid name')
                self._redirect(f'/edit?id={student_id}', session_id)
                return
            
            grade = float(form_data.get('grade', ''))
            if grade < 0 or grade > 100:
                self._set_flash_message('error', 'Grade must be 0-100')
                self._redirect(f'/edit?id={student_id}', session_id)
                return
            
            # Update
            student['name'] = name
            student['grade'] = grade
            
            # Persist
            stores.save_students(STUDENTS)
            
            # Redirect with flash
            self._set_flash_message('success', f'Student {name} updated successfully')
            self._redirect('/students', session_id)
            
        except ValueError:
            self._redirect('/students', session_id)
    
    def _handle_delete(self, student_id, session_id):
        """Handle GET /delete?id=X - Delete student"""
        global STUDENTS
        
        if not student_id:
            self._redirect('/students')
            return
        
        try:
            sid = int(student_id)
            student = next((s for s in STUDENTS if s['id'] == sid), None)
            
            if student:
                name = student['name']
                STUDENTS = [s for s in STUDENTS if s['id'] != sid]
                stores.save_students(STUDENTS)
                
                self._set_flash_message('success', f'Student {name} deleted successfully')
            else:
                self._set_flash_message('error', f'Student not found')
            
            self._redirect('/students', session_id)
            
        except ValueError:
            self._redirect('/students')
    
    def _get_session_from_cookie(self):
        """Get session ID from cookie"""
        cookie_header = self.headers.get('Cookie', '')
        
        if not cookie_header:
            return None
        
        try:
            cookies = SimpleCookie()
            cookies.load(cookie_header)
            session_id = cookies.get('session_id')
            return session_id.value if session_id else None
        except:
            return None
    
    def _set_flash_message(self, message_type, message):
        """Set flash message (stored in global dict)"""
        session_id = self._get_session_from_cookie() or str(uuid.uuid4())
        FLASH_MESSAGES[session_id] = {
            'type': message_type,
            'message': message
        }
        return session_id
    
    def _get_and_clear_flash(self, session_id):
        """Get and clear flash message"""
        if session_id and session_id in FLASH_MESSAGES:
            message = FLASH_MESSAGES[session_id]
            del FLASH_MESSAGES[session_id]
            return message
        return None
    
    def _calculate_statistics(self, students):
        """Calculate dashboard statistics"""
        if not students:
            return {
                'total_students': 0,
                'average_grade': 0,
                'pass_rate': 0
            }
        
        total = len(students)
        average = sum(s['grade'] for s in students) / total
        passing = len([s for s in students if s['grade'] >= 60])
        pass_rate = (passing / total) * 100 if total > 0 else 0
        
        return {
            'total_students': total,
            'average_grade': average,
            'pass_rate': pass_rate
        }
    
    def _redirect(self, path, session_id=None, status=302):
        """Send HTTP redirect (PRG pattern)"""
        self.send_response(status)
        self.send_header('Location', path)
        
        if session_id:
            cookie = SimpleCookie()
            cookie['session_id'] = session_id
            cookie['session_id']['path'] = '/'
            cookie['session_id']['max-age'] = 3600
            self.send_header('Set-Cookie', cookie['session_id'].OutputString())
        
        self.end_headers()
    
    def _render_html(self, html, status_code=200):
        """Send HTML response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
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
    # Load existing students
    STUDENTS = stores.load_students()
    
    # Create ThreadingHTTPServer for concurrent requests
    server = ThreadingHTTPServer(('localhost', 8007), ServerHandler)
    
    print("╔══════════════════════════════════════════╗")
    print("║  Student Dashboard Server                ║")
    print("╚══════════════════════════════════════════╝")
    print("\nServer started on http://localhost:8007")
    print("\nAvailable endpoints:")
    print("  GET  / - Dashboard with statistics")
    print("  GET  /students - Student list")
    print("  GET  /add - Add student form")
    print("  POST /add - Submit add form (redirects)")
    print("  GET  /edit?id=X - Edit student")
    print("  POST /edit - Submit edit form (redirects)")
    print("  GET  /delete?id=X - Delete student (redirects)")
    print("\nFeatures:")
    print("  ✓ HTTP 302 redirects after POST (PRG pattern)")
    print("  ✓ Flash messages for user feedback")
    print("  ✓ Statistics calculation (avg, pass rate)")
    print("  ✓ Dynamic HTML templates with f-strings")
    print("  ✓ ThreadingHTTPServer for concurrency")
    print("\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        stores.save_students(STUDENTS)
