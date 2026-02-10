"""
V2PracticeAttempt Model
Tracks user's practice attempts with AI feedback
"""
from datetime import datetime
from app.shared.extensions import db


class V2PracticeAttempt(db.Model):
    """
    Records each practice attempt in the Revise section.

    Stores user's sentence, AI feedback, and correctness score.
    Useful for tracking progress and analyzing learning patterns.

    Example:
        attempt = V2PracticeAttempt(
            user_id=1,
            word_id=1,
            user_sentence='Yo cocino pasta.',
            ai_feedback='Great! Minor suggestion: ...',
            is_correct=True
        )
    """
    __tablename__ = 'v2_practice_attempts'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
        index=True
    )
    word_id = db.Column(
        db.Integer,
        db.ForeignKey('v2_words.id'),
        nullable=False,
        index=True
    )

    # Practice Data
    user_sentence = db.Column(db.Text, nullable=False)
    ai_feedback = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    # Timestamp
    attempted_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    # Relationships
    user = db.relationship('User', backref='v2_practice_attempts')

    def __repr__(self):
        return f'<V2PracticeAttempt user_id={self.user_id} word_id={self.word_id}>'

    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'word_id': self.word_id,
            'user_sentence': self.user_sentence,
            'ai_feedback': self.ai_feedback,
            'is_correct': self.is_correct,
            'attempted_at': self.attempted_at.isoformat()
        }
