from flask import Blueprint, request, jsonify
from flask_login import login_user
from models.user import User
from services.user_service import create_user

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    user, error = create_user(name, email, password)

    if error == "Missing required fields":
        return jsonify({'error': error}), 400
    if error == "User already exists":
        return jsonify({'error': error}), 409

    login_user(user)
    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login_user_route():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Missing credentials'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    login_user(user)

    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
    }), 200