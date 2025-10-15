from flask import Flask
from flask_cors import CORS
from .utils.db import init_db

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object('app.config.Config')
    
    #Initialize database
    init_db(app)

    #Register Blueprints
    from app.routes.products import products_bp
    from app.routes.sales import sales_bp
    from app.routes.rents import rents_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')
    app.register_blueprint(rents_bp, url_prefix='/api/rents')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    return app


 