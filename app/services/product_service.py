from app.models import db, Product
from sqlalchemy.exc import IntegrityError

class ProductService:
    
    @staticmethod
    def get_all_products(category=None, search=None, include_inactive=False):

        query = Product.query

        if not include_inactive:
            query = query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(
                (Product.name.ilike(f'%{search}%')) |
                (Product.description.ilike(f'%{search}%')) |
                (Product.barcode == search) |
                (Product.sku == search)
            )
        
        return query.all()
    
    @staticmethod
    def get_product_by_id(product_id):

        return Product.query.get(product_id)
    
    @staticmethod
    def create_product(product_data):
        # Check for existing product with the same name and size
        existing_product = Product.query.filter_by(
            name=product_data.get('name'),
            size=product_data.get('size')
        ).first()

        if existing_product:
            return None, "Product with this name and size already exists"
            
        try:
            # Explicitly map fields to the model
            new_product = Product(
                name=product_data.get('name'),
                description=product_data.get('description'),
                category=product_data.get('category'),
                size=product_data.get('size'),
                sale_price=product_data.get('sale_price'),
                buying_price=product_data.get('buying_price'),
                rent_price_per_day=product_data.get('rent_price_per_day'),
                quantity_in_stock=product_data.get('quantity_in_stock', 0),
                reorder_level=product_data.get('reorder_level', 0),
                barcode=product_data.get('barcode'),
                sku=product_data.get('sku')
            )
            db.session.add(new_product)
            db.session.commit()
            return new_product, None
        except IntegrityError as e:
            db.session.rollback()
            return None, "Product with this barcode or SKU already exists"
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def update_product(product_id, product_data):
        product = Product.query.get(product_id)
        
        if not product:
            return None, "Product not found"
        
        try:
            for key, value in product_data.items():
                if value is not None:
                    setattr(product, key, value)
            
            db.session.commit()
            return product, None
        except IntegrityError:
            db.session.rollback()
            return None, "Product with this barcode or SKU already exists"
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        
        if not product:
            return False, "Product not found"
        
        try:
            product.is_active = False
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def update_stock(product_id, quantity_change):
        product = Product.query.get(product_id)
        
        if not product:
            return None, "Product not found"
        
        new_quantity = product.quantity_in_stock + quantity_change
        
        if new_quantity < 0:
            return None, "Insufficient stock"
        
        product.quantity_in_stock = new_quantity
        db.session.commit()
        
        return product, None

    @staticmethod
    def get_low_stock_products(threshold=10):
        return Product.query.filter(Product.quantity_in_stock < threshold).all()