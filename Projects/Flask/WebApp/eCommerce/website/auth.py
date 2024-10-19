from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'this is login page'

@auth.route('/sign-up')
def sign_up():
    return 'this is sign-up page'