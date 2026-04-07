# =========================
# Flask App Factory (FINAL FIXED CORS)
# =========================

from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, migrate, jwt, setup_logging
from flask_cors import CORS


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_logging(app)

    # =========================
    # 🔥 FINAL CORS FIX
    # =========================
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "https://angular-ecommerce-site-ekkt5b8m0-raghunadh28-1386s-projects.vercel.app"
                ]
            }
        },
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.api.product_routes import product_bp, angular_product_bp

    app.register_blueprint(product_bp, url_prefix="/api/v1/products")
    app.register_blueprint(angular_product_bp, url_prefix="/api/angularProduct")

    @app.get("/")
    def health():
        return jsonify({"status": "Product-Service-UP"}), 200

    return app
