"""
V2 Create Route
Allows users to add/edit words in their vocabulary database
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required


def register_create_routes(bp):
    """Register create routes"""

    @bp.route('/create', methods=['GET', 'POST'])
    @login_required
    def create():
        """Create/edit words page"""

        if request.method == 'POST':
            # TODO Phase 5: Handle word creation
            flash('Word creation will be implemented in Phase 5', 'info')
            return redirect(url_for('v2.create'))

        # TODO Phase 5: Load user's existing words
        words = []  # Placeholder

        return render_template('v2/create.html', words=words)
