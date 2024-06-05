import sqlite3
import json
from datetime import datetime

def filteredAllPosts(url):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        query_params = url['query_params']

        query_string = """
        SELECT
            p.id,
            p.user_id,
            p.title,
            p.publication_date,
            p.category_id,
            c.label,
            u.first_name,
            u.last_name
        FROM Posts p
        JOIN Users u
            ON p.user_id = u.id
        LEFT JOIN Categories c
            ON p.category_id = c.id
        """

        if query_params:
            first_query_key = list(query_params.keys())[0]
            query_string += f" WHERE {first_query_key} = {query_params[first_query_key][0]}"
            query_string += " AND publication_date <= DATE('now') ORDER BY publication_date DESC"
            db_cursor.execute(query_string)
        else:
            query_string += "WHERE approved = TRUE"
            query_string += " AND publication_date <= DATE('now') ORDER BY publication_date DESC"
            db_cursor.execute(query_string)
        
        query_results = db_cursor.fetchall()

        posts=[]
        for row in query_results:
            post = {
                "id": row['id'],
                "user_id": row['user_id'],
                "title": row['title'],
                "publication_date": row['publication_date'],
                "author": f"{row['first_name']} {row['last_name']}",
                "category_name": row['label']
            }
            db_cursor.execute("""
            SELECT t.label
            FROM Tags t
            JOIN PostTags pt ON t.id = pt.tag_id
            WHERE pt.post_id = ?
            """, (row['id'],))
            tag_results = db_cursor.fetchall()
            tags = [tag['label'] for tag in tag_results]

            post["tags"] = tags
            posts.append(post)

        serialized_posts = json.dumps(posts)

    return serialized_posts

def postDetails(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.title,
            p.publication_date,
            p.category_id,
            p.image_url,
            p.content,
            c.label,
            u.first_name,
            u.last_name
        FROM Posts p
        JOIN Users u
            ON p.user_id = u.id
        LEFT JOIN Categories c
            ON p.category_id = c.id
        WHERE p.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()

        post = {
                "id": query_results['id'],
                "user_id": query_results['user_id'],
                "title": query_results['title'],
                "publication_date": query_results['publication_date'],
                "author": f"{query_results['first_name']} {query_results['last_name']}",
                "category_name": query_results['label'],
                "image_url": query_results['image_url'],
                "content": query_results['content']
            }
        db_cursor.execute("""
        SELECT t.label
        FROM Tags t
        JOIN PostTags pt ON t.id = pt.tag_id
        WHERE pt.post_id = ?
        """, (query_results['id'],))
        tag_results = db_cursor.fetchall()
        tags = [tag['label'] for tag in tag_results]
        post["tags"] = tags

        serialized_post = json.dumps(dict(query_results))
        return serialized_post