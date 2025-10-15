from flask import Blueprint, request, jsonify
from app.services.rent_service import RentService
from app.schemas.rent_schema import RentCreate, RentReturn
from datetime import datetime

rents_bp = Blueprint('rents', __name__)

@rents_bp.route('/', methods=['GET'])
def get_rents():
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Convert date strings to datetime 
    if start_date:
        start_date = datetime.fromisoformat(start_date)
    if end_date:
        end_date = datetime.fromisoformat(end_date)
    
    rents = RentService.get_all_rents(
        status=status,
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify({
        'success': True,
        'data': [rent.to_dict() for rent in rents],
        'count': len(rents)
    }), 200

@rents_bp.route('/<int:rent_id>', methods=['GET'])
def get_rent(rent_id):
    rent = RentService.get_rent_by_id(rent_id)
    
    if not rent:
        return jsonify({
            'success': False,
            'message': 'Rental not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': rent.to_dict()
    }), 200

@rents_bp.route('/', methods=['POST'])
def create_rent():
    try:
        data = request.get_json()
        
        # Validate using Pydantic schema
        rent_schema = RentCreate(**data)
        
        # Get user_id from session/token (implement authentication later)
        user_id = request.headers.get('X-User-Id', 1)  # Default to 1 for now
        
        rent, error = RentService.create_rent(rent_schema.dict(), user_id=user_id)
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Rental created successfully',
            'data': rent.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@rents_bp.route('/<int:rent_id>/return', methods=['POST'])
def return_rent(rent_id):
    try:
        data = request.get_json()
        
        # Validate using Pydantic schema
        return_schema = RentReturn(**data)
        
        rent, error = RentService.return_rent(rent_id, return_schema.dict())
        
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Rental returned successfully',
            'data': rent.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@rents_bp.route('/active', methods=['GET'])
def get_active_rents():
    rents = RentService.get_all_rents(status='active')
    
    return jsonify({
        'success': True,
        'data': [rent.to_dict() for rent in rents],
        'count': len(rents)
    }), 200

@rents_bp.route('/overdue', methods=['GET'])
def get_overdue_rents():
    rents = RentService.get_overdue_rents()
    
    return jsonify({
        'success': True,
        'data': [rent.to_dict() for rent in rents],
        'count': len(rents)
    }), 200

@rents_bp.route('/customer/<phone>', methods=['GET'])
def get_customer_rents(phone):
    from app.models import Rent
    
    rents = Rent.query.filter_by(customer_phone=phone).order_by(Rent.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'data': [rent.to_dict() for rent in rents],
        'count': len(rents)
    }), 200