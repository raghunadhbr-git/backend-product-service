from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.product import Product

product_bp = Blueprint("products", __name__)
angular_product_bp = Blueprint("angular_products", __name__)

# ============================================================
# PRODUCT SERVICE HEALTH
# ============================================================
@product_bp.get("/")
def product_service_health():
    return jsonify({"status": "product-service UP"}), 200


# ============================================================
# INTERNAL: DECREASE PRODUCT STOCK (ORDERS FLOW)
# POST /api/v1/products/decrease-stock
# ============================================================
@product_bp.post("/decrease-stock")
@jwt_required()
def decrease_stock():
    data = request.get_json() or {}
    items = data.get("items", [])

    if not items:
        return jsonify({"error": "No items provided"}), 400

    for item in items:
        product = Product.query.get(item["product_id"])
        qty = int(item["quantity"])

        if not product:
            return jsonify({"error": f"Product {item['product_id']} not found"}), 404

        if product.stock < qty:
            return jsonify({
                "error": f"Insufficient stock for product {product.id}"
            }), 400

        product.stock -= qty

    db.session.commit()

    return jsonify({"message": "Stock updated successfully"}), 200


# ============================================================
# ANGULAR HEALTH CHECK
# ============================================================
@angular_product_bp.get("/health")
def angular_health():
    return jsonify({"status": "angular-product-service UP"}), 200


# ============================================================
# ADD PRODUCT
# ============================================================
@angular_product_bp.post("/add")
@jwt_required()
def angular_add_product():
    data = request.get_json() or {}

    product = Product(
        name=data.get("name"),
        price=float(data.get("price")),
        description=data.get("description", ""),
        image=data.get("image", ""),
        category=data.get("category", ""),
        color=data.get("color", ""),
        stock=int(data.get("stock", 0))
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product added", "_id": product.id}), 201


# ============================================================
# GET ALL PRODUCTS
# ============================================================
@angular_product_bp.get("/get")
def angular_get_products():
    products = Product.query.all()

    return jsonify([
        {
            "_id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "image": p.image,
            "category": p.category,
            "color": p.color,
            "stock": p.stock
        }
        for p in products
    ]), 200
