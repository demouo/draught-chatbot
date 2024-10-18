# init.py
import sqlite3
from ...config.db_config import DB_NAME, TABLE_NAME
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            summary TEXT,
            start_time TEXT,
            messages TEXT
        )
    ''')
    conn.commit()
    conn.close()
