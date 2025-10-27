from app import create_app
from app.models import db, Product, Sale, SaleItem
from datetime import datetime, timedelta

def add_dummy_products():
    products_data = [
        {'name': 'Laptop HP Pavilion', 'description': 'High-performance laptop with 16GB RAM and 512GB SSD', 'category': 'Electronics', 'sale_price': 75000, 'rent_price_per_day': 2500, 'quantity_in_stock': 10, 'quantity_rented': 0, 'barcode': 'LAP001', 'sku': 'HP-PAV-001'},
        {'name': 'Wireless Mouse Logitech', 'description': 'Ergonomic wireless mouse with USB receiver', 'category': 'Accessories', 'sale_price': 1500, 'rent_price_per_day': 50, 'quantity_in_stock': 25, 'quantity_rented': 0, 'barcode': 'MOU001', 'sku': 'LOG-MOU-001'},
        {'name': 'Office Chair Executive', 'description': 'Comfortable executive office chair with lumbar support', 'category': 'Furniture', 'sale_price': 12000, 'rent_price_per_day': 400, 'quantity_in_stock': 15, 'quantity_rented': 2, 'barcode': 'CHR001', 'sku': 'OFF-CHR-001'},
        {'name': 'USB-C Cable 2m', 'description': 'Fast charging USB-C cable, 2 meters long', 'category': 'Accessories', 'sale_price': 800, 'rent_price_per_day': 30, 'quantity_in_stock': 50, 'quantity_rented': 0, 'barcode': 'CAB001', 'sku': 'USB-CAB-001'},
        {'name': 'Projector Epson', 'description': 'Full HD projector with 3000 lumens brightness', 'category': 'Electronics', 'sale_price': 45000, 'rent_price_per_day': 1500, 'quantity_in_stock': 5, 'quantity_rented': 1, 'barcode': 'PRJ001', 'sku': 'EPS-PRJ-001'}
    ]
    
    print('Adding dummy products...')
    added = []
    for p in products_data:
        existing = Product.query.filter_by(sku=p['sku']).first()
        if existing:
            added.append(existing)
        else:
            product = Product(**p)
            db.session.add(product)
            added.append(product)
            print(f"Added: {p['name']}")
    db.session.commit()
    return added

app = create_app()
with app.app_context():
    print('Adding dummy data...')
    products = add_dummy_products()
    print('Done!')
