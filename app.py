from flask import Flask, render_template, request, session, jsonify
import random
import os
import uuid
from dotenv import load_dotenv # type: ignore
from database import db, init_db, VocabularyWord, SentenceTemplate, UserSession, WordPractice
from sqlalchemy import func # type: ignore

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure app from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-fallback')
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///spanish_vocab.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Check if database needs seeding
with app.app_context():
    word_count = VocabularyWord.query.count()
    if word_count == 0:
        print("\n" + "="*60)
        print("⚠️  WARNING: Database is empty!")
        print("="*60)
        print("The database has no vocabulary words.")
        print("Please run: python3 seed_database.py")
        print("="*60 + "\n")


def get_or_create_session_id():
    """Get or create a session ID for tracking user progress"""
    if 'user_session_id' not in session:
        session['user_session_id'] = str(uuid.uuid4())

        # Create user session in database
        user_session = UserSession(session_id=session['user_session_id'])
        db.session.add(user_session)
        db.session.commit()

    return session['user_session_id']


def get_user_stats(session_id):
    """Get user progress statistics"""
    total_practiced = WordPractice.query.filter_by(session_id=session_id).count()
    total_learned = WordPractice.query.filter_by(session_id=session_id, marked_learned=True).count()

    # Get stats by theme
    theme_stats = db.session.query(
        WordPractice.theme,
        func.count(WordPractice.id).label('count')
    ).filter_by(session_id=session_id).group_by(WordPractice.theme).all()

    return {
        'total_practiced': total_practiced,
        'total_learned': total_learned,
        'by_theme': {theme: count for theme, count in theme_stats}
    }


def record_word_practice(session_id, word_id, theme, word_type):
    """Record that a user practiced a word"""
    # Check if already practiced in this session
    existing = WordPractice.query.filter_by(
        session_id=session_id,
        word_id=word_id
    ).first()

    if not existing:
        practice = WordPractice(
            session_id=session_id,
            word_id=word_id,
            theme=theme,
            word_type=word_type
        )
        db.session.add(practice)
        db.session.commit()


def generate_sentences(theme, word_type, session_id=None):
    """Generate 5 sentences with new Spanish words from database"""
    # Query vocabulary words from database
    words = VocabularyWord.query.filter_by(theme=theme, word_type=word_type).all()

    if not words:
        return []

    # Query sentence templates from database
    templates = SentenceTemplate.query.filter_by(theme=theme, word_type=word_type).all()

    if not templates:
        return []

    # Select 5 random words
    selected_words = random.sample(words, min(5, len(words)))

    # Select 5 random templates (or reuse if less than 5)
    selected_templates = random.sample(templates, min(5, len(templates)))

    sentences = []
    for i, word in enumerate(selected_words):
        # Get the template (cycle through if we have fewer templates than words)
        template = selected_templates[i % len(selected_templates)]

        # Create Spanish sentence
        spanish_sentence = template.spanish_template.replace(
            '{word}',
            f'<mark>{word.spanish_word}</mark>'
        )

        # Create English sentence
        english_sentence = template.english_template.replace(
            '{word}',
            f'<mark>{word.english_translation}</mark>'
        )

        # Check if this word is marked as learned
        is_learned = False
        if session_id:
            practice = WordPractice.query.filter_by(
                session_id=session_id,
                word_id=word.id
            ).first()
            if practice and practice.marked_learned:
                is_learned = True

        sentences.append({
            'spanish': spanish_sentence,
            'english': english_sentence,
            'word_id': word.id,
            'is_learned': is_learned
        })

    return sentences


@app.after_request
def add_header(response):
    """Add headers to prevent caching during development"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    sentences = []
    theme = ''
    word_type = ''
    stats = None

    # Get or create session
    session_id = get_or_create_session_id()
    stats = get_user_stats(session_id)

    if request.method == 'POST':
        theme = request.form.get('theme', '').lower()
        word_type = request.form.get('word_type', '').lower()

        if theme and word_type:
            sentences = generate_sentences(theme, word_type, session_id)

            # Record practice for each word
            for sentence in sentences:
                record_word_practice(session_id, sentence['word_id'], theme, word_type)

            # Refresh stats after recording practice
            stats = get_user_stats(session_id)

    return render_template('index.html', sentences=sentences, theme=theme, word_type=word_type, stats=stats)


@app.route('/api/mark-learned', methods=['POST'])
def mark_learned():
    """API endpoint to mark a word as learned"""
    session_id = get_or_create_session_id()
    word_id = request.json.get('word_id')

    if not word_id:
        return jsonify({'error': 'word_id is required'}), 400

    # Find the practice record
    practice = WordPractice.query.filter_by(
        session_id=session_id,
        word_id=word_id
    ).first()

    if practice:
        practice.marked_learned = not practice.marked_learned  # Toggle
        db.session.commit()
        return jsonify({
            'success': True,
            'marked_learned': practice.marked_learned,
            'stats': get_user_stats(session_id)
        })
    else:
        return jsonify({'error': 'Practice record not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
