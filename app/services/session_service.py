"""
Session Management Service
Handles user session creation and linking to authenticated users
"""
import uuid
from flask import session
from flask_login import current_user
from app.models import db, UserSession


class SessionService:
    """Service for managing user sessions"""

    @staticmethod
    def get_or_create_session_id():
        """
        Get or create a session ID for tracking user progress.

        For authenticated users: links the session to their user_id.
        This ensures progress follows the user across devices/browsers.
        """
        try:
            if 'user_session_id' not in session:
                session['user_session_id'] = str(uuid.uuid4())

                # Create user session in database, linked to user if authenticated
                try:
                    user_id = current_user.id if current_user.is_authenticated else None
                except (AttributeError, RuntimeError):
                    user_id = None

                user_session = UserSession(
                    session_id=session['user_session_id'],
                    user_id=user_id
                )
                db.session.add(user_session)
                db.session.commit()
            else:
                # Update existing session with user_id if user just logged in
                try:
                    if current_user.is_authenticated:
                        user_session = UserSession.query.filter_by(
                            session_id=session['user_session_id']
                        ).first()
                        if user_session and user_session.user_id is None:
                            # Link existing anonymous session to authenticated user
                            user_session.user_id = current_user.id
                            db.session.commit()
                        elif not user_session:
                            # Session ID in cookie but no DB record - create one
                            # This can happen if the database was reset but cookies persisted
                            user_session = UserSession(
                                session_id=session['user_session_id'],
                                user_id=current_user.id
                            )
                            db.session.add(user_session)
                            db.session.commit()
                except (AttributeError, RuntimeError):
                    pass

            return session['user_session_id']
        except RuntimeError:
            # Outside request context (e.g., in tests)
            return 'test-session-id'

    @staticmethod
    def get_user_identifier():
        """
        Get the identifier to use for tracking user progress.

        For authenticated users: use user_id (progress follows them everywhere)
        For anonymous users: use session_id (progress tied to browser session)

        Returns:
            tuple: (identifier_type, identifier_value) where type is 'user_id' or 'session_id'
        """
        try:
            if current_user.is_authenticated:
                return ('user_id', current_user.id)
        except (AttributeError, RuntimeError):
            # Outside request context or user not loaded
            pass
        return ('session_id', SessionService.get_or_create_session_id())
