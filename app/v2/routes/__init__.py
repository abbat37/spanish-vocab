"""
V2 Route Registration
Registers all v2 routes on the blueprint
"""


def register_routes(bp):
    """Register all v2 routes"""
    from .dashboard import register_dashboard_routes
    from .create import register_create_routes
    from .study import register_study_routes
    from .revise import register_revise_routes
    from .api import api_bp

    # Register all route modules
    register_dashboard_routes(bp)
    register_create_routes(bp)
    register_study_routes(bp)
    register_revise_routes(bp)

    # Register API routes with /api prefix
    bp.register_blueprint(api_bp, url_prefix='/api')
