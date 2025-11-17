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
            Product.is_active == True,
            Product.quantity_in_stock < 10
        ).count()
        
        # Total products
        total_products = Product.query.filter(Product.is_active == True).count()
        
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
    
    @staticmethod
    def get_cashflow_by_date(days=30):
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Sales revenue by date
        sales_by_date = db.session.query(
            func.date(Sale.created_at).label('date'),
            func.sum(Sale.total_amount).label('revenue')
        ).filter(
            Sale.created_at >= start_date,
            Sale.created_at <= end_date
        ).group_by('date').all()

        # Rents revenue by date
        rents_by_date = db.session.query(
            func.date(Rent.created_at).label('date'),
            func.sum(Rent.total_amount).label('revenue')
        ).filter(
            Rent.created_at >= start_date,
            Rent.created_at <= end_date
        ).group_by('date').all()

        # Combine and format the data
        cashflow_data = {}
        for row in sales_by_date:
            date_str = row.date
            if date_str not in cashflow_data:
                cashflow_data[date_str] = {'sales': 0, 'rents': 0}
            cashflow_data[date_str]['sales'] += row.revenue

        for row in rents_by_date:
            date_str = row.date.isoformat()
            if date_str not in cashflow_data:
                cashflow_data[date_str] = {'sales': 0, 'rents': 0}
            cashflow_data[date_str]['rents'] += row.revenue
            
        # Format for chart
        chart_data = []
        for date_str, revenues in sorted(cashflow_data.items()):
            chart_data.append({
                'date': date_str,
                'sales': round(revenues['sales'], 2),
                'rents': round(revenues['rents'], 2),
                'total': round(revenues['sales'] + revenues['rents'], 2)
            })
            
        return chart_data
    
    @staticmethod
    def get_sales_by_date(days=30):
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        sales_by_date = db.session.query(
            func.date(Sale.created_at).label('date'),
            func.sum(Sale.total_amount).label('amount')
        ).filter(
            Sale.created_at >= start_date,
            Sale.created_at <= end_date
        ).group_by('date').order_by('date').all()

        labels = [datetime.strptime(row.date, '%Y-%m-%d').strftime('%b %d') for row in sales_by_date]
        values = [round(row.amount, 2) for row in sales_by_date]

        return {'labels': labels, 'values': values}

    @staticmethod
    def get_sales_by_month():
        sales_by_month = db.session.query(
            func.strftime('%Y-%m', Sale.created_at).label('month'),
            func.sum(Sale.total_amount).label('amount')
        ).group_by('month').order_by('month').all()

        labels = [datetime.strptime(row.month, '%Y-%m').strftime('%B %Y') for row in sales_by_month]
        values = [round(row.amount, 2) for row in sales_by_month]

        return {'labels': labels, 'values': values}

    @staticmethod
    def get_low_stock_products(threshold=10):
        """
        Retrieves products with stock quantity below a certain threshold.
        """
        low_stock_products = Product.query.filter(
            Product.is_active == True,
            Product.quantity_in_stock < threshold
        ).all()
        
        return [product.to_dict() for product in low_stock_products]