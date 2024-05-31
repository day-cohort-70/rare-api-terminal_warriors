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
        conn.commit()
        return {"id": id}


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
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Tags WHERE id = ?
""", (pk,)
)
        conn.commit()
        return db_cursor.rowcount > 0