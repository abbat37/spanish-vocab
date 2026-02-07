"""
Vocabulary Models
"""
from . import db


class VocabularyWord(db.Model):
    """Model for storing Spanish vocabulary words"""
    __tablename__ = 'vocabulary_words'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50), nullable=False, index=True)
    word_type = db.Column(db.String(20), nullable=False, index=True)
    spanish_word = db.Column(db.String(100), nullable=False)
    english_translation = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<VocabularyWord {self.spanish_word}>'

    def to_dict(self):
        return {
            'id': self.id,
            'theme': self.theme,
            'word_type': self.word_type,
            'spanish_word': self.spanish_word,
            'english_translation': self.english_translation
        }


class SentenceTemplate(db.Model):
    """Model for sentence templates"""
    __tablename__ = 'sentence_templates'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50), nullable=False, index=True)
    word_type = db.Column(db.String(20), nullable=False, index=True)
    spanish_template = db.Column(db.Text, nullable=False)
    english_template = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<SentenceTemplate {self.theme}-{self.word_type}>'

    def to_dict(self):
        return {
            'id': self.id,
            'theme': self.theme,
            'word_type': self.word_type,
            'spanish_template': self.spanish_template,
            'english_template': self.english_template
        }
