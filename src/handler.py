# Third party libraries
import mysql.connector

# Internal imports
from decl import DB_CONFIG
from utl.logger import Logger

logger = Logger()


class Handler:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.close_connection()

    def insert(self, sender, receiver, message):
        try:
            insert_query = "INSERT INTO messages (sender, receiver, message, unread) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(insert_query, (sender, receiver, message, 1))
            self.conn.commit()
        except (mysql.connector.Error, Exception) as err:
            logger.info(f"Error during insert: {err}")

    def get_all_messages_for(self, username):
        try:
            select_all_query = "SELECT message_id, sender, message FROM messages WHERE receiver = %s AND unread=1"
            self.cursor.execute(select_all_query, (username,))
            result = self.cursor.fetchall()

            # Update the read status for selected messages
            update_query = "UPDATE messages SET unread = 0 WHERE message_id = %s"
            for row in result:
                message_id = row[0]
                self.cursor.execute(update_query, (message_id,))
            self.conn.commit()

            return [
                (
                    sender, message
                 )
                for message_id, sender, message in result
            ]
        except (mysql.connector.Error, Exception) as err:
            logger.info(f"Error during get_all: {err}")
            return None

    def insert_user(self, user_data):
        insert_query = "INSERT INTO users (id, full_name, email, profile_pic) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_query, user_data)
        self.conn.commit()

    def get_user(self, user_id):
        res = "SELECT * FROM users WHERE id=%s"
        self.cursor.execute(res, (user_id,))
        user = self.cursor.fetchone()
        if user:
            return user

    def close_connection(self):
        try:
            self.cursor.close()
            self.conn.close()
        except ReferenceError:
            pass


# Usage
handler = Handler()
