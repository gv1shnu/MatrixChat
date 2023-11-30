# Third party libraries
import cryptography
import mysql.connector
from cryptography.fernet import Fernet

# Internal imports
from decl import CURRENT_USER, KEY_FILE
from utl.logger import Logger

# Standard library
import os

logger = Logger()


class EncryptionUtility:
    def __init__(self):
        self.key_file = KEY_FILE
        self.encryption_key = self.load_key()

    def write_key(self):
        key = Fernet.generate_key()
        with open(self.key_file, "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        if not os.path.exists(self.key_file):
            self.write_key()
        return open(self.key_file, "rb").read()

    def generate_cipher(self):
        try:
            return Fernet(self.encryption_key)
        except Exception as err:
            logger.info(f"Error while generating cipher: {err}")

    def encrypt(self, message):
        try:
            cipher = self.generate_cipher()
            encrypted_message = cipher.encrypt(message.encode())
            return encrypted_message
        except Exception as e:
            logger.debug(f"Encryption error: {e}")

    def decrypt(self, encrypted_message):
        try:
            cipher = self.generate_cipher()
            decrypted_message = cipher.decrypt(encrypted_message).decode()
            return decrypted_message
        except cryptography.fernet.InvalidToken as e:
            logger.error(f"InvalidToken exception: {e}")
            return None
        except Exception as e:
            logger.error(f"Generic exception: {e}")


class Handler:
    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.encryptionUtility = EncryptionUtility()
        self.cursor = self.db.cursor()

    def __del__(self):
        self.close_connection()

    def insert(self, receiver, message):
        try:
            encrypted_message = self.encryptionUtility.encrypt(message)
            encrypted_sender = self.encryptionUtility.encrypt(CURRENT_USER)
            encrypted_receiver = self.encryptionUtility.encrypt(receiver)
            insert_query = "INSERT INTO messages (sender, receiver, message_content) VALUES (%s, %s, %s)"
            self.cursor.execute(insert_query, (encrypted_sender, encrypted_receiver, encrypted_message))
            self.db.commit()
        except (mysql.connector.Error, Exception) as err:
            logger.info(f"Error during insert: {err}")

    def get_all(self):
        try:
            select_all_query = "SELECT sender, message_content FROM messages WHERE receiver = %s"
            self.cursor.execute(select_all_query, (CURRENT_USER,))
            result = self.cursor.fetchall()
            return [(sender, self.encryptionUtility.decrypt(message)) for sender, message in result]
        except (mysql.connector.Error, Exception) as err:
            logger.info(f"Error during get_all: {err}")
            return None

    def close_connection(self):
        try:
            self.cursor.close()
            self.db.close()
        except ReferenceError:
            pass


# Usage
handler = Handler(
    host=os.environ.get('matrixHost'),
    user=os.environ.get('matrixUser'),
    password=os.environ.get('matrixPassword'),
    database=os.environ.get('matrixDb')
)
