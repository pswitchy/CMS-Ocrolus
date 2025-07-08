from flask import Flask
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from app.extensions import db, migrate, jwt
from app.api import api_bp

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    return app