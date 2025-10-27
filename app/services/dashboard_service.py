from app.models import db, Sale, Rent, Product
from sqlalchemy import func
from datetime import datetime, timedelta

class DashboardService:
    
    @staticmethod
    def get_dashboard_stats(start_date=None, end_date=None):
        
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Sales statistics
        sales = Sale.query.filter(
            Sale.created_at >= start_date,
            Sale.created_at <= end_date
        ).all()
        
        total_sales_count = len(sales)
        total_sales_revenue = sum(sale.total_amount for sale in sales)
        
        # Rentals statistics
        rents = Rent.query.filter(
            Rent.created_at >= start_date,
            Rent.created_at <= end_date
        ).all()
        
        total_rents_count = len(rents)
        total_rents_revenue = sum(rent.total_amount for rent in rents)
        
        # Active rentals
        active_rents = Rent.query.filter_by(rental_status='active').count()
        
        # Overdue rentals
        overdue_rents = Rent.query.filter(
            Rent.rental_status == 'active',
            Rent.end_date < datetime.utcnow()
        ).count()
        
        # Low stock products (less than 10 units)
        low_stock_products = Product.query.filter(
            Product.quantity_in_stock < 10
        ).count()
        
        # Total products
        total_products = Product.query.count()
        
        return {
            'sales': {
                'count': total_sales_count,
                'revenue': round(total_sales_revenue, 2)
            },
            'rentals': {
                'count': total_rents_count,
                'revenue': round(total_rents_revenue, 2),
                'active': active_rents,
                'overdue': overdue_rents
            },
            'products': {
                'total': total_products,
                'low_stock': low_stock_products
            },
            'total_revenue': round(total_sales_revenue + total_rents_revenue, 2)
        }
    
    @staticmethod
    def get_top_selling_products(limit=10):
        
        from app.models.sale import SaleItem
        
        results = db.session.query(
            Product.id,
            Product.name,
            func.sum(SaleItem.quantity).label('total_sold'),
            func.sum(SaleItem.subtotal).label('total_revenue')
        ).join(SaleItem).group_by(Product.id).order_by(
            func.sum(SaleItem.quantity).desc()
        ).limit(limit).all()
        
        return [
            {
                'product_id': r.id,
                'product_name': r.name,
                'total_sold': r.total_sold,
                'total_revenue': round(r.total_revenue, 2)
            }
            for r in results
        ]
    
    @staticmethod
    def get_revenue_by_date(days=7):
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        sales_by_date = db.session.query(
            func.date(Sale.created_at).label('date'),
            func.sum(Sale.total_amount).label('revenue')
        ).filter(
            Sale.created_at >= start_date,
            Sale.created_at <= end_date
        ).group_by(func.date(Sale.created_at)).all()
        
        return [
            {
                'date': str(r.date),
                'revenue': round(r.revenue, 2)
            }
            for r in sales_by_date
        ]