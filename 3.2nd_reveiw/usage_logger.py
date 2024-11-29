import sqlite3
from datetime import datetime

def init_logger():
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS usage_logs
                 (timestamp TEXT,
                  user_type TEXT,
                  user_id TEXT,
                  action TEXT)''')
    
    conn.commit()
    conn.close()

def log_activity(user_type, user_id, action):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    c.execute('''INSERT INTO usage_logs 
                 (timestamp, user_type, user_id, action)
                 VALUES (?, ?, ?, ?)''',
              (timestamp, user_type, user_id, action))
    
    conn.commit()
    conn.close()

def get_user_logs(user_id):
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    
    c.execute("""SELECT timestamp, action 
                 FROM usage_logs 
                 WHERE user_id = ?
                 ORDER BY timestamp DESC""", 
              (user_id,))
    
    logs = c.fetchall()
    conn.close()
    
    return logs

def get_all_logs():
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()
    
    c.execute("""SELECT timestamp, user_type, user_id, action 
                 FROM usage_logs 
                 ORDER BY timestamp DESC""")
    
    logs = c.fetchall()
    conn.close()
    
    return logs
