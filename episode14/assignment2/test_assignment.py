"""
EPISODE 14 - ASSIGNMENT 2: Test Suite
Tests for advanced template systems with list rendering and data management
"""

import unittest
import os
import sys
import time
import threading
from http.server import HTTPServer
import requests
from urllib.parse import urlencode
import json

# Import solution
from solution import (
    read_template, html_escape, render_template, escape_attribute,
    student_row_html, render_student_list, StudentListHandler,
    get_students, save_students, BASE_DIR, get_templates_dir
)


class TestEscapeAttribute(unittest.TestCase):
    """Test escape_attribute function for attributes"""
    
    def test_escape_quotes_in_attribute(self):
        """Test double quotes are escaped"""
        result = escape_attribute('value"with"quotes')
        self.assertEqual(result, 'value&quot;with&quot;quotes')
    
    def test_escape_single_quotes(self):
        """Test single quotes are escaped in attributes"""
        result = escape_attribute("onclick='alert(1)'")
        self.assertIn('&#x27;', result)
    
    def test_escape_ampersand_first(self):
        """Test & is escaped first"""
        result = escape_attribute('&<>')
        self.assertEqual(result, '&amp;&lt;&gt;')
    
    def test_url_with_params(self):
        """Test escaping URLs with parameters"""
        result = escape_attribute('/students/edit?id=1&name=Bob')
        self.assertIn('&amp;', result)  # & should become &amp;
        self.assertNotIn('&amp;amp;', result)  # Not double-escaped


class TestStudentRow(unittest.TestCase):
    """Test student_row_html function"""
    
    def test_build_student_row(self):
        """Test building HTML row from student dict"""
        student = {
            'id': '12345',
            'name': 'Alice',
            'email': 'alice@example.com',
            'grade': '85'
        }
        
        result = student_row_html(student)
        
        self.assertIn('<tr>', result)
        self.assertIn('</tr>', result)
        self.assertIn('Alice', result)
        self.assertIn('alice@example.com', result)
        self.assertIn('85', result)
    
    def test_student_row_pass_status(self):
        """Test pass status for grade >= 60"""
        student = {'id': '1', 'name': 'Bob', 'email': 'bob@ex.com', 'grade': '75'}
        result = student_row_html(student)
        
        self.assertIn('Pass', result)
        self.assertIn('class="pass"', result)
    
    def test_student_row_fail_status(self):
        """Test fail status for grade < 60"""
        student = {'id': '2', 'name': 'Carol', 'email': 'carol@ex.com', 'grade': '45'}
        result = student_row_html(student)
        
        self.assertIn('Fail', result)
        self.assertIn('class="fail"', result)
    
    def test_student_row_xss_in_name(self):
        """Test XSS prevention in student name"""
        student = {'id': '3', 'name': '<script>alert("XSS")</script>', 'email': 'test@ex.com', 'grade': '70'}
        result = student_row_html(student)
        
        self.assertNotIn('<script>', result)
        self.assertIn('&lt;script&gt;', result)
    
    def test_student_row_xss_in_attribute(self):
        """Test XSS prevention in attributes"""
        student = {'id': '"><script>alert("XSS")</script><"', 'name': 'Test', 'email': 'test@ex.com', 'grade': '70'}
        result = student_row_html(student)
        
        # ID is used in href attribute, should be escaped
        self.assertNotIn('"><script>', result)
        self.assertIn('&quot;&gt;', result)
    
    def test_student_row_missing_fields(self):
        """Test handling missing student fields"""
        student = {'id': '4'}  # Missing name, email, grade
        result = student_row_html(student)
        
        self.assertIn('<tr>', result)
        self.assertIn('Unknown', result)  # Default for name


