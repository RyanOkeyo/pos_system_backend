from flask import Blueprint, request, jsonify
from app.services.dashboard_service import DashboardService
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    # Get date range from query params
    days = request.args.get('days', 30, type=int)
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Allow custom date range
    custom_start = request.args.get('start_date')
    custom_end = request.args.get('end_date')
    
    if custom_start:
        start_date = datetime.fromisoformat(custom_start)
    if custom_end:
        end_date = datetime.fromisoformat(custom_end)
    
    stats = DashboardService.get_dashboard_stats(
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify({
        'success': True,
        'data': stats,
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
    }), 200

@dashboard_bp.route('/top-products', methods=['GET'])
def get_top_products():
    limit = request.args.get('limit', 10, type=int)
    
    products = DashboardService.get_top_selling_products(limit=limit)
    
    return jsonify({
        'success': True,
        'data': products,
        'count': len(products)
    }), 200

@dashboard_bp.route('/revenue-by-date', methods=['GET'])
def get_revenue_by_date():
    days = request.args.get('days', 7, type=int)
    
    revenue_data = DashboardService.get_revenue_by_date(days=days)
    
    return jsonify({
        'success': True,
        'data': revenue_data,
        'count': len(revenue_data)
    }), 200

@dashboard_bp.route('/summary', methods=['GET'])
def get_summary():
    days = request.args.get('days', 30, type=int)
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    stats = DashboardService.get_dashboard_stats(start_date, end_date)
    top_products = DashboardService.get_top_selling_products(limit=5)
    revenue_trend = DashboardService.get_revenue_by_date(days=7)
    
    return jsonify({
        'success': True,
        'data': {
            'stats': stats,
            'top_products': top_products,
            'revenue_trend': revenue_trend
        },
        'period': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
    }), 200

@dashboard_bp.route('/alerts', methods=['GET'])
def get_alerts():
    from app.models import Product
    from app.services.rent_service import RentService
    
    alerts = []
    
    # Low stock alerts
    low_stock_products = Product.query.filter(
        Product.quantity_in_stock < 10
    ).all()
    
    for product in low_stock_products:
        alerts.append({
            'type': 'low_stock',
            'severity': 'warning',
            'message': f'Low stock: {product.name} ({product.quantity_in_stock} units)',
            'product_id': product.id
        })
    
    # Overdue rentals
    overdue_rents = RentService.get_overdue_rents()
    
    for rent in overdue_rents:
        days_overdue = (datetime.utcnow() - rent.end_date).days
        alerts.append({
            'type': 'overdue_rental',
            'severity': 'error',
            'message': f'Overdue rental: {rent.rent_number} by {rent.customer_name} ({days_overdue} days)',
            'rent_id': rent.id
        })
    
    return jsonify({
        'success': True,
        'data': alerts,
        'count': len(alerts)
    }), 200