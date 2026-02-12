"""
V2 Revise Route
Practice writing sentences with AI feedback
"""
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.v2.models import V2Word, V2PracticeAttempt
from app.v2.services.llm_service import get_llm_service
from app.shared.extensions import db


def register_revise_routes(bp):
    """Register revise routes"""

    @bp.route('/revise')
    @login_required
    def revise():
        """Revise page - Practice with feedback"""
        # Get filter parameters
        theme = request.args.get('theme', '')
        word_type = request.args.get('word_type', '')
        include_unlearned = request.args.get('include_unlearned', '') == 'on'

        # Build query - by default show learned words only
        query = V2Word.query.filter_by(user_id=current_user.id)

        # Filter by learned status
        if include_unlearned:
            # Show both learned and unlearned
            pass
        else:
            # Show only learned words (default)
            query = query.filter_by(is_learned=True)

        # Apply filters
        if theme:
            query = query.filter(V2Word.themes.contains(theme))
        if word_type:
            query = query.filter_by(word_type=word_type)

        # Get random word
        word = query.order_by(db.func.random()).first()

        return render_template(
            'v2/revise.html',
            word=word,
            filters={'theme': theme, 'word_type': word_type, 'include_unlearned': include_unlearned}
        )

    @bp.route('/api/revise/submit', methods=['POST'])
    @login_required
    def submit_practice():
        """Submit practice sentence for AI feedback."""
        try:
            data = request.get_json()
            word_id = data.get('word_id')
            user_sentence = data.get('sentence', '').strip()

            if not user_sentence:
                return jsonify({
                    'success': False,
                    'error': 'Please write a sentence'
                }), 400

            # Find word
            word = V2Word.query.filter_by(
                id=word_id,
                user_id=current_user.id
            ).first()

            if not word:
                return jsonify({
                    'success': False,
                    'error': 'Word not found'
                }), 404

            # Get AI feedback
            llm_service = get_llm_service()
            feedback = llm_service.analyze_sentence(
                user_sentence=user_sentence,
                target_word=word.spanish,
                word_english=word.english,
                word_type=word.word_type
            )

            if not feedback:
                return jsonify({
                    'success': False,
                    'error': 'Failed to generate feedback'
                }), 500

            # Save practice attempt
            attempt = V2PracticeAttempt(
                user_id=current_user.id,
                word_id=word.id,
                user_sentence=user_sentence,
                ai_feedback=feedback['feedback_text'],
                is_correct=feedback['is_correct']
            )
            db.session.add(attempt)
            db.session.commit()

            return jsonify({
                'success': True,
                'feedback': feedback
            })

        except Exception as e:
            db.session.rollback()
            print(f"Error submitting practice: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500
