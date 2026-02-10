"""
V2 Revise Route
Practice writing sentences with AI feedback
"""
from flask import render_template, request, jsonify
from flask_login import login_required


def register_revise_routes(bp):
    """Register revise routes"""

    @bp.route('/revise')
    @login_required
    def revise():
        """Revise page - Practice with feedback"""
        # TODO Phase 5: Load a random learned word to practice

        # Placeholder data
        practice_word = {
            'id': 1,
            'spanish': 'cocinar',
            'english': 'to cook',
            'word_type': 'verb',
            'theme': 'cooking'
        }

        return render_template('v2/revise.html', word=practice_word)

    @bp.route('/revise/submit', methods=['POST'])
    @login_required
    def revise_submit():
        """Handle practice sentence submission"""
        # TODO Phase 4: Send to LLM for feedback

        user_sentence = request.json.get('sentence', '')

        # Placeholder response
        return jsonify({
            'feedback': 'AI feedback will be implemented in Phase 4',
            'is_correct': True,
            'suggestions': []
        })
