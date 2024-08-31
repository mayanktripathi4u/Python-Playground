from flask import Blueprint, jsonify, request
from app.services.user_service import get_user, create_user

bp = Blueprint('user', __name__, url_prefix='/api/users')

@bp.route('/', methods=['GET'])
def list_users():
    users = get_user()
    return jsonify(users)

@bp.route('/', methods=['POST'])
def add_user():
    data = request.json
    new_user = create_user(data)
    return jsonify(new_user), 201
