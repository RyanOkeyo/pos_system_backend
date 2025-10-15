from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.product import Product 
from app.models.sale import Sale, SaleItem
from app.models.rent import Rent, RentItem
from app.models.user import User

__all__ = ['db', 'Product', 'Sale', 'SaleItem', 'Rent', 'RentItem', 'User']

