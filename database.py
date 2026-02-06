"""
Database models for Spanish Vocabulary Learning App
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Model for user accounts"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to user sessions (for migration of anonymous sessions)
    sessions = db.relationship('UserSession', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        """Hash and set the password"""
        # bcrypt requires bytes, so we encode the password string
        password_bytes = password.encode('utf-8')
        # Generate salt and hash the password
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches the hash"""
        password_bytes = password.encode('utf-8')
        password_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash_bytes)

    def to_dict(self):
        """Convert to dictionary format (excluding password)"""
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class VocabularyWord(db.Model):
    """Model for storing Spanish vocabulary words"""
    __tablename__ = 'vocabulary_words'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50), nullable=False, index=True)  # cooking, work, sports, restaurant
    word_type = db.Column(db.String(20), nullable=False, index=True)  # verb, noun, adj
    spanish_word = db.Column(db.String(100), nullable=False)
    english_translation = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<VocabularyWord {self.spanish_word} ({self.english_translation})>'

    def to_dict(self):
        """Convert to dictionary format"""
        return {
            'id': self.id,
            'theme': self.theme,
            'word_type': self.word_type,
            'spanish_word': self.spanish_word,
            'english_translation': self.english_translation
        }


class SentenceTemplate(db.Model):
    """Model for storing sentence templates"""
    __tablename__ = 'sentence_templates'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50), nullable=False, index=True)
    word_type = db.Column(db.String(20), nullable=False, index=True)
    spanish_template = db.Column(db.String(500), nullable=False)
    english_template = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SentenceTemplate {self.theme}/{self.word_type}>'

    def to_dict(self):
        """Convert to dictionary format"""
        return {
            'id': self.id,
            'theme': self.theme,
            'word_type': self.word_type,
            'spanish_template': self.spanish_template,
            'english_template': self.english_template
        }


class UserSession(db.Model):
    """Model for tracking user sessions (both anonymous and authenticated)"""
    __tablename__ = 'user_sessions'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)  # NULL for anonymous sessions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserSession {self.session_id} user_id={self.user_id}>'


class WordPractice(db.Model):
    """Model for tracking which words a user has practiced"""
    __tablename__ = 'word_practice'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    word_id = db.Column(db.Integer, db.ForeignKey('vocabulary_words.id'), nullable=False)
    theme = db.Column(db.String(50), nullable=False)
    word_type = db.Column(db.String(20), nullable=False)
    practiced_at = db.Column(db.DateTime, default=datetime.utcnow)
    marked_learned = db.Column(db.Boolean, default=False)

    # Relationship to vocabulary word
    word = db.relationship('VocabularyWord', backref='practices')

    def __repr__(self):
        return f'<WordPractice session={self.session_id} word_id={self.word_id}>'

    def to_dict(self):
        """Convert to dictionary format"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'word_id': self.word_id,
            'theme': self.theme,
            'word_type': self.word_type,
            'practiced_at': self.practiced_at.isoformat(),
            'marked_learned': self.marked_learned
        }


def init_db(app):
    """Initialize the database with the Flask app"""
    db.init_app(app)

    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
