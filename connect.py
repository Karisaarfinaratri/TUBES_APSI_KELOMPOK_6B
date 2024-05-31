import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('info_in.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    date_posted DATE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS scholarships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    provider TEXT NOT NULL,
    deadline DATE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS competitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    organizer TEXT NOT NULL,
    date TEXT NOT NULL
)
''')

# Commit and close
conn.commit()
conn.close()
