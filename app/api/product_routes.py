from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.product import Product, ProductVariant

product_bp = Blueprint("products", __name__)
angular_product_bp = Blueprint("angular_products", __name__)


# ============================================================
# PRODUCT SERVICE HEALTH
# ============================================================
@product_bp.get("/")
def product_service_health():
    return jsonify({"status": "product-service UP"}), 200


# ============================================================
# 🔻 DECREASE VARIANT STOCK (ORDER PLACED)
# ============================================================
@product_bp.post("/decrease-stock")
@jwt_required()
def decrease_stock():
    data = request.get_json() or {}
    items = data.get("items", [])

    if not items:
        return jsonify({"error": "No items provided"}), 400

    for item in items:
        variant = ProductVariant.query.filter_by(
            id=item["variant_id"],
            product_id=item["product_id"]
        ).first()

        if not variant:
            return jsonify({"error": "Variant not found"}), 404

        qty = int(item["quantity"])

        if variant.stock < qty:
            return jsonify({
                "error": "Insufficient stock",
                "variant_id": variant.id,
                "available": variant.stock
            }), 400

        variant.stock -= qty

    db.session.commit()
    return jsonify({"message": "Stock decreased"}), 200


# ============================================================
# 🔁 RESTORE VARIANT STOCK (CANCEL / RETURN)
# ============================================================
@product_bp.post("/restore-stock")
@jwt_required()
def restore_stock():
    data = request.get_json() or {}
    items = data.get("items", [])

    if not items:
        return jsonify({"error": "No items provided"}), 400

    for item in items:
        variant = ProductVariant.query.filter_by(
            id=item["variant_id"],
            product_id=item["product_id"]
        ).first()

        if not variant:
            return jsonify({"error": "Variant not found"}), 404

        qty = int(item["quantity"])
        variant.stock += qty

    db.session.commit()
    return jsonify({"message": "Stock restored"}), 200
