from app.models import db, Rent, RentItem, Product
from app.utils.calculations import calculate_rent_total, calculate_late_fee
from app.utils.helpers import generate_rent_number, validate_stock
from datetime import datetime

class RentService:
    
    @staticmethod
    def get_all_rents(status=None, start_date=None, end_date=None):
    
        query = Rent.query
        
        if status:
            query = query.filter_by(rental_status=status)
        
        if start_date:
            query = query.filter(Rent.start_date >= start_date)
        
        if end_date:
            query = query.filter(Rent.end_date <= end_date)
        
        return query.order_by(Rent.created_at.desc()).all()
    
    @staticmethod
    def get_rent_by_id(rent_id):
    
        return Rent.query.get(rent_id)
    
    @staticmethod
    def create_rent(rent_data, user_id=None):
        try:
            # Validate stock for all items
            for item in rent_data['items']:
                product = Product.query.get(item['product_id'])
                if not product:
                    return None, f"Product {item['product_id']} not found"
                
                is_valid, message = validate_stock(product, item['quantity'])
                if not is_valid:
                    return None, f"Product '{product.name}': {message}"
            
            # Calculate totals
            totals = calculate_rent_total(
                rent_data['items'],
                rent_data['start_date'],
                rent_data['end_date'],
                rent_data.get('deposit_percentage', 0.2)
            )
            
            # Create rent
            rent = Rent(
                rent_number=generate_rent_number(),
                customer_name=rent_data['customer_name'],
                customer_phone=rent_data['customer_phone'],
                customer_email=rent_data.get('customer_email'),
                customer_id_number=rent_data.get('customer_id_number'),
                start_date=datetime.fromisoformat(rent_data['start_date'].replace('Z', '+00:00')),
                end_date=datetime.fromisoformat(rent_data['end_date'].replace('Z', '+00:00')),
                subtotal=totals['subtotal'],
                deposit_amount=totals['deposit_amount'],
                total_amount=totals['total'],
                payment_method=rent_data['payment_method'],
                payment_status='paid',
                rental_status='active',
                user_id=user_id
            )
            
            db.session.add(rent)
            db.session.flush()
            
            # Create rent items and update stock
            for item_data in rent_data['items']:
                product = Product.query.get(item_data['product_id'])
                
                subtotal = item_data['quantity'] * item_data['daily_rate'] * totals['number_of_days']
                
                rent_item = RentItem(
                    rent_id=rent.id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    daily_rate=item_data['daily_rate'],
                    number_of_days=totals['number_of_days'],
                    subtotal=subtotal
                )
                
                db.session.add(rent_item)
                
                # Update product rented quantity
                product.quantity_rented += item_data['quantity']
            
            db.session.commit()
            return rent, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def return_rent(rent_id, return_data):
        
        rent = Rent.query.get(rent_id)
        
        if not rent:
            return None, "Rental not found"
        
        if rent.rental_status == 'returned':
            return None, "Rental already returned"
        
        try:
            actual_return_date = datetime.fromisoformat(
                return_data['actual_return_date'].replace('Z', '+00:00')
            )
            
            rent.actual_return_date = actual_return_date
            rent.rental_status = 'returned'
            
            # Calculate late fee if overdue
            if actual_return_date > rent.end_date:
                total_daily_rate = sum(item.daily_rate * item.quantity for item in rent.items)
                late_fee = calculate_late_fee(
                    rent.end_date.isoformat(),
                    actual_return_date.isoformat(),
                    total_daily_rate
                )
                rent.late_fee = late_fee
                rent.total_amount += late_fee
            
            # Update rent items and product stock
            for item_info in return_data['items']:
                rent_item = RentItem.query.filter_by(
                    rent_id=rent_id,
                    product_id=item_info['product_id']
                ).first()
                
                if rent_item:
                    rent_item.returned = True
                    rent_item.condition_on_return = item_info.get('condition_on_return', 'good')
                    
                    # Return stock
                    product = Product.query.get(rent_item.product_id)
                    product.quantity_rented -= rent_item.quantity
            
            db.session.commit()
            return rent, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_overdue_rents():
    
        now = datetime.utcnow()
        return Rent.query.filter(
            Rent.rental_status == 'active',
            Rent.end_date < now
        ).all()