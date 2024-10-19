# import bcrypt
from auth import auth
from flask import render_template, redirect, session, url_for, flash
from models.user import User
from auth.forms.login_form import LoginForm
from auth.forms.sign_up_form import RegisterForm
from datetime import datetime
from models import db


# @app.before_request
# def update_last_seen():
#     if current_user.is_authenticated:
#         current_user.last_seen = datetime.now(tzinfo=UTC) #utcnow doesn't actually attach a timezone
#         db.session.add(current_user) 
#         db.session.commit()

@auth.route('/auth/login', methods = ['GET', 'POST'])
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): 
        email = form.email.data
        password = form.password.data
        last_login = datetime.now()

        print(f"Email : {email} and Password : {password}")

        # # Retrieve data into Database
        # Fetch the user from the database by email
        user = User.query.filter_by(email = email).first()

        if user and user.check_password(password):
            # Log the user in using Flask-Login's login_user (https://pypi.org/project/Flask-Login/)
            # login_user(user)

            session['user_email'] = email
            session['user_name'] = user.username
            session['user_id'] = user.id

            flash("Login successful! Welcome back.", "success")
            return redirect(url_for('core.dashboard'))  # Replace 'core.dashboard' with your dashboard route

        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template('login.html', form = form)

@auth.route('/auth/register', methods = ['GET', 'POST'])
@auth.route('/register', methods = ['GET', 'POST'])
def register_api():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        last_login = datetime.now()

        # Fetch the user from the database by email
        user = User.query.filter_by(email = email).first()

        if user:
            flash("User already exists! Please Login.", "error")
            return render_template('auth.login')
        else:
            # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # print(f"Hased Password is on length {len(hashed_password)} : {hashed_password}")
            # print(f"User entered Data : \nUser Name : {username}\nEmail : {email}\nPassword : {password}")

            new_user = User(username = username, email = email, last_login = last_login)
            new_user.set_password(password=password)
            db.session.add(new_user)
            db.session.commit()

        flash("Registration Successfull! Please Login.", "success")

        return redirect(url_for('auth.login')) # Provide name of function

    return render_template('register.html', form = form)

@auth.route('/logout')
def logout():
    flash("You have been logged-out successfully!", "info")
    session.pop('user_email', None)
    session.pop('user_name', None)
    session.pop('user_id', None) 
    return redirect(url_for('auth.login'))