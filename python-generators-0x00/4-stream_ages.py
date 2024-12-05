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


def stream_user_ages():
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor()
    query = "SELECT age FROM user_data;"
    cursor.execute(query)

    for row in cursor:
        yield row[0]  
    
    cursor.close()
    connection.close()


def calculate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found in the database.")
