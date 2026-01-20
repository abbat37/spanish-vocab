"""
Test file with intentional failures to demonstrate debugging
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, generate_sentences
from database import db, VocabularyWord, SentenceTemplate


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            _seed_test_data()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def _seed_test_data():
    """Seed test data"""
    words = [
        VocabularyWord(theme='cooking', word_type='verb', spanish_word='cocinar', english_translation='to cook'),
        VocabularyWord(theme='cooking', word_type='verb', spanish_word='hornear', english_translation='to bake'),
    ]
    for word in words:
        db.session.add(word)

    templates = [
        SentenceTemplate(theme='cooking', word_type='verb',
                        spanish_template='Me gusta {word}.',
                        english_template='I like to {word}.'),
    ]
    for template in templates:
        db.session.add(template)

    db.session.commit()


class TestFailureExamples:
    """Examples of failing tests and how to fix them"""

    def test_wrong_expectation(self, client):
        """
        FAILURE TYPE: Assertion Error - Wrong Expected Value

        This test expects the wrong number of sentences.
        We're expecting 10, but the function returns maximum 2 (based on test data).

        HOW TO FIX: Update the assertion to match actual behavior (2 sentences)
        """
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            # INTENTIONAL FAILURE: We only have 2 words in test data
            assert len(sentences) == 10, f"Expected 10 sentences but got {len(sentences)}"

    def test_wrong_type_check(self, client):
        """
        FAILURE TYPE: Type Mismatch

        This test expects a dictionary but gets a list.

        HOW TO FIX: Change expectation to list, or fix the function return type
        """
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            # INTENTIONAL FAILURE: Returns list, not dict
            assert isinstance(sentences, dict), f"Expected dict but got {type(sentences)}"

    def test_missing_key(self, client):
        """
        FAILURE TYPE: KeyError - Missing Dictionary Key

        This test tries to access a key that doesn't exist.

        HOW TO FIX: Use correct key name ('spanish' not 'spanish_text')
        """
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            if sentences:
                # INTENTIONAL FAILURE: Key is 'spanish', not 'spanish_text'
                spanish_text = sentences[0]['spanish_text']
                assert len(spanish_text) > 0

    def test_wrong_content_check(self, client):
        """
        FAILURE TYPE: Content Mismatch

        This test expects specific content that won't be there.

        HOW TO FIX: Check for actual content or make test more flexible
        """
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            if sentences:
                # INTENTIONAL FAILURE: This specific word might not appear
                assert 'freír' in sentences[0]['spanish'], "Expected 'freír' in sentence"

    def test_api_wrong_status_code(self, client):
        """
        FAILURE TYPE: HTTP Status Code Mismatch

        This test expects 404 but endpoint returns 400 for missing data.

        HOW TO FIX: Expect 400 (bad request) instead of 404 (not found)
        """
        response = client.post('/api/mark-learned',
                              json={},  # Missing word_id
                              content_type='application/json')

        # INTENTIONAL FAILURE: Returns 400 (bad request), not 404
        assert response.status_code == 404, f"Expected 404 but got {response.status_code}"


class TestPassingExamples:
    """Corrected versions of the failing tests"""

    def test_correct_sentence_count(self, client):
        """✅ FIXED: Check for actual number based on test data"""
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            # We have 2 words and 1 template in test data
            assert len(sentences) <= 2, f"Expected at most 2 sentences, got {len(sentences)}"
            assert len(sentences) > 0, "Should have at least 1 sentence"

    def test_correct_type_check(self, client):
        """✅ FIXED: Check for list, not dict"""
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            assert isinstance(sentences, list), f"Expected list but got {type(sentences)}"

    def test_correct_key_access(self, client):
        """✅ FIXED: Use correct key name"""
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            if sentences:
                # Correct key name is 'spanish'
                spanish_text = sentences[0]['spanish']
                assert len(spanish_text) > 0

    def test_flexible_content_check(self, client):
        """✅ FIXED: Check for any word, not specific one"""
        with app.app_context():
            sentences = generate_sentences('cooking', 'verb')
            if sentences:
                # Check for <mark> tag (highlights) instead of specific word
                assert '<mark>' in sentences[0]['spanish'], "Expected highlighted word"

    def test_correct_status_code(self, client):
        """✅ FIXED: Expect 400 for bad request"""
        response = client.post('/api/mark-learned',
                              json={},  # Missing word_id
                              content_type='application/json')

        # Correct: missing required field returns 400 (bad request)
        assert response.status_code == 400, f"Expected 400 but got {response.status_code}"
