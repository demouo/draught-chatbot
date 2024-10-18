# helper.py
import sqlite3
import json

def add_history(user_name, summary, start_time, messages):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO history (user_name, summary, start_time, messages)
        VALUES (?, ?, ?, ?)
    ''', (user_name, summary, start_time, json.dumps(messages)))
    conn.commit()
    last_id = c.lastrowid  # 获取最后插入行的 ID
    conn.close()
    return last_id  # 返回插入记录的 ID

def get_history(user_name):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('SELECT id, summary, start_time FROM history WHERE user_name = ?', (user_name,))
    history = c.fetchall()
    conn.close()
    return history

def clear_history(user_name):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('DELETE FROM history WHERE user_name = ?', (user_name,))
    conn.commit()
    conn.close()