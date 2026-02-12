"""
V2 API Routes
RESTful API endpoints for bulk word processing
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.shared.extensions import limiter, db
from app.v2.services.llm_service import get_llm_service
from app.v2.services.word_service import WordService
from app.v2.utils import parse_bulk_word_input, truncate_if_needed, validate_word_before_llm
from app.v2.models import V2Word

api_bp = Blueprint('v2_api', __name__)


@api_bp.route('/process-words', methods=['POST'])
@login_required
@limiter.limit("10 per minute")
def process_words():
    """
    Bulk process Spanish words with LLM.

    Request JSON:
        {
            "raw_text": "Frío\\nSol\\nViento"
        }

    Response JSON:
        {
            "success": true,
            "words": [
                {
                    "id": 1,
                    "spanish": "Frío",
                    "english": "Cold",
                    "word_type": "adjective",
                    "themes": ["weather"],
                    "is_learned": false
                }
            ],
            "stats": {
                "processed": 3,
                "created": 3,
                "duplicates": 0,
                "failed": 0,
                "rejected": 0
            },
            "errors": []
        }
    """
    try:
        # Get request data
        data = request.get_json()
        if not data or 'raw_text' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing raw_text parameter'
            }), 400

        raw_text = data['raw_text']

        # Parse input
        words = parse_bulk_word_input(raw_text)

        if not words:
            return jsonify({
                'success': False,
                'error': 'No valid words found in input'
            }), 400

        # Truncate if needed (cost protection)
        words, was_truncated = truncate_if_needed(words, max_words=50)
        truncation_warning = f"Limited to 50 words. {len(words)} extra words not processed." if was_truncated else None

        # Validate each word before LLM (deterministic checks)
        valid_words = []
        rejected_words = []
        validation_errors = []

        for word in words:
            is_valid, error_msg = validate_word_before_llm(word, current_user.id)
            if is_valid:
                valid_words.append(word)
            else:
                rejected_words.append(word)
                validation_errors.append(f"'{word}': {error_msg}")

        if not valid_words:
            return jsonify({
                'success': False,
                'error': 'No valid Spanish words found',
                'errors': validation_errors
            }), 400

        # Layer 2: LLM validation for complex cases (mixed language, gibberish, English)
        llm_service = get_llm_service()
        validated_words, llm_rejected = llm_service.validate_spanish_words(valid_words)

        # Add LLM rejection reasons to errors
        for word, reason in llm_rejected:
            rejected_words.append(word)
            validation_errors.append(f"'{word}': {reason}")

        if not validated_words:
            return jsonify({
                'success': False,
                'error': 'No valid Spanish words found after validation',
                'errors': validation_errors
            }), 400

        # Process with LLM (translation and categorization)
        processed_words, llm_error = llm_service.process_words_bulk(validated_words)

        if llm_error:
            return jsonify({
                'success': False,
                'error': llm_error,
                'errors': validation_errors
            }), 500

        if not processed_words:
            return jsonify({
                'success': False,
                'error': 'No words could be processed',
                'errors': validation_errors
            }), 400

        # Create words in database
        created_words, db_errors, db_stats = WordService.bulk_create_words(
            current_user.id,
            processed_words
        )

        # Prepare response
        words_data = [word.to_dict() for word in created_words]

        all_errors = validation_errors + db_errors
        if truncation_warning:
            all_errors.insert(0, truncation_warning)

        stats = {
            'processed': len(words),
            'created': db_stats['created'],
            'duplicates': db_stats['duplicates'],
            'failed': db_stats['failed'],
            'rejected': len(rejected_words)
        }

        return jsonify({
            'success': True,
            'words': words_data,
            'stats': stats,
            'errors': all_errors if all_errors else []
        }), 200

    except Exception as e:
        print(f"Error in process_words: {e}")
        return jsonify({
            'success': False,
            'error': 'Server error occurred',
            'details': str(e)
        }), 500

@api_bp.route('/words/<int:word_id>', methods=['PUT'])
@login_required
def update_word(word_id):
    """
    Update a word's details.

    Request JSON:
        {
            "spanish": "cocinar",
            "english": "to cook",
            "word_type": "verb",
            "themes": ["food", "home"]
        }

    Response JSON:
        {
            "success": true,
            "word": {...}
        }
    """
    try:
        data = request.get_json()

        # Find word (ensure it belongs to current user)
        word = V2Word.query.filter_by(
            id=word_id,
            user_id=current_user.id
        ).first()

        if not word:
            return jsonify({
                'success': False,
                'error': 'Word not found'
            }), 404

        # Validate input
        spanish = data.get('spanish', '').strip()
        english = data.get('english', '').strip()
        word_type = data.get('word_type', '').strip()
        themes = data.get('themes', [])

        if not spanish or not english or not word_type:
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400

        if len(themes) == 0 or len(themes) > 3:
            return jsonify({
                'success': False,
                'error': 'Please select 1-3 themes'
            }), 400

        # Check for duplicates (if Spanish word changed)
        if word.spanish.lower() != spanish.lower():
            existing = V2Word.query.filter(
                V2Word.user_id == current_user.id,
                V2Word.id != word_id,
                db.func.lower(V2Word.spanish) == spanish.lower()
            ).first()

            if existing:
                return jsonify({
                    'success': False,
                    'error': f'Word "{spanish}" already exists'
                }), 400

        # Update word
        word.spanish = spanish
        word.english = english
        word.word_type = word_type
        word.themes = ','.join(themes)

        db.session.commit()

        return jsonify({
            'success': True,
            'word': word.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating word: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@api_bp.route('/words/<int:word_id>', methods=['DELETE'])
@login_required
def delete_word(word_id):
    """
    Delete a word (cascades to examples and practice attempts).

    Response JSON:
        {
            "success": true
        }
    """
    try:
        # Find word (ensure it belongs to current user)
        word = V2Word.query.filter_by(
            id=word_id,
            user_id=current_user.id
        ).first()

        if not word:
            return jsonify({
                'success': False,
                'error': 'Word not found'
            }), 404

        # Delete (cascades automatically)
        db.session.delete(word)
        db.session.commit()

        return jsonify({
            'success': True
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting word: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
