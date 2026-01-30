from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.product import Product, ProductVariant

product_bp = Blueprint("products", __name__)
angular_product_bp = Blueprint("angular_products", __name__)

# ============================================================
# HEALTH
# ============================================================
@product_bp.get("/")
def health():
    return jsonify({"status": "product-service UP"}), 200


# ============================================================
# ADD PRODUCT (SELLER)
# ============================================================
@product_bp.post("/add")
@jwt_required()
def add_product():
    data = request.get_json()

    product = Product(
        name=data["name"],
        price=data["price"],
        description=data.get("description"),
        category=data.get("category"),
        image=data.get("image")
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "category": product.category
    }), 201


# ============================================================
# GET ALL PRODUCTS
# ============================================================
@product_bp.get("/list")
def list_products():
    products = Product.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category": p.category,
            "image": p.image,
            "variants": [
                {
                    "variant_id": v.id,
                    "color": v.color,
                    "stock": v.stock
                } for v in p.variants
            ]
        } for p in products
    ]), 200


# ============================================================
# GET SINGLE PRODUCT
# ============================================================
@product_bp.get("/<int:product_id>")
def get_product(product_id):
    p = Product.query.get_or_404(product_id)

    return jsonify({
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "category": p.category,
        "image": p.image,
        "variants": [
            {
                "variant_id": v.id,
                "color": v.color,
                "stock": v.stock
            } for v in p.variants
        ]
    }), 200


# ============================================================
# ADD VARIANT (SELLER)
# ============================================================
@product_bp.post("/<int:product_id>/variants")
@jwt_required()
def add_variant(product_id):
    data = request.get_json()
    Product.query.get_or_404(product_id)

    variant = ProductVariant(
        product_id=product_id,
        color=data["color"],
        stock=data["stock"]
    )

    db.session.add(variant)
    db.session.commit()

    return jsonify({
        "variant_id": variant.id,
        "color": variant.color,
        "stock": variant.stock
    }), 201


# ============================================================
# 🔻 DECREASE STOCK (ORDER PLACED)
# ============================================================
@product_bp.post("/decrease-stock")
@jwt_required()
def decrease_stock():
    data = request.get_json() or {}
    items = data.get("items", [])

    for item in items:
        variant = ProductVariant.query.filter_by(
            id=item["variant_id"],
            product_id=item["product_id"]
        ).first()

        if not variant:
            return jsonify({"error": "Variant not found"}), 404

        if variant.stock < item["quantity"]:
            return jsonify({
                "error": "Insufficient stock",
                "variant_id": variant.id,
                "available": variant.stock
            }), 400

        variant.stock -= item["quantity"]

    db.session.commit()
    return jsonify({"message": "Stock decreased"}), 200


# ============================================================
# 🔁 RESTORE STOCK (CANCEL / RETURN)
# ============================================================
@product_bp.post("/restore-stock")
@jwt_required()
def restore_stock():
    data = request.get_json() or {}
    items = data.get("items", [])

    for item in items:
        variant = ProductVariant.query.filter_by(
            id=item["variant_id"],
            product_id=item["product_id"]
        ).first()

        if not variant:
            return jsonify({"error": "Variant not found"}), 404

        variant.stock += item["quantity"]

    db.session.commit()
    return jsonify({"message": "Stock restored"}), 200


# ============================================================
# ANGULAR COMPAT ROUTES (READ ONLY)
# ============================================================
@angular_product_bp.get("/get")
def angular_get_all():
    return list_products()


@angular_product_bp.get("/get/<int:product_id>")
def angular_get_single(product_id):
    return get_product(product_id)
