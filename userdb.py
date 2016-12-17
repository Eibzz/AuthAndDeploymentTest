import os
import psycopg2
import psycopg2.extras
import urllib.parse

class UserDB:

    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def createTableUsers(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR, encpass VARCHAR, firstname VARCHAR(255), lastname VARCHAR(255))")
        self.connection.commit()

    def emailExists(self,email):
        self.cursor.execute("SELECT * FROM users where email = %s", [email])
        users = self.cursor.fetchall()
        print("exists: ",len(users)>0)
        return (len(users)>0)
        
    def getUserByEmail(self, email):
        self.cursor.execute("SELECT * FROM users where email = %s", [email])
        user = self.cursor.fetchone()
        return user

    def getUserByID(self, userid):
        self.cursor.execute("SELECT * FROM users where id = %s", [userid])
        user = self.cursor.fetchone()
        return user

    def createUser(self,email,encpass,firstname,lastname):
        self.cursor.execute("INSERT INTO users (email,encpass,firstname,lastname) VALUES (%s,%s,%s,%s)",[email,encpass,firstname,lastname])
        self.connection.commit()

    def deleteUser(self, userid):
        self.cursor.execute("DELETE FROM users WHERE id=%s",[userid])
        self.connection.commit()
        
