import sqlite3
import pandas as pd
from datetime import datetime
import streamlit as st

class ExpenseManager:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_expense_table()

    def create_expense_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT,
                       date DATE,
                       amount REAL, 
                       category TEXT, 
                       description TEXT)''')
        self.conn.commit()

    def add_expense(self, name, date, amount, category, description):
        self.c.execute("INSERT INTO expenses (name, date, amount, category, description) VALUES (?, ?, ?, ?, ?)", 
                       (name, date, amount, category, description))
        self.conn.commit()

    def get_expenses(self, user_email=""):
        # self.c.execute("SELECT * FROM expenses WHERE 1 = 1 AND (? = '' OR user_email = ?)", (user_email, user_email))
        # rows = self.c.fetchall()
        # return pd.DataFrame(rows, columns=['id', 'user_email', 'amount', 'category', 'date', 'description'])
        
        query = f"SELECT * FROM expenses WHERE 1 = 1 AND (? = '' OR user_email = ?), (user_email, user_email)"
        return pd.read_sql(query, self.conn, params=(user_email, user_email))
    
    def delete_expense(self, expense_id):
        self.c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()

class IncomeManager:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_income_table()

    def create_income_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS incomes (
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT,
                       date DATE,
                       amount REAL, 
                       source TEXT, 
                       description TEXT)''')
        self.conn.commit()

    def add_income(self, name, date, amount, source, description):
        self.c.execute("INSERT INTO incomes (name, date, amount, source, description) VALUES (?, ?, ?, ?, ?)", 
                       (name, date, amount, source, description))
        self.conn.commit()

    def get_incomes(self, user_email=""):
        query = f"SELECT * FROM incomes WHERE 1 = 1 AND (? = '' OR user_email = ?), (user_email, user_email)"
        return pd.read_sql(query, self.conn, params=(user_email, user_email))

    def delete_income(self, income_id):
        self.c.execute("DELETE FROM incomes WHERE id = ?", (income_id,))
        self.conn.commit()

class Account:
    def __init__(self, db_name="expenses.db"):
        self.IncomeManager = IncomeManager(db_name)
        self.ExpenseManager = ExpenseManager(db_name)
        self.Balance = 0.0

    def get_balance(self, user_email=""):
        total_income = self.IncomeManager.get_incomes(user_email)['amount'].sum()
        total_expense = self.ExpenseManager.get_expenses(user_email)['amount'].sum()
        self.Balance = total_income - total_expense
        return self.Balance
    
    def addExpense(self, name, date, amount, category, description):
        self.ExpenseManager.add_expense(name, date, amount, category, description)
        self.Balance -= amount
        st.success(f"Expense of {amount} added successfully!")

    def addIncome(self, name, date, amount, source, description):
        self.IncomeManager.add_income(name, date, amount, source, description)
        self.Balance += amount
        st.success(f"Income of {amount} added successfully!")

    def expenseList(self, user_email=""):
        return self.ExpenseManager.get_expenses(user_email)
    
    def incomeList(self, user_email=""):
        return self.IncomeManager.get_incomes(user_email)   
    
    def deleteExpense(self, expense_id):
        expenses = self.ExpenseManager.get_expenses()
        if expenses.empty:
            st.warning("No expenses found.")
            return
        
        if expense_id not in expenses['id'].values:
            amount = expenses.loc[expenses['id'] == expense_id, 'amount'].values[0]
            self.ExpenseManager.delete_expense(expense_id)
            self.Balance += amount
            st.success(f"Expense with ID {expense_id} deleted successfully!")
        else:
            st.warning(f"Expense with ID {expense_id} not found.")

    def deleteIncome(self, income_id):
        incomes = self.IncomeManager.get_incomes()
        if incomes.empty:
            st.warning("No incomes found.")
            return
        
        if income_id not in incomes['id'].values:
            amount = incomes.loc[incomes['id'] == income_id, 'amount'].values[0]
            self.IncomeManager.delete_income(income_id)
            self.Balance -= amount
            st.success(f"Income with ID {income_id} deleted successfully!")
        else:
            st.warning(f"Income with ID {income_id} not found.")

    def format_transaction_for_all(self):
        expenses = self.ExpenseManager.get_expenses()
        incomes = self.IncomeManager.get_incomes()

        forwarded_expenses = expenses[['name', 'date', 'amount', 'category', 'description']].to_dict(orient='records')
        forwarded_incomes = incomes[['name', 'date', 'amount', 'source', 'description']].to_dict(orient='records')

        transactions = {
            "income": forwarded_incomes,
            "expenses": forwarded_expenses
        }
        return transactions
    
