from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.product_service import ProductService
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.utils.helpers import role_required

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'], strict_slashes=False)
@products_bp.route('/', methods=['GET'], strict_slashes=False)
def get_products():
    category = request.args.get('category')
    search = request.args.get('search')

    products = ProductService.get_all_products(category=category, search=search)

    return jsonify({
        'success': True,
        'data': [product.to_dict() for product in products],
        'count': len(products)
    }), 200

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductService.get_product_by_id(product_id)

    if not product:
        return jsonify({
            'success': False,
            'message': 'Product not found'
        }), 404

    return jsonify({
        'success': True,
        'data': product.to_dict()
    }), 200

@products_bp.route('', methods=['POST'], strict_slashes=False)
@products_bp.route('/', methods=['POST'], strict_slashes=False)
@jwt_required()
@role_required('admin')
def create_product():
    try:
        data = request.get_json()

        product_schema = ProductCreate(**data)
        product, error = ProductService.create_product(product_schema.dict())

        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400

        return jsonify({
            'success': True,
            'message': 'Product created successfully',
            'data': product.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_product(product_id):
    try:
        data = request.get_json()
        product_schema = ProductUpdate(**data)

        product, error = ProductService.update_product(
            product_id,
            product_schema.dict(exclude_unset=True)
        )

        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400

        return jsonify({
            'success': True,
            'message': 'Product updated successfully',
            'data': product.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_product(product_id):
    success, error = ProductService.delete_product(product_id)

    if not success:
        return jsonify({
            'success': False,
            'message': error
        }), 400

    return jsonify({
        'success': True,
        'message': 'Product deleted successfully'
    }), 200

@products_bp.route('/<int:product_id>/stock', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def update_stock(product_id):
    try:
        data = request.get_json()
        quantity_change = data.get('quantity_change', 0)

        product, error = ProductService.update_stock(product_id, quantity_change)

        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400

        return jsonify({
            'success': True,
            'message': 'Stock updated successfully',
            'data': product.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@products_bp.route('/low-stock', methods=['GET'])
def get_low_stock_products():
    threshold = request.args.get('threshold', 10, type=int)
    products = ProductService.get_low_stock_products(threshold=threshold)

    return jsonify({
        'success': True,
        'data': [product.to_dict() for product in products],
        'count': len(products)
    }), 200