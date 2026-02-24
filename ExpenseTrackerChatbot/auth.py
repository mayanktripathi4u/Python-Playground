import sqlite3
import streamlit as st
import hashlib

class AuthManager:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_user_table()

    def create_user_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS users (
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       email TEXT UNIQUE, 
                       password TEXT)''')
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, email, password):
        try:
            hashed_password = self.hash_password(password)
            self.c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, email, password):
        hashed_password = self.hash_password(password)
        self.c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_password))
        return self.c.fetchone() is not None