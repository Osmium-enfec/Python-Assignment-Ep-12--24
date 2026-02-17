"""
EPISODE 13 - ASSIGNMENT 1: Data persistence module
"""

import json
import os
from threading import Lock

STUDENTS_FILE = 'students.json'
FILE_LOCK = Lock()


def load_students():
    """
    Load students from JSON file
    
    Returns:
        list: List of student dictionaries
    """
    if not os.path.exists(STUDENTS_FILE):
        return []
    
    try:
        with open(STUDENTS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading students: {e}")
        return []


def save_students(students):
    """
    Save students to JSON file (thread-safe)
    
    Args:
        students (list): List of student dictionaries
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with FILE_LOCK:
            with open(STUDENTS_FILE, 'w') as f:
                json.dump(students, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving students: {e}")
        return False


def delete_file():
    """Delete the students file (for testing)"""
    if os.path.exists(STUDENTS_FILE):
        os.remove(STUDENTS_FILE)
