import sqlite3
import json

def list_post_tags(url):

    query_params = url['query_params']

    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory=sqlite3.Row
        db_cursor=conn.cursor()

        query_string = """
            SELECT
                *
            FROM PostTags
        """

        #check for query parameters
        if query_params:
            conditions = []
            parameters = []

            #look at each key/value pair and dynamically add each condition to SQL query (query_string)
            for key, values in query_params.items():

                conditions.append(f"{key} = ?")
                parameters.append(values[0])

            query_string += " WHERE " + " AND " .join(conditions)
            db_cursor.execute(query_string,(parameters))

        else:
            db_cursor.execute(query_string)

        #Write the SQL query to get the information you want

        query_results=db_cursor.fetchall()

        users=[]
        for row in query_results:
            users.append(dict(row))

        response_body=json.dumps(users)

    return response_body

def retrieve_post_tag(pk):

    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            *
        FROM PostTags
        WHERE id = ?
        """, (pk,))

        user = db_cursor.fetchone()

    if user is None:
        return 'id not found'

    post_tag = dict(user)
    response_body = json.dumps(post_tag)

    return response_body


def create_post_tag(request_body):

    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into PostTags (
            post_id,
            tag_id
        ) 
        values (?,?)
        """, (request_body['post_id'],request_body['tag_id']))

        id = db_cursor.lastrowid

        response_body = json.dumps({
            'id': id,
            'post_id': request_body['post_id'],
            'tag_id': request_body['tag_id'],
        })

        return response_body
    

def delete_post_tag(pk):
    
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE
        FROM PostTags
        WHERE id = ?
        """, (pk,))

        number_of_rows_delete = db_cursor.rowcount

    return True if number_of_rows_delete > 0 else False


def update_post_tag(pk, request_body):
    
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE PostTags
            SET
                post_id = ?,
                tag_id = ?
            WHERE id = ?
            """,
            (request_body["post_id"],request_body["tag_id"],pk)
        )

    updated_post_tag = {
        "id": pk,
        "post_id": request_body['post_id'],
        "tag_id": request_body['tag_id']
    }

    response_body = json.dumps(updated_post_tag)

    return response_body
