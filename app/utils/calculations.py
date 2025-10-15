from datetime import datetime

def calculate_sale_total(items):
   
    subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
    tax_rate = 0.0  # Set your tax rate (e.g., 0.10 for 10%)
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount
    
    return {
        'subtotal': round(subtotal, 2),
        'tax_amount': round(tax_amount, 2),
        'total': round(total, 2)
    }

def calculate_rent_total(items, start_date, end_date, deposit_percentage=0.2):
   
    # Calculate number of days
    start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    number_of_days = (end - start).days + 1  # Include both start and end day
    
    if number_of_days < 1:
        number_of_days = 1
    
    # Calculate subtotal
    subtotal = sum(
        item['quantity'] * item['daily_rate'] * number_of_days 
        for item in items
    )
    
    # Calculate deposit (default 20% of subtotal)
    deposit = subtotal * deposit_percentage
    
    total = subtotal + deposit
    
    return {
        'subtotal': round(subtotal, 2),
        'deposit_amount': round(deposit, 2),
        'total': round(total, 2),
        'number_of_days': number_of_days
    }

def calculate_late_fee(end_date, actual_return_date, daily_rate, late_fee_multiplier=1.5):
  
    end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    actual_return = datetime.fromisoformat(actual_return_date.replace('Z', '+00:00'))
    
    days_late = (actual_return - end).days
    
    if days_late <= 0:
        return 0
    
    late_fee = days_late * daily_rate * late_fee_multiplier
    return round(late_fee, 2)

def apply_discount(subtotal, discount_type, discount_value):
  
    if discount_type == 'percentage':
        discount_amount = subtotal * (discount_value / 100)
    else:  # fixed
        discount_amount = discount_value
    
    return round(discount_amount, 2)