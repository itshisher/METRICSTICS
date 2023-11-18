import mysql.connector
'''
class to setup and connect to the database 
includes user signup functionality 
'''
class Database:
    def __init__(self):
        # an instance method that initializes a newly created object
        # connects to the database
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="userDB"
        )
        self.cursor = self.db_connection.cursor()

    def create_user(self, fullname, email, username, password):
        # user signup setup
        try:
            self.cursor.execute(
                "INSERT INTO users (full_name, email, username, password) VALUES (%s, %s, %s, %s)",
                (fullname, email, username, password)
            )
            self.db_connection.commit() # save the info to the database
            return True
        except mysql.connector.errors.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        # user login verification with info saved in the database
        self.cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = self.cursor.fetchone()
        return bool(result and result[0] == password)
