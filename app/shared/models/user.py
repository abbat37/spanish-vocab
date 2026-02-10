"""
User Model (Shared across versions)
"""
from flask_login import UserMixin
from datetime import datetime
import bcrypt
from app.shared.extensions import db


class User(UserMixin, db.Model):
    """Model for user accounts"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to user sessions
    sessions = db.relationship('UserSession', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        """Hash and set the password"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches the hash"""
        password_bytes = password.encode('utf-8')
        password_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash_bytes)

    def to_dict(self):
        """Convert to dictionary format (excluding password)"""
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
