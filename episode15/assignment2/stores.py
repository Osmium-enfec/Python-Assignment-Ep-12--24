"""
Stores module for Episode 15 Assignment 2
Extended data persistence with search and filter operations
"""

import json
import os
import threading

STUDENTS_FILE = 'students_data.json'
file_lock = threading.Lock()


def load_students():
    """Load students from JSON file"""
    with file_lock:
        if os.path.exists(STUDENTS_FILE):
            with open(STUDENTS_FILE, 'r') as f:
                return json.load(f)
    return {}


def save_students(students):
    """Save students to JSON file"""
    with file_lock:
        with open(STUDENTS_FILE, 'w') as f:
            json.dump(students, f, indent=2)


def search_students(students, query):
    """Search students by name or roll number"""
    if not query:
        return students
    
    query_lower = query.lower()
    results = {}
    
    for roll_no, student in students.items():
        if (query_lower in roll_no.lower() or 
            query_lower in student.get('name', '').lower()):
            results[roll_no] = student
    
    return results


def filter_students(students, criteria):
    """Filter students by various criteria"""
    results = students.copy()
    
    # Filter by minimum grade
    if 'grade_min' in criteria:
        try:
            min_grade = float(criteria['grade_min'])
            results = {k: v for k, v in results.items() 
                      if float(v.get('grade', 0)) >= min_grade}
        except (ValueError, KeyError):
            pass
    
    # Filter by maximum grade
    if 'grade_max' in criteria:
        try:
            max_grade = float(criteria['grade_max'])
            results = {k: v for k, v in results.items() 
                      if float(v.get('grade', 0)) <= max_grade}
        except (ValueError, KeyError):
            pass
    
    # Filter by minimum attendance
    if 'attendance_min' in criteria:
        try:
            min_att = float(criteria['attendance_min'])
            results = {k: v for k, v in results.items() 
                      if float(v.get('attendance', 0)) >= min_att}
        except (ValueError, KeyError):
            pass
    
    # Filter by maximum attendance
    if 'attendance_max' in criteria:
        try:
            max_att = float(criteria['attendance_max'])
            results = {k: v for k, v in results.items() 
                      if float(v.get('attendance', 0)) <= max_att}
        except (ValueError, KeyError):
            pass
    
    # Filter by fees paid status
    if 'fees_paid' in criteria:
        fees_paid = criteria['fees_paid'].lower() == 'true'
        results = {k: v for k, v in results.items() 
                  if v.get('fees_paid') == fees_paid}
    
    return results


def sort_students(students, key='roll_no', reverse=False):
    """Sort students by key"""
    if key == 'name':
        return dict(sorted(students.items(), 
                          key=lambda x: x[1].get('name', ''), 
                          reverse=reverse))
    elif key == 'grade':
        return dict(sorted(students.items(), 
                          key=lambda x: float(x[1].get('grade', 0)), 
                          reverse=reverse))
    elif key == 'attendance':
        return dict(sorted(students.items(), 
                          key=lambda x: float(x[1].get('attendance', 0)), 
                          reverse=reverse))
    else:  # roll_no
        return dict(sorted(students.items(), reverse=reverse))


def get_statistics(students):
    """Calculate statistics from students data"""
    if not students:
        return {
            'total': 0,
            'average_grade': 0,
            'average_attendance': 0,
            'pass_count': 0,
            'fail_count': 0,
            'high_attendance_count': 0,
            'low_attendance_count': 0,
            'total_fees_paid': 0,
            'total_fees_pending': 0
        }
    
    total = len(students)
    grades = [float(s.get('grade', 0)) for s in students.values()]
    attendance = [float(s.get('attendance', 0)) for s in students.values()]
    
    avg_grade = sum(grades) / total if total > 0 else 0
    avg_att = sum(attendance) / total if total > 0 else 0
    
    pass_count = len([g for g in grades if g >= 60])
    fail_count = total - pass_count
    high_att = len([a for a in attendance if a >= 80])
    low_att = total - high_att
    
    fees_paid = len([s for s in students.values() if s.get('fees_paid')])
    fees_pending = total - fees_paid
    
    return {
        'total': total,
        'average_grade': round(avg_grade, 2),
        'average_attendance': round(avg_att, 2),
        'pass_count': pass_count,
        'fail_count': fail_count,
        'high_attendance_count': high_att,
        'low_attendance_count': low_att,
        'total_fees_paid': fees_paid,
        'total_fees_pending': fees_pending
    }
