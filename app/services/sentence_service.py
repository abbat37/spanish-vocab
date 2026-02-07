"""
Sentence Generation Service
Handles generating practice sentences with vocabulary words
"""
import random
from app.models import VocabularyWord, SentenceTemplate, UserSession, WordPractice
from .session_service import SessionService


class SentenceService:
    """Service for generating practice sentences"""

    @staticmethod
    def generate_sentences(theme, word_type, identifier_type=None, identifier_value=None):
        """
        Generate 5 sentences with Spanish words from database.

        Args:
            theme: Theme category (cooking, work, sports, restaurant)
            word_type: Type of word (verb, noun, adj)
            identifier_type: 'user_id' or 'session_id' (optional, will auto-detect)
            identifier_value: The actual ID value (optional, will auto-detect)

        Returns:
            list: List of sentence dictionaries with spanish, english, word_id, and is_learned
        """
        # Get user identifier if not provided
        if identifier_type is None or identifier_value is None:
            identifier_type, identifier_value = SessionService.get_user_identifier()

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

        # Get session IDs to check for learned status
        if identifier_type == 'user_id':
            user_sessions = UserSession.query.filter_by(user_id=identifier_value).all()
            session_ids = [s.session_id for s in user_sessions]
        else:
            session_ids = [identifier_value]

        sentences = []
        for i, word in enumerate(selected_words):
            # Get the template (cycle through if we have fewer templates than words)
            template = selected_templates[i % len(selected_templates)]

            # Create Spanish sentence with highlighted word
            spanish_sentence = template.spanish_template.replace(
                '{word}',
                f'<mark>{word.spanish_word}</mark>'
            )

            # Create English sentence with highlighted word
            english_sentence = template.english_template.replace(
                '{word}',
                f'<mark>{word.english_translation}</mark>'
            )

            # Check if this word is marked as learned in any of the user's sessions
            is_learned = False
            if session_ids:
                practice = WordPractice.query.filter(
                    WordPractice.session_id.in_(session_ids),
                    WordPractice.word_id == word.id,
                    WordPractice.marked_learned == True
                ).first()
                is_learned = practice is not None

            sentences.append({
                'spanish': spanish_sentence,
                'english': english_sentence,
                'word_id': word.id,
                'is_learned': is_learned
            })

        return sentences
