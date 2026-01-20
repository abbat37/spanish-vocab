"""
Tests for Flask application routes and functionality
"""
import pytest
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, generate_sentences, get_user_stats, record_word_practice
from database import db, VocabularyWord, SentenceTemplate, WordPractice, UserSession


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for tests
    app.config['SECRET_KEY'] = 'test-secret-key'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Seed test data
            _seed_test_data()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def _seed_test_data():
    """Seed database with test data"""
    # Add test vocabulary words
    words = [
        VocabularyWord(theme='cooking', word_type='verb', spanish_word='cocinar', english_translation='to cook'),
        VocabularyWord(theme='cooking', word_type='verb', spanish_word='hornear', english_translation='to bake'),
        VocabularyWord(theme='cooking', word_type='noun', spanish_word='sartén', english_translation='pan'),
        VocabularyWord(theme='work', word_type='verb', spanish_word='trabajar', english_translation='to work'),
        VocabularyWord(theme='sports', word_type='adj', spanish_word='rápido', english_translation='fast'),
    ]
    for word in words:
        db.session.add(word)

    # Add test sentence templates
    templates = [
        SentenceTemplate(theme='cooking', word_type='verb',
                        spanish_template='Me gusta {word} todos los días.',
                        english_template='I like to {word} every day.'),
        SentenceTemplate(theme='cooking', word_type='verb',
                        spanish_template='Voy a {word} algo especial.',
                        english_template='I\'m going to {word} something special.'),
        SentenceTemplate(theme='cooking', word_type='noun',
                        spanish_template='Necesito comprar un/una {word} nuevo/a.',
                        english_template='I need to buy a new {word}.'),
        SentenceTemplate(theme='work', word_type='verb',
                        spanish_template='Tengo que {word} mañana.',
                        english_template='I have to {word} tomorrow.'),
        SentenceTemplate(theme='sports', word_type='adj',
                        spanish_template='El jugador es muy {word}.',
                        english_template='The player is very {word}.'),
    ]
    for template in templates:
        db.session.add(template)

    db.session.commit()


