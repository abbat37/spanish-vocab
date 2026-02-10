"""
V2GeneratedExample Model
AI-generated example sentences for vocabulary words
"""
from datetime import datetime
from app.shared.extensions import db


class V2GeneratedExample(db.Model):
    """
    AI-generated example sentences for vocabulary study.

    Each word can have multiple examples generated over time.
    User can regenerate examples if they don't like them.

    Example:
        example = V2GeneratedExample(
            word_id=1,
            spanish_sentence='Me gusta cocinar con mi familia.',
            english_translation='I like to cook with my family.'
        )
    """
    __tablename__ = 'v2_generated_examples'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    word_id = db.Column(
        db.Integer,
        db.ForeignKey('v2_words.id'),
        nullable=False,
        index=True
    )

    # Example Sentences
    spanish_sentence = db.Column(db.Text, nullable=False)
    english_translation = db.Column(db.Text, nullable=False)

    # Metadata
    generated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<V2GeneratedExample for word_id={self.word_id}>'

    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'word_id': self.word_id,
            'spanish': self.spanish_sentence,
            'english': self.english_translation,
            'generated_at': self.generated_at.isoformat()
        }
