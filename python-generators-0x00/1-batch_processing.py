import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

env = os.environ

def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host=env.get('MYSQL_HOST', 'localhost'),
            user=env.get('MYSQL_USER'),
            password=env.get('MYSQL_PASSWORD'),
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True) 
        offset = 0

        while True:
            cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset};")
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch
            offset += batch_size

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user) 