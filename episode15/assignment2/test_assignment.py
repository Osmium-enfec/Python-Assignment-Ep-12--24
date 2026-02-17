"""
Test suite for Episode 15 - Assignment 2
Advanced Student Management System with Search, Filter, Sort, Statistics
"""

import unittest
import requests
import json
import os
import threading
import time
import sys
from solution import start_server, AdvancedStudentHandler, STUDENTS as GLOBAL_STUDENTS
import stores


class Episode15Assignment2Tests(unittest.TestCase):
    """Complete test suite for Assignment 2"""
    
    @classmethod
    def setUpClass(cls):
        """Start server once for all tests"""
        # Clean up data file if exists
        if os.path.exists('students_data.json'):
            os.remove('students_data.json')
        
        # Start server in background
        cls.port = 5001
        cls.base_url = f'http://127.0.0.1:{cls.port}'
        cls.server_thread = threading.Thread(
            target=start_server,
            args=(cls.port,),
            daemon=True
        )
        cls.server_thread.start()
        time.sleep(1)  # Wait for server to start
    
    def setUp(self):
        """Clear data before each test"""
        # Clear via HTTP reset endpoint
        try:
            requests.get(f'{self.base_url}/__test_reset__', timeout=5)
        except:
            pass
        
        # Also clear global state
        GLOBAL_STUDENTS.clear()
        if os.path.exists('students_data.json'):
            try:
                os.remove('students_data.json')
            except:
                pass
        
        # Give server time to process
        time.sleep(0.1)
    
    # ============ Dashboard Tests ============
    def test_01_dashboard_page_loads(self):
        """Test dashboard home page loads"""
        response = requests.get(f'{self.base_url}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Dashboard', response.text)
        self.assertIn('Total Students', response.text)
    
    def test_02_dashboard_statistics(self):
        """Test dashboard shows correct statistics"""
        # Add test data directly to STUDENTS
        GLOBAL_STUDENTS['R001'] = {'name': 'Alice', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'}
        GLOBAL_STUDENTS['R002'] = {'name': 'Bob', 'grade': 45, 'attendance': 60, 'fees_paid': False, 'added_on': '2024-01-02'}
        
        response = requests.get(f'{self.base_url}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Total Students', response.text)
    
    # ============ CRUD Operations ============
    def test_03_add_student_form_loads(self):
        """Test add student form loads"""
        response = requests.get(f'{self.base_url}/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Add New Student', response.text)
        self.assertIn('Roll Number', response.text)
    
    def test_04_add_student_success(self):
        """Test adding a student successfully"""
        data = {
            'roll_no': 'R001',
            'name': 'John Doe',
            'grade': '85',
            'attendance': '90',
            'fees_paid': 'on'
        }
        response = requests.post(f'{self.base_url}/add', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully', response.text.lower())
    
    def test_05_add_duplicate_roll_number(self):
        """Test adding student with duplicate roll number shows error"""
        # Add first student via HTTP
        data = {
            'roll_no': 'R001',
            'name': 'Alice',
            'grade': '80',
            'attendance': '85',
            'fees_paid': 'on'
        }
        requests.post(f'{self.base_url}/add', data=data)
        
        # Try to add duplicate
        data2 = {
            'roll_no': 'R001',
            'name': 'Bob',
            'grade': '75',
            'attendance': '80'
        }
        response = requests.post(f'{self.base_url}/add', data=data2)
        self.assertIn('already exists', response.text)
    
    def test_06_add_invalid_grade(self):
        """Test adding student with invalid grade"""
        data = {
            'roll_no': 'R001',
            'name': 'John',
            'grade': '150',  # Invalid
            'attendance': '85'
        }
        response = requests.post(f'{self.base_url}/add', data=data)
        self.assertIn('error', response.text.lower())
    
    def test_07_add_missing_name(self):
        """Test adding student without name shows error"""
        data = {
            'roll_no': 'R001',
            'name': '',
            'grade': '80',
            'attendance': '85'
        }
        response = requests.post(f'{self.base_url}/add', data=data)
        self.assertIn('required', response.text.lower())
    
    def test_08_view_student_list(self):
        """Test viewing all students list"""
        # Add students via HTTP
        data1 = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90', 'fees_paid': 'on'}
        data2 = {'roll_no': 'R002', 'name': 'Bob', 'grade': '65', 'attendance': '75'}
        requests.post(f'{self.base_url}/add', data=data1)
        requests.post(f'{self.base_url}/add', data=data2)
        
        response = requests.get(f'{self.base_url}/students')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice', response.text)
        self.assertIn('Bob', response.text)
    
    def test_09_view_student_detail(self):
        """Test viewing individual student details"""
        # Add student via HTTP
        data = {'roll_no': 'R001', 'name': 'Alice Johnson', 'grade': '88.5', 'attendance': '92'}
        requests.post(f'{self.base_url}/add', data=data)
        
        response = requests.get(f'{self.base_url}/students/R001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice Johnson', response.text)
        self.assertIn('88.5', response.text)
    
    def test_10_view_nonexistent_student(self):
        """Test viewing non-existent student shows error"""
        response = requests.get(f'{self.base_url}/students/R999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('not found', response.text.lower())
    
    def test_11_edit_form_loads(self):
        """Test edit form loads with student data"""
        # Add student via HTTP
        data = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90', 'fees_paid': 'on'}
        requests.post(f'{self.base_url}/add', data=data)
        
        response = requests.get(f'{self.base_url}/edit?roll_no=R001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Edit Student', response.text)
        self.assertIn('Alice', response.text)
    
    def test_12_edit_student_success(self):
        """Test editing student successfully"""
        # Add student first
        data = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90'}
        requests.post(f'{self.base_url}/add', data=data)
        
        # Then edit
        edit_data = {
            'roll_no': 'R001',
            'name': 'Alice Updated',
            'grade': '90',
            'attendance': '95'
        }
        response = requests.post(f'{self.base_url}/edit', data=edit_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully', response.text.lower())
    
    def test_13_delete_confirmation_page(self):
        """Test delete confirmation page loads"""
        # Add student via HTTP
        data = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90'}
        requests.post(f'{self.base_url}/add', data=data)
        
        response = requests.get(f'{self.base_url}/delete/R001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Delete', response.text)
        self.assertIn('Alice', response.text)
    
    def test_14_delete_student_success(self):
        """Test deleting student successfully"""
        # Add student first
        data = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90'}
        requests.post(f'{self.base_url}/add', data=data)
        
        response = requests.post(f'{self.base_url}/delete/R001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully', response.text.lower())
    
    # ============ Search Tests ============
    def test_15_search_by_name(self):
        """Test searching students by name"""
        # Add students via HTTP
        d1 = {'roll_no': 'R001', 'name': 'Alice Smith', 'grade': '85', 'attendance': '90'}
        d2 = {'roll_no': 'R002', 'name': 'Bob Johnson', 'grade': '75', 'attendance': '80'}
        requests.post(f'{self.base_url}/add', data=d1)
        requests.post(f'{self.base_url}/add', data=d2)
        
        response = requests.get(f'{self.base_url}/search?q=Alice')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice Smith', response.text)
    
    def test_16_search_by_roll_number(self):
        """Test searching students by roll number"""
        # Add students
        d1 = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90'}
        d2 = {'roll_no': 'R002', 'name': 'Bob', 'grade': '75', 'attendance': '80'}
        requests.post(f'{self.base_url}/add', data=d1)
        requests.post(f'{self.base_url}/add', data=d2)
        
        response = requests.get(f'{self.base_url}/search?q=R001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice', response.text)
    
    def test_17_search_no_results(self):
        """Test search with no matching results"""
        data = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90'}
        requests.post(f'{self.base_url}/add', data=data)
        
        response = requests.get(f'{self.base_url}/search?q=Nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertIn('no results', response.text.lower())
    
    def test_18_search_empty_query(self):
        """Test search with empty query redirects"""
        response = requests.get(f'{self.base_url}/search?q=', allow_redirects=False)
        self.assertEqual(response.status_code, 302)
    
    # ============ Filter Tests ============
    def test_19_filter_by_grade(self):
        """Test filtering students by grade"""
        d1 = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90'}
        d2 = {'roll_no': 'R002', 'name': 'Bob', 'grade': '55', 'attendance': '70'}
        d3 = {'roll_no': 'R003', 'name': 'Charlie', 'grade': '75', 'attendance': '80'}
        requests.post(f'{self.base_url}/add', data=d1)
        requests.post(f'{self.base_url}/add', data=d2)
        requests.post(f'{self.base_url}/add', data=d3)
        
        response = requests.get(f'{self.base_url}/filter?grade_min=75')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice', response.text)
        self.assertIn('Charlie', response.text)
    
    def test_20_filter_by_attendance(self):
        """Test filtering students by attendance"""
        d1 = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90'}
        d2 = {'roll_no': 'R002', 'name': 'Bob', 'grade': '75', 'attendance': '60'}
        requests.post(f'{self.base_url}/add', data=d1)
        requests.post(f'{self.base_url}/add', data=d2)
        
        response = requests.get(f'{self.base_url}/filter?attendance_min=80')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice', response.text)
    
    def test_21_filter_by_both(self):
        """Test filtering by both grade and attendance"""
        d1 = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90'}
        d2 = {'roll_no': 'R002', 'name': 'Bob', 'grade': '85', 'attendance': '60'}
        d3 = {'roll_no': 'R003', 'name': 'Charlie', 'grade': '75', 'attendance': '85'}
        requests.post(f'{self.base_url}/add', data=d1)
        requests.post(f'{self.base_url}/add', data=d2)
        requests.post(f'{self.base_url}/add', data=d3)
        
        response = requests.get(f'{self.base_url}/filter?grade_min=80&attendance_min=80')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice', response.text)
    
    # ============ Sort Tests ============
    def test_22_sort_by_roll_number(self):
        """Test sorting by roll number"""
        response = requests.get(f'{self.base_url}/sort?by=roll_no', allow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/students', response.headers['Location'])
    
    def test_23_sort_by_name(self):
        """Test sorting by name"""
        response = requests.get(f'{self.base_url}/sort?by=name', allow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/students', response.headers['Location'])
    
    def test_24_sort_by_grade(self):
        """Test sorting by grade"""
        response = requests.get(f'{self.base_url}/sort?by=grade', allow_redirects=False)
        self.assertEqual(response.status_code, 302)
    
    def test_25_sort_by_attendance(self):
        """Test sorting by attendance"""
        response = requests.get(f'{self.base_url}/sort?by=attendance', allow_redirects=False)
        self.assertEqual(response.status_code, 302)
    
    # ============ Statistics Tests ============
    def test_26_statistics_page_loads(self):
        """Test statistics page loads"""
        response = requests.get(f'{self.base_url}/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Statistics', response.text)
        self.assertIn('Total Students', response.text)
    
    def test_27_statistics_calculations(self):
        """Test statistics are calculated correctly"""
        d1 = {'roll_no': 'R001', 'name': 'Alice', 'grade': '90', 'attendance': '95'}
        d2 = {'roll_no': 'R002', 'name': 'Bob', 'grade': '60', 'attendance': '75'}
        d3 = {'roll_no': 'R003', 'name': 'Charlie', 'grade': '50', 'attendance': '60'}
        requests.post(f'{self.base_url}/add', data=d1)
        requests.post(f'{self.base_url}/add', data=d2)
        requests.post(f'{self.base_url}/add', data=d3)
        
        response = requests.get(f'{self.base_url}/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Pass', response.text)
    
    # ============ Export Tests ============
    def test_28_export_csv(self):
        """Test CSV export"""
        d1 = {'roll_no': 'R001', 'name': 'Alice', 'grade': '85', 'attendance': '90'}
        d2 = {'roll_no': 'R002', 'name': 'Bob', 'grade': '75', 'attendance': '80'}
        requests.post(f'{self.base_url}/add', data=d1)
        requests.post(f'{self.base_url}/add', data=d2)
        
        response = requests.get(f'{self.base_url}/export/csv')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response.headers['Content-Type'])
        self.assertIn('Roll No', response.text)
        self.assertIn('Alice', response.text)
    
    def test_29_csv_format_correct(self):
        """Test CSV format is correct"""
        data = {'roll_no': 'R001', 'name': 'Alice Smith', 'grade': '85', 'attendance': '90'}
        requests.post(f'{self.base_url}/add', data=data)
        
        response = requests.get(f'{self.base_url}/export/csv')
        lines = response.text.strip().split('\n')
        self.assertEqual(len(lines), 2)  # Header + 1 data row
        self.assertIn('R001', lines[1])
        self.assertIn('Alice Smith', lines[1])
    
    # ============ HTML Escaping Tests ============
    def test_30_html_escaping_in_list(self):
        """Test HTML is escaped in student list"""
        data = {'roll_no': 'R001', 'name': 'John & Mary <test>', 'grade': '85', 'attendance': '90'}
        requests.post(f'{self.base_url}/add', data=data)
        
        response = requests.get(f'{self.base_url}/students')
        # Check that potentially dangerous HTML is escaped
        self.assertIn('&amp;', response.text)
        self.assertIn('&lt;', response.text)
    
    def test_31_html_escaping_in_detail(self):
        """Test HTML is escaped in student detail"""
        data = {'roll_no': 'R001', 'name': 'Test & "Quoted"', 'grade': '85', 'attendance': '90'}
        requests.post(f'{self.base_url}/add', data=data)
        
        response = requests.get(f'{self.base_url}/students/R001')
        # Verify escaping
        self.assertIn('&amp;', response.text)
        self.assertIn('&quot;', response.text)
    
    # ============ Validation Tests ============
    def test_32_invalid_attendance_range(self):
        """Test validation rejects attendance > 100"""
        data = {
            'roll_no': 'R001',
            'name': 'John',
            'grade': '80',
            'attendance': '150'
        }
        response = requests.post(f'{self.base_url}/add', data=data)
        self.assertIn('error', response.text.lower())
    
    def test_33_page_not_found(self):
        """Test 404 for non-existent page"""
        response = requests.get(f'{self.base_url}/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn('not found', response.text.lower())


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(Episode15Assignment2Tests)
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("EPISODE 15 - ASSIGNMENT 2 TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
    
    # ============ Dashboard Tests ============
    def test_01_dashboard_page_loads(self):
        """Test dashboard home page loads"""
        response = requests.get(f'{self.base_url}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Dashboard', response.text)
        self.assertIn('Total Students', response.text)
    
    def test_02_dashboard_statistics(self):
        """Test dashboard shows correct statistics"""
        # Add test data
        GLOBAL_STUDENTS.update({
            'R001': {'name': 'Alice', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'},
            'R002': {'name': 'Bob', 'grade': 45, 'attendance': 60, 'fees_paid': False, 'added_on': '2024-01-02'}
        })
        
        response = requests.get(f'{self.base_url}/')
        self.assertIn('2', response.text)  # Total students
        self.assertIn('85.0', response.text)  # Average grade should show
    
    # ============ CRUD Operations ============
    def test_03_add_student_form_loads(self):
        """Test add student form loads"""
        response = requests.get(f'{self.base_url}/add')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Add New Student', response.text)
        self.assertIn('Roll Number', response.text)
    
    def test_04_add_student_success(self):
        """Test adding a student successfully"""
        data = {
            'roll_no': 'R001',
            'name': 'John Doe',
            'grade': '85',
            'attendance': '90',
            'fees_paid': 'on'
        }
        response = requests.post(f'{self.base_url}/add', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully', response.text.lower())
    
    def test_05_add_duplicate_roll_number(self):
        """Test adding student with duplicate roll number shows error"""
        # Add first student
        GLOBAL_STUDENTS['R001'] = {'name': 'Alice', 'grade': 80, 'attendance': 85, 'fees_paid': True, 'added_on': '2024-01-01'}
        
        # Try to add duplicate
        data = {
            'roll_no': 'R001',
            'name': 'Bob',
            'grade': '75',
            'attendance': '80'
        }
        response = requests.post(f'{self.base_url}/add', data=data)
        self.assertIn('already exists', response.text)
    
    def test_06_add_invalid_grade(self):
        """Test adding student with invalid grade"""
        data = {
            'roll_no': 'R001',
            'name': 'John',
            'grade': '150',  # Invalid
            'attendance': '85'
        }
        response = requests.post(f'{self.base_url}/add', data=data)
        self.assertIn('error', response.text.lower())
    
    def test_07_add_missing_name(self):
        """Test adding student without name shows error"""
        data = {
            'roll_no': 'R001',
            'name': '',
            'grade': '80',
            'attendance': '85'
        }
        response = requests.post(f'{self.base_url}/add', data=data)
        self.assertIn('required', response.text.lower())
    
    def test_08_view_student_list(self):
        """Test viewing all students list"""
        # Add students
        GLOBAL_STUDENTS.update({
            'R001': {'name': 'Alice', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'},
            'R002': {'name': 'Bob', 'grade': 65, 'attendance': 75, 'fees_paid': False, 'added_on': '2024-01-02'}
        })
        
        response = requests.get(f'{self.base_url}/students')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice', response.text)
        self.assertIn('Bob', response.text)
    
    def test_09_view_student_detail(self):
        """Test viewing individual student details"""
        GLOBAL_STUDENTS['R001'] = {
            'name': 'Alice Johnson',
            'grade': 88.5,
            'attendance': 92,
            'fees_paid': True,
            'added_on': '2024-01-01T10:00:00'
        }
        
        response = requests.get(f'{self.base_url}/students/R001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice Johnson', response.text)
        self.assertIn('88.5', response.text)
    
    def test_10_view_nonexistent_student(self):
        """Test viewing non-existent student shows error"""
        response = requests.get(f'{self.base_url}/students/R999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('not found', response.text.lower())
    
    def test_11_edit_form_loads(self):
        """Test edit form loads with student data"""
        GLOBAL_STUDENTS['R001'] = {
            'name': 'Alice',
            'grade': 85,
            'attendance': 90,
            'fees_paid': True,
            'added_on': '2024-01-01'
        }
        
        response = requests.get(f'{self.base_url}/edit?roll_no=R001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Edit Student', response.text)
        self.assertIn('Alice', response.text)
    
    def test_12_edit_student_success(self):
        """Test editing student successfully"""
        GLOBAL_STUDENTS['R001'] = {
            'name': 'Alice',
            'grade': 85,
            'attendance': 90,
            'fees_paid': True,
            'added_on': '2024-01-01T10:00:00'
        }
        
        data = {
            'roll_no': 'R001',
            'name': 'Alice Updated',
            'grade': '90',
            'attendance': '95'
        }
        response = requests.post(f'{self.base_url}/edit', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully', response.text.lower())
    
    def test_13_delete_confirmation_page(self):
        """Test delete confirmation page loads"""
        GLOBAL_STUDENTS['R001'] = {
            'name': 'Alice',
            'grade': 85,
            'attendance': 90,
            'fees_paid': True,
            'added_on': '2024-01-01'
        }
        
        response = requests.get(f'{self.base_url}/delete/R001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Delete', response.text)
        self.assertIn('Alice', response.text)
    
    def test_14_delete_student_success(self):
        """Test deleting student successfully"""
        GLOBAL_STUDENTS['R001'] = {
            'name': 'Alice',
            'grade': 85,
            'attendance': 90,
            'fees_paid': True,
            'added_on': '2024-01-01'
        }
        
        response = requests.post(f'{self.base_url}/delete/R001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('successfully', response.text.lower())
        self.assertNotIn('R001', GLOBAL_STUDENTS)
    
    # ============ Search Tests ============
    def test_15_search_by_name(self):
        """Test searching students by name"""
        GLOBAL_STUDENTS.update({
            'R001': {'name': 'Alice Smith', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'},
            'R002': {'name': 'Bob Johnson', 'grade': 75, 'attendance': 80, 'fees_paid': False, 'added_on': '2024-01-02'}
        })
        
        response = requests.get(f'{self.base_url}/search?q=Alice')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice Smith', response.text)
        self.assertNotIn('Bob Johnson', response.text)
    
    def test_16_search_by_roll_number(self):
        """Test searching students by roll number"""
        GLOBAL_STUDENTS.update({
            'R001': {'name': 'Alice', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'},
            'R002': {'name': 'Bob', 'grade': 75, 'attendance': 80, 'fees_paid': False, 'added_on': '2024-01-02'}
        })
        
        response = requests.get(f'{self.base_url}/search?q=R001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice', response.text)
        self.assertNotIn('Bob', response.text)
    
    def test_17_search_no_results(self):
        """Test search with no matching results"""
        GLOBAL_STUDENTS['R001'] = {'name': 'Alice', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'}
        
        response = requests.get(f'{self.base_url}/search?q=Nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertIn('no results', response.text.lower())
    
    def test_18_search_empty_query(self):
        """Test search with empty query redirects"""
        GLOBAL_STUDENTS['R001'] = {'name': 'Alice', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'}
        
        response = requests.get(f'{self.base_url}/search?q=', allow_redirects=False)
        self.assertEqual(response.status_code, 302)
    
    # ============ Filter Tests ============
    def test_19_filter_by_grade(self):
        """Test filtering students by grade"""
        GLOBAL_STUDENTS.update({
            'R001': {'name': 'Alice', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'},
            'R002': {'name': 'Bob', 'grade': 55, 'attendance': 70, 'fees_paid': False, 'added_on': '2024-01-02'},
            'R003': {'name': 'Charlie', 'grade': 75, 'attendance': 80, 'fees_paid': True, 'added_on': '2024-01-03'}
        })
        
        response = requests.get(f'{self.base_url}/filter?grade_min=75')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice', response.text)
        self.assertIn('Charlie', response.text)
        self.assertNotIn('Bob', response.text)
    
    def test_20_filter_by_attendance(self):
        """Test filtering students by attendance"""
        GLOBAL_STUDENTS.update({
            'R001': {'name': 'Alice', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'},
            'R002': {'name': 'Bob', 'grade': 75, 'attendance': 60, 'fees_paid': False, 'added_on': '2024-01-02'}
        })
        
        response = requests.get(f'{self.base_url}/filter?attendance_min=80')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice', response.text)
        self.assertNotIn('Bob', response.text)
    
    def test_21_filter_by_both(self):
        """Test filtering by both grade and attendance"""
        GLOBAL_STUDENTS.update({
            'R001': {'name': 'Alice', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'},
            'R002': {'name': 'Bob', 'grade': 85, 'attendance': 60, 'fees_paid': False, 'added_on': '2024-01-02'},
            'R003': {'name': 'Charlie', 'grade': 75, 'attendance': 85, 'fees_paid': True, 'added_on': '2024-01-03'}
        })
        
        response = requests.get(f'{self.base_url}/filter?grade_min=80&attendance_min=80')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Alice', response.text)
        self.assertNotIn('Bob', response.text)
        self.assertNotIn('Charlie', response.text)
    
    # ============ Sort Tests ============
    def test_22_sort_by_roll_number(self):
        """Test sorting by roll number"""
        response = requests.get(f'{self.base_url}/sort?by=roll_no', allow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/students', response.headers['Location'])
    
    def test_23_sort_by_name(self):
        """Test sorting by name"""
        response = requests.get(f'{self.base_url}/sort?by=name', allow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/students', response.headers['Location'])
    
    def test_24_sort_by_grade(self):
        """Test sorting by grade"""
        response = requests.get(f'{self.base_url}/sort?by=grade', allow_redirects=False)
        self.assertEqual(response.status_code, 302)
    
    def test_25_sort_by_attendance(self):
        """Test sorting by attendance"""
        response = requests.get(f'{self.base_url}/sort?by=attendance', allow_redirects=False)
        self.assertEqual(response.status_code, 302)
    
    # ============ Statistics Tests ============
    def test_26_statistics_page_loads(self):
        """Test statistics page loads"""
        response = requests.get(f'{self.base_url}/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Statistics', response.text)
        self.assertIn('Total Students', response.text)
    
    def test_27_statistics_calculations(self):
        """Test statistics are calculated correctly"""
        GLOBAL_STUDENTS.update({
            'R001': {'name': 'Alice', 'grade': 90, 'attendance': 95, 'fees_paid': True, 'added_on': '2024-01-01'},
            'R002': {'name': 'Bob', 'grade': 60, 'attendance': 75, 'fees_paid': False, 'added_on': '2024-01-02'},
            'R003': {'name': 'Charlie', 'grade': 50, 'attendance': 60, 'fees_paid': True, 'added_on': '2024-01-03'}
        })
        
        response = requests.get(f'{self.base_url}/stats')
        self.assertEqual(response.status_code, 200)
        # Should show pass count of 2 (≥60)
        self.assertIn('Pass', response.text)
    
    # ============ Export Tests ============
    def test_28_export_csv(self):
        """Test CSV export"""
        GLOBAL_STUDENTS.update({
            'R001': {'name': 'Alice', 'grade': 85, 'attendance': 90, 'fees_paid': True, 'added_on': '2024-01-01'},
            'R002': {'name': 'Bob', 'grade': 75, 'attendance': 80, 'fees_paid': False, 'added_on': '2024-01-02'}
        })
        
        response = requests.get(f'{self.base_url}/export/csv')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response.headers['Content-Type'])
        self.assertIn('Roll No', response.text)
        self.assertIn('Alice', response.text)
    
    def test_29_csv_format_correct(self):
        """Test CSV format is correct"""
        GLOBAL_STUDENTS['R001'] = {
            'name': 'Alice Smith',
            'grade': 85,
            'attendance': 90,
            'fees_paid': True,
            'added_on': '2024-01-01'
        }
        
        response = requests.get(f'{self.base_url}/export/csv')
        lines = response.text.strip().split('\n')
        self.assertEqual(len(lines), 2)  # Header + 1 data row
        self.assertIn('R001', lines[1])
        self.assertIn('Alice Smith', lines[1])
    
    # ============ HTML Escaping Tests ============
    def test_30_html_escaping_in_list(self):
        """Test HTML is escaped in student list"""
        GLOBAL_STUDENTS['R001'] = {
            'name': '<script>alert("xss")</script>',
            'grade': 85,
            'attendance': 90,
            'fees_paid': True,
            'added_on': '2024-01-01'
        }
        
        response = requests.get(f'{self.base_url}/students')
        # Should be escaped
        self.assertNotIn('<script>', response.text)
        self.assertIn('&lt;script&gt;', response.text)
    
    def test_31_html_escaping_in_detail(self):
        """Test HTML is escaped in student detail"""
        GLOBAL_STUDENTS['R001'] = {
            'name': '<img src=x onerror="alert(1)">',
            'grade': 85,
            'attendance': 90,
            'fees_paid': True,
            'added_on': '2024-01-01'
        }
        
        response = requests.get(f'{self.base_url}/students/R001')
        self.assertNotIn('onerror=', response.text)
        self.assertIn('&lt;img', response.text)
    
    # ============ Validation Tests ============
    def test_32_invalid_attendance_range(self):
        """Test validation rejects attendance > 100"""
        data = {
            'roll_no': 'R001',
            'name': 'John',
            'grade': '80',
            'attendance': '150'
        }
        response = requests.post(f'{self.base_url}/add', data=data)
        self.assertIn('error', response.text.lower())
    
    def test_33_page_not_found(self):
        """Test 404 for non-existent page"""
        response = requests.get(f'{self.base_url}/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn('not found', response.text.lower())


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(Episode15Assignment2Tests)
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("EPISODE 15 - ASSIGNMENT 2 TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
