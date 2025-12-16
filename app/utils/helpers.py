from datetime import datetime
import random
import string
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, get_jwt

def generate_sale_number():
    
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.digits, k=5))
    return f"SALE-{date_str}-{random_str}"

def generate_rent_number():
  
    date_str = datetime.now().strftime('%Y%m%d')
    random_str = ''.join(random.choices(string.digits, k=5))
    return f"RENT-{date_str}-{random_str}"

def validate_stock(product, requested_quantity):
  
    available = product.quantity_in_stock - product.quantity_rented
    
    if available >= requested_quantity:
        return True, "Stock available"
    else:
        return False, f"Insufficient stock. Available: {available}, Requested: {requested_quantity}"

def format_currency(amount):
    
    return f"ksh{amount:,.2f}"

def paginate_results(query, page=1, per_page=10):
    
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')

            if user_role == role:
                return fn(*args, **kwargs)
            else:
                return jsonify({'message': f'Access restricted to {role}s'}), 403
        return wrapper
    return decorator