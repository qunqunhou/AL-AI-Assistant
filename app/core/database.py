
import mysql.connector

from app.core.config import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER
)




def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )



def init_db():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """

        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTO_INCREMENT,

            username VARCHAR(255) NOT NULL UNIQUE,

            password VARCHAR(255) NOT NULL,

            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """
    )

    cursor.execute(
        """

        CREATE TABLE IF NOT EXISTS messages(

            id INTEGER PRIMARY KEY AUTO_INCREMENT,

            user_id INTEGER NOT NULL,

            role VARCHAR(255) NOT NULL,

            content TEXT NOT NULL,

            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
        """
    )


    conn.commit()

    cursor.close()
    conn.close()