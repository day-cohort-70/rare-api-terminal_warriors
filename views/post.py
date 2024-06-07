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

        posts = []
        for row in query_results:
            post = {
                "id": row["id"],
                "user_id": row["user_id"],
                "title": row['title'],
                "publication_date": row['publication_date'],
                "author": f"{row['first_name']} {row['last_name']}",
                "category_name": row['label'],
            }
            db_cursor.execute(
                """
            SELECT t.label
            FROM Tags t
            JOIN PostTags pt ON t.id = pt.tag_id
            WHERE pt.post_id = ?
            """,
                (row["id"],),
            )
            tag_results = db_cursor.fetchall()
            tags = [tag['label'] for tag in tag_results]

            post["tags"] = tags
            posts.append(post)

        serialized_posts = json.dumps(posts)

    return serialized_posts



def create_post(post_request_body):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Corrected SQL query
        db_cursor.execute(
            """
        INSERT INTO Posts (
            user_id,
            category_id,
            title,
            publication_date,
            image_url,
            content,
            approved
        ) 
        VALUES (?,?,?,?,?,?,?)
            """,
            (
                post_request_body["user_id"],  # Assuming user_id is passed in the request body
                post_request_body["category_id"],
                post_request_body["title"],
                post_request_body["publication_date"],
                post_request_body["image_url"],
                post_request_body["content"],
                post_request_body["approved"],
            ),
        )

        id = db_cursor.lastrowid
        # Corrected response body construction
        response_body = {
            "id": id,
            "user_id": post_request_body["user_id"],
            "category_id": post_request_body["category_id"],
            "title": post_request_body["title"],
            "publication_date": post_request_body["publication_date"],
            "image_url": post_request_body["image_url"],
            "content": post_request_body["content"],
            "approved": post_request_body["approved"]
        }

        print(post_request_body)
        return json.dumps(response_body)

