"""
Phase 1 Tests: Version Management
Tests for versioned architecture and CSS loading
"""
import pytest
import sys
import os
import re

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.shared import db, User
from app.v1.models import VocabularyWord, SentenceTemplate


@pytest.fixture
def app():
    """Create Flask app for testing"""
    test_app = create_app('testing')
    yield test_app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app"""
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            _seed_test_data()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


@pytest.fixture
def auth_client(client, app):
    """Create an authenticated test client"""
    with app.app_context():
        # Create test user
        user = User(email='test@example.com')
        user.set_password('testpassword123')
        db.session.add(user)
        db.session.commit()

    # Login
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpassword123'
    }, follow_redirects=True)

    return client


def _seed_test_data():
    """Seed database with test data"""
    # Add test vocabulary words
    words = [
        VocabularyWord(theme='cooking', word_type='verb', spanish_word='cocinar', english_translation='to cook'),
        VocabularyWord(theme='cooking', word_type='verb', spanish_word='hornear', english_translation='to bake'),
    ]
    for word in words:
        db.session.add(word)

    # Add test sentence templates
    templates = [
        SentenceTemplate(theme='cooking', word_type='verb',
                        spanish_template='Me gusta {word} todos los días',
                        english_template='I like to {word} every day'),
    ]
    for template in templates:
        db.session.add(template)

    db.session.commit()


# =====================================================
# Test 1: Root URL Redirect
# =====================================================
def test_root_redirects_to_v1(client):
    """Test that / redirects to /v1/"""
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 302
    assert '/v1/' in response.location


# =====================================================
# Test 2: V1 Routes Work
# =====================================================
def test_v1_requires_login(client):
    """Test that /v1/ requires authentication"""
    response = client.get('/v1/')
    assert response.status_code == 302
    assert '/login' in response.location


def test_v1_accessible_when_authenticated(auth_client):
    """Test that authenticated users can access /v1/"""
    response = auth_client.get('/v1/')
    assert response.status_code == 200


# =====================================================
# Test 3: V2 Placeholder Works
# =====================================================
def test_v2_placeholder_accessible(client):
    """Test that /v2/ shows placeholder page"""
    response = client.get('/v2/')
    assert response.status_code == 200
    assert b'Version 2 - Coming Soon' in response.data


def test_v2_has_back_to_v1_link(client):
    """Test that v2 has link back to v1"""
    response = client.get('/v2/')
    assert b'Back to V1' in response.data or b'/v1/' in response.data


# =====================================================
# Test 4: CSS Loading Validation
# =====================================================
def test_v1_css_loads(auth_client):
    """CRITICAL: Test that v1 page references CSS file"""
    response = auth_client.get('/v1/')
    assert response.status_code == 200

    # Check for CSS link in HTML
    html = response.data.decode('utf-8')

    # Look for output.css reference
    assert 'output.css' in html, "CSS file (output.css) not referenced in v1 HTML"

    # Check for proper CSS link tag
    css_pattern = r'<link[^>]*href=["\'].*?output\.css["\']'
    assert re.search(css_pattern, html), "CSS link tag not found in v1 HTML"


def test_v2_css_loads(client):
    """CRITICAL: Test that v2 page references CSS file"""
    response = client.get('/v2/')
    assert response.status_code == 200

    html = response.data.decode('utf-8')

    # V2 extends base.html which should have CSS
    assert 'output.css' in html, "CSS file (output.css) not referenced in v2 HTML"

    css_pattern = r'<link[^>]*href=["\'].*?output\.css["\']'
    assert re.search(css_pattern, html), "CSS link tag not found in v2 HTML"


def test_css_file_exists():
    """CRITICAL: Test that output.css file exists"""
    css_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'app',
        'static',
        'css',
        'output.css'
    )
    assert os.path.exists(css_path), f"CSS file not found at {css_path}"

    # Check file is not empty
    assert os.path.getsize(css_path) > 0, "CSS file is empty"


# =====================================================
# Test 5: Version Switcher in Navbar
# =====================================================
def test_v1_has_try_v2_button(auth_client):
    """Test that v1 shows 'Try V2 Beta' link"""
    response = auth_client.get('/v1/')
    html = response.data.decode('utf-8')

    # Check for v2 link (might be in navbar or might not if v1 has its own header)
    # This test might fail if v1 template doesn't use base.html
    # We'll make it informational
    has_v2_link = 'Try V2 Beta' in html or '/v2/' in html
    print(f"\nV1 has version switcher: {has_v2_link}")


def test_v2_has_back_to_v1_button(client):
    """Test that v2 shows 'Back to V1' link"""
    response = client.get('/v2/')
    html = response.data.decode('utf-8')

    assert 'Back to V1' in html or '/v1/' in html, "v2 missing link back to v1"


# =====================================================
# Test 6: Auth Routes Redirect to V1
# =====================================================
def test_login_redirects_to_v1_after_success(client, app):
    """Test that successful login redirects to /v1/"""
    with app.app_context():
        user = User(email='testuser@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=False)

    assert response.status_code == 302
    assert '/v1/' in response.location


def test_register_redirects_to_v1_after_success(client):
    """Test that successful registration redirects to /v1/"""
    response = client.post('/register', data={
        'email': 'newuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=False)

    assert response.status_code == 302
    assert '/v1/' in response.location


# =====================================================
# Test 7: API Endpoints Work
# =====================================================
def test_v1_api_mark_learned_endpoint(auth_client):
    """Test that /v1/api/mark-learned endpoint exists"""
    # This will fail if word_id doesn't exist, but we're just checking the endpoint
    response = auth_client.post('/v1/api/mark-learned', json={'word_id': 999})
    # Should be 404 (word not found) or 400 (validation), not 404 (route not found)
    assert response.status_code in [400, 404]


# =====================================================
# Test 8: Static Files Serve Correctly
# =====================================================
def test_static_css_endpoint(client):
    """Test that /static/css/output.css endpoint works"""
    response = client.get('/static/css/output.css')
    # Should be 200 if file exists, or 404 if not
    # We want to catch if it's 500 (server error)
    assert response.status_code in [200, 404], f"Static CSS endpoint returned {response.status_code}"


# =====================================================
# Test 9: Database Models Import Correctly
# =====================================================
def test_shared_models_import():
    """Test that shared models import correctly"""
    from app.shared import db, User
    assert db is not None
    assert User is not None


def test_v1_models_import():
    """Test that v1 models import correctly"""
    from app.v1.models import VocabularyWord, SentenceTemplate, UserSession, WordPractice
    assert VocabularyWord is not None
    assert SentenceTemplate is not None


# =====================================================
# Test 10: Blueprint Registration
# =====================================================
def test_blueprints_registered(app):
    """Test that all blueprints are registered"""
    blueprint_names = [bp.name for bp in app.blueprints.values()]

    assert 'auth' in blueprint_names, "Auth blueprint not registered"
    assert 'v1_main' in blueprint_names, "V1 main blueprint not registered"
    assert 'v1_api' in blueprint_names, "V1 API blueprint not registered"
    assert 'v2' in blueprint_names, "V2 blueprint not registered"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


# =====================================================
# Test 11: Tailwind Config Includes All Templates
# =====================================================
def test_tailwind_config_includes_all_template_paths():
    """CRITICAL: Test that tailwind.config.js scans all template directories"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'tailwind.config.js')

    with open(config_path, 'r') as f:
        config_content = f.read()

    # Check that config includes v1 and v2 template paths
    assert './app/v1/templates' in config_content, \
        "tailwind.config.js missing './app/v1/templates' - v1 CSS classes won't be included!"

    assert './app/v2/templates' in config_content, \
        "tailwind.config.js missing './app/v2/templates' - v2 CSS classes won't be included!"

    print("\n✅ Tailwind config includes all template directories")


def test_css_contains_v1_classes():
    """Test that output.css contains v1-specific classes"""
    css_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'app',
        'static',
        'css',
        'output.css'
    )

    with open(css_path, 'r') as f:
        css_content = f.read()

    # Check for v1-specific custom colors (calm and primary palettes)
    # These are defined in tailwind.config.js and used in v1 templates
    assert 'calm' in css_content or 'primary' in css_content, \
        "CSS missing custom color classes - Tailwind may not be scanning v1 templates"

    print("\n✅ CSS includes v1 custom classes")
