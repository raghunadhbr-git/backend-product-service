from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, cors, setup_logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_logging(app)
    app.logger.info("Product service starting...")

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .api.product_routes import product_bp, angular_product_bp

    app.register_blueprint(product_bp, url_prefix="/api/v1/products")
    app.register_blueprint(angular_product_bp, url_prefix="/api/angularProduct")

    app.logger.info("Product service started successfully.")
    return app
