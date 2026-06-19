import sqlite3
import utils

print("Testing database connection...")

DB_FILE = "blog.db"


# DATABASE INITIALIZATION


def init_db():
    db_conn = sqlite3.connect(DB_FILE)
    cursor = db_conn.cursor()
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
    db_conn.commit()
    db_conn.close()


# now we need to convert the db tables into a python format, a dict that we can modify and manipulate


def format_sqlite_row_to_dict(row: sqlite3.Row) -> dict:
    # converts sqlite row that is apparently a tuple into a dict
    if not row:
        return None

    return {
        "id": row[0],
        "title": row[1],
        "content": row[2],
        "category": row[3],
        "tags": utils.format_string_to_tags(row[4]),
        "created_at": row[5],
        "updated_at": row[6],
    }


# CRUD FUNCTIONS
# create


def create_blog_post(title: str, content: str, category: str, tags: list[str]) -> dict:
    now = utils.get_current_timestamp()
    tags_string = utils.format_tags_to_string(tags)

    db_conn = sqlite3.connect(DB_FILE)
    cursor = db_conn.cursor()
    cursor.execute(
        """
         INSERT INTO posts (title, content, category, tags, created_at, updated_at)
         VALUES (?, ?, ?, ?, ?, ?)                
        """,
        (title, content, category, tags_string, now, now),
    )
    db_conn.commit()

    post_id = cursor.lastrowid
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))

    row: sqlite3.Row = cursor.fetchone()
    db_conn.close()

    return format_sqlite_row_to_dict(row)


# read
def get_all_blog_posts(search_term: str = None) -> list[dict]:
    db_conn = sqlite3.connect(DB_FILE)
    cursor = db_conn.cursor()

    if search_term:
        wildcard_search = f"%{search_term}%"

        cursor.execute(
            """
            SELECT * FROM posts
            WHERE title LIKE ? 
            OR content LIKE ? 
            OR category LIKE ?
            OR tags LIKE ?
            """,
            (wildcard_search, wildcard_search, wildcard_search, wildcard_search),
        )
    else:
        cursor.execute("""SELECT * FROM posts""")
    rows = cursor.fetchall()
    db_conn.close()

    return [format_sqlite_row_to_dict(row) for row in rows]


def get_blog_post(post_id: int) -> dict:
    db_conn = sqlite3.connect(DB_FILE)
    cursor = db_conn.cursor()

    cursor.execute(
        """
        SELECT * FROM posts 
        WHERE id = ?
        """,
        (post_id,),
    )

    row = cursor.fetchone()
    db_conn.close()
    return format_sqlite_row_to_dict(row)


def update_blog_post(
    post_id: int, title: str, content: str, category: str, tags: list[str]
) -> dict:
    now = utils.get_current_timestamp()
    tags_string = utils.format_tags_to_string(tags)

    db_conn = sqlite3.connect(DB_FILE)
    cursor = db_conn.cursor()

    # 1. update statement using the postid
    cursor.execute(
        """
        UPDATE posts 
        SET title = ?, content = ?, category = ?, tags = ?, updated_at = ?
        WHERE id = ?            
        """,
        (title, content, category, tags_string, now, post_id,),
    )
    

    db_conn.commit()
    
    # 2. get the updated row 
    cursor.execute(
        """
        SELECT * FROM posts 
        WHERE id = ?         
        """, 
        (post_id,),
    )
    row = cursor.fetchone()
    db_conn.close()
    
    return format_sqlite_row_to_dict(row)


def delete_blog_post(post_id: int) -> dict:
    db_conn = sqlite3.connect(DB_FILE)
    cursor = db_conn.cursor()
    
    cursor.execute(
        """
        DELETE FROM posts
        WHERE id = ?           
        """, (post_id,),)
    
    db_conn.commit()
    
    deleted_rows = cursor.rowcount # this counts how many rows where actuallly modified, deleted or whaterver not the toatal number of rows 
    db_conn.close()
    
    return deleted_rows > 0  # it the deleted is more than 0 then that means sommething did actually change, hence delete worked 