"""
V2 Create Route
Allows users to add/edit words in their vocabulary database
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.v2.services.word_service import WordService


def register_create_routes(bp):
    """Register create routes"""

    @bp.route('/create', methods=['GET'])
    @login_required
    def create():
        """Create/edit words page - bulk AI entry only"""

        # Load user's existing words
        words = WordService.get_user_words(current_user.id)

        return render_template('v2/create.html', words=words)