class TestRoutes:
    """Test Flask routes"""

    def test_home_page_loads(self, client):
        """Test that home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Spanish Word Learner' in response.data

    def test_home_page_has_form(self, client):
        """Test that home page contains the form elements"""
        response = client.get('/')
        assert b'<select id="theme"' in response.data
        assert b'<select id="word_type"' in response.data
        assert b'Generate Sentences' in response.data

    def test_generate_sentences_post(self, client):
        """Test POST request to generate sentences"""
        response = client.post('/', data={
            'theme': 'cooking',
            'word_type': 'verb'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'cocinar' in response.data or b'hornear' in response.data

    def test_invalid_theme(self, client):
        """Test with invalid theme"""
        response = client.post('/', data={
            'theme': 'invalid',
            'word_type': 'verb'
        })

        assert response.status_code == 200
        # Should handle gracefully, not crash


class TestGenerateSentences:
    """Test sentence generation functionality"""

    def test_generate_sentences_returns_list(self, client):
        """Test that generate_sentences returns a list"""
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            assert isinstance(sentences, list)

    def test_generate_sentences_count(self, client):
        """Test that generate_sentences returns correct number of sentences"""
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            assert len(sentences) <= 5  # Should return up to 5 sentences
            assert len(sentences) > 0   # Should return at least 1

    def test_generate_sentences_structure(self, client):
        """Test that sentences have correct structure"""
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            if sentences:
                sentence = sentences[0]
                assert 'spanish' in sentence
                assert 'english' in sentence
                assert 'word_id' in sentence
                assert 'is_learned' in sentence

    def test_generate_sentences_has_highlighted_words(self, client):
        """Test that sentences have highlighted words"""
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            if sentences:
                assert '<mark>' in sentences[0]['spanish']
                assert '<mark>' in sentences[0]['english']

    def test_generate_sentences_invalid_theme(self, client):
        """Test with invalid theme returns empty list"""
        with app.app_context():
            sentences = generate_sentences('invalid_theme', 'verb')
            assert sentences == []

    def test_generate_sentences_invalid_word_type(self, client):
        """Test with invalid word type returns empty list"""
        with app.app_context():
            sentences = generate_sentences('cooking', 'invalid_type')
            assert sentences == []


class TestProgressTracking:
    """Test progress tracking functionality"""

    def test_record_word_practice(self, client):
        """Test recording word practice"""
        with app.app_context():
            test_session_id = 'test-session-123'

            # Record practice
            record_word_practice(test_session_id, 1, 'cooking', 'verb')

            # Verify it was recorded
            practice = WordPractice.query.filter_by(
                session_id=test_session_id,
                word_id=1
            ).first()

            assert practice is not None
            assert practice.theme == 'cooking'
            assert practice.word_type == 'verb'
            assert practice.marked_learned is False

    def test_record_word_practice_no_duplicates(self, client):
        """Test that duplicate practices are not recorded"""
        with app.app_context():
            test_session_id = 'test-session-456'

            # Record practice twice
            record_word_practice(test_session_id, 1, 'cooking', 'verb')
            record_word_practice(test_session_id, 1, 'cooking', 'verb')

            # Should only have one record
            count = WordPractice.query.filter_by(
                session_id=test_session_id,
                word_id=1
            ).count()

            assert count == 1

    def test_get_user_stats_empty(self, client):
        """Test getting stats for user with no practice"""
        with app.app_context():
            stats = get_user_stats('new-user-session')

            assert stats['total_practiced'] == 0
            assert stats['total_learned'] == 0
            assert stats['by_theme'] == {}

    def test_get_user_stats_with_practice(self, client):
        """Test getting stats for user with practice"""
        with app.app_context():
            test_session_id = 'test-session-789'

            # Record some practice
            record_word_practice(test_session_id, 1, 'cooking', 'verb')
            record_word_practice(test_session_id, 2, 'cooking', 'verb')
            record_word_practice(test_session_id, 4, 'work', 'verb')

            stats = get_user_stats(test_session_id)

            assert stats['total_practiced'] == 3
            assert stats['total_learned'] == 0
            assert 'cooking' in stats['by_theme']
            assert 'work' in stats['by_theme']
            assert stats['by_theme']['cooking'] == 2
            assert stats['by_theme']['work'] == 1

    def test_mark_learned_api(self, client):
        """Test marking a word as learned via API"""
        with app.app_context():
            # Create a session and practice record
            test_session_id = 'test-api-session'
            user_session = UserSession(session_id=test_session_id)
            db.session.add(user_session)

            practice = WordPractice(
                session_id=test_session_id,
                word_id=1,
                theme='cooking',
                word_type='verb'
            )
            db.session.add(practice)
            db.session.commit()

        # Make API request with session
        with client.session_transaction() as sess:
            sess['user_session_id'] = test_session_id

        response = client.post('/api/mark-learned',
                              json={'word_id': 1},
                              content_type='application/json')

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['marked_learned'] is True


class TestDatabase:
    """Test database models"""

    def test_vocabulary_word_creation(self, client):
        """Test creating a vocabulary word"""
        with app.app_context():
            word = VocabularyWord(
                theme='test',
                word_type='verb',
                spanish_word='probar',
                english_translation='to test'
            )
            db.session.add(word)
            db.session.commit()

            saved_word = VocabularyWord.query.filter_by(spanish_word='probar').first()
            assert saved_word is not None
            assert saved_word.english_translation == 'to test'

    def test_sentence_template_creation(self, client):
        """Test creating a sentence template"""
        with app.app_context():
            template = SentenceTemplate(
                theme='test',
                word_type='verb',
                spanish_template='Yo {word}.',
                english_template='I {word}.'
            )
            db.session.add(template)
            db.session.commit()

            saved_template = SentenceTemplate.query.filter_by(
                spanish_template='Yo {word}.'
            ).first()
            assert saved_template is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
