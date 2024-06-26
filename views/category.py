import sqlite3
import json


def list_categories():
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            *
        FROM Categories
        """)

        query_results = db_cursor.fetchall()

    categories = []

    for row in query_results:
        categories.append(dict(row))

    serialized_categories = json.dumps(categories)

    return serialized_categories


def retrieve_category(pk):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            *
        FROM Categories
        WHERE id = ?
        """, (pk,))

        category = db_cursor.fetchone()

    if category is None:
        return 'id not found'

    category_dictionary = dict(category)
    return json.dumps(category_dictionary)


def create_category(user_request_body):

    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Categories (
            label
        ) 
        values (?)
        """, (user_request_body['label'],))

        id = db_cursor.lastrowid

        return json.dumps({
            'id': id,
            'label': user_request_body['label']
        })


def delete_category(pk):
    
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE
        FROM Categories
        WHERE id = ?
        """, (pk,))

        number_of_rows_delete = db_cursor.rowcount

    return True if number_of_rows_delete > 0 else False


def update_category(pk, body):
    
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Categories
            SET
                label = ?
            WHERE id = ?
            """,
            (body["label"],pk)
        )

    updated_category = {
        "id": pk,
        "label": body['label']
    }

    return json.dumps(updated_category)