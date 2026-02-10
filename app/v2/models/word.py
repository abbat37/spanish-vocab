"""
V2Word Model
User's custom vocabulary database
"""
from datetime import datetime
from app.shared.extensions import db


class V2Word(db.Model):
    """
    User-created vocabulary words with AI-generated metadata.

    Example:
        word = V2Word(
            user_id=1,
            spanish='cocinar',
            english='to cook',
            word_type='verb',
            themes='food,home'
        )
    """
    __tablename__ = 'v2_words'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Word Data
    spanish = db.Column(db.String(100), nullable=False, index=True)
    english = db.Column(db.String(200), nullable=False)
    word_type = db.Column(
        db.String(20),
        nullable=False,
        index=True
    )  # verb, noun, adjective, adverb, phrase, function_word, number, other

    # Themes (comma-separated for simplicity in Phase 3)
    # Example: "weather,emotions" or "food,home,work"
    themes = db.Column(db.String(200), nullable=False, index=True)

    # Learning Status
    is_learned = db.Column(db.Boolean, default=False, nullable=False, index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    examples = db.relationship(
        'V2GeneratedExample',
        backref='word',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    practice_attempts = db.relationship(
        'V2PracticeAttempt',
        backref='word',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    user = db.relationship('User', backref='v2_words')

    def __repr__(self):
        return f'<V2Word {self.spanish} ({self.english})>'

    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'spanish': self.spanish,
            'english': self.english,
            'word_type': self.word_type,
            'themes': self.themes.split(',') if self.themes else [],
            'is_learned': self.is_learned,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @property
    def theme_list(self):
        """Get themes as list"""
        return self.themes.split(',') if self.themes else []

    @theme_list.setter
    def theme_list(self, themes):
        """Set themes from list"""
        self.themes = ','.join(themes) if themes else ''
