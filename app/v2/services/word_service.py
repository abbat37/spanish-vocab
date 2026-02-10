"""
Word Service for V2
Handles word CRUD operations and queries
"""
from typing import List, Optional, Dict, Tuple
from sqlalchemy import or_
from app.shared.extensions import db
from app.v2.models import V2Word


class WordService:
    """Service for managing V2 vocabulary words"""

    @staticmethod
    def get_user_words(user_id: int, filters: Optional[Dict] = None) -> List[V2Word]:
        """
        Get user's words with optional filters.

        Args:
            user_id: User ID
            filters: Optional dict with 'word_type', 'themes', 'is_learned', 'search'

        Returns:
            List of V2Word objects
        """
        query = V2Word.query.filter_by(user_id=user_id)

        if filters:
            # Filter by word type
            if filters.get('word_type'):
                query = query.filter(V2Word.word_type == filters['word_type'])

            # Filter by theme (contains)
            if filters.get('theme'):
                query = query.filter(V2Word.themes.contains(filters['theme']))

            # Filter by learned status
            if 'is_learned' in filters:
                query = query.filter(V2Word.is_learned == filters['is_learned'])

            # Search by Spanish or English word
            if filters.get('search'):
                search_term = f"%{filters['search']}%"
                query = query.filter(
                    or_(
                        V2Word.spanish.ilike(search_term),
                        V2Word.english.ilike(search_term)
                    )
                )

        return query.order_by(V2Word.created_at.desc()).all()

    @staticmethod
    def get_random_word(user_id: int, is_learned: bool = False) -> Optional[V2Word]:
        """
        Get random word for study/revise.

        Args:
            user_id: User ID
            is_learned: True for revise (learned words), False for study (unlearned)

        Returns:
            Random V2Word or None
        """
        return V2Word.query.filter_by(
            user_id=user_id,
            is_learned=is_learned
        ).order_by(db.func.random()).first()

    @staticmethod
    def mark_word_learned(word_id: int, user_id: int, learned: bool = True) -> bool:
        """
        Toggle word learned status.

        Args:
            word_id: Word ID
            user_id: User ID (for security)
            learned: New learned status

        Returns:
            True if successful, False if word not found
        """
        word = V2Word.query.filter_by(id=word_id, user_id=user_id).first()

        if not word:
            return False

        word.is_learned = learned
        db.session.commit()
        return True

    @staticmethod
    def delete_word(word_id: int, user_id: int) -> bool:
        """
        Delete word (will cascade to examples and practice attempts).

        Args:
            word_id: Word ID
            user_id: User ID (for security)

        Returns:
            True if deleted, False if not found
        """
        word = V2Word.query.filter_by(id=word_id, user_id=user_id).first()

        if not word:
            return False

        db.session.delete(word)
        db.session.commit()
        return True

    @staticmethod
    def bulk_create_words(user_id: int, processed_words: List[Dict]) -> Tuple[List[V2Word], List[str], Dict]:
        """
        Create multiple words with error handling.

        Args:
            user_id: User ID
            processed_words: List of dicts with spanish, english, word_type, themes

        Returns:
            (created_words, error_messages, stats)
            - created_words: List of V2Word objects that were created
            - error_messages: List of error strings for words that failed
            - stats: Dict with 'processed', 'created', 'duplicates', 'failed'
        """
        created_words = []
        error_messages = []
        duplicates = 0
        failed = 0

        for word_data in processed_words:
            try:
                spanish = word_data.get('spanish', '').strip()
                english = word_data.get('english', '').strip()
                word_type = word_data.get('word_type', 'other')
                themes = word_data.get('themes', ['other'])

                # Check for duplicate (case-insensitive)
                existing = V2Word.query.filter(
                    V2Word.user_id == user_id,
                    V2Word.spanish.ilike(spanish)
                ).first()

                if existing:
                    duplicates += 1
                    error_messages.append(f"'{spanish}' already exists")
                    continue

                # Convert theme list to comma-separated string
                if isinstance(themes, list):
                    themes_str = ','.join(themes)
                else:
                    themes_str = str(themes)

                # Create word
                word = V2Word(
                    user_id=user_id,
                    spanish=spanish,
                    english=english,
                    word_type=word_type,
                    themes=themes_str,
                    is_learned=False
                )

                db.session.add(word)
                created_words.append(word)

            except Exception as e:
                failed += 1
                error_messages.append(f"Failed to create '{word_data.get('spanish', 'unknown')}': {str(e)}")

        # Commit all at once
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error_messages.append(f"Database error: {str(e)}")
            return [], error_messages, {
                'processed': len(processed_words),
                'created': 0,
                'duplicates': duplicates,
                'failed': len(processed_words)
            }

        stats = {
            'processed': len(processed_words),
            'created': len(created_words),
            'duplicates': duplicates,
            'failed': failed
        }

        return created_words, error_messages, stats
