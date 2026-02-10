"""
V1 Blueprint Factory
Registers all v1 routes with /v1 prefix
"""
from app.v1.routes import main_bp, api_bp


def create_v1_blueprint():
    """
    Create and configure v1 blueprint

    Returns:
        dict: Dictionary with v1 blueprints (main and api)
    """
    return {
        'main': main_bp,
        'api': api_bp
    }
