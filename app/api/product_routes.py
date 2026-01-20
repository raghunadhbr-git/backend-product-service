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
# DECREASE PRODUCT STOCK (ORDER PLACED)
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
            return jsonify({"error": "Product not found"}), 404

        if product.stock < qty:
            return jsonify({"error": "Insufficient stock"}), 400

        product.stock -= qty

    db.session.commit()
    return jsonify({"message": "Stock decreased"}), 200


# ============================================================
# 🔥 RESTORE PRODUCT STOCK (CANCEL / RETURN)
# ============================================================
@product_bp.post("/restore-stock")
@jwt_required()
def restore_stock():
    data = request.get_json() or {}
    items = data.get("items", [])

    if not items:
        return jsonify({"error": "No items provided"}), 400

    for item in items:
        product = Product.query.get(item["product_id"])
        qty = int(item["quantity"])

        if not product:
            return jsonify({"error": "Product not found"}), 404

        product.stock += qty

    db.session.commit()
    return jsonify({"message": "Stock restored"}), 200
