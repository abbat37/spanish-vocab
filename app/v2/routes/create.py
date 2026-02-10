"""
V2 Create Route
Allows users to add/edit words in their vocabulary database
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.v2.services.word_service import WordService


def register_create_routes(bp):
    """Register create routes"""

    @bp.route('/create', methods=['GET', 'POST'])
    @login_required
    def create():
        """Create/edit words page"""

        if request.method == 'POST':
            # TODO Phase 5: Handle single word creation
            return redirect(url_for('v2.create'))

        # Load user's existing words
        words = WordService.get_user_words(current_user.id)

        return render_template('v2/create.html', words=words)
