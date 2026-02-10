# Phase 3: V2 Database Schema & Models

**Status:** Ready to implement
**Created:** 2026-02-10
**Duration:** 1-2 sessions
**Dependencies:** Phase 2 (V2 Scaffold) - COMPLETE

---

## Overview

Phase 3 establishes the database foundation for V2's vocabulary learning system. We'll create models for user-created words, AI-generated examples, learning progress, and practice attempts - all isolated from V1's schema.

**Learning Objectives:**
- Design normalized database schema
- Create SQLAlchemy models with relationships
- Write Flask-Migrate migrations
- Understand foreign keys and indexes
- Practice safe schema evolution

---

## Database Design

### Schema Diagram

```
┌─────────────────────────────────────────────────────┐
│  User (Shared - already exists)                     │
│  - id (PK)                                          │
│  - email                                            │
│  - password_hash                                    │
└─────────────────┬───────────────────────────────────┘
                  │
                  │ (1:Many)
                  ↓
┌─────────────────────────────────────────────────────┐
│  V2Word                                             │
│  - id (PK)                                          │
│  - user_id (FK → User)                              │
│  - spanish (indexed)                                │
│  - english                                          │
│  - word_type (verb/noun/adj/adverb/phrase)          │
│  - themes (comma-separated: weather,food)           │
│  - is_learned (boolean, default False)              │
│  - created_at (timestamp)                           │
│  - updated_at (timestamp)                           │
└─────────────────┬───────────────────────────────────┘
                  │
                  │ (1:Many)
                  ↓
┌─────────────────────────────────────────────────────┐
│  V2GeneratedExample                                 │
│  - id (PK)                                          │
│  - word_id (FK → V2Word)                            │
│  - spanish_sentence                                 │
│  - english_translation                              │
│  - generated_at (timestamp)                         │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  V2PracticeAttempt                                  │
│  - id (PK)                                          │
│  - user_id (FK → User)                              │
│  - word_id (FK → V2Word)                            │
│  - user_sentence (what user wrote)                  │
│  - ai_feedback (LLM response)                       │
│  - is_correct (boolean)                             │
│  - attempted_at (timestamp)                         │
└─────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Step 1: Create V2 Models

**Create `app/v2/models/__init__.py`:**

```python
"""
V2 Database Models
Isolated from V1 - new vocabulary learning system
"""
from .word import V2Word
from .example import V2GeneratedExample
from .practice import V2PracticeAttempt

__all__ = [
    'V2Word',
    'V2GeneratedExample',
    'V2PracticeAttempt'
]
```

---

**Create `app/v2/models/word.py`:**

```python
"""
V2Word Model
User's custom vocabulary database
"""
from datetime import datetime
from app.shared.extensions import db


