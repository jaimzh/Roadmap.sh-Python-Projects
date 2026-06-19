import sqlite3

print("Testing database connection...")

DB_FILE = "blog.db"



# DATABASE INITIALIZATION

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL, 
            Content TEXT NOT NULL, 
            category TEXT NOT NULL,
            tags TEXT NOT NULL, -- Stored as a comma-separated string instead of a list 
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
            )
        """)
    conn.commit()
    conn.close()
