import sqlite3


DB = "ai_chat.db"


def get_connection():
    return sqlite3.connect(DB)



def init_db():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.executescript(
        """

        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT NOT NULL UNIQUE,

            password TEXT NOT NULL,

            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );


        CREATE TABLE IF NOT EXISTS messages(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            role TEXT NOT NULL,

            content TEXT NOT NULL,

            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        );

        """
    )


    conn.commit()

    conn.close()