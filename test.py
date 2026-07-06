import bcrypt as bc
import sqlite3
import pandas as pd

# =========================================================================
# SECURITY LAYER — Password hashing and verification
# =========================================================================

def hash_password(plaintext_password):
    """Hashes a plain text password using bcrypt."""
    password_bytes = plaintext_password.encode('utf-8')
    salt = bc.gensalt()
    hashed_password = bc.hashpw(password_bytes, salt).decode('utf-8')
    return hashed_password

def verify_password(plaintext_password, hashed_password):
    """Checks if a plain text password matches a stored bcrypt hash."""
    password_bytes = plaintext_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bc.checkpw(password_bytes, hashed_bytes)

def check_password(password):
    """Validates password strength — returns True if it meets all rules."""
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

# =========================================================================
# DATABASE LAYER — Table creation and CRUD operations
# =========================================================================

def create_user_table(conn):
    """Creates the users table if it doesn't already exist."""
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    );'''
    cur.execute(sql)
    conn.commit()

def add_user(conn, name, password_hash):
    """Inserts a new user into the database. Returns True on success."""
    try:
        cur = conn.cursor()
        sql = 'INSERT INTO users (username, password_hash) VALUES (?, ?)'
        cur.execute(sql, (name, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Error: Username '{name}' already exists.")
        return False

def get_all_users(conn):
    """Returns all users from the database."""
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    return cur.fetchall()

def get_user(conn, name):
    """Returns a single user row by username, or None if not found."""
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = ?', (name,))
    return cur.fetchone()

def update_user(conn, old_name, new_name):
    """Updates a user's username."""
    cur = conn.cursor()
    cur.execute('UPDATE users SET username = ? WHERE username = ?', (new_name, old_name))
    conn.commit()

def delete_user(conn, user_name):
    """Deletes a user by username."""
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE username = ?', (user_name,))
    conn.commit()

# =========================================================================
# AUTH LAYER — Registration and login logic
# =========================================================================

def register_user(conn):
    """Collects user input, validates, hashes password, and stores in DB."""
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ")
    conf_password = input("Please re-enter your password: ")

    if not username:
        print("Username cannot be empty.")
        return

    # Check if username already taken — queries DB, not flat file
    if get_user(conn, username):
        print("Username already exists. Please choose a different username.")
        return

    if not check_password(password):
        print("Password too weak! Need 8+ characters, uppercase, lowercase, digit, and special character (!@#$%&*|).")
        return

    if password != conf_password:
        print("Passwords do not match!")
        return

    # Only hash AFTER all validation passes
    hashed_password = hash_password(password)
    if add_user(conn, username, hashed_password):
        print("Registration successful! You can now log in.")

def login_user(conn):
    """Collects credentials, verifies against stored hash, returns True/False."""
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ")

    user = get_user(conn, username)

    if user and verify_password(password, user[2]):  # user[2] is the password_hash column
        print("Login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False

# =========================================================================
# DATA MIGRATION LAYER — CSV → SQLite
# =========================================================================

def migrate_cyber_incidents(conn):
    """Migrates cyber_incidents.csv into the SQLite database."""
    data = pd.read_csv('DATA/cyber_incidents.csv')
    data.to_sql('cyber_incidents', conn, if_exists='replace', index=False)

def get_all_cyber_incidents(conn):
    """Returns all cyber incidents as a DataFrame."""
    return pd.read_sql('SELECT * FROM cyber_incidents', conn)

def migrate_datasets_metadata(conn):
    """Migrates datasets_metadata.csv into the SQLite database."""
    data = pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata', conn, if_exists='replace', index=False)

def get_all_datasets_metadata(conn):
    """Returns all dataset metadata as a DataFrame."""
    return pd.read_sql('SELECT * FROM datasets_metadata', conn)

def migrate_it_tickets(conn):
    """Migrates it_tickets.csv into the SQLite database."""
    data = pd.read_csv('DATA/it_tickets.csv')
    data.to_sql('it_tickets', conn, if_exists='replace', index=False)

def get_all_it_tickets(conn):
    """Returns all IT tickets as a DataFrame."""
    return pd.read_sql('SELECT * FROM it_tickets', conn)

# =========================================================================
# ENTRY POINT — CLI menu
# =========================================================================

def main():
    try:
        conn = sqlite3.connect('DATA/project_data.db')
        create_user_table(conn)
    except sqlite3.OperationalError:
        print("Database file not found. Please ensure the 'DATA' directory exists.")
        return

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            register_user(conn)       # FIXED — passes conn, collects input internally
        elif choice == '2':
            login_user(conn)          # FIXED — same pattern
        elif choice == '3':
            print("Goodbye!")
            conn.close()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
