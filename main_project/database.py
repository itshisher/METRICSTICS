import mysql.connector

class Database:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root12345",
            database="userDB"
        )
        self.cursor = self.db_connection.cursor()

    def create_user(self, fullname, email, username, password):
        try:
            self.cursor.execute(
                "INSERT INTO users (full_name, email, username, password) VALUES (%s, %s, %s, %s)",
                (fullname, email, username, password)
            )
            self.db_connection.commit()
            return True
        except mysql.connector.errors.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = self.cursor.fetchone()
        return bool(result and result[0] == password)
