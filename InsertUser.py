import sqlite3

def insert_user(username, password):
    # Connect to the database
    conn = sqlite3.connect('Database/users.db')
    cursor = conn.cursor()
    
    
    # Insert a new user into the 'users' table
    cursor.execute('''
        INSERT INTO users (username,  password)
        VALUES (?, ?)
    ''', (username, password))

    # Commit the changes and close the connection
    conn.commit()
    cursor.execute('SELECT * FROM users')
    usersdata = cursor.fetchall()
    for user in usersdata:
        print(user)

    conn.close()

insert_user('ToBeIT67TheSecond', 'password')
