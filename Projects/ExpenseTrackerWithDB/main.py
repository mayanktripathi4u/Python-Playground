# Expense Tracker App in Python

# STep 1: Create a Database to Store Expenses

import sqlite3
from datetime import datetime

# Create Initialization Function

def init():
    conn = sqlite3.connect('spent.db')

    cur = conn.cursor()

    command = """create table if not exists expenses(amount number, category string, message string, date string);"""

    cur.execute(command)

    conn.commit()

# init()
# Database created successfully now lets add info.
def log(amount, category, message=''):
    # message is optional
    # lets add a date value
    date = str(datetime.now())

    # Connect Database
    conn = sqlite3.connect('spent.db')

    # Lets create
    
    cur = conn.cursor()

    command = """insert into expenses(amount, category, message, date) values({}, '{}', '{}', '{}');""".format(amount, category, message, date)
    
    cur.execute(command)

    conn.commit()

# log(120, 'food', 'lunch')
# print("Successful.")

def view(category=None):
    conn = sqlite3.connect('spent.db')

    # Lets create
    
    cur = conn.cursor()
    if category:
        sql1 = """select sum(amount) from expenses where category = '{}'; """.format(category)
        sql2 = """select * from expenses where category = '{}'; """.format(category)
    else:
        sql1 = """select sum(amount) from expenses ; """
        sql2 = """select * from expenses ; """
    
    cur.execute(sql1)
    total_amount = cur.fetchone()[0]
    cur.execute(sql2)
    result = cur.fetchall()

    return total_amount, result

print(view())