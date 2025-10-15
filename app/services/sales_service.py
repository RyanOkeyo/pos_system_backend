from app.models import db, Sale, SaleItem, Product
from app.utils.calculations import calculate_sale_total, apply_discount
from app.utils.helpers import generate_sale_number, validate_stock
from datetime import datetime

class SalesService:
    
    @staticmethod
    def get_all_sales(start_date=None, end_date=None, payment_method=None):
        query = Sale.query
        
        if start_date:
            query = query.filter(Sale.created_at >= start_date)
        
        if end_date:
            query = query.filter(Sale.created_at <= end_date)
        
        if payment_method:
            query = query.filter_by(payment_method=payment_method)
        
        return query.order_by(Sale.created_at.desc()).all()
    
    @staticmethod
    def get_sale_by_id(sale_id):
        
        return Sale.query.get(sale_id)
    
    @staticmethod
    def create_sale(sale_data, user_id=None):
        
        try:
            # Validate stock for all items
            for item in sale_data['items']:
                product = Product.query.get(item['product_id'])
                if not product:
                    return None, f"Product {item['product_id']} not found"
                
                is_valid, message = validate_stock(product, item['quantity'])
                if not is_valid:
                    return None, f"Product '{product.name}': {message}"
            
            # Calculate totals
            totals = calculate_sale_total(sale_data['items'])
            
            # Apply discount if provided
            discount_amount = sale_data.get('discount_amount', 0)
            final_total = totals['total'] - discount_amount
            
            # Create sale
            sale = Sale(
                sale_number=generate_sale_number(),
                customer_name=sale_data.get('customer_name'),
                customer_phone=sale_data.get('customer_phone'),
                subtotal=totals['subtotal'],
                tax_amount=totals['tax_amount'],
                discount_amount=discount_amount,
                total_amount=final_total,
                payment_method=sale_data['payment_method'],
                payment_status='completed',
                user_id=user_id
            )
            
            db.session.add(sale)
            db.session.flush()  # Get sale.id before adding items
            
            # Create sale items and update stock
            for item_data in sale_data['items']:
                product = Product.query.get(item_data['product_id'])
                
                subtotal = item_data['quantity'] * item_data['unit_price']
                
                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=item_data['product_id'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    subtotal=subtotal
                )
                
                db.session.add(sale_item)
                
                # Update product stock
                product.quantity_in_stock -= item_data['quantity']
            
            db.session.commit()
            return sale, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_sales_summary(start_date=None, end_date=None):
        
        query = Sale.query
        
        if start_date:
            query = query.filter(Sale.created_at >= start_date)
        
        if end_date:
            query = query.filter(Sale.created_at <= end_date)
        
        sales = query.all()
        
        total_sales = len(sales)
        total_revenue = sum(sale.total_amount for sale in sales)
        
        return {
            'total_sales': total_sales,
            'total_revenue': round(total_revenue, 2),
            'average_sale': round(total_revenue / total_sales, 2) if total_sales > 0 else 0
        }