import streamlit as st

from app_model.metadatas import get_all_datasets_metadata
from app_model.db import get_db_connection

if st.session_state['logged_in']:
    st.success("You are logged in!")

conn = get_db_connection()

st.title("📋 Dataset Metadata Info")
st.write("Overview information detailing data structures, ownership matrix logs, and file schemas.")

try:
    meta_df = get_all_datasets_metadata(conn)

    col1, col2 = st.columns(2)

    col1.metric(label="Total Tracked Tables", value=len(meta_df))    
    col2.metric(label="Database Status", value="Connected")
        
    st.write("---")
    st.subheader("Database Schema Table")
    st.dataframe(meta_df, width="stretch")
        
except Exception as e:
        st.error(f"Error in loading: {e}")
