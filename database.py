"""
Database models for Spanish Vocabulary Learning App
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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
    """Model for tracking user sessions (simple session-based tracking)"""
    __tablename__ = 'user_sessions'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserSession {self.session_id}>'


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
