import sqlite3

DB="ai_chat.db"

conn=sqlite3.connect(DB)
cursor=conn.cursor()
cursor.execute(
    '''
    DELETE FROM users WHERE id > 6
    '''
)

conn.commit()

conn.close()