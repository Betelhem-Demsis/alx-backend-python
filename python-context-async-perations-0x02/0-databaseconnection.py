import sqlite3
def DatabaseConnection():
    def __init__(self,ALX_prodev):
        self.ALX_prodev =ALX_prodev
        self.connection=None

    def __enter__(self):
        self.connection=sqlite3.connect(self.database_name)
        return self.connection.cursor()
  

    def __exit__(self, exc_type, exc_value, traceback): 
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            self.connection.close()  
    
if __name__ == "__main__":
    database_name = "ALX_prodev"

  
    with DatabaseConnection(database_name) as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

    with DatabaseConnection(database_name) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)


