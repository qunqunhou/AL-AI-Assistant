from app.core.database import  get_connection



def create_user(username,password):


    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute(
        '''
        INSERT INTO users(
            username,
            password
        )
        VALUES
        (?,?)
        ''',
        (
            username,
            password
        )
    )


    conn.commit()


    user_id=cursor.lastrowid

    conn.close()


    return user_id



def get_user_by_username(username):

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute(
        '''
        SELECT id,username,password
        FROM users
        WHERE username=?
        ''',
        (username,)
    )


    user=cursor.fetchone()


    conn.close()


    return user



def get_user_by_id(user_id):

    conn=get_connection()

    cursor=conn.cursor()


    cursor.execute(
        '''
        SELECT id,username
        FROM users
        WHERE id=?
        ''',
        (user_id,)
    )

    user=cursor.fetchone()

    conn.close()

    return user