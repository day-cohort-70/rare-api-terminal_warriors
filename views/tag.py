#tag.py
import sqlite3
import json
from datetime import datetime


def create_tag(tag_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            INSERT INTO TAGS(label)
            VALUES(?)
            """,
            (tag_data["label"],),
        )
        id = db_cursor.lastrowid

        return json.dumps({"id": id})


def list_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute(
            """
        SELECT
                          t.id,
                          t.label
                          FROM Tags t
"""
        )
        query_results = db_cursor.fetchall()

        tags = []
        for row in query_results:
            tags.append(dict(row))

        serialized_tags = json.dumps(tags)

    return serialized_tags

def delete_tag(pk):
    
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE
        FROM Tags
        WHERE id = ?
        """, (pk,))

        number_of_rows_delete = db_cursor.rowcount

    return True if number_of_rows_delete > 0 else False

def update_tag(pk, tag_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute(
            """
            UPDATE Tags
            SET label = ?
            WHERE id = ?
            """,
            (tag_data["label"], pk)
        )
        number_of_rows_updated = db_cursor.rowcount
    return True if number_of_rows_updated > 0 else False
