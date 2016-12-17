import os
import psycopg2
import psycopg2.extras
import urllib.parse

class MessageDB:

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

    def createTableMessages(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, timestamp VARCHAR(255), sender VARCHAR(255), message VARCHAR)")
        self.connection.commit()


    def insertMessage(self,timestamp,sender,message):
        self.cursor.execute("INSERT INTO messages (timestamp,sender,message) VALUES (%s,%s,%s)",[timestamp,sender,message])
        self.connection.commit()

    def getAllMessages(self):
        self.cursor.execute("SELECT * FROM messages ORDER BY id DESC")
        messages = self.cursor.fetchall()
        return messages
    

    