class V2Word(db.Model):
    """
    User-created vocabulary words with AI-generated metadata.

    Example:
        word = V2Word(
            user_id=1,
            spanish='cocinar',
            english='to cook',
            word_type='verb',
            themes='food,home'
        )
    """
    __tablename__ = 'v2_words'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Word Data
    spanish = db.Column(db.String(100), nullable=False, index=True)
    english = db.Column(db.String(200), nullable=False)
    word_type = db.Column(
        db.String(20),
        nullable=False,
        index=True
    )  # verb, noun, adj, adverb, phrase

    # Themes (comma-separated for simplicity in Phase 3)
    # Example: "weather,emotions" or "food,home,work"
    themes = db.Column(db.String(200), nullable=False, index=True)

    # Learning Status
    is_learned = db.Column(db.Boolean, default=False, nullable=False, index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    examples = db.relationship(
        'V2GeneratedExample',
        backref='word',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    practice_attempts = db.relationship(
        'V2PracticeAttempt',
        backref='word',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    user = db.relationship('User', backref='v2_words')

    def __repr__(self):
        return f'<V2Word {self.spanish} ({self.english})>'

    def to_dict(self):
        """Convert to dictionary for JSON responses"""
        return {
            'id': self.id,
            'spanish': self.spanish,
            'english': self.english,
            'word_type': self.word_type,
            'themes': self.themes.split(',') if self.themes else [],
            'is_learned': self.is_learned,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @property
    def theme_list(self):
        """Get themes as list"""
        return self.themes.split(',') if self.themes else []

    @theme_list.setter
    def theme_list(self, themes):
        """Set themes from list"""
        self.themes = ','.join(themes) if themes else ''
```

---

**Create `app/v2/models/example.py`:**

```python
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
```

---

**Create `app/v2/models/practice.py`:**

```python
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
        db.ForeignKey('user.id'),
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
```

---

### Step 2: Create Database Migration

**Generate migration:**

```bash
python3 -m flask db migrate -m "Add V2 vocabulary tables (words, examples, practice)"
```

**Review generated migration file:**

The migration should create these tables:
- `v2_words`
- `v2_generated_examples`
- `v2_practice_attempts`

**Key indexes to verify:**
- `v2_words.user_id` (for querying user's words)
- `v2_words.spanish` (for search)
- `v2_words.word_type` (for filtering)
- `v2_words.themes` (for filtering)
- `v2_words.is_learned` (for study/revise logic)
- `v2_generated_examples.word_id` (for fetching examples)
- `v2_practice_attempts.user_id` (for stats)
- `v2_practice_attempts.word_id` (for word history)

---

### Step 3: Apply Migration

**Local (SQLite):**
```bash
python3 -m flask db upgrade
```

**Production (PostgreSQL):**
Migration will be applied automatically during deployment via CI/CD.

---

### Step 4: Create Helper Utilities

**Create `app/v2/services/__init__.py`:**

```python
"""
V2 Business Logic Services
"""
from .word_service import WordService
from .stats_service import StatsService

__all__ = ['WordService', 'StatsService']
```

**Create `app/v2/services/word_service.py`:**

```python
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
```

---

**Create `app/v2/services/stats_service.py`:**

```python
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
```

---

## Testing Plan

**Create `tests/test_phase3_models.py`:**

```python
"""Tests for Phase 3 - V2 Database Models"""
import pytest
from app.v2.models import V2Word, V2GeneratedExample, V2PracticeAttempt
from app.shared.extensions import db


def test_create_v2_word(app, test_user):
    """Test creating a V2 word"""
    word = V2Word(
        user_id=test_user.id,
        spanish='cocinar',
        english='to cook',
        word_type='verb',
        themes='food,home'
    )
    db.session.add(word)
    db.session.commit()

    assert word.id is not None
    assert word.spanish == 'cocinar'
    assert word.theme_list == ['food', 'home']


def test_word_examples_relationship(app, test_user):
    """Test word -> examples relationship"""
    word = V2Word(
        user_id=test_user.id,
        spanish='frío',
        english='cold',
        word_type='adj',
        themes='weather'
    )
    db.session.add(word)
    db.session.commit()

    example = V2GeneratedExample(
        word_id=word.id,
        spanish_sentence='Hace frío hoy.',
        english_translation='It is cold today.'
    )
    db.session.add(example)
    db.session.commit()

    assert len(word.examples.all()) == 1
    assert word.examples.first().spanish_sentence == 'Hace frío hoy.'


def test_cascade_delete(app, test_user):
    """Test that deleting word cascades to examples"""
    word = V2Word(
        user_id=test_user.id,
        spanish='sol',
        english='sun',
        word_type='noun',
        themes='weather'
    )
    db.session.add(word)
    db.session.commit()

    example = V2GeneratedExample(
        word_id=word.id,
        spanish_sentence='El sol brilla.',
        english_translation='The sun shines.'
    )
    db.session.add(example)
    db.session.commit()

    example_id = example.id

    # Delete word
    db.session.delete(word)
    db.session.commit()

    # Example should be deleted too
    assert V2GeneratedExample.query.get(example_id) is None
```

---

## Success Criteria

Phase 3 is complete when:

- [ ] All three V2 models created (Word, Example, Practice)
- [ ] Database migration generated and reviewed
- [ ] Migration applied locally (SQLite)
- [ ] WordService and StatsService implemented
- [ ] All model tests passing
- [ ] Foreign keys and indexes verified
- [ ] Cascade deletes working correctly
- [ ] Documentation complete

---

## Next Phase Preview

**Phase 4 will use these models to:**
- Store bulk-processed words in `V2Word`
- Generate examples and store in `V2GeneratedExample`
- Track practice attempts in `V2PracticeAttempt`

---

**Ready to implement Phase 3! 🚀**