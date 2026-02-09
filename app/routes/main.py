"""
Main Application Routes
Handles the main vocabulary practice interface
"""
from flask import Blueprint, render_template, request
from flask_login import login_required
from app.services import SessionService, StatsService, SentenceService

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Main vocabulary practice page"""
    sentences = []
    theme = ''
    word_type = ''
    stats = None

    # Get or create session (this links session to user if authenticated)
    session_id = SessionService.get_or_create_session_id()

    # Get stats using user_id for authenticated users
    identifier_type, identifier_value = SessionService.get_user_identifier()
    stats = StatsService.get_user_stats(identifier_type, identifier_value)

    # Ensure all themes are always present in stats (even with 0)
    all_themes = ['cooking', 'work', 'sports', 'restaurant']
    if stats and 'by_theme' in stats:
        for theme_name in all_themes:
            if theme_name not in stats['by_theme']:
                stats['by_theme'][theme_name] = 0

    if request.method == 'POST':
        theme = request.form.get('theme', '').lower()
        word_type = request.form.get('word_type', '').lower()

        if theme and word_type:
            sentences = SentenceService.generate_sentences(
                theme, word_type, identifier_type, identifier_value
            )

            # Record practice for each word
            for sentence in sentences:
                StatsService.record_word_practice(
                    session_id, sentence['word_id'], theme, word_type
                )

            # Refresh stats after recording practice
            stats = StatsService.get_user_stats(identifier_type, identifier_value)

            # Ensure all themes are always present
            all_themes = ['cooking', 'work', 'sports', 'restaurant']
            if stats and 'by_theme' in stats:
                for theme_name in all_themes:
                    if theme_name not in stats['by_theme']:
                        stats['by_theme'][theme_name] = 0

    return render_template(
        'index.html',
        sentences=sentences,
        theme=theme,
        word_type=word_type,
        stats=stats
    )
