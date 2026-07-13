import sqlite3
import streamlit as st

@st.cache_resource
def get_db_connection():
    """
    Creates and caches the database connection. 
    check_same_thread=False allows Streamlit's multiple worker threads 
    to safely interact with the SQLite file.
    """
    return sqlite3.connect('DATA/project_data.db', check_same_thread=False)

# This exposes the connection object safely to the rest of your app modules
conn = get_db_connection()