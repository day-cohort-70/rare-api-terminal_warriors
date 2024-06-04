import sqlite3
import json
from datetime import datetime


def filteredAllPosts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id,
            p.post_id,
            p.title,
            p.publication_date,
            p.category_id,
            c.label,
            u.first_name,
            u.last_name
        FROM Posts p
        JOIN Posts u
            ON p.post_id = u.id
        LEFT JOIN Categories c
            ON p.category_id = c.id
        WHERE approved = TRUE
        AND publication_date <= DATE('now')
        ORDER BY publication_date DESC
        """
        )
        query_results = db_cursor.fetchall()

        posts = []
        for row in query_results:
            post = {
                "id": row["id"],
                "post_id": row["post_id"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "author": f"{row['first_name']} {row['last_name']}",
                "category_name": row["label"],
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
            tags = [tag["label"] for tag in tag_results]

            post["tags"] = tags
            posts.append(post)

        serialized_posts = json.dumps(posts)

    return serialized_posts


def create_post(post_request_body):

    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert Into Posts (
            user_id,
            category_id,
            title,
            publication _date,
            image_url,
            content,
            approved 
        ) 
            VALUES (?,?,?,?,?,?,?, 1)
            """,
            (
                post_request_body[
                    "user_id"
                ],  # Assuming user_id is passed in the request body
                post_request_body["category_id"],
                post_request_body["title"],
                post_request_body["publication_date"],
                post_request_body["image_url"],
                post_request_body["content"],
                post_request_body["approved"],
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"message": f"Post {id} created successfully", "valid": True})
