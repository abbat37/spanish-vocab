"""
V1 API Routes
RESTful API endpoints for AJAX operations
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
from marshmallow import ValidationError
from app.shared.extensions import db
from app.v1.models import WordPractice
from app.v1.services import SessionService, StatsService
from app.v1.utils.validators import MarkLearnedSchema

api_bp = Blueprint('v1_api', __name__)


@api_bp.route('/mark-learned', methods=['POST'])
@login_required
def mark_learned():
    """
    API endpoint to mark a word as learned.

    Request JSON:
        {
            "word_id": int
        }

    Returns:
        JSON with success status, marked_learned boolean, and updated stats
    """
    # Validate incoming request data
    schema = MarkLearnedSchema()
    try:
        data = schema.load(request.json or {})
    except ValidationError as err:
        return jsonify({
            'error': 'Validation failed',
            'details': err.messages
        }), 400

    session_id = SessionService.get_or_create_session_id()
    word_id = data['word_id']

    # Find the practice record in the current session
    practice = WordPractice.query.filter_by(
        session_id=session_id,
        word_id=word_id
    ).first()

    if practice:
        # Toggle learned status
        practice.marked_learned = not practice.marked_learned
        db.session.commit()

        # Get updated stats across all user sessions
        identifier_type, identifier_value = SessionService.get_user_identifier()
        return jsonify({
            'success': True,
            'marked_learned': practice.marked_learned,
            'stats': StatsService.get_user_stats(identifier_type, identifier_value)
        })
    else:
        return jsonify({'error': 'Practice record not found'}), 404
