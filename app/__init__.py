from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, cors, setup_logging


def create_app(testing: bool = False):
    """
    Flask application factory.

    testing=True  -> used by pytest
    testing=False -> default (dev / prod)
    """
    app = Flask(__name__)

    # ------------------------------------
    # CONFIGURATION
    # ------------------------------------
    if testing:
        # Safe test configuration
        app.config.from_object(Config)
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            JWT_SECRET_KEY="test-secret-key"
        )
    else:
        app.config.from_object(Config)

    # ------------------------------------
    # LOGGING
    # ------------------------------------
    setup_logging(app)
    app.logger.info("Product service starting...")

    # ------------------------------------
    # EXTENSIONS
    # ------------------------------------
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # ------------------------------------
    # BLUEPRINTS
    # ------------------------------------
    from .api.product_routes import product_bp, angular_product_bp

    app.register_blueprint(product_bp, url_prefix="/api/v1/products")
    app.register_blueprint(angular_product_bp, url_prefix="/api/angularProduct")

    app.logger.info("Product service started successfully.")
    return app
