import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS enrollments
                 (student_id TEXT, course_code TEXT, enrollment_date TEXT,
                  PRIMARY KEY (student_id, course_code))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS recommendations
                 (student_id TEXT, recommended_course TEXT,
                  PRIMARY KEY (student_id, recommended_course))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS course_capacity
                 (course_code TEXT PRIMARY KEY,
                  total_seats INTEGER DEFAULT 60,
                  last_modified TEXT)''')
    
    courses = ['CSE228', 'CSE3114', 'CSE3005', 'CSE3115', 'CSE3014', 
              'CSE3112', 'CSE243', 'CSE3111', 'CSE6002', 'BCA217',
              'CSA3020', 'CSE3113', 'CSE3134', 'CSE3001', 'CSE3036',
              'CSE5006', 'CSE3106', 'CSE2037', 'CSE2039', 'MAT1002',
              'CSE3152', 'CSE2060', 'CSE2015', 'CSE3087']
    
    for course in courses:
        c.execute("""INSERT OR IGNORE INTO course_capacity (course_code, total_seats)
                     VALUES (?, 60)""", (course,))
    
    conn.commit()
    conn.close()

def get_student_enrollments(student_id):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM enrollments WHERE student_id = ?", (student_id,))
    enrollments = c.fetchall()
    conn.close()
    return enrollments

def get_all_enrollments():
    conn = sqlite3.connect('courses.db')
    df = pd.read_sql_query("SELECT * FROM enrollments", conn)
    conn.close()
    return df

def delete_enrollment(student_id, course_code):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("DELETE FROM enrollments WHERE student_id = ? AND course_code = ?",
             (student_id, course_code))
    conn.commit()
    conn.close()

def delete_all_enrollments_for_course(course_code):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("DELETE FROM enrollments WHERE course_code = ?", (course_code,))
    conn.commit()
    conn.close()

def update_course_capacity(course_code, new_capacity):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("""UPDATE course_capacity 
                 SET total_seats = ?, last_modified = ?
                 WHERE course_code = ?""",
             (new_capacity, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), course_code))
    conn.commit()
    conn.close()
    return True

def get_course_capacity(course_code):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("SELECT total_seats FROM course_capacity WHERE course_code = ?", 
             (course_code,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 60

def get_all_course_capacities():
    conn = sqlite3.connect('courses.db')
    df = pd.read_sql_query("SELECT * FROM course_capacity", conn)
    conn.close()
    return df

def add_enrollment(student_id, course_code, enrollment_date):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    try:
        c.execute("""SELECT * FROM enrollments 
                    WHERE student_id = ? AND course_code = ?""", 
                 (student_id, course_code))
        if c.fetchone() is None:
            total_seats = get_course_capacity(course_code)
            current_enrollments = len(get_all_enrollments()[
                get_all_enrollments()['course_code'] == course_code
            ])
            if current_enrollments < total_seats:
                c.execute("""INSERT INTO enrollments 
                            (student_id, course_code, enrollment_date)
                            VALUES (?, ?, ?)""",
                         (student_id, course_code, enrollment_date))
                conn.commit()
                return True
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")

def is_student_enrolled(student_id):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM enrollments WHERE student_id = ?", (student_id,))
    count = c.fetchone()[0]
    conn.close()
    return count > 0
