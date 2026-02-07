"""
Database Models
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models so they're available when importing from app.models
from .user import User
from .vocabulary import VocabularyWord, SentenceTemplate
from .session import UserSession, WordPractice

__all__ = [
    'db',
    'User',
    'VocabularyWord',
    'SentenceTemplate',
    'UserSession',
    'WordPractice'
]
