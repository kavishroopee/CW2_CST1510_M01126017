# All imports are placed at the top of the file for better organization and readability.
import bcrypt as bc
import sqlite3
import streamlit as st

# Taking infos from files
from app_model.schema import create_user_table
from app_model.db import conn
from app_model.users import add_user, get_user

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


def register_user(conn):
    st.subheader("Create a new account")

    username = st.text_input("Enter your username:", key="reg_user").strip()
    password = st.text_input("Enter your password:", type="password", key="reg_pass")
    conf_password = st.text_input("Please re-enter your password:", type="password", key="reg_conf_pass")
    
    hashed_password = hash_password(password)
    if add_user(conn, username, hashed_password):
        st.success("Registration successful! You can now log in.")


    if st.button("Register", type="primary"):

        if not username:
            st.error("Username cannot be empty.")
            return
        
        if get_user(conn, username):
            st.error(f"Username '{username}' already exists.")
            return
        
        if not check_password(password):
            st.error("Password must be at least 8 characters long, contain uppercase and lowercase letters, a digit, and a special character (!@#$%&*|).")
            return

        if not password:
            st.error("Password cannot be empty.")
            return

        if password != conf_password:
            st.error("Passwords do not match.")
            return

        
def login_user(conn):
    st.subheader("Log in to your account")

    username = st.text_input("Enter your username:", key="login_user")
    password = st.text_input("Enter your password:", type="password", key="login_pass")

    with open('DATA/users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        stored_username, stored_password = user.strip().split(',')
        if username == stored_username and password == stored_password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome back, {username}!")
            st.rerun()
            return    
    
    if st.button("Log In", type="primary"):
        user = get_user(conn, username)
    
        if user and verify_password(password, user[2]):  # user[2] is the password hash
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password.")   
            
def main():
    if "logged_in" not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None

    try:
        conn = sqlite3.connect('DATA/project_data.db')
        create_user_table(conn)

    except sqlite3.OperationalError:
        st.error("Database file not found. Please ensure 'DATA' directory exists.")
        return
    
    st.title("My Intelligence Platform")
    st.subheader("Cyber Incidents Dashboard")    

    if st.session_state['logged_in']:
        st.sidebar.write(f"Logged in as: **{st.session_state['username']}**")
        if st.sidebar.button("Log Out"):
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.success("You have been logged out.")
            st.rerun()

    else: 
        opt_1 , opt_2 = st.tabs(["Login", "Register"])
        with opt_1:
            login_user(conn)
        with opt_2:
            register_user(conn)    

    
if __name__ == "__main__":
    main()
