from flask import Blueprint, request, jsonify
from app.models import User
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight successful'}), 200
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role', 'user')
    security_code = data.get('security_code')

    if not username or not password or not email:
        return jsonify({'message': 'Username, password, and email are required'}), 400

    user, error = AuthService.register_user(username, password, email, role, security_code)

    if error:
        return jsonify({'message': error}), 400

    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight successful'}), 200
    data = request.get_json()
    login_identifier = data.get('username') or data.get('email')
    password = data.get('password')

    if not login_identifier or not password:
        return jsonify({'message': 'Username/email and password are required'}), 400

    token, error = AuthService.login_user(login_identifier, password)

    if error:
        return jsonify({'message': error}), 401
    
    user = User.query.filter((User.username == login_identifier) | (User.email == login_identifier)).first()

    return jsonify({'access_token': token, 'user': user.to_dict()})

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'message': 'Email is required'}), 400

    message, error = AuthService.request_password_reset(email)
    if error:
        return jsonify({'message': error}), 404
    
    return jsonify({'message': message}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('password')
    if not new_password:
        return jsonify({'message': 'New password is required'}), 400

    message, error = AuthService.reset_password(token, new_password)
    if error:
        return jsonify({'message': error}), 400
        
    return jsonify({'message': message}), 200
