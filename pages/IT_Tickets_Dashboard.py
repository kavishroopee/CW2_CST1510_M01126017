import streamlit as st

from app_model.it_tickets import get_all_it_tickets
from app_model.db import get_db_connection

if st.session_state['logged_in']:
    st.success("You are logged in!")

conn = get_db_connection()
Data = get_all_it_tickets(conn)

st.title("Welcome to the 🎫 IT Tickets Dashboard")

Data = get_all_it_tickets(conn)

with st.sidebar:
        st.header("Navigation")
        priority = st.selectbox('Select Ticket Priority', Data['priority'].unique()) 

filter_tickets = Data[Data['priority'] == priority]

col1, col2 = st.columns(2)

with col1:
        st.subheader(f"IT Tickets by status {priority}")
        st.bar_chart(filter_tickets['status'].value_counts())

with col2:
        st.subheader(f"Ticket Status {priority}")
        st.bar_chart(filter_tickets['status'].value_counts())

st.subheader("Filtered Ticket Logs")
st.dataframe(filter_tickets, width="stretch") 
