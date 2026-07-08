import sqlite3
import bcrypt as bc


# Add a new user to the database

def hash_password(plaintext_password):
    password_bytes = plaintext_password.encode('utf-8')
    salt = bc.gensalt()
    hashed_password = bc.hashpw(password_bytes, salt).decode('utf-8')
    return hashed_password

def verify_password(plaintext_password, hashed_password):
    password_bytes = plaintext_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bc.checkpw(password_bytes, hashed_bytes)


def  add_user(conn, name, password_hash):
    try:
        cur = conn.cursor()
        sql = 'INSERT INTO users (username, password_hash) VALUES (?, ?)'
        param = (name, password_hash)
        cur.execute(sql, param)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Error: Username '{name}' already exists.")
        return False
    
def migrate_users(conn):
    with open('DATA/users.txt', 'r') as f:
        users = f.readlines()

    for user in users:
        username, password = user.strip().split(',')
        hashed_password = hash_password(password)
        add_user(conn, username, hashed_password)        

# Retrieve all users from the database
def get_all_users(conn):
    cur = conn.cursor()
    sql = 'SELECT * FROM users'
    cur.execute(sql)
    users = cur.fetchall()
    conn.close()  # Close the connection after fetching the data
    return users

# Retrieve a specific user by username
def get_user(conn, name):
    cur = conn.cursor()
    sql = 'SELECT * FROM users WHERE username = ?'
    param = (name,)
    cur.execute(sql, param)
    user = cur.fetchone()
    conn.close()  # Close the connection after fetching the data
    return user

# Update a user's username in the database
def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    sql = 'UPDATE users SET username = ? WHERE username = ?'
    param = (new_name, old_name)
    cur.execute(sql, param)
    conn.commit()

# Delete a user from the database
def delete_user(conn, user_name):
    cur = conn.cursor()
    sql = 'DELETE FROM users WHERE username = ?'
    param = (user_name,)
    cur.execute(sql, param)
    conn.commit()

