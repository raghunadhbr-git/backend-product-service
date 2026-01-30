from app.models.product import Product
from app.extensions import db


def create_product(data):
    product = Product(
        name=data["name"],
        price=data["price"],
        description=data.get("description"),
        category=data.get("category")
    )
    db.session.add(product)
    db.session.commit()
    return product


def get_product(product_id):
    return Product.query.get(product_id)


def get_all_products():
    return Product.query.all()
