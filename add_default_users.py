from app import create_app, db
from app.models.user import User

def add_default_users():
    app = create_app()
    with app.app_context():
        # Admin user
        if not User.query.filter_by(email='admintest@gmail.com').first():
            admin_user = User(
                username='admin',
                email='admintest@gmail.com',
                role='admin'
            )
            admin_user.set_password('zxcv')
            db.session.add(admin_user)
            print("Admin user created.")

        # Normal user
        if not User.query.filter_by(email='usertest@gmail.com').first():
            normal_user = User(
                username='user',
                email='usertest@gmail.com',
                role='user'
            )
            normal_user.set_password('zxcv')
            db.session.add(normal_user)
            print("Normal user created.")

        db.session.commit()
        print("Default users checked/created successfully.")

if __name__ == '__main__':
    add_default_users()
