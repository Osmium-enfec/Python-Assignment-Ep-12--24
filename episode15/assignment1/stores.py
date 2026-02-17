"""
EPISODE 15 - Data Persistence Module
Handles loading and saving student data
"""

import json
import os
from threading import Lock

STUDENTS_FILE = 'students_ep15.json'
FILE_LOCK = Lock()


def load_students():
    """Load students from JSON file"""
    if not os.path.exists(STUDENTS_FILE):
        return {}
    
    try:
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading students: {e}")
        return {}


def save_students(students):
    """Save students to JSON file (thread-safe)"""
    try:
        with FILE_LOCK:
            with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(students, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving students: {e}")
        return False


def delete_file():
    """Delete the students file (for testing)"""
    if os.path.exists(STUDENTS_FILE):
        os.remove(STUDENTS_FILE)
