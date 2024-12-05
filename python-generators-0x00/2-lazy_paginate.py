import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

env = os.environ

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host=env.get('MYSQL_HOST', 'localhost'),
            user=env.get('MYSQL_USER'),
            password=env.get('MYSQL_PASSWORD'),
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def paginate_users(connection, page_size, offset):
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset};"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def lazy_paginate(page_size):
    connection = connect_to_prodev()
    if not connection:
        return

    offset = 0
    while True:
        page = paginate_users(connection, page_size, offset)
        if not page:  
            break
        yield page
        offset += page_size  

    connection.close()
