from flask import Blueprint, jsonify
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required
from app.utils.helpers import role_required

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_users():
    users = UserService.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    success, error = UserService.delete_user(user_id)
    if not success:
        return jsonify({'message': error}), 404
    return jsonify({'message': 'User deleted successfully'}), 200
