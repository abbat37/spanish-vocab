"""
Application Factory
Creates and configures the Flask application with version support
"""
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, redirect, url_for

from app.config import config
from app.shared import db, login_manager, limiter, migrate, User


def create_app(config_name=None):
    """
    Application factory pattern with version support.

    Args:
        config_name: Configuration to use (development, production, testing)

    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login"""
        return User.query.get(int(user_id))

    # Initialize rate limiting
    limiter.init_app(app)
    limiter._storage_uri = app.config.get('RATELIMIT_STORAGE_URL')

    # Initialize Sentry for error tracking
    if app.config.get('SENTRY_DSN'):
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[FlaskIntegration()],
            environment=app.config.get('SENTRY_ENVIRONMENT', 'development'),
            traces_sample_rate=0.1
        )

    # ROOT URL: Redirect to /v1/ (default version)
    @app.route('/')
    def root_redirect():
        """Redirect root URL to v1"""
        return redirect(url_for('v1_main.index'))

    # Register SHARED routes (no prefix)
    from app.routes import auth_bp
    app.register_blueprint(auth_bp)

    # Register V1 blueprints with /v1 prefix
    from app.v1 import create_v1_blueprint
    v1_blueprints = create_v1_blueprint()
    app.register_blueprint(v1_blueprints['main'], url_prefix='/v1')
    app.register_blueprint(v1_blueprints['api'], url_prefix='/v1/api')

    # Apply rate limiting to v1 API
    limiter.limit("10 per minute")(v1_blueprints['api'])

    # Register V2 blueprint with /v2 prefix (placeholder)
    from app.v2 import create_v2_blueprint
    v2_bp = create_v2_blueprint()
    app.register_blueprint(v2_bp, url_prefix='/v2')

    # Create database tables
    with app.app_context():
        db.create_all()

    # Add headers to prevent caching during development
    @app.after_request
    def add_header(response):
        """Add cache control headers"""
        if app.config['DEBUG']:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
        return response

    return app
