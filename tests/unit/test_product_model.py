from app.models.product import Product

def test_product_creation():
    p = Product(name="Phone", price=100)
    assert p.name == "Phone"
    assert p.price == 100
