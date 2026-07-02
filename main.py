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

def register_user(username, password):
    hashed_password = hash_password(password)
    with open('users.txt', 'a') as f:
     f.write(f"{username},{hashed_password}\n")    

def login_user(username, password):
    try:
        with open("users.txt", "r") as f:
            for line in f.readlines():
                user, hash = line.strip().split(",", 1)
                if user == username:
                    return verify_password(password, hash)
    except FileNotFoundError:
        print("User database not found.")
    return False

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

def name_check(username):
    try: # Error handling is needed as for the first time, no names will be in the file and an error will occur 
        with open("users.txt", "r") as f:
            for line in f : # Reads line by line; most efficient and not power consuming
                user, _ = line.strip().split(",", 1)
                if user == username:
                    print("Username already exists. Please choose a different username.")
                    return False
    except FileNotFoundError:
        pass  # If the file doesn't exist, no need to check for existing usernames
        print("User database not found. A new one will be created upon registration.")
        return True

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
    
def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("> ")
        if choice == "1":
            register_func()
        elif choice == "2":
            login_func()
        elif choice == "3":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()    
