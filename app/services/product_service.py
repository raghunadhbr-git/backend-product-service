from app.models.product import Product
from app.extensions import db


def create_product(data):
    try:
        if not data or "name" not in data or "price" not in data:
            raise ValueError("Missing required fields")

        product = Product(
            name=data["name"],
            price=data["price"],
            description=data.get("description"),
            category=data.get("category"),
            image=data.get("image")
        )

        db.session.add(product)
        db.session.commit()

        return product

    except Exception as e:
        print("❌ SERVICE ERROR:", str(e))
        raise


def get_product(product_id):
    return Product.query.get(product_id)


def get_all_products():
    return Product.query.all()