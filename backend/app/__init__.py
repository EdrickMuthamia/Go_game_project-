from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize app-specific configurations
    Config.init_app(app)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.game import bp as game_bp
    app.register_blueprint(game_bp, url_prefix='/api/game')

    # Import models to ensure they are registered with SQLAlchemy
    from app.auth.models import User
    from app.game.models import Game

    # JWT error handlers
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return {'message': f'Invalid token: {error_string}'}, 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'message': 'Token has expired'}, 422

    @jwt.unauthorized_loader
    def unauthorized_callback(error_string):
        return {'message': f'Authorization required: {error_string}'}, 422

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'message': 'Not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {'message': 'Internal server error'}, 500

    return app