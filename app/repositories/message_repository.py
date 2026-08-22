from app.core.database import get_connection


def get_history(user_id):
    conn =get_connection()
    cursor=conn.cursor()
    cursor.execute(
        '''
        SELECT role,content
        FROM messages
        WHERE user_id=%s
        ORDER BY id
        ''',
        (user_id,)
    )

    rows=cursor.fetchall()

    cursor.close()
    conn.close()

    history=[]

    for row in rows:

        history.append(
            {
                "role":row[0],
                "content":row[1]
            }
        )

    return history



def add_message(user_id,role,content):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        '''
        INSERT INTO messages
        (
            user_id,
            role,
            content
        )

        VALUES
        (%s,%s,%s)
        ''',
        (
            user_id,
            role,
            content
        )
    )

    conn.commit()

    cursor.close()
    conn.close()



def delete_history(user_id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        '''
        DELETE FROM messages
        WHERE user_id=%s
        ''',
        (user_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_history_count(user_id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        '''
        SELECT COUNT(*)
        FROM messages
        WHERE user_id=%s
        ''',
        (user_id,)
    )

    

    count=cursor.fetchone()

    cursor.close()
    conn.close()

    return count[0]/2