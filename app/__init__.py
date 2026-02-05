from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, migrate, jwt, cors, setup_logging


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_logging(app)

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.api.product_routes import product_bp, angular_product_bp

    app.register_blueprint(product_bp, url_prefix="/api/v1/products")
    app.register_blueprint(angular_product_bp, url_prefix="/api/angularProduct")

    @app.get("/")
    def health():
        return jsonify({"status": "product-service UP"}), 200

    
    return app
