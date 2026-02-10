"""
V2 Study Route
Flashcard-style learning with AI-generated examples
"""
from flask import render_template, request, jsonify
from flask_login import login_required


def register_study_routes(bp):
    """Register study routes"""

    @bp.route('/study')
    @login_required
    def study():
        """Study page - Flashcard learning"""
        # TODO Phase 5: Load a random unlearned word with examples

        # Placeholder data
        current_word = {
            'id': 1,
            'spanish': 'cocinar',
            'english': 'to cook',
            'word_type': 'verb',
            'theme': 'cooking',
            'examples': [
                'Me gusta cocinar con mi familia.',
                'Ella sabe cocinar muy bien.',
                'Voy a cocinar pasta esta noche.'
            ]
        }

        return render_template('v2/study.html', word=current_word)