class TestRenderStudentList(unittest.TestCase):
    """Test render_student_list function"""
    
    def test_render_empty_list(self):
        """Test rendering empty student list"""
        result = render_student_list([])
        
        self.assertIn('No students found', result)
    
    def test_render_single_student(self):
        """Test rendering list with one student"""
        students = [
            {'id': '1', 'name': 'Alice', 'email': 'alice@ex.com', 'grade': '85'}
        ]
        
        result = render_student_list(students)
        
        self.assertIn('<table', result)
        self.assertIn('Alice', result)
        self.assertIn('<thead>', result)
        self.assertIn('<tbody>', result)
    
    def test_render_multiple_students(self):
        """Test rendering list with multiple students"""
        students = [
            {'id': '1', 'name': 'Alice', 'email': 'alice@ex.com', 'grade': '85'},
            {'id': '2', 'name': 'Bob', 'email': 'bob@ex.com', 'grade': '92'},
            {'id': '3', 'name': 'Carol', 'email': 'carol@ex.com', 'grade': '55'}
        ]
        
        result = render_student_list(students)
        
        self.assertIn('Alice', result)
        self.assertIn('Bob', result)
        self.assertIn('Carol', result)
        self.assertEqual(result.count('<tr>'), 4)  # 1 header + 3 data rows
    
    def test_table_headers(self):
        """Test table headers are present"""
        students = [{'id': '1', 'name': 'Test', 'email': 'test@ex.com', 'grade': '70'}]
        result = render_student_list(students)
        
        headers = ['ID', 'Name', 'Email', 'Grade', 'Status', 'Actions']
        for header in headers:
            self.assertIn(header, result)
    
    def test_edit_delete_links(self):
        """Test Edit and Delete links are generated"""
        students = [{'id': '123', 'name': 'Test', 'email': 'test@ex.com', 'grade': '70'}]
        result = render_student_list(students)
        
        self.assertIn('/students/edit?id=', result)
        self.assertIn('/students/delete?id=', result)
        self.assertIn('Edit', result)
        self.assertIn('Delete', result)


class TestDataPersistence(unittest.TestCase):
    """Test student data persistence"""
    
    def setUp(self):
        """Clear students before each test"""
        file_path = os.path.join(BASE_DIR, 'students.json')
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def tearDown(self):
        """Cleanup after each test"""
        file_path = os.path.join(BASE_DIR, 'students.json')
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def test_save_and_load_students(self):
        """Test saving and loading students"""
        students = [
            {'id': '1', 'name': 'Alice', 'email': 'alice@ex.com', 'grade': '85'},
            {'id': '2', 'name': 'Bob', 'email': 'bob@ex.com', 'grade': '92'}
        ]
        
        save_students(students)
        loaded = get_students()
        
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]['name'], 'Alice')
        self.assertEqual(loaded[1]['name'], 'Bob')
    
    def test_load_nonexistent_file(self):
        """Test loading when no file exists"""
        result = get_students()
        self.assertEqual(result, [])
    
    def test_students_file_format(self):
        """Test students are saved as valid JSON"""
        students = [
            {'id': '1', 'name': 'Test', 'email': 'test@ex.com', 'grade': '75'}
        ]
        
        save_students(students)
        
        file_path = os.path.join(BASE_DIR, 'students.json')
        with open(file_path, 'r') as f:
            content = f.read()
            data = json.loads(content)  # Should parse without error
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], '1')


