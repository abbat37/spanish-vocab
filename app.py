from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
import random
import os
import uuid
from dotenv import load_dotenv # type: ignore
from database import db, init_db, VocabularyWord, SentenceTemplate, UserSession, WordPractice, User
from sqlalchemy import func # type: ignore
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from marshmallow import Schema, fields, ValidationError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize Sentry for error tracking
# Only initialize if SENTRY_DSN is provided (production)
SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
        profiles_sample_rate=0.1,  # 10% for profiling
        environment=os.getenv('FLASK_ENV', 'production'),  # Tag errors by environment
    )

app = Flask(__name__)

# Configure app from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-fallback')
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'

# Database configuration
# Get DATABASE_URL from environment, fallback to SQLite for local dev
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///spanish_vocab.db')

# Render provides postgres:// but SQLAlchemy needs postgresql://
# This conversion ensures compatibility
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not authenticated
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

# Initialize rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Auto-seed database on startup if empty
with app.app_context():
    word_count = VocabularyWord.query.count()
    if word_count == 0:
        print("\n" + "="*60)
        print("⚠️  Database is empty - auto-seeding...")
        print("="*60)

        # Import and run seeding
        try:
            from seed_database import seed_vocabulary, seed_sentence_templates
            seed_vocabulary()
            seed_sentence_templates()
            print("✅ Database seeded successfully on startup!")
            print(f"Total words: {VocabularyWord.query.count()}")
            print(f"Total templates: {SentenceTemplate.query.count()}")
            print("="*60 + "\n")
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            print("Please run manually: python3 seed_database.py")
            print("="*60 + "\n")


# API Validation Schemas
class MarkLearnedSchema(Schema):
    """Validation schema for mark-learned endpoint"""
    word_id = fields.Integer(required=True, error_messages={
        'required': 'word_id is required',
        'invalid': 'word_id must be a valid integer'
    })
    learned = fields.Boolean(error_messages={
        'invalid': 'learned must be a boolean (true/false)'
    })


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


# Authentication Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('register.html')

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('login'))

        # Create new user
        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)

        # Link anonymous session to new user account (if exists)
        if 'user_session_id' in session:
            anonymous_session_id = session['user_session_id']
            user_session = UserSession.query.filter_by(session_id=anonymous_session_id).first()
            if user_session:
                user_session.user_id = new_user.id

        db.session.commit()

        # Log the user in
        login_user(new_user)
        flash('Account created successfully! Welcome to Spanish Word Learner.', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Validation
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('login.html')

        # Find user
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()

            # Log the user in
            login_user(user)
            flash(f'Welcome back, {email}!', 'success')

            # Redirect to next page or index
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@login_required
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
@limiter.limit("10 per minute")
def mark_learned():
    """API endpoint to mark a word as learned"""
    # Validate incoming request data
    schema = MarkLearnedSchema()
    try:
        data = schema.load(request.json or {})
    except ValidationError as err:
        # Return validation errors with 400 status
        return jsonify({'error': 'Validation failed', 'details': err.messages}), 400

    session_id = get_or_create_session_id()
    word_id = data['word_id']

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
