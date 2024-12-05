import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

env = os.environ

def stream_users():
    try:
        connection = mysql.connector.connect(
            host=env.get('MYSQL_HOST', 'localhost'),
            user=env.get('MYSQL_USER'),
            password=env.get('MYSQL_PASSWORD'),
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM user_data;")

        for row in cursor:
            yield row

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
