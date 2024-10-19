from flask import Blueprint
import os

# Define the path to the frontend directory
template_dir = os.path.abspath('../frontend/core')
print(f"Template Dir ==> {template_dir}")

core = Blueprint('core', __name__, template_folder = template_dir)

from core import routes