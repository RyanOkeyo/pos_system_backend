from datetime import datetime
import random
import string

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