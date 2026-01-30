from datetime import datetime
from ..extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)

    image = db.Column(db.String(500))
    category = db.Column(db.String(100))

    # ⚠️ KEEP TEMP (used by old Angular forms)
    color = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Product {self.id} {self.name}>"


class ProductVariant(db.Model):
    __tablename__ = "product_variants"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    color = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    product = db.relationship("Product", backref="variants")

    def __repr__(self):
        return f"<Variant product={self.product_id} color={self.color} stock={self.stock}>"
