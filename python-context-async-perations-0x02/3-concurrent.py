import asyncio
import aiosqlite


async def async_fetch_users(ALX_prodev):
    async with aiosqlite.connect(ALX_prodev) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users:")
            for row in results:
                print(row)
    return 


async def async_fetch_older_users(ALX_prodev):
    async with aiosqlite.connect(ALX_prodev) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("Users older than 40:")
            for row in results:
                print(row)
    return 


async def fetch_concurrently():
    database_name = "ALX_prodev"

   
    async with aiosqlite.connect(database_name) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL
            )
        """)
      
        await db.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", ("John Doe", 30, "john.doe@example.com"))
        await db.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", ("Jane Doe", 50, "jane.doe@example.com"))
        await db.commit()

    
    await asyncio.gather(
        async_fetch_users(database_name), 
        async_fetch_older_users(database_name) 
    )


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
