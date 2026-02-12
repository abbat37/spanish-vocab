"""
V2 Study Route
Flashcard-style learning with AI-generated examples
"""
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.v2.models import V2Word, V2GeneratedExample
from app.v2.services.llm_service import get_llm_service
from app.shared.extensions import db


def register_study_routes(bp):
    """Register study routes"""

    @bp.route('/study')
    @login_required
    def study():
        """Study page - Flashcard learning"""
        # Get filter parameters
        theme = request.args.get('theme', '')
        word_type = request.args.get('word_type', '')

        # Build query for unlearned words
        query = V2Word.query.filter_by(
            user_id=current_user.id,
            is_learned=False
        )

        # Apply filters
        if theme:
            query = query.filter(V2Word.themes.contains(theme))
        if word_type:
            query = query.filter_by(word_type=word_type)

        # Get random word
        word = query.order_by(db.func.random()).first()

        if not word:
            return render_template('v2/study.html', word=None, filters={'theme': theme, 'word_type': word_type})

        # Check if examples exist
        examples = V2GeneratedExample.query.filter_by(word_id=word.id).all()

        return render_template(
            'v2/study.html',
            word=word,
            examples=[ex.to_dict() for ex in examples],
            has_examples=len(examples) > 0,
            filters={'theme': theme, 'word_type': word_type}
        )

    @bp.route('/api/study/generate-examples/<int:word_id>', methods=['POST'])
    @login_required
    def generate_examples(word_id):
        """Generate AI examples for a word."""
        try:
            # Find word (ensure belongs to user)
            word = V2Word.query.filter_by(
                id=word_id,
                user_id=current_user.id
            ).first()

            if not word:
                return jsonify({
                    'success': False,
                    'error': 'Word not found'
                }), 404

            # Generate examples with LLM
            llm_service = get_llm_service()
            examples = llm_service.generate_examples(
                spanish=word.spanish,
                english=word.english,
                word_type=word.word_type,
                count=3
            )

            if not examples:
                return jsonify({
                    'success': False,
                    'error': 'Failed to generate examples'
                }), 500

            # Save to database
            for ex in examples:
                example = V2GeneratedExample(
                    word_id=word.id,
                    spanish_sentence=ex['spanish'],
                    english_translation=ex['english']
                )
                db.session.add(example)

            db.session.commit()

            return jsonify({
                'success': True,
                'examples': examples
            })

        except Exception as e:
            db.session.rollback()
            print(f"Error generating examples: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500

    @bp.route('/api/study/mark-learned/<int:word_id>', methods=['POST'])
    @login_required
    def mark_learned(word_id):
        """Mark word as learned."""
        try:
            word = V2Word.query.filter_by(
                id=word_id,
                user_id=current_user.id
            ).first()

            if not word:
                return jsonify({
                    'success': False,
                    'error': 'Word not found'
                }), 404

            word.is_learned = True
            db.session.commit()

            return jsonify({'success': True})

        except Exception as e:
            db.session.rollback()
            print(f"Error marking word learned: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500
