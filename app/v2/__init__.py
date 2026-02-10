"""
V2 Blueprint Factory
Registers all v2 routes with /v2 prefix
"""
import os
from flask import Blueprint

def create_v2_blueprint():
    """
    Create and configure v2 blueprint

    Returns:
        Blueprint: Configured v2 blueprint (placeholder for Phase 2)
    """
    # Get the absolute path to v2 templates directory
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    v2_bp = Blueprint('v2', __name__, template_folder=template_dir)

    # Import routes
    from app.v2.routes import register_routes
    register_routes(v2_bp)

    return v2_bp
