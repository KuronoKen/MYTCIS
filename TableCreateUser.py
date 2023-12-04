import sqlite3

# Connect to the database (creates a new one if it doesn't exist)
conn = sqlite3.connect('Database/users.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table for users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()