from app.models import db, Product
from sqlalchemy.exc import IntegrityError

class ProductService:
    
    @staticmethod
    def get_all_products(category=None, search=None):

        query = Product.query
        
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
        try:
            product = Product(**product_data)
            db.session.add(product)
            db.session.commit()
            return product, None
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
            db.session.delete(product)
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