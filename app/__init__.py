from flask import Flask
from flask_cors import CORS
from app.utils.db import init_db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.models import db
import os

def create_app():
    app = Flask(__name__, instance_path="/tmp/instance")
    
    # Define allowed origins
    origins = [
        "https://pos-system-frontend-tau.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://pos-system-frontend-git-main-ryans-projects-86863339.vercel.app",
        "https://pos-backend-oai2.onrender.com",
        "https://pos-system-backend-beta.vercel.app",
        "https://pos-system-backend-git-main-ryans-projects-86863339.vercel.app",
        "https://pos-system-backend-g1jox451s-ryans-projects-86863339.vercel.app",
        "https://pos-system-backend-g3d2emkkz-ryans-projects-86863339.vercel.app"
    ]

    CORS(app, resources={r"/api/*": {"origins": origins}}, supports_credentials=True)

    app.config.from_object('app.config.Config')

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #Initialize database
    init_db(app)

    # Initialize Migrate
    migrate = Migrate(app, db)

    # Initialize JWT Manager
    jwt = JWTManager(app)

    #Register Blueprints
    from app.routes.products import products_bp
    from app.routes.sales import sales_bp
    from app.routes.rents import rents_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp

    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')
    app.register_blueprint(rents_bp, url_prefix='/api/rents')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    @app.route('/')
    def index():
        return {"status": "healthy"}

    return app


