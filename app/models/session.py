"""
Session and Practice Tracking Models
"""
from datetime import datetime
from . import db


class UserSession(db.Model):
    """Model for tracking user sessions (both anonymous and authenticated)"""
    __tablename__ = 'user_sessions'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
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
    marked_learned = db.Column(db.Boolean, default=False)
    practiced_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<WordPractice session={self.session_id} word={self.word_id}>'
