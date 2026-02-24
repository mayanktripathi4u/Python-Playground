import streamlit as st
import sqlite3
import time
from utils.expenseTracker import ExpenseManager, IncomeManager, Account
from auth import AuthManager

st.title("Expense Tracker with Chatbot")
st.write("An AI powered financial assistant to help you manage your expenses and income.")

auth = AuthManager()

# Session sate for user authentication & tracking user login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if auth.login_user(email, password):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("Logged in successfully!")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("Invalid email or password.")

with tab2:
    st.subheader("Register")
    reg_email = st.text_input("New Email to Register with", key="reg_email")
    reg_password = st.text_input("Password", type="password", key="reg_password")
    if st.button("Register"):
        if auth.register_user(reg_email, reg_password):
            st.success("Registered successfully! Please log in.")
        else:
            st.error("Registration failed. Email may already be in use.")

# Check if the user is logged in
if st.session_state.logged_in:
    st.success(f"Welcome, {st.session_state.user_email}!\nHead to side bar to use features.")

# Dynamically set the database name
db_name = "expenses.db"

# Initialize the managers with the database name
ExManager = ExpenseManager(db_name)
InManager = IncomeManager(db_name)
AccManager = Account(db_name)

# Establish a connection to the SQLite database
conn = sqlite3.connect(db_name)
c = conn.cursor()

if st.session_state.logged_in:
    st.toast("You are logged in! Use the sidebar to navigate through the features.")

# Close the database connection when the app is closed
conn.close()
