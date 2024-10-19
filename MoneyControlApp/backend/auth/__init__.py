from flask import Blueprint
import os

# Define the path to the frontend directory
template_dir = os.path.abspath('../frontend/auth')

auth = Blueprint('auth', __name__, template_folder = template_dir)

from auth import routes