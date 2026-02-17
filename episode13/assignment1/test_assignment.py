"""
EPISODE 13 - ASSIGNMENT 1: Test Suite
Tests for variable scopes and data persistence
"""

import unittest
import json
import os
from urllib.parse import urlencode
from http.server import ThreadingHTTPServer
import threading
import time
import requests
from solution import StudentHandler, create_validator, STUDENTS
import stores


class TestVariableScopes(unittest.TestCase):
    """Test variable scope concepts"""
    
    def test_closure_validator_basic(self):
        """Test closure validator with valid data"""
        validator = create_validator()
        
        student = {'id': '101', 'name': 'John Doe', 'grade': '85'}
        is_valid, errors = validator(student)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_closure_validator_duplicate_id(self):
        """Test closure validator rejects duplicate IDs"""
        validator = create_validator()
        
        student1 = {'id': '101', 'name': 'John', 'grade': '85'}
        student2 = {'id': '101', 'name': 'Jane', 'grade': '90'}
        
        is_valid1, errors1 = validator(student1)
        is_valid2, errors2 = validator(student2)
        
        self.assertTrue(is_valid1)
        self.assertFalse(is_valid2)
        self.assertTrue(any('already exists' in e for e in errors2))
    
    def test_closure_validator_invalid_name(self):
        """Test closure validator rejects invalid name"""
        validator = create_validator()
        
        student = {'id': '101', 'name': 'A', 'grade': '85'}
        is_valid, errors = validator(student)
        
        self.assertFalse(is_valid)
        self.assertTrue(any('2-50 characters' in e for e in errors))
    
    def test_closure_validator_invalid_grade(self):
        """Test closure validator rejects invalid grade"""
        validator = create_validator()
        
        student = {'id': '101', 'name': 'John', 'grade': '150'}
        is_valid, errors = validator(student)
        
        self.assertFalse(is_valid)
        self.assertTrue(any('0-100' in e for e in errors))
    
    def test_closure_validator_invalid_id(self):
        """Test closure validator rejects invalid ID"""
        validator = create_validator()
        
        student = {'id': '0', 'name': 'John', 'grade': '85'}
        is_valid, errors = validator(student)
        
        self.assertFalse(is_valid)
        self.assertTrue(any('positive' in e for e in errors))


class TestDataPersistence(unittest.TestCase):
    """Test data persistence"""
    
    def setUp(self):
        """Clean up before each test"""
        stores.delete_file()
    
    def tearDown(self):
        """Clean up after each test"""
        stores.delete_file()
    
    def test_save_and_load_students(self):
        """Test saving and loading students"""
        students = [
            {'id': 101, 'name': 'John', 'grade': 85.0},
            {'id': 102, 'name': 'Jane', 'grade': 90.0}
        ]
        
        # Save
        success = stores.save_students(students)
        self.assertTrue(success)
        
        # Load
        loaded = stores.load_students()
        self.assertEqual(loaded, students)
    
    def test_load_nonexistent_file(self):
        """Test loading when file doesn't exist"""
        stores.delete_file()
        students = stores.load_students()
        
        self.assertEqual(students, [])
    
    def test_save_empty_list(self):
        """Test saving empty student list"""
        success = stores.save_students([])
        
        self.assertTrue(success)
        self.assertEqual(stores.load_students(), [])


class TestStudentHandler(unittest.TestCase):
    """Test HTTP student handler"""
    
    @classmethod
    def setUpClass(cls):
        """Start server"""
        # Create fresh handler class for this test
        class FreshStudentHandler(StudentHandler):
            validator = create_validator()  # Fresh validator
        
        cls.server = ThreadingHTTPServer(('localhost', 8006), FreshStudentHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.5)
        
        cls.base_url = 'http://localhost:8006'
    
    @classmethod
    def tearDownClass(cls):
        """Shutdown server"""
        cls.server.shutdown()
    
    def setUp(self):
        """Clear data before each test"""
        from solution import STUDENTS
        stores.delete_file()
        STUDENTS.clear()
        # Reset validator since it holds state
        from solution import StudentHandler
        StudentHandler.validator = create_validator()
    
    def tearDown(self):
        """Clean up after each test"""
        from solution import STUDENTS
        stores.delete_file()
        STUDENTS.clear()
    
    def test_add_valid_student(self):
        """Test adding valid student"""
        data = {
            'id': '101',
            'name': 'John Doe',
            'grade': '85'
        }
        response = requests.post(f'{self.base_url}/add-student', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['student']['name'], 'John Doe')
    
    def test_add_duplicate_id(self):
        """Test adding student with duplicate ID"""
        data1 = {'id': '101', 'name': 'John', 'grade': '85'}
        data2 = {'id': '101', 'name': 'Jane', 'grade': '90'}
        
        response1 = requests.post(f'{self.base_url}/add-student', data=urlencode(data1))
        response2 = requests.post(f'{self.base_url}/add-student', data=urlencode(data2))
        
        result1 = response1.json()
        result2 = response2.json()
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 400)
        self.assertTrue(any('exists' in e for e in result2['errors']))
    
    def test_invalid_grade_range(self):
        """Test invalid grade range"""
        data = {
            'id': '101',
            'name': 'John',
            'grade': '150'
        }
        response = requests.post(f'{self.base_url}/add-student', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(any('0-100' in e for e in result['errors']))
    
    def test_invalid_name_length(self):
        """Test invalid name length"""
        data = {
            'id': '101',
            'name': 'A',
            'grade': '85'
        }
        response = requests.post(f'{self.base_url}/add-student', data=urlencode(data))
        result = response.json()
        
        self.assertEqual(response.status_code, 400)
    
    def test_data_persists(self):
        """Test data is persisted to file"""
        data = {
            'id': '101',
            'name': 'John Doe',
            'grade': '85'
        }
        requests.post(f'{self.base_url}/add-student', data=urlencode(data))
        
        # Check file was created
        self.assertTrue(os.path.exists('students.json'))
        
        # Verify content
        loaded = stores.load_students()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]['name'], 'John Doe')
    
    def test_invalid_endpoint(self):
        """Test invalid endpoint"""
        response = requests.post(f'{self.base_url}/invalid')
        
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'requests', '-q'])
    
    unittest.main()
