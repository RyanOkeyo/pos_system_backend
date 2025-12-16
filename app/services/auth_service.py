from app.models import db, User
from flask_jwt_extended import create_access_token
from datetime import datetime
from flask import current_app

class AuthService:

    @staticmethod
    def register_user(username, password, email, role='user', security_code=None):
        if role == 'admin':
            if not security_code or security_code != current_app.config['ADMIN_SECURITY_CODE']:
                return None, "Invalid security code for admin registration"

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return None, "User with this username or email already exists"
        
        try:
            new_user = User(
                username=username,
                email=email,
                role=role
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            return new_user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def login_user(login_identifier, password):
        user = User.query.filter((User.username == login_identifier) | (User.email == login_identifier)).first()

        if user and user.check_password(password):
            if not user.is_active:
                return None, "User account is disabled"
            
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            additional_claims = {"role": user.role}
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
            return access_token, None
        
        return None, "Invalid credentials"

    @staticmethod
    def request_password_reset(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return None, "User with this email does not exist"
        
        token = user.get_reset_token()
        # In a real app, you would email this token. For this demo, we print it.
        print(f"Password reset link: http://localhost:3000/reset-password/{token}")
        return "Password reset link has been generated. Check the console.", None

    @staticmethod
    def reset_password(token, new_password):
        user = User.verify_reset_token(token)
        if not user:
            return None, "Invalid or expired token"
        
        try:
            user.set_password(new_password)
            db.session.commit()
            return "Password has been reset successfully.", None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
