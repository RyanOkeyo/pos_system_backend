from flask import Blueprint, request, jsonify
from app.services.sales_service import SalesService
from app.schemas.sale_schema import SaleCreate
from datetime import datetime

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/', methods=['GET'])
def get_sales():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payment_method = request.args.get('payment_method')
    
    # Convert date strings to datetime 
    if start_date:
        start_date = datetime.fromisoformat(start_date)
    if end_date:
        end_date = datetime.fromisoformat(end_date)
    
    sales = SalesService.get_all_sales(
        start_date=start_date,
        end_date=end_date,
        payment_method=payment_method
    )
    
    return jsonify({
        'success': True,
        'data': [sale.to_dict() for sale in sales],
        'count': len(sales)
    }), 200

@sales_bp.route('/<int:sale_id>', methods=['GET'])
def get_sale(sale_id):
    sale = SalesService.get_sale_by_id(sale_id)
    
    if not sale:
        return jsonify({
            'success': False,
            'message': 'Sale not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': sale.to_dict()
    }), 200

@sales_bp.route('/', methods=['POST'])
def create_sale():
    try:
        data = request.get_json()
        
        # Validate using Pydantic schema
        sale_schema = SaleCreate(**data)
        
        # Get user_id from session/token (implement authentication later)
        user_id = request.headers.get('X-User-Id', 1)  # Default to 1 for now
        
        sale, error = SalesService.create_sale(sale_schema.dict(), user_id=user_id)
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Sale created successfully',
            'data': sale.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@sales_bp.route('/summary', methods=['GET'])
def get_sales_summary():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Convert date strings to datetime
    if start_date:
        start_date = datetime.fromisoformat(start_date)
    if end_date:
        end_date = datetime.fromisoformat(end_date)
    
    summary = SalesService.get_sales_summary(
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify({
        'success': True,
        'data': summary
    }), 200

@sales_bp.route('/recent', methods=['GET'])
def get_recent_sales():
    limit = request.args.get('limit', 10, type=int)
    
    sales = SalesService.get_all_sales()[:limit]
    
    return jsonify({
        'success': True,
        'data': [sale.to_dict() for sale in sales],
        'count': len(sales)
    }), 200