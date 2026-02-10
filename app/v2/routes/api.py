"""
V2 API Routes
RESTful API endpoints for bulk word processing
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.shared.extensions import limiter
from app.v2.services.llm_service import get_llm_service
from app.v2.services.word_service import WordService
from app.v2.utils import parse_bulk_word_input, truncate_if_needed, validate_word_before_llm

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

        # Process with LLM
        llm_service = get_llm_service()
        processed_words = llm_service.process_words_bulk(valid_words)

        if not processed_words:
            return jsonify({
                'success': False,
                'error': 'LLM processing failed',
                'errors': ['Unable to process words with AI. Please try again.']
            }), 500

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
