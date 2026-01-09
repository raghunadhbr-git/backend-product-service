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


# ============================================================
# GET SINGLE PRODUCT
# ============================================================
@angular_product_bp.get("/get/<int:id>")
def angular_get_single_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "_id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "image": product.image,
        "category": product.category,
        "color": product.color,
        "stock": product.stock
    }), 200


# ============================================================
# UPDATE PRODUCT
# ============================================================
@angular_product_bp.patch("/update")
@jwt_required()
def angular_update_product():
    data = request.get_json() or {}

    product = Product.query.get(data.get("productId"))
    if not product:
        return jsonify({"error": "Product not found"}), 404

    updated = data.get("updatedData", {})

    product.name = updated.get("name", product.name)
    product.price = float(updated.get("price", product.price))
    product.description = updated.get("description", product.description)
    product.image = updated.get("image", product.image)
    product.category = updated.get("category", product.category)
    product.color = updated.get("color", product.color)
    product.stock = int(updated.get("stock", product.stock))

    db.session.commit()

    return jsonify({"message": "Product updated"}), 200


# ============================================================
# DELETE PRODUCT
# ============================================================
@angular_product_bp.delete("/delete")
@jwt_required()
def angular_delete_product():
    data = request.get_json() or {}

    product = Product.query.get(data.get("productId"))
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted"}), 200
