"""
V2 Dashboard Route
Shows overview of learning progress and quick links
"""
from flask import render_template
from flask_login import login_required, current_user
from app.v2.services.stats_service import StatsService


def register_dashboard_routes(bp):
    """Register dashboard routes"""

    @bp.route('/')
    @login_required
    def dashboard():
        """V2 Dashboard - Overview page"""
        stats = StatsService.get_user_stats(current_user.id)
        return render_template('v2/dashboard.html', stats=stats)
