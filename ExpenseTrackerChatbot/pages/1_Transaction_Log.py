import streamlit as st
from utils.expenseTracker import Account
import time

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to view your transaction log.")
    st.stop()

user_email = st.session_state.user_email
# db_name = f"{user_email}.db"
db_name = f"{user_email.replace('@', '_at_').replace('.', '_dot_')}.db"
account = Account(db_name = db_name)

st.title("Transaction Log")
st.divider()
if "balance" not in st.session_state:
    st.session_state.balance = account.get_balance(user_email)

formatted_balance = f"${st.session_state.balance:,.2f}"
st.write(f"Current Balance: {formatted_balance}")

# Add Expense
with st.expander("1. Add New Expense"):
    with st.form("expense_form"):
        exp_name = st.text_input("Expense Name / Title")
        exp_date = st.date_input("Expense Date")
        exp_amount = st.number_input("Expense Amount", min_value=0.0, format="%.2f")
        # exp_category = st.selectbox("Expense Category", ["Food", "Transport", "Utilities", "Entertainment", "Other"])
        exp_category = st.selectbox("Expense Category", ("-","Food 🍕", "Transport 🚌", "Utilities ⛽️", "Entertainment 🎥", "Health ⛑️", "Education 📚", "Shopping 🛒", "Other"))
        exp_description = st.text_area("Expense Description")
        exp_submit = st.form_submit_button("Add Expense ✅")

        if exp_submit:
            account.addExpense(exp_name, exp_date.strftime("%Y-%m-%d"), exp_amount, exp_category, exp_description)
            # st.session_state.balance = account.get_balance(user_email)
            st.session_state.balance -= exp_amount
            st.toast("✅ Expense added! Refreshing transaction log...")
            time.sleep(1.5)
            st.rerun()

# Add Income
with st.expander("2. Add New Income"):
    with st.form("income_form"):
        inc_name = st.text_input("Income Name / Title")
        inc_date = st.date_input("Income Date")
        inc_amount = st.number_input("Income Amount", min_value=0.0, format="%.2f")
        inc_source = st.text_input("Income Source")
        inc_description = st.text_area("Income Description")
        inc_submit = st.form_submit_button("Add Income ✅")

        if inc_submit:
            account.addIncome(inc_name, inc_date.strftime("%Y-%m-%d"), inc_amount, inc_source, inc_description)
            # st.session_state.balance = account.get_balance(user_email)
            st.session_state.balance += inc_amount
            st.toast("✅ Income added! Refreshing transaction log...")
            time.sleep(1.5)
            st.rerun()
             
