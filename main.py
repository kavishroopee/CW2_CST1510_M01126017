import bcrypt as bc
import sqlite3, pandas as pd

def hash_password(plaintext_password):
    password_bytes = plaintext_password.encode('utf-8')
    salt = bc.gensalt()
    hashed_password = bc.hashpw(password_bytes, salt).decode('utf-8')
    return hashed_password

def verify_password(plaintext_password, hashed_password):
    password_bytes = plaintext_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bc.checkpw(password_bytes, hashed_bytes)

def check_password(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False    
    if not any(char in "!@#$%&*|" for char in password):
        return False
    return True  

def create_user_table(conn):
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
        );'''
    cur.execute(sql)
    conn.commit()  

# Add a new user to the database
def  add_user(conn, name, password_hash):
    try:

        cur = conn.cursor()
        sql = 'INSERT INTO users (username, password_hash) VALUES (?, ?)'
        cur.execute(sql, (name, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Error: Username '{name}' already exists.")
        return False

def register_user(conn, username, password):
    hashed_password = hash_password(password)
    username = input("Enter your username:").strip()
    password = input("Enter your password:")
    conf_password = input("Please re-enter your password: ")

    if not username:
        print("Username cannot be empty.")
        return
    if not check_password(password):
        print("Password too weak! Need 8+ characters, including uppercase, lowercase, digit, and special character.")
        return
    if password != conf_password:
        print("Passwords do not match!")
        return
    
    hashed_password = hash_password(password)
    if add_user(conn, username, hashed_password):
        print("Registration successful! You can now log in.")

def login_user(conn, username, password):
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ")

    user = get_user(conn, username)
    
    if user and verify_password(password, user[2]):  # user[2] is the password hash
        print("Login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False    
    

# Retrieve all users from the database
def get_all_users(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    return cur.fetchall()

# Retrieve a specific user by username
def get_user(conn, name):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (name,))
    return cur.fetchone()

# Update a user's username in the database
def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    cur.execute('UPDATE users SET username = ? WHERE username = ?', (new_name, old_name))
    conn.commit()

# Delete a user from the database
def delete_user(conn, user_name):
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE username = ?', (user_name,))
    conn.commit()


def name_check(username):
    try: # Error handling is needed as for the first time, no names will be in the file and an error will occur 
        with open("DATA/users.txt", "r") as f:
            for line in f : # Reads line by line; most efficient and not power consuming
                user, _ = line.strip().split(",", 1)
                if user == username:
                    print("Username already exists. Please choose a different username.")
                    return False
        return True # Returns True if the username is not found in the file        
    except FileNotFoundError:
        return True# Returns True if the file does not exist, meaning no usernames are registered yet

def register_func():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    conf_password = input("Please re-enter your password: ")
    
    if not name_check(username):
        return
    if not check_password(password):
        print("Password too weak! Need 8+ characters, including uppercase, lowercase, digit, and special character.")
        return
    if password != conf_password:
        print("Passwords do not match!")
        return
    register_user(username, password)
    print("Registration successful! You can now log in.")
    
def login_func():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if login_user(username, password):
        print("Login successful!")
    else:
        print("Invalid username or password.")
    

# Add a new user to the database
def  add_user(conn, name, password_hash):
    try:

        cur = conn.cursor()
        sql = 'INSERT INTO users (username, password_hash) VALUES (?, ?)'
        cur.execute(sql, (name, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Error: Username '{name}' already exists.")
        return False

# Retrieve all users from the database
def get_all_users(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    return cur.fetchall()

# Retrieve a specific user by username
def get_user(conn, name):
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (name,))
    return cur.fetchone()

# Update a user's username in the database
def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    cur.execute('UPDATE users SET username = ? WHERE username = ?', (new_name, old_name))
    conn.commit()

# Delete a user from the database
def delete_user(conn, user_name):
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE username = ?', (user_name,))
    conn.commit()

def register_user(conn):
    username = input("Enter your username:").strip()
    password = input("Enter your password:")
    conf_password = input("Please re-enter your password: ")

    if not username:
        print("Username cannot be empty.")
        return
    if not check_password(password):
        print("Password too weak! Need 8+ characters, including uppercase, lowercase, digit, and special character.")
        return
    if password != conf_password:
        print("Passwords do not match!")
        return
    
    hashed_password = hash_password(password)
    if add_user(conn, username, hashed_password):
        print("Registration successful! You can now log in.")

        
        
# Migration functions for datasets
def migrate_cyber_incidents(conn):
    data = pd.read_csv('DATA/cyber_incidents.csv')
    data.to_sql('cyber_incidents', conn)

def get_all_cyber_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    return pd.read_sql(sql, conn)

def migrate_datasets_metadata(conn):
    data = pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata', conn)

def get_all_datasets_metadata(conn):
    sql = 'SELECT * FROM datasets_metadata'
    return pd.read_sql(sql, conn)

def migrate_it_tickets(conn):
    data = pd.read_csv('DATA/it_tickets.csv')
    data.to_sql('it_tickets', conn)

def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    return pd.read_sql(sql, conn)        


def main():
    try:
        conn = sqlite3.connect('DATA/project_data.db')
        create_user_table(conn)

    except sqlite3.OperationalError:
        print("Database file not found. Please ensure 'project_data.db' exists in the 'DATA' directory.")
        return

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register_user(conn)
        elif choice == '2':
            login_user(conn)
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")    


if __name__ == "__main__":
    main()    
