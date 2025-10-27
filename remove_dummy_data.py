from app import create_app
from app.models import db, Product

DUMMY_SKUS = {
    'HP-PAV-001',
    'LOG-MOU-001',
    'OFF-CHR-001',
    'USB-CAB-001',
    'EPS-PRJ-001'
}


def remove_dummy_products():
    removed_products = []
    removed_sales = []

    products = Product.query.filter(Product.sku.in_(DUMMY_SKUS)).all()

    for product in products:
        # Capture sales tied to this product
        for sale_item in list(product.sale_items):
            sale = sale_item.sale
            db.session.delete(sale_item)
            if sale and len(sale.items) <= 1:
                removed_sales.append(sale.sale_number)
                db.session.delete(sale)

        removed_products.append(product.sku)
        db.session.delete(product)

    db.session.commit()
    return removed_products, removed_sales


def main():
    app = create_app()
    with app.app_context():
        products, sales = remove_dummy_products()
        if products:
            print(f"Removed products: {', '.join(products)}")
        else:
            print('No dummy products found.')

        if sales:
            print(f"Removed dependent sales: {', '.join(sales)}")


if __name__ == '__main__':
    main()
