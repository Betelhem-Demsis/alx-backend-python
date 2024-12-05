import mysql.connector
import csv
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

env = os.environ

def connect_db():  
    try:
        connection = mysql.connector.connect(
            host=env.get('MYSQL_HOST', 'localhost'),
            user=env.get('MYSQL_USER'),  
            password=env.get('MYSQL_PASSWORD'), 
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

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

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX(user_id)
            );
        """)
        print("Table user_data created successfully.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                user_id = str(uuid.uuid4()) 
                name = row['name']
                email = row['email']
                age = row['age']
                
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE name=name;  -- Prevent duplicate entries
                """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted into user_data table successfully.")
        cursor.close()
    except Exception as err:
        print(f"Error: {err}")
