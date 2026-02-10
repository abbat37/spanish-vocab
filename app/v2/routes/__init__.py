"""
V2 Routes (Placeholder)
Will be implemented in Phase 2
"""
from flask import render_template

def register_routes(bp):
    """Register v2 routes on the blueprint"""

    @bp.route('/')
    def index():
        """V2 home page (placeholder)"""
        return render_template('v2/index.html')
