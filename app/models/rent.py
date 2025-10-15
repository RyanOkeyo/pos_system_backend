from datetime import datetime
from . import db

class Rent(db.Model):
 
    __tablename__ = 'rents'
    
    id = db.Column(db.Integer, primary_key=True)
    rent_number = db.Column(db.String(50), unique=True, nullable=False)
    
    # Customer information (required for rentals)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(100))
    customer_id_number = db.Column(db.String(50))
    
    # Rental period
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    actual_return_date = db.Column(db.DateTime)
    
    # Financial details
    subtotal = db.Column(db.Float, nullable=False)
    deposit_amount = db.Column(db.Float, default=0)
    late_fee = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Payment information
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, partial
    
    # Status tracking
    rental_status = db.Column(db.String(20), default='active')  # active, returned, overdue, cancelled
    
    # Tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    items = db.relationship('RentItem', backref='rent', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Rent {self.rent_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'rent_number': self.rent_number,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_email': self.customer_email,
            'customer_id_number': self.customer_id_number,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'actual_return_date': self.actual_return_date.isoformat() if self.actual_return_date else None,
            'subtotal': self.subtotal,
            'deposit_amount': self.deposit_amount,
            'late_fee': self.late_fee,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'rental_status': self.rental_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items]
        }


class RentItem(db.Model):
   
    __tablename__ = 'rent_items'
    
    id = db.Column(db.Integer, primary_key=True)
    rent_id = db.Column(db.Integer, db.ForeignKey('rents.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Item details
    quantity = db.Column(db.Integer, nullable=False)
    daily_rate = db.Column(db.Float, nullable=False)
    number_of_days = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    # Return tracking
    returned = db.Column(db.Boolean, default=False)
    condition_on_return = db.Column(db.String(50))  # good, damaged, lost
    
    def __repr__(self):
        return f'<RentItem {self.product_id} x {self.quantity}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'rent_id': self.rent_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'daily_rate': self.daily_rate,
            'number_of_days': self.number_of_days,
            'subtotal': self.subtotal,
            'returned': self.returned,
            'condition_on_return': self.condition_on_return
        }