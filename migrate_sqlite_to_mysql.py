import sqlite3
import mysql.connector


SQLITE_DB = "/data/ai_chat.db"


MYSQL_CONFIG = {
    "host": "mysql",
    "port": 3306,
    "database": "al_ai",
    "user": "ai_user",
    "password": "ai_password",
}


def main():

    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_cursor = sqlite_conn.cursor()

    mysql_conn = mysql.connector.connect(
        **MYSQL_CONFIG
    )
    mysql_cursor = mysql_conn.cursor()


    try:

        # 读取 SQLite 用户
        sqlite_cursor.execute(
            """
            SELECT id, username, password, create_time
            FROM users
            ORDER BY id
            """
        )

        users = sqlite_cursor.fetchall()


        # 迁移 users
        for user in users:

            user_id, username, password, create_time = user

            mysql_cursor.execute(
                """
                INSERT INTO users(
                    id,
                    username,
                    password,
                    create_time
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    user_id,
                    username,
                    password,
                    create_time
                )
            )


        # 读取 SQLite messages
        sqlite_cursor.execute(
            """
            SELECT id, user_id, role, content, create_time
            FROM messages
            ORDER BY id
            """
        )

        messages = sqlite_cursor.fetchall()


        # 迁移 messages
        for message in messages:

            message_id, user_id, role, content, create_time = message

            mysql_cursor.execute(
                """
                INSERT INTO messages(
                    id,
                    user_id,
                    role,
                    content,
                    create_time
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    message_id,
                    user_id,
                    role,
                    content,
                    create_time
                )
            )


        mysql_conn.commit()

        print(
            f"迁移成功：users={len(users)}, messages={len(messages)}"
        )


    except Exception:

        mysql_conn.rollback()

        raise


    finally:

        sqlite_cursor.close()
        sqlite_conn.close()

        mysql_cursor.close()
        mysql_conn.close()


if __name__ == "__main__":
    main()