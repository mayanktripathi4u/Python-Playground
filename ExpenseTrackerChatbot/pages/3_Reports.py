import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
import cohere
from utils.expenseTracker import Account
from utils.synbot import get_gudget_insights

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to view your reports.")
    st.stop()

user_email = st.session_state.user_email
# db_name = f"{user_email}.db"
db_name = f"{user_email.replace('@', '_at_').replace('.', '_dot_')}.db"
account = Account(db_name = db_name)

st.title("Expense & Income Reports")
st.write("A Financial Overview of Your Transactions")
st.divider()

expenses_df = account.expenseList(user_email)
income_df = account.incomeList(user_email)

if not expenses_df.empty:
    expenses_df['date'] = pd.to_datetime(expenses_df['date'])
if not income_df.empty:
    income_df['date'] = pd.to_datetime(income_df['date'])

col1, col2 = st.columns(2)
with col1:
    if not expenses_df.empty:
        category_data = expenses_df.groupby('category')['amount'].sum().reset_index()
        fig_expanse_pie = px.pie(
            category_data,
            names='category',
            values='amount',
            title='Expense Distribution by Category',
            hole=0.4
        )
        st.plotly_chart(fig_expanse_pie, use_container_width=True)
    else:
        st.write("No expense data to display.")

# Income breakdown
with col2:
    if not income_df.empty:
        source_data = income_df.groupby('source')['amount'].sum().reset_index()
        fig_income_pie = px.pie(
            source_data,
            names='source',
            values='amount',
            title='Income Distribution by Source',
            hole=0.4
        )
        st.plotly_chart(fig_income_pie, use_container_width=True)
    else:
        st.write("No income data to display.")

if not expenses_df.empty and not income_df.empty:
    expenses_df['month'] = expenses_df['date'].dt.strftime('%Y-%m')
    income_df['month'] = income_df['date'].dt.strftime('%Y-%m')

    monthly_expense = expenses_df.groupby('month')['amount'].sum().reset_index()
    monthly_income = income_df.groupby('month')['amount'].sum().reset_index()

    # Create an area chart for monthly expenses and income
    fig = px.area(
        pd.concat([monthly_expense.assign(type='Expense'), monthly_income.assign(type='Income')]),
        x='month',
        y='amount',
        color='type',
        title='Monthly Expenses vs Income Trend',
        line_group='Type',
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)


# bar chart: monthly spending by categroy
if not expenses_df.empty:
    category_monthly_data = expenses_df.groupby(['month', 'category'])['amount'].sum().reset_index()
    fig_category_bar = px.bar(
        category_monthly_data,
        x='month',
        y='amount',
        color='category',
        barmode='group',
        title='Monthly Spending by Category'
    )
    st.plotly_chart(fig_category_bar, use_container_width=True)

# Standard bar chart: Income vs Expense
if not expenses_df.empty and not income_df.empty:
    stacked_data = pd.merge([
        monthly_expense.assign(Type="Expense"),
        monthly_income.assign(Type="Income")
    ])
    fig_stacked_bar = px.bar(stacked_data, x='month', y='amount', color='Type', title='Monthly Income vs Expense', barmode='stack')

with st.sidebar:
    st.markdown(
        """
        <style>
        .chatbot-container {
            display: flex;
            align-item: center;
            gap: 10px;
            cursor: pointer;
            margin-bottom: 20px;
        }

        .chatbot-icon {
            background-color: #ff4b87;
            color: 40px;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
        }

        .chatbot-name {
            background-color: white;
            color: #333;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
        </style>
        <div class="chatbot-container" onclick="document.getElementById('chatbot_expander').click();">
            <div class="chatbot-icon">💬</div>
            <div class="chatbot-name">Gudget Chatbot</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("Gudget Chatbot", expanded=False):
        st.write(f"Hi {st.session_state.user_email.split('@')[0]}! I'm Gudget, your personal financial assistant. Ask me anything about your expenses and income!")

        user_query = st.text_input("Enter your question here:", key="chatbot_query")

        if st.button("Send"):
            if user_query.strip() == "":
                st.warning("Please enter a question.")
            else:
                with st.spinner("Generating response..."):
                    transaction_text = account.format_transaction_for_all()
                    budget_tip = get_budget_insights(user_query=user_query, transactions=transaction_text)
                    st.write(budget_tip)
                    # response = get_gudget_insights(co, user_query, expenses_df, income_df)
                    # st.markdown(f"**Gudget's Response:** {response}")
                    