import sqlite3
import pandas as pd

# Existing database initialization function
def init_db():
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    
    # Create enrollments table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS enrollments
                 (student_id TEXT, course_code TEXT, enrollment_date TEXT,
                  PRIMARY KEY (student_id, course_code))''')
    
    # Create course_capacity table to store seat allocations
    c.execute('''CREATE TABLE IF NOT EXISTS course_capacity
                 (course_code TEXT PRIMARY KEY, capacity INTEGER)''')
    
    # Populate course_capacity with default values if not exists
    courses = [
        'CSE228', 'CSE3114', 'CSE3005', 'CSE3115', 'CSE3014', 
        'CSE3112', 'CSE243', 'CSE3111', 'CSE6002', 'BCA217',
        'CSA3020', 'CSE3113', 'CSE3134', 'CSE3001', 'CSE3036',
        'CSE5006', 'CSE3106', 'CSE2037', 'CSE2039', 'MAT1002',
        'CSE3152', 'CSE2060', 'CSE2015', 'CSE3087'
    ]
    
    # Check if course_capacity is empty
    c.execute("SELECT COUNT(*) FROM course_capacity")
    if c.fetchone()[0] == 0:
        # Default capacity of 60 for each course
        for course in courses:
            c.execute("INSERT OR REPLACE INTO course_capacity (course_code, capacity) VALUES (?, ?)", (course, 60))
    
    conn.commit()
    conn.close()

# Get course capacity
def get_course_capacity(course_code):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("SELECT capacity FROM course_capacity WHERE course_code = ?", (course_code,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 60  # Default to 60 if not found

# Update course capacity
def update_course_capacity(course_code, new_capacity):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO course_capacity (course_code, capacity) VALUES (?, ?)", 
              (course_code, new_capacity))
    conn.commit()
    conn.close()

# Get course enrollment
def get_course_enrollment(course_code):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM enrollments WHERE course_code = ?", (course_code,))
    count = c.fetchone()[0]
    conn.close()
    return count

# Delete enrollment for a specific student from a course
def delete_enrollment(student_id, course_code):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("DELETE FROM enrollments WHERE student_id = ? AND course_code = ?", (student_id, course_code))
    conn.commit()
    conn.close()

# Delete all enrollments for a specific course
def delete_all_enrollments_for_course(course_code):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("DELETE FROM enrollments WHERE course_code = ?", (course_code,))
    conn.commit()
    conn.close()

# Get all enrollments
def get_all_enrollments():
    conn = sqlite3.connect('courses.db')
    df = pd.read_sql_query("SELECT * FROM enrollments", conn)
    conn.close()
    return df