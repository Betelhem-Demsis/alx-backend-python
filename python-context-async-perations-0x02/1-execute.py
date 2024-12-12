import sqlite3

class ExecuteQuery:
    def __init__(self,ALX_prodev,query,params=None):
        self.ALX_prodev=ALX_prodev
        self.query=query
        self.params=params
        self.connection=None
    
    def __enter__(self):
        self.connection=sqlite3.connect(self.database_name)
        self.cursor=self.connection.cursor()
        self.cursor.execute(self.query,self.params)
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            self.connection.close()

if __name__ == "__main__":
    database_name="ALX_prodev"

    with ExecuteQuery(database_name, """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    """) as cursor:
        pass 

    with ExecuteQuery(database_name, "SELECT * FROM users WHERE age > ?", (25,)) as cursor:
        results = cursor.fetchall()
        for row in results:
            print(row)
