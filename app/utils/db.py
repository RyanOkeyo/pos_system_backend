from app.models import db 

def init_db(app):
    db.init_app(app)

    # with app.app_context():
    #     #Create tables
    #     db.create_all()
    #     print("Database initialized successfully!")

def get_db():
    return db
