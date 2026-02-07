"""
Statistics Service
Handles user progress statistics and tracking
"""
from sqlalchemy import func
from app.models import db, UserSession, WordPractice
from .session_service import SessionService


class StatsService:
    """Service for managing user statistics"""

    @staticmethod
    def get_user_stats(identifier_type=None, identifier_value=None):
        """
        Get user progress statistics.

        Args:
            identifier_type: 'user_id' or 'session_id'
            identifier_value: The actual ID value

        Returns:
            dict: Statistics including total_practiced, total_learned, and by_theme breakdown
        """
        if identifier_type is None or identifier_value is None:
            identifier_type, identifier_value = SessionService.get_user_identifier()

        if identifier_type == 'user_id':
            # Get all sessions for this user
            user_sessions = UserSession.query.filter_by(user_id=identifier_value).all()
            session_ids = [s.session_id for s in user_sessions]

            # Get practice records from all user's sessions
            total_practiced = WordPractice.query.filter(
                WordPractice.session_id.in_(session_ids)
            ).count() if session_ids else 0

            total_learned = WordPractice.query.filter(
                WordPractice.session_id.in_(session_ids),
                WordPractice.marked_learned == True
            ).count() if session_ids else 0

            # Get stats by theme
            theme_stats = db.session.query(
                WordPractice.theme,
                func.count(WordPractice.id).label('count')
            ).filter(
                WordPractice.session_id.in_(session_ids)
            ).group_by(WordPractice.theme).all() if session_ids else []

        else:  # session_id
            total_practiced = WordPractice.query.filter_by(session_id=identifier_value).count()
            total_learned = WordPractice.query.filter_by(
                session_id=identifier_value,
                marked_learned=True
            ).count()

            theme_stats = db.session.query(
                WordPractice.theme,
                func.count(WordPractice.id).label('count')
            ).filter_by(session_id=identifier_value).group_by(WordPractice.theme).all()

        return {
            'total_practiced': total_practiced,
            'total_learned': total_learned,
            'by_theme': {theme: count for theme, count in theme_stats}
        }

    @staticmethod
    def record_word_practice(session_id, word_id, theme, word_type):
        """
        Record that a user practiced a word.

        Args:
            session_id: Session identifier
            word_id: Vocabulary word ID
            theme: Word theme
            word_type: Word type (verb, noun, adj)
        """
        # Check if already practiced in this session
        existing = WordPractice.query.filter_by(
            session_id=session_id,
            word_id=word_id
        ).first()

        if not existing:
            practice = WordPractice(
                session_id=session_id,
                word_id=word_id,
                theme=theme,
                word_type=word_type
            )
            db.session.add(practice)
            db.session.commit()
