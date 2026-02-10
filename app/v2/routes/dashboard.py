"""
V2 Dashboard Route
Shows overview of learning progress and quick links
"""
from flask import render_template
from flask_login import login_required


def register_dashboard_routes(bp):
    """Register dashboard routes"""

    @bp.route('/')
    @login_required
    def dashboard():
        """V2 Dashboard - Overview page"""
        # TODO Phase 3: Query user's word count, learned count, etc.
        stats = {
            'total_words': 0,  # Placeholder
            'learned_words': 0,
            'practice_count': 0
        }

        return render_template('v2/dashboard.html', stats=stats)
