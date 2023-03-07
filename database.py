import sqlite3

def create_connection():
    conn = sqlite3.connect('chat.db')
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 message TEXT,
                 role TEXT)''')
    conn.commit()
    conn.close()

def add_message(message, role):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO messages (message, role) VALUES (?, ?)", (message, role))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM messages")
    rows = c.fetchall()
    conn.close()
    return rows