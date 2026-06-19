import sqlite3

print("Testing database connection...")

DB_FILE = "blog.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create the table structure
cursor.execute("""CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT NOT NULL, 
        Content TEXT NOT NULL, 
        category TEXT NOT NULL,
        tags TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
        )
    """)
conn.commit()
conn.close()

print("Database file 'blog.db' successfully created with a 'posts' table!")
