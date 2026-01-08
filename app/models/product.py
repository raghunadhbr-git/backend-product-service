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
    color = db.Column(db.String(50))

    # 🔥 INVENTORY
    stock = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Product {self.id} {self.name}>"
