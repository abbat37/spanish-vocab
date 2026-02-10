"""
Stats Service for V2
Calculates learning statistics and progress
"""
from typing import Dict
from sqlalchemy import func
from app.v2.models import V2Word, V2PracticeAttempt


class StatsService:
    """Service for calculating V2 learning statistics"""

    @staticmethod
    def get_user_stats(user_id: int) -> Dict:
        """
        Get comprehensive stats for dashboard.

        Args:
            user_id: User ID

        Returns:
            Dict with stats
        """
        total_words = V2Word.query.filter_by(user_id=user_id).count()
        learned_words = V2Word.query.filter_by(
            user_id=user_id,
            is_learned=True
        ).count()
        practice_count = V2PracticeAttempt.query.filter_by(user_id=user_id).count()

        # Stats by theme
        theme_stats = {}
        words = V2Word.query.filter_by(user_id=user_id).all()
        for word in words:
            for theme in word.theme_list:
                if theme not in theme_stats:
                    theme_stats[theme] = {'total': 0, 'learned': 0}
                theme_stats[theme]['total'] += 1
                if word.is_learned:
                    theme_stats[theme]['learned'] += 1

        return {
            'total_words': total_words,
            'learned_words': learned_words,
            'practice_count': practice_count,
            'by_theme': theme_stats
        }
