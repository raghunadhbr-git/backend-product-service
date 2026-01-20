from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.product import ProductVariant

product_bp = Blueprint("products", __name__)


@product_bp.post("/decrease-stock")
@jwt_required()
def decrease_stock():
    data = request.get_json() or {}
    items = data.get("items", [])

    if not items:
        return jsonify({"error": "No items provided"}), 400

    try:
        # 🔒 Lock rows & validate first
        variants = {}

        for item in items:
            variant_id = item["variant_id"]
            qty = int(item["quantity"])

            variant = (
                ProductVariant.query
                .filter_by(id=variant_id)
                .with_for_update()
                .first()
            )

            if not variant:
                return jsonify({
                    "error": f"Variant {variant_id} not found"
                }), 404

            if variant.stock < qty:
                return jsonify({
                    "error": f"Insufficient stock for variant {variant_id}"
                }), 400

            variants[variant] = qty

        # 🔻 Deduct stock
        for variant, qty in variants.items():
            variant.stock -= qty

        db.session.commit()
        return jsonify({"message": "Stock updated successfully"}), 200

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Stock update failed"}), 500
