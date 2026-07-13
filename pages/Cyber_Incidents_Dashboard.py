import streamlit as st
import pandas as pd

from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.db import get_db_connection

if st.session_state['logged_in']:
    st.success("You are logged in!")

conn = get_db_connection()
data = get_all_cyber_incidents(conn)

st.title("Welcome to the 🛡️ Cyber Incident Dashboard")

with st.sidebar:
        st.header("Navigation")
        severity = st.selectbox('Select Severity  Level', data['severity'].unique())

data['timestamp'] = pd.to_datetime(data['timestamp'])
filtered_data = data[data['severity'] == severity]   

col1, col2 = st.columns(2)

with col1:
        st.subheader(f"Incidents by Category : {severity}")
        st.bar_chart(filtered_data['category'].value_counts())

with col2:
        st.subheader("Category Trend Over Time")
        st.line_chart(filtered_data, x='timestamp', y='category')

st.subheader("Filtered Data Logs") 
st.dataframe(filtered_data, width="stretch")   
