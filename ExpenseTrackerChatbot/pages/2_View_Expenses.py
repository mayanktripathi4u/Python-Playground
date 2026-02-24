import streamlit as st
from utils.expenseTracker import Account
import time

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to view your expenses.")
    st.stop()

user_email = st.session_state.user_email
# db_name = f"{user_email}.db"
db_name = f"{user_email.replace('@', '_at_').replace('.', '_dot_')}.db"

account = Account(db_name = db_name)

st.title("View Transaction Expenses")
st.divider()

st.subheader("Your Expenses")
expenses_df = account.expenseList(user_email)
if expenses_df.empty:
    st.caption("No expenses recorded yet. >^<")
else:
    # st.dataframe(expenses_df.style.format({"amount": "${:,.2f}"}), use_container_width=True)
    st.dataframe(expenses_df)

if not expenses_df.empty:
    with st.expander("Delete an Expense"):
        with st.form("delete_expense_form"):
            del_expense_id = st.number_input("Enter Expense ID to Delete", min_value=1, step=1)
            if st.form_submit_button("Delete Expense ❌"):
                account.deleteExpense(del_expense_id)
                st.toast("✅ Expense deleted! Refreshing expense list...")
                time.sleep(1.5)
                st.rerun()

# Income Section
st.subheader("Your Incomes")
incomes_df = account.incomeList(user_email)
if incomes_df.empty:
    st.caption("No incomes recorded yet. >^<")
else:
    # st.dataframe(incomes_df.style.format({"amount": "${:,.2f}"}), use_container_width=True)
    st.dataframe(incomes_df)

# Delete Income
if not incomes_df.empty:
    with st.expander("Delete an Income"):
        with st.form("delete_income_form"):
            del_income_id = st.number_input("Enter Income ID to Delete", min_value=1, step=1)
            if st.form_submit_button("Delete Income ❌"):
                account.deleteIncome(del_income_id)
                st.toast("✅ Income deleted! Refreshing income list...")
                time.sleep(1.5)
                st.rerun()