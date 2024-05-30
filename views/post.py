import sqlite3
import json
from datetime import datetime

def filteredAllPosts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.title,
            p.publication_date
        FROM Posts p
        WHERE approved = TRUE
        AND publication_date <= DATE('now')
        ORDER BY publication_date DESC
        """)
        query_results = db_cursor.fetchall()

        posts=[]
        for row in query_results:
            post = {
                "id": row['id'],
                "user_id": row['user_id'],
                "title": row['title'],
                "publication_date": row['publication_date']
            }
            posts.append(post)

        serialized_posts = json.dumps(posts)

    return serialized_posts