class TestStudentListHTTPServer(unittest.TestCase):
    """Test HTTP server with student management"""
    
    @classmethod
    def setUpClass(cls):
        """Start server"""
        cls.server = HTTPServer(('localhost', 8020), StudentListHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.5)
        cls.base_url = 'http://localhost:8020'
        
        # Clear students
        file_path = os.path.join(BASE_DIR, 'students.json')
        if os.path.exists(file_path):
            os.remove(file_path)
    
    @classmethod
    def tearDownClass(cls):
        """Shutdown server"""
        cls.server.shutdown()
        
        # Cleanup
        file_path = os.path.join(BASE_DIR, 'students.json')
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def setUp(self):
        """Clear students before each test"""
        file_path = os.path.join(BASE_DIR, 'students.json')
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def tearDown(self):
        """Cleanup after each test"""
        file_path = os.path.join(BASE_DIR, 'students.json')
        if os.path.exists(file_path):
            os.remove(file_path)
    
    def test_home_page_loads(self):
        """Test home page loads"""
        response = requests.get(f'{self.base_url}/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Student List', response.text)
        self.assertIn('<!DOCTYPE html>', response.text)
    
    def test_home_page_no_students(self):
        """Test home page when no students"""
        response = requests.get(f'{self.base_url}/')
        
        self.assertIn('No students found', response.text)
    
    def test_add_page_loads(self):
        """Test add student page"""
        response = requests.get(f'{self.base_url}/add')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Add New Student', response.text)
        self.assertIn('<form', response.text)
    
    def test_add_student_success(self):
        """Test adding a new student"""
        data = {
            'name': 'Alice',
            'email': 'alice@example.com',
            'grade': '85'
        }
        response = requests.post(
            f'{self.base_url}/students/add',
            data=urlencode(data),
            allow_redirects=False
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/')
    
    def test_add_student_persists(self):
        """Test added student appears in list"""
        data = {
            'name': 'Bob',
            'email': 'bob@example.com',
            'grade': '92'
        }
        requests.post(f'{self.base_url}/students/add', data=urlencode(data))
        
        response = requests.get(f'{self.base_url}/')
        
        self.assertIn('Bob', response.text)
        self.assertIn('bob@example.com', response.text)
        self.assertIn('92', response.text)
    
    def test_add_student_xss_blocked(self):
        """Test XSS is prevented when adding student"""
        data = {
            'name': '<script>alert("XSS")</script>',
            'email': 'test@ex.com',
            'grade': '70'
        }
        requests.post(f'{self.base_url}/students/add', data=urlencode(data))
        
        response = requests.get(f'{self.base_url}/')
        
        self.assertNotIn('<script>', response.text)
        self.assertIn('&lt;script&gt;', response.text)
    
    def test_edit_student_page(self):
        """Test edit student page"""
        # Add a student first
        data = {'name': 'Carol', 'email': 'carol@ex.com', 'grade': '75'}
        requests.post(f'{self.base_url}/students/add', data=urlencode(data))
        
        # Get student ID from list
        response = requests.get(f'{self.base_url}/')
        self.assertIn('Carol', response.text)
        
        # Parse ID from href (would need regex in real test)
        # For now, just verify edit page works with a valid ID
        students = get_students()
        if students:
            student_id = students[0]['id']
            response = requests.get(f'{self.base_url}/students/edit?id={student_id}')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('Edit Student', response.text)
            self.assertIn('Carol', response.text)
    
    def test_update_student(self):
        """Test updating student"""
        # Add a student
        data = {'name': 'David', 'email': 'david@ex.com', 'grade': '70'}
        requests.post(f'{self.base_url}/students/add', data=urlencode(data))
        
        students = get_students()
        student_id = students[0]['id']
        
        # Update
        update_data = {
            'id': student_id,
            'name': 'David Updated',
            'email': 'david_new@ex.com',
            'grade': '88'
        }
        response = requests.post(
            f'{self.base_url}/students/update',
            data=urlencode(update_data),
            allow_redirects=False
        )
        
        self.assertEqual(response.status_code, 302)
        
        # Verify update
        response = requests.get(f'{self.base_url}/')
        self.assertIn('David Updated', response.text)
        self.assertIn('david_new@ex.com', response.text)
        self.assertIn('88', response.text)
    
    def test_delete_student(self):
        """Test deleting student"""
        # Add a student
        data = {'name': 'Eve', 'email': 'eve@ex.com', 'grade': '65'}
        requests.post(f'{self.base_url}/students/add', data=urlencode(data))
        
        students = get_students()
        student_id = students[0]['id']
        
        # Delete
        response = requests.post(
            f'{self.base_url}/students/delete?id={student_id}',
            allow_redirects=False
        )
        
        self.assertEqual(response.status_code, 302)
        
        # Verify deletion
        response = requests.get(f'{self.base_url}/')
        self.assertIn('No students found', response.text)
    
    def test_multiple_students_display(self):
        """Test displaying multiple students"""
        students_data = [
            {'name': 'Alice', 'email': 'alice@ex.com', 'grade': '85'},
            {'name': 'Bob', 'email': 'bob@ex.com', 'grade': '92'},
            {'name': 'Carol', 'email': 'carol@ex.com', 'grade': '55'}
        ]
        
        for data in students_data:
            requests.post(f'{self.base_url}/students/add', data=urlencode(data))
        
        response = requests.get(f'{self.base_url}/')
        
        self.assertIn('Alice', response.text)
        self.assertIn('Bob', response.text)
        self.assertIn('Carol', response.text)
        self.assertEqual(response.text.count('<tr>'), 4)  # 1 header + 3 students
    
    def test_pass_fail_display(self):
        """Test pass/fail status display"""
        pass_student = {'name': 'Pass Student', 'email': 'pass@ex.com', 'grade': '75'}
        fail_student = {'name': 'Fail Student', 'email': 'fail@ex.com', 'grade': '45'}
        
        requests.post(f'{self.base_url}/students/add', data=urlencode(pass_student))
        requests.post(f'{self.base_url}/students/add', data=urlencode(fail_student))
        
        response = requests.get(f'{self.base_url}/')
        
        # Should have both Pass and Fail statuses
        pass_count = response.text.count('class="pass"')
        fail_count = response.text.count('class="fail"')
        
        self.assertGreater(pass_count, 0)
        self.assertGreater(fail_count, 0)
    
    def test_404_invalid_edit(self):
        """Test 404 for invalid student ID"""
        response = requests.get(f'{self.base_url}/students/edit?id=invalid')
        
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'requests', '-q'])
    
    unittest.main()
