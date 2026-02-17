"""
EPISODE 15 - Assignment 2: Advanced Student Management System
Complete solution with search, filter, sort, export, and statistics
"""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import json
import os
import signal
import sys
from datetime import datetime
import csv
import io
import stores
import page


# Global variables
STUDENTS = {}
CURRENT_SORT = 'roll_no'
CURRENT_FILTER = {}

def reset_for_testing():
    """Reset all globals - used for testing"""
    global STUDENTS, CURRENT_SORT
    STUDENTS.clear()
    CURRENT_SORT = 'roll_no'


class AdvancedStudentHandler(BaseHTTPRequestHandler):
    """Advanced HTTP handler for student management with search, filter, sort"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        params = parse_qs(parsed_url.query)
        
        try:
            # Test-only endpoint to reset state
            if path == '/__test_reset__':
                self._handle_test_reset()
            elif path == '/':
                self._handle_home()
            elif path == '/students':
                self._handle_list()
            elif path == '/add':
                self._handle_add_form()
            elif path.startswith('/students/'):
                roll_no = path.split('/')[-1]
                self._handle_student_detail(roll_no)
            elif path == '/search':
                query = params.get('q', [''])[0]
                self._handle_search(query)
            elif path == '/filter':
                self._handle_filter(params)
            elif path == '/sort':
                sort_by = params.get('by', ['roll_no'])[0]
                self._handle_sort(sort_by)
            elif path == '/stats':
                self._handle_statistics()
            elif path == '/export/csv':
                self._handle_export_csv()
            elif path == '/edit':
                roll_no = params.get('roll_no', [''])[0]
                self._handle_edit_form(roll_no)
            elif path.startswith('/delete/'):
                roll_no = path.split('/')[-1]
                self._handle_delete_confirm(roll_no)
            else:
                self._send_html(page.render_error('Page not found'), 404)
        except Exception as e:
            self._send_html(page.render_error(f'Error: {str(e)}'), 500)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        try:
            if path == '/add':
                self._handle_add_post()
            elif path == '/edit':
                self._handle_edit_post()
            elif path.startswith('/delete/'):
                roll_no = path.split('/')[-1]
                self._handle_delete_post(roll_no)
            else:
                self._send_html(page.render_error('Not found'), 404)
        except Exception as e:
            self._send_html(page.render_error(f'Error: {str(e)}'), 500)
    
    def _handle_home(self):
        """Show dashboard with statistics and recent students"""
        global STUDENTS
        
        stats = self._calculate_statistics()
        recent = sorted(STUDENTS.values(), 
                       key=lambda x: x.get('added_on', ''), 
                       reverse=True)[:5]
        
        html = page.render_dashboard(STUDENTS, stats, recent)
        self._send_html(html)
    
    def _handle_list(self):
        """Show all students list"""
        global STUDENTS, CURRENT_SORT
        
        students = STUDENTS.copy()
        
        # Apply current sorting
        if CURRENT_SORT == 'name':
            sorted_students = sorted(students.items(), 
                                    key=lambda x: x[1].get('name', ''))
        elif CURRENT_SORT == 'grade':
            sorted_students = sorted(students.items(), 
                                    key=lambda x: x[1].get('grade', 0), 
                                    reverse=True)
        elif CURRENT_SORT == 'attendance':
            sorted_students = sorted(students.items(), 
                                    key=lambda x: x[1].get('attendance', 0), 
                                    reverse=True)
        else:  # roll_no
            sorted_students = sorted(students.items())
        
        html = page.render_student_list(dict(sorted_students), CURRENT_SORT)
        self._send_html(html)
    
    def _handle_search(self, query):
        """Search students by name or roll number"""
        global STUDENTS
        
        if not query:
            self._redirect('/students')
            return
        
        query_lower = query.lower()
        results = {}
        
        for roll_no, student in STUDENTS.items():
            if (query_lower in roll_no.lower() or 
                query_lower in student.get('name', '').lower()):
                results[roll_no] = student
        
        html = page.render_search_results(results, query)
        self._send_html(html)
    
    def _handle_filter(self, params):
        """Filter students by grade or attendance"""
        global STUDENTS
        
        results = STUDENTS.copy()
        applied_filters = {}
        
        # Filter by grade
        if 'grade_min' in params:
            try:
                grade_min = float(params['grade_min'][0])
                results = {k: v for k, v in results.items() 
                          if float(v.get('grade', 0)) >= grade_min}
                applied_filters['grade_min'] = grade_min
            except (ValueError, KeyError):
                pass
        
        # Filter by attendance
        if 'attendance_min' in params:
            try:
                att_min = float(params['attendance_min'][0])
                results = {k: v for k, v in results.items() 
                          if float(v.get('attendance', 0)) >= att_min}
                applied_filters['attendance_min'] = att_min
            except (ValueError, KeyError):
                pass
        
        html = page.render_filter_results(results, applied_filters)
        self._send_html(html)
    
    def _handle_sort(self, sort_by):
        """Handle sorting"""
        global CURRENT_SORT
        
        if sort_by not in ['roll_no', 'name', 'grade', 'attendance']:
            sort_by = 'roll_no'
        
        CURRENT_SORT = sort_by
        self._redirect('/students')
    
    def _handle_statistics(self):
        """Show statistics dashboard"""
        global STUDENTS
        
        stats = self._calculate_statistics()
        html = page.render_statistics(stats)
        self._send_html(html)
    
    def _handle_export_csv(self):
        """Export students as CSV"""
        global STUDENTS
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(['Roll No', 'Name', 'Grade', 'Attendance', 'Fees Paid', 'Added On'])
        
        # Data rows
        for roll_no, student in sorted(STUDENTS.items()):
            writer.writerow([
                roll_no,
                student.get('name', ''),
                student.get('grade', ''),
                student.get('attendance', ''),
                'Yes' if student.get('fees_paid') else 'No',
                student.get('added_on', '')
            ])
        
        csv_content = output.getvalue()
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/csv')
        self.send_header('Content-Disposition', 'attachment; filename="students.csv"')
        self.end_headers()
        self.wfile.write(csv_content.encode('utf-8'))
    
    def _handle_add_form(self):
        """Show add student form"""
        html = page.render_add_form()
        self._send_html(html)
    
    def _handle_add_post(self):
        """Handle add student POST"""
        global STUDENTS
        
        form_data = self._read_form()
        errors = []
        
        # Validate roll_no
        roll_no = form_data.get('roll_no', '').strip()
        if not roll_no:
            errors.append('Roll number is required')
        elif roll_no in STUDENTS:
            errors.append('Roll number already exists')
        
        # Validate name
        name = form_data.get('name', '').strip()
        if not name:
            errors.append('Name is required')
        elif len(name) < 2 or len(name) > 100:
            errors.append('Name must be 2-100 characters')
        
        # Validate grade
        try:
            grade = float(form_data.get('grade', 0))
            if grade < 0 or grade > 100:
                errors.append('Grade must be 0-100')
        except ValueError:
            errors.append('Grade must be a number')
        
        # Validate attendance
        try:
            attendance = float(form_data.get('attendance', 0))
            if attendance < 0 or attendance > 100:
                errors.append('Attendance must be 0-100')
        except ValueError:
            errors.append('Attendance must be a number')
        
        if errors:
            html = page.render_add_form(errors)
            self._send_html(html)
            return
        
        # Add student
        STUDENTS[roll_no] = {
            'name': page.html_escape(name),
            'grade': float(form_data.get('grade', 0)),
            'attendance': float(form_data.get('attendance', 0)),
            'fees_paid': form_data.get('fees_paid') == 'on',
            'added_on': datetime.now().isoformat()
        }
        
        stores.save_students(STUDENTS)
        
        html = page.render_add_success(roll_no, name)
        self._send_html(html)
    
    def _handle_edit_form(self, roll_no):
        """Show edit student form"""
        global STUDENTS
        
        if roll_no not in STUDENTS:
            self._send_html(page.render_error('Student not found'), 404)
            return
        
        student = STUDENTS[roll_no]
        html = page.render_edit_form(roll_no, student)
        self._send_html(html)
    
    def _handle_edit_post(self):
        """Handle edit student POST"""
        global STUDENTS
        
        form_data = self._read_form()
        roll_no = form_data.get('roll_no', '').strip()
        
        if roll_no not in STUDENTS:
            self._send_html(page.render_error('Student not found'), 404)
            return
        
        errors = []
        student = STUDENTS[roll_no]
        
        # Validate name
        name = form_data.get('name', '').strip()
        if not name:
            errors.append('Name is required')
        elif len(name) < 2 or len(name) > 100:
            errors.append('Name must be 2-100 characters')
        
        # Validate grade
        try:
            grade = float(form_data.get('grade', 0))
            if grade < 0 or grade > 100:
                errors.append('Grade must be 0-100')
        except ValueError:
            errors.append('Grade must be a number')
        
        # Validate attendance
        try:
            attendance = float(form_data.get('attendance', 0))
            if attendance < 0 or attendance > 100:
                errors.append('Attendance must be 0-100')
        except ValueError:
            errors.append('Attendance must be a number')
        
        if errors:
            html = page.render_edit_form(roll_no, student, errors)
            self._send_html(html)
            return
        
        # Update student
        student['name'] = page.html_escape(name)
        student['grade'] = float(form_data.get('grade', 0))
        student['attendance'] = float(form_data.get('attendance', 0))
        student['fees_paid'] = form_data.get('fees_paid') == 'on'
        student['updated_on'] = datetime.now().isoformat()
        
        stores.save_students(STUDENTS)
        
        html = page.render_edit_success(roll_no, name)
        self._send_html(html)
    
    def _handle_student_detail(self, roll_no):
        """Show student details"""
        global STUDENTS
        
        if roll_no not in STUDENTS:
            self._send_html(page.render_error('Student not found'), 404)
            return
        
        student = STUDENTS[roll_no]
        html = page.render_student_detail(roll_no, student)
        self._send_html(html)
    
    def _handle_delete_confirm(self, roll_no):
        """Show delete confirmation"""
        global STUDENTS
        
        if roll_no not in STUDENTS:
            self._send_html(page.render_error('Student not found'), 404)
            return
        
        student = STUDENTS[roll_no]
        html = page.render_delete_confirm(roll_no, student)
        self._send_html(html)
    
    def _handle_delete_post(self, roll_no):
        """Handle delete student POST"""
        global STUDENTS
        
        if roll_no not in STUDENTS:
            self._send_html(page.render_error('Student not found'), 404)
            return
        
        student = STUDENTS[roll_no]
        del STUDENTS[roll_no]
        stores.save_students(STUDENTS)
        
        html = page.render_delete_success(roll_no, student['name'])
        self._send_html(html)
    
    def _calculate_statistics(self):
        """Calculate dashboard statistics"""
        global STUDENTS
        
        if not STUDENTS:
            return {
                'total_students': 0,
                'average_grade': 0,
                'average_attendance': 0,
                'pass_count': 0,
                'fail_count': 0,
                'high_attendance': 0,
                'low_attendance': 0
            }
        
        total = len(STUDENTS)
        grades = [s.get('grade', 0) for s in STUDENTS.values()]
        attendance = [s.get('attendance', 0) for s in STUDENTS.values()]
        
        avg_grade = sum(grades) / total if total > 0 else 0
        avg_attendance = sum(attendance) / total if total > 0 else 0
        
        pass_count = len([g for g in grades if g >= 60])
        fail_count = total - pass_count
        high_att = len([a for a in attendance if a >= 80])
        low_att = len([a for a in attendance if a < 80])
        
        return {
            'total_students': total,
            'average_grade': avg_grade,
            'average_attendance': avg_attendance,
            'pass_count': pass_count,
            'fail_count': fail_count,
            'high_attendance': high_att,
            'low_attendance': low_att
        }
    
    def _redirect(self, path):
        """Send redirect response"""
        self.send_response(302)
        self.send_header('Location', path)
        self.end_headers()
    
    def _handle_test_reset(self):
        """Reset state for testing (internal use only)"""
        global STUDENTS, CURRENT_SORT
        STUDENTS.clear()
        CURRENT_SORT = 'roll_no'
        
        # Remove data file if exists
        if os.path.exists('students_data.json'):
            try:
                os.remove('students_data.json')
            except:
                pass
        
        self._send_html('<html><body>Reset complete</body></html>')
    
    def _send_html(self, html, status_code=200):
        """Send HTML response"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _read_form(self):
        """Read form data from POST"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        body_string = body.decode('utf-8')
        parsed = parse_qs(body_string)
        return {k: v[0] for k, v in parsed.items()}
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def start_server(port=5001):
    """Start the HTTP server"""
    global STUDENTS
    
    # Load existing students
    STUDENTS = stores.load_students()
    
    server = ThreadingHTTPServer(('127.0.0.1', port), AdvancedStudentHandler)
    
    print("╔══════════════════════════════════════════╗")
    print("║  Advanced Student Management System      ║")
    print("║  Episode 15 - Assignment 2               ║")
    print("╚══════════════════════════════════════════╝")
    print(f"\nServer running on http://127.0.0.1:{port}")
    print("\nFeatures:")
    print("  ✓ Complete CRUD operations")
    print("  ✓ Search by name or roll number")
    print("  ✓ Filter by grade and attendance")
    print("  ✓ Sort by different columns")
    print("  ✓ Export to CSV")
    print("  ✓ Dashboard statistics")
    print("  ✓ Advanced validation")
    print("\nEndpoints:")
    print("  GET  / - Dashboard")
    print("  GET  /students - Student list")
    print("  GET  /add - Add form")
    print("  POST /add - Add student")
    print("  GET  /students/<roll_no> - Student detail")
    print("  GET  /edit?roll_no=X - Edit form")
    print("  POST /edit - Update student")
    print("  GET  /delete/<roll_no> - Delete confirm")
    print("  POST /delete/<roll_no> - Delete student")
    print("  GET  /search?q=term - Search")
    print("  GET  /filter?grade_min=80&attendance_min=75 - Filter")
    print("  GET  /sort?by=name - Sort")
    print("  GET  /stats - Statistics")
    print("  GET  /export/csv - Export CSV")
    print("\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        stores.save_students(STUDENTS)
        server.shutdown()
        sys.exit(0)


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    start_server(port)
