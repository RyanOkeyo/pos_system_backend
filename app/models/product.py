from datetime import datetime
from . import db

class Product(db.Model):

    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    size = db.Column(db.String(50))
    
    # Pricing
    sale_price = db.Column(db.Float, nullable=False)
    buying_price = db.Column(db.Float)
    rent_price_per_day = db.Column(db.Float)
    
    # Inventory
    quantity_in_stock = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=0)
    quantity_rented = db.Column(db.Integer, default=0)
    
    # Product details
    barcode = db.Column(db.String(50), unique=True)
    sku = db.Column(db.String(50), unique=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sale_items = db.relationship('SaleItem', backref='product', lazy=True)
    rent_items = db.relationship('RentItem', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'size': self.size,
            'sale_price': self.sale_price,
            'buying_price': self.buying_price,
            'rent_price_per_day': self.rent_price_per_day,
            'quantity_in_stock': self.quantity_in_stock,
            'reorder_level': self.reorder_level,
            'quantity_rented': self.quantity_rented,
            'barcode': self.barcode,
            'sku': self.sku,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }