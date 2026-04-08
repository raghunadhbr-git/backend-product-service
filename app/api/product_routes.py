from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.product import Product, ProductVariant

product_bp = Blueprint("products", __name__)
angular_product_bp = Blueprint("angular_products", __name__)

# ============================================================
# ADD PRODUCT (SELLER)
# ============================================================
@product_bp.post("/add")
@jwt_required()
def add_product():
    try:
        data = request.get_json()
        print("🔥 ADD PRODUCT PAYLOAD:", data)

        # ✅ VALIDATION
        if not data or "name" not in data or "price" not in data:
            return jsonify({"error": "Missing required fields"}), 400

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

    except Exception as e:
        print("❌ ERROR ADD PRODUCT:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500


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
# ANGULAR ROUTES
# ============================================================
@angular_product_bp.get("/get")
def angular_get_all():
    return list_products()