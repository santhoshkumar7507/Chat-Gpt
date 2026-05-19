import sqlite3
import os
from datetime import datetime

os.makedirs("backend/database", exist_ok=True)
conn = sqlite3.connect("backend/database/sqlite.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        created_at TEXT
    )
""")
conn.commit()

def save_memory(question, answer):
    cursor.execute(
        "INSERT INTO memory(question, answer, created_at) VALUES (?, ?, ?)",
        (question, answer, str(datetime.now()))
    )
    conn.commit()

def get_history():
    cursor.execute("SELECT * FROM memory ORDER BY id DESC")
    return cursor.fetchall()
