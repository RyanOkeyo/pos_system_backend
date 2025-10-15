from datetime import datetime
# Import db from models package to avoid circular import
from . import db

class Sale(db.Model):
    
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    sale_number = db.Column(db.String(50), unique=True, nullable=False)
    
    # Customer information (optional)
    customer_name = db.Column(db.String(100))
    customer_phone = db.Column(db.String(20))
    
    # Sale totals
    subtotal = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, default=0)
    discount_amount = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Payment information
    payment_method = db.Column(db.String(50))  # cash, card, mobile
    payment_status = db.Column(db.String(20), default='completed')  # completed, pending, refunded
    
    # Tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    items = db.relationship('SaleItem', backref='sale', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Sale {self.sale_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'sale_number': self.sale_number,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'subtotal': self.subtotal,
            'tax_amount': self.tax_amount,
            'discount_amount': self.discount_amount,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items]
        }


class SaleItem(db.Model):
    
    __tablename__ = 'sale_items'
    
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Item details
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<SaleItem {self.product_id} x {self.quantity}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'subtotal': self.subtotal
        }