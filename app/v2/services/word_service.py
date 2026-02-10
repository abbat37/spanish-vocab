"""
Word Service for V2
Handles word CRUD operations and queries
"""
from typing import List, Optional, Dict
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
