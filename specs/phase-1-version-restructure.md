# Phase 1: Restructure for Version Management

**Status:** COMPLETED
**Created:** 2026-02-09
**Completed:** 2026-02-10
**Goal:** Refactor existing Flask app to support multiple versions (v1 and v2) using Blueprint namespacing

---

## Overview

This phase establishes the foundation for running multiple versions of the Spanish vocabulary app simultaneously. We'll restructure the existing codebase to isolate v1 functionality while preparing the architecture for v2.

**Learning Objectives:**
- Understand Flask Blueprint URL prefixing and namespacing
- Learn production code organization for versioned applications
- Master the "Shared Infrastructure" pattern used by Stripe, Shopify, GitHub
- Practice safe refactoring without breaking existing functionality

---

## Current State (Before Phase 1)

### Current URL Structure
```
https://spanish-vocab.duckdns.org/
├── /                           # Main practice page (main_bp)
├── /login                      # Auth routes (auth_bp)
├── /register
├── /logout
└── /api/mark-learned           # API routes (api_bp)
```

### Current Directory Structure
```
app/
├── __init__.py                 # Application factory
├── config.py                   # Configuration
├── models/                     # Database models
│   ├── user.py
│   ├── session.py
│   └── vocabulary.py
├── routes/                     # Route blueprints
│   ├── auth.py                 # auth_bp
│   ├── main.py                 # main_bp
│   └── api.py                  # api_bp
├── services/                   # Business logic
│   ├── session_service.py
│   ├── stats_service.py
│   └── sentence_service.py
├── utils/                      # Utilities
│   └── validators.py
├── templates/
│   ├── index.html
│   ├── login.html
│   └── register.html
└── static/
    ├── css/
    └── js/
```

### Current Blueprint Registration
```python
# app/__init__.py
from app.routes import auth_bp, main_bp, api_bp
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(api_bp)
```

---

## Target State (After Phase 1)

### Target URL Structure
```
https://spanish-vocab.duckdns.org/
├── /login                      # Shared auth (NO version prefix)
├── /register                   # Shared auth
├── /logout                     # Shared auth
├── /v1/                        # v1 main page (existing functionality)
├── /v1/api/mark-learned        # v1 API
└── /v2/                        # v2 routes (placeholder for Phase 2)
```

**Key Changes:**
- Auth routes remain at root level (shared across versions)
- All v1 routes get `/v1` prefix
- v2 placeholder blueprint registered (empty for now)

### Target Directory Structure
```
app/
├── __init__.py                 # MODIFIED: New blueprint registration
├── config.py                   # UNCHANGED
├── shared/                     # NEW: Shared infrastructure
│   ├── __init__.py
│   ├── extensions.py           # db, login_manager, limiter, migrate
│   └── models/                 # Shared models
│       ├── __init__.py
│       └── user.py             # Moved from app/models/user.py
├── v1/                         # NEW: v1 namespace (existing app moved here)
│   ├── __init__.py             # NEW: v1 blueprint factory
│   ├── models/                 # Moved from app/models/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   └── vocabulary.py
│   ├── routes/                 # Moved from app/routes/
│   │   ├── __init__.py
│   │   ├── main.py             # Route: /v1/
│   │   └── api.py              # Route: /v1/api/*
│   ├── services/               # Moved from app/services/
│   │   ├── session_service.py
│   │   ├── stats_service.py
│   │   └── sentence_service.py
│   ├── utils/                  # Moved from app/utils/
│   │   └── validators.py
│   └── templates/              # Moved from app/templates/
│       └── v1/
│           └── index.html
├── v2/                         # NEW: v2 namespace (placeholder)
│   ├── __init__.py             # NEW: v2 blueprint factory (empty routes)
│   └── routes/
│       └── __init__.py
├── templates/                  # Shared templates
│   ├── base.html               # NEW: Base template (optional)
│   ├── login.html              # Remains for shared auth
│   └── register.html           # Remains for shared auth
├── routes/                     # Shared routes (auth only)
│   ├── __init__.py
│   └── auth.py                 # MODIFIED: Import User from shared
└── static/                     # UNCHANGED
    ├── css/
    └── js/
```

---

## Implementation Steps

### Step 1: Create Shared Infrastructure

**Goal:** Extract shared components (database, auth, extensions) into `app/shared/`

#### 1.1 Create `app/shared/extensions.py`
```python
"""
Shared Flask Extensions
Used across all application versions
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate

# Initialize extensions (will be bound to app in create_app)
db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)
migrate = Migrate()
```

**Why:** Centralizes extension initialization so all versions use the same database, auth, and rate limiter.

#### 1.2 Move User Model to Shared
```bash
mkdir -p app/shared/models
mv app/models/user.py app/shared/models/user.py
```

**Modify `app/shared/models/user.py`:**
- Change import: `from app.models import db` → `from app.shared.extensions import db`

**Create `app/shared/models/__init__.py`:**
```python
from .user import User

__all__ = ['User']
```

**Create `app/shared/__init__.py`:**
```python
from .extensions import db, login_manager, limiter, migrate
from .models import User

__all__ = ['db', 'login_manager', 'limiter', 'migrate', 'User']
```

**Why:** User model is shared because both v1 and v2 use the same authentication system.

---

### Step 2: Create v1 Namespace

**Goal:** Move existing app code into `app/v1/` with proper imports

#### 2.1 Create Directory Structure
```bash
mkdir -p app/v1/models
mkdir -p app/v1/routes
mkdir -p app/v1/services
mkdir -p app/v1/utils
mkdir -p app/v1/templates/v1
```

#### 2.2 Move Existing Code
```bash
# Move models (except user.py which is now shared)
mv app/models/session.py app/v1/models/
mv app/models/vocabulary.py app/v1/models/

# Move routes (except auth.py which stays shared)
mv app/routes/main.py app/v1/routes/
mv app/routes/api.py app/v1/routes/

# Move services
mv app/services/*.py app/v1/services/

# Move utils
mv app/utils/*.py app/v1/utils/

# Move templates
mv app/templates/index.html app/v1/templates/v1/
```

#### 2.3 Update Imports in v1 Files

**Pattern:** Replace `app.models` → `app.shared.extensions` or `app.v1.models`

**Files to update:**
1. `app/v1/models/session.py`
2. `app/v1/models/vocabulary.py`
3. `app/v1/routes/main.py`
4. `app/v1/routes/api.py`
5. `app/v1/services/session_service.py`
6. `app/v1/services/stats_service.py`
7. `app/v1/services/sentence_service.py`

**Example - `app/v1/models/session.py`:**
```python
# BEFORE
from app.models import db

# AFTER
from app.shared.extensions import db
```

**Example - `app/v1/routes/main.py`:**
```python
# BEFORE
from app.services import SessionService, StatsService, SentenceService

# AFTER
from app.v1.services import SessionService, StatsService, SentenceService
```

#### 2.4 Create v1 Blueprint Factory

**Create `app/v1/__init__.py`:**
```python
"""
V1 Blueprint Factory
Registers all v1 routes with /v1 prefix
"""
from flask import Blueprint
from app.v1.routes import main_bp as v1_main_bp, api_bp as v1_api_bp

def create_v1_blueprint():
    """
    Create and configure v1 blueprint

    Returns:
        Blueprint: Configured v1 blueprint with all routes
    """
    # Create parent blueprint with /v1 prefix
    # Note: url_prefix will be set during registration in app/__init__.py

    # Register sub-blueprints
    # These are registered WITHOUT url_prefix here because
    # the parent /v1 prefix is applied during app registration

    return {
        'main': v1_main_bp,
        'api': v1_api_bp
    }
```

**Create `app/v1/routes/__init__.py`:**
```python
from flask import Blueprint

# Create blueprints for v1
main_bp = Blueprint('v1_main', __name__, template_folder='../templates')
api_bp = Blueprint('v1_api', __name__)

# Import routes to register them with blueprints
from . import main, api

__all__ = ['main_bp', 'api_bp']
```

**Update `app/v1/routes/main.py`:**
```python
"""
V1 Main Application Routes
Handles the main vocabulary practice interface (v1)
"""
from flask import render_template, request
from flask_login import login_required
from app.v1.routes import main_bp
from app.v1.services import SessionService, StatsService, SentenceService


@main_bp.route('/', methods=['GET', 'POST'])  # Will be /v1/
@login_required
def index():
    """V1 vocabulary practice page"""
    # ... existing code unchanged ...

    return render_template(
        'v1/index.html',  # Changed path
        sentences=sentences,
        theme=theme,
        word_type=word_type,
        stats=stats
    )
```

**Update `app/v1/routes/api.py`:**
```python
"""
V1 API Routes
Handles API endpoints for v1
"""
from flask import request, jsonify
from flask_login import login_required
from app.v1.routes import api_bp
from app.v1.services import SessionService, StatsService
from app.shared.extensions import db
from app.v1.models import WordPractice


@api_bp.route('/api/mark-learned', methods=['POST'])  # Will be /v1/api/mark-learned
@login_required
def mark_learned():
    """Toggle word learned status (v1)"""
    # ... existing code unchanged ...
    pass
```

**Create `app/v1/models/__init__.py`:**
```python
from .session import UserSession
from .vocabulary import VocabularyWord, SentenceTemplate, WordPractice

__all__ = ['UserSession', 'VocabularyWord', 'SentenceTemplate', 'WordPractice']
```

**Create `app/v1/services/__init__.py`:**
```python
from .session_service import SessionService
from .stats_service import StatsService
from .sentence_service import SentenceService

__all__ = ['SessionService', 'StatsService', 'SentenceService']
```

---

### Step 3: Create v2 Placeholder

**Goal:** Set up v2 structure with empty routes (will implement in Phase 2)

#### 3.1 Create Directory Structure
```bash
mkdir -p app/v2/routes
mkdir -p app/v2/templates/v2
```

#### 3.2 Create v2 Blueprint Factory

**Create `app/v2/__init__.py`:**
```python
"""
V2 Blueprint Factory
Registers all v2 routes with /v2 prefix
"""
from flask import Blueprint

def create_v2_blueprint():
    """
    Create and configure v2 blueprint

    Returns:
        Blueprint: Configured v2 blueprint (placeholder for Phase 2)
    """
    v2_bp = Blueprint('v2', __name__, template_folder='templates/v2')

    # Import routes (will add in Phase 2)
    from app.v2.routes import register_routes
    register_routes(v2_bp)

    return v2_bp
```

**Create `app/v2/routes/__init__.py`:**
```python
"""
V2 Routes (Placeholder)
Will be implemented in Phase 2
"""
from flask import render_template

def register_routes(bp):
    """Register v2 routes on the blueprint"""

    @bp.route('/')
    def index():
        """V2 home page (placeholder)"""
        return render_template('v2/index.html')
```

**Create `app/v2/templates/v2/index.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>V2 Coming Soon</title>
</head>
<body>
    <h1>Version 2 - Coming Soon</h1>
    <p>V2 features will be implemented in Phase 2.</p>
    <a href="/v1/">Return to V1</a>
</body>
</html>
```

---

### Step 4: Update Application Factory

**Goal:** Modify `app/__init__.py` to register versioned blueprints

**Update `app/__init__.py`:**
```python
"""
Application Factory
Creates and configures the Flask application with version support
"""
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask, redirect, url_for

from app.config import config
from app.shared import db, login_manager, limiter, migrate, User


def create_app(config_name=None):
    """
    Application factory pattern with version support.

    Args:
        config_name: Configuration to use (development, production, testing)

    Returns:
        Configured Flask application instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID for Flask-Login"""
        return User.query.get(int(user_id))

    # Initialize rate limiting
    limiter.init_app(app)
    limiter._storage_uri = app.config.get('RATELIMIT_STORAGE_URL')

    # Initialize Sentry for error tracking
    if app.config.get('SENTRY_DSN'):
        sentry_sdk.init(
            dsn=app.config['SENTRY_DSN'],
            integrations=[FlaskIntegration()],
            environment=app.config.get('SENTRY_ENVIRONMENT', 'development'),
            traces_sample_rate=0.1
        )

    # ROOT URL: Redirect to /v1/ (default version)
    @app.route('/')
    def root_redirect():
        """Redirect root URL to v1"""
        return redirect(url_for('v1_main.index'))

    # Register SHARED routes (no prefix)
    from app.routes import auth_bp
    app.register_blueprint(auth_bp)

    # Register V1 blueprints with /v1 prefix
    from app.v1 import create_v1_blueprint
    v1_blueprints = create_v1_blueprint()
    app.register_blueprint(v1_blueprints['main'], url_prefix='/v1')
    app.register_blueprint(v1_blueprints['api'], url_prefix='/v1')

    # Apply rate limiting to v1 API
    limiter.limit("10 per minute")(v1_blueprints['api'])

    # Register V2 blueprint with /v2 prefix (placeholder)
    from app.v2 import create_v2_blueprint
    v2_bp = create_v2_blueprint()
    app.register_blueprint(v2_bp, url_prefix='/v2')

    # Create database tables
    with app.app_context():
        db.create_all()

    # Add headers to prevent caching during development
    @app.after_request
    def add_header(response):
        """Add cache control headers"""
        if app.config['DEBUG']:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '-1'
        return response

    return app
```

**Key Addition:**
- Added `@app.route('/')` to redirect root URL to `/v1/`
- Import `redirect` and `url_for` from Flask

---

### Step 5: Update Shared Auth Routes

**Goal:** Update auth.py to import from shared models

**Update `app/routes/auth.py`:**
```python
"""
Authentication Routes (Shared across versions)
Handles user registration, login, and logout
"""
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.shared import db, User
from app.v1.models import UserSession  # Still using v1 session model for now

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('v1_main.index'))  # Changed: v1_main.index

    # ... rest of code unchanged except for redirects ...

    if request.method == 'POST':
        # ... validation code ...

        # SUCCESS REDIRECT:
        return redirect(url_for('v1_main.index'))  # Changed

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('v1_main.index'))  # Changed

    if request.method == 'POST':
        # ... authentication code ...

        # SUCCESS REDIRECT:
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('v1_main.index'))  # Changed

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
```

**Key Changes:**
- Import `User` from `app.shared` instead of `app.models`
- Change redirect targets: `main.index` → `v1_main.index`

---

### Step 6: Add Version Switcher to Navbar

**Goal:** Add navigation links to switch between v1 and v2

#### 6.1 Create Shared Base Template (Optional but Recommended)

**Create `app/templates/base.html`:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Spanish Vocabulary Learning{% endblock %}</title>
    <link href="{{ url_for('static', filename='css/output.css') }}" rel="stylesheet">
</head>
<body class="bg-gray-50">
    <!-- Version Switcher Navbar -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Logo/Title -->
                <div class="flex items-center">
                    <h1 class="text-xl font-bold text-gray-900">
                        Spanish Vocabulary
                        {% if request.path.startswith('/v2') %}
                        <span class="ml-2 text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">V2 Beta</span>
                        {% else %}
                        <span class="ml-2 text-sm bg-gray-100 text-gray-600 px-2 py-1 rounded">V1</span>
                        {% endif %}
                    </h1>
                </div>

                <!-- Version Switcher + Auth Links -->
                <div class="flex items-center space-x-4">
                    <!-- Version Switcher -->
                    {% if request.path.startswith('/v2') %}
                    <a href="/v1/" class="text-sm text-gray-600 hover:text-gray-900">
                        ← Back to V1
                    </a>
                    {% else %}
                    <a href="/v2/" class="text-sm bg-blue-600 text-white px-3 py-2 rounded hover:bg-blue-700">
                        Try V2 Beta →
                    </a>
                    {% endif %}

                    <!-- Auth Links -->
                    {% if current_user.is_authenticated %}
                    <span class="text-sm text-gray-600">{{ current_user.email }}</span>
                    <a href="{{ url_for('auth.logout') }}" class="text-sm text-gray-600 hover:text-gray-900">
                        Logout
                    </a>
                    {% else %}
                    <a href="{{ url_for('auth.login') }}" class="text-sm text-gray-600 hover:text-gray-900">
                        Login
                    </a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>

    <!-- Page Content -->
    <main>
        {% block content %}{% endblock %}
    </main>

    {% block scripts %}{% endblock %}
</body>
</html>
```

#### 6.2 Update V1 Template to Use Base

**Update `app/v1/templates/v1/index.html`:**

Add at the top:
```html
{% extends "base.html" %}

{% block title %}Practice - Spanish Vocabulary{% endblock %}

{% block content %}
<!-- Your existing index.html content goes here -->
<!-- Remove <html>, <head>, <body> tags - keep only the content -->
{% endblock %}
```

#### 6.3 Update V2 Placeholder Template

**Update `app/v2/templates/v2/index.html`:**
```html
{% extends "base.html" %}

{% block title %}V2 Coming Soon - Spanish Vocabulary{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto px-4 py-12 text-center">
    <h1 class="text-4xl font-bold text-gray-900 mb-4">Version 2 - Coming Soon</h1>
    <p class="text-lg text-gray-600 mb-8">
        V2 will feature context-rich vocabulary learning with AI-generated examples and practice.
    </p>
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 text-left mb-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-3">What's New in V2:</h2>
        <ul class="space-y-2 text-gray-700">
            <li>📝 <strong>Create:</strong> Build your custom word database with tags and themes</li>
            <li>🎴 <strong>Study:</strong> Flashcards with AI-generated context examples</li>
            <li>✍️ <strong>Revise:</strong> Practice with instant AI feedback</li>
        </ul>
    </div>
    <a href="/v1/" class="inline-block bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300">
        ← Return to V1
    </a>
</div>
{% endblock %}
```

**Why This Pattern:**
- Single base template = consistent navbar across all pages
- Easy to update version switcher in one place
- Tailwind CSS classes for professional look
- Current version badge (V1 vs V2 Beta)
- Auth state display (logged-in user email)

**Production Example:**
This is how GitHub shows "Try the new navigation" banner - same concept!

---

### Step 7: Update Auth Templates with Base Template

**Goal:** Make login/register pages use the base template for consistency

**Update `app/templates/login.html`:**
- Wrap existing content with `{% extends "base.html" %}` and `{% block content %}`
- This gives login/register pages the same navbar

**Update `app/templates/register.html`:**
- Same approach as login.html

**Note:** This is optional for Phase 1 but recommended for visual consistency.

---

### Step 8: Clean Up Old Directories

**Goal:** Remove empty directories from pre-refactor structure

```bash
# Remove old directories (should be empty now)
rm -rf app/models
rm -rf app/services
rm -rf app/utils

# Keep app/routes but only with auth.py
# (main.py and api.py moved to v1/)
```

**Verify `app/routes/` only contains:**
- `__init__.py`
- `auth.py`

**Update `app/routes/__init__.py`:**
```python
"""
Shared Route Blueprints
"""
from .auth import auth_bp

__all__ = ['auth_bp']
```

---

## Testing Plan

### Manual Testing Checklist

**Goal:** Verify v1 works with `/v1` prefix and auth still works

#### Test 1: Auth Flow (Shared Routes)
- [ ] Navigate to `http://localhost:8080/register`
- [ ] Register a new account
- [ ] Verify redirect to `/v1/` (not `/`)
- [ ] Log out
- [ ] Log in with same account
- [ ] Verify redirect to `/v1/`

#### Test 2: V1 Functionality
- [ ] Access `http://localhost:8080/v1/`
- [ ] Select theme and word type
- [ ] Click "Generate Sentences"
- [ ] Mark a word as learned
- [ ] Verify stats update in dashboard
- [ ] Check API endpoint: `/v1/api/mark-learned`

#### Test 3: V2 Placeholder
- [ ] Navigate to `http://localhost:8080/v2/`
- [ ] Verify placeholder page displays
- [ ] Click "Return to V1" link

#### Test 4: Root Redirect
- [ ] Navigate to `http://localhost:8080/` (root)
- [ ] Should automatically redirect to `/v1/`
- [ ] Verify you land on the v1 practice page

#### Test 5: Version Switcher
- [ ] On `/v1/` page, verify navbar shows "Try V2 Beta →" button
- [ ] Click "Try V2 Beta" button
- [ ] Verify redirect to `/v2/`
- [ ] On `/v2/` page, verify navbar shows "← Back to V1" link
- [ ] Click "Back to V1" link
- [ ] Verify redirect back to `/v1/`

#### Test 6: Database Integrity
- [ ] Run `python3 -m flask db current`
- [ ] Verify migrations are up to date
- [ ] Check that existing data is preserved:
  ```python
  from app import create_app
  from app.shared import db, User
  from app.v1.models import WordPractice

  app = create_app()
  with app.app_context():
      users = User.query.all()
      practices = WordPractice.query.all()
      print(f"Users: {len(users)}, Practices: {len(practices)}")
  ```

### Automated Testing

**Update existing tests in `tests/test_app.py`:**

```python
# Update test URLs to use /v1 prefix
def test_v1_index_requires_login(client):
    """Test that /v1/ redirects to login"""
    response = client.get('/v1/')
    assert response.status_code == 302
    assert '/login' in response.location

def test_v1_generate_sentences(client, auth_client):
    """Test v1 sentence generation"""
    response = auth_client.post('/v1/', data={
        'theme': 'cooking',
        'word_type': 'verb'
    })
    assert response.status_code == 200

def test_v2_placeholder(client):
    """Test v2 placeholder page"""
    response = client.get('/v2/')
    assert response.status_code == 200
    assert b'Coming Soon' in response.data
```

---

## Deployment Strategy

### Local Development
1. Checkout new branch: `git checkout -b phase-1-version-restructure`
2. Make changes following this spec
3. Test locally (see Testing Plan)
4. Commit changes

### CI/CD Pipeline
**No changes needed!** Existing GitHub Actions workflow will work as-is.

### Production Deployment
1. Merge to main branch
2. CI/CD automatically deploys
3. Verify in production:
   - `https://spanish-vocab.duckdns.org/v1/` works
   - `https://spanish-vocab.duckdns.org/login` works
   - `https://spanish-vocab.duckdns.org/v2/` shows placeholder

### Rollback Plan
If issues arise:
```bash
git revert <commit-hash>
git push origin main
```
CI/CD will automatically deploy the rollback.

---

## Success Criteria

Phase 1 is complete when:

- [ ] All existing v1 functionality works at `/v1/*` URLs
- [ ] Auth routes work at root level (`/login`, `/register`, `/logout`)
- [ ] V2 placeholder accessible at `/v2/`
- [ ] All tests pass
- [ ] No database data lost
- [ ] Code is organized in `app/shared/`, `app/v1/`, `app/v2/` structure
- [ ] Production deployment successful
- [ ] Documentation updated (README.md)

---

## Migration Considerations

### Database Migrations
**No migrations needed for Phase 1!**

Reason: We're only moving code, not changing database schema. All existing models remain functional.

### Breaking Changes
**Auth redirects changed:**
- Old: After login → `/`
- New: After login → `/v1/`

**Impact:** Users will be redirected to `/v1/` instead of `/`. Functionally identical.

---

## Next Phase Preview

**Phase 2 will add:**
- V2 route structure (create, study, revise)
- V2 templates (basic HTML)
- Navigation between v1 and v2
- Dashboard accessible from both versions

**Phase 3 will add:**
- V2 database models and migrations
- LLM service integration (Claude via Portkey)

---

## Design Decisions

### 1. Root URL Behavior
**Decision:** Redirect to `/v1/` automatically

Users visiting `https://spanish-vocab.duckdns.org/` will be automatically redirected to `/v1/`. This is the pattern used by most production apps (Stripe, GitHub) where the old version remains the default until you're ready to promote v2.

**Implementation:** Add root redirect in `app/__init__.py`

### 2. Version Switcher in Navbar
**Decision:** Add in Phase 1

We'll add a "Try V2 Beta" link in the navbar. This helps with testing and follows the production pattern of gradual user migration (like GitHub's "Try new navigation" approach).

**Implementation:** Update navbar in templates to include version switcher

### 3. LLM Integration (Phase 4)
**Decision:** Use Portkey SDK

We'll use Portkey's Python SDK which wraps the Claude API and provides:
- Built-in analytics and cost tracking per project
- Automatic rate limiting and retry logic
- Request/response logging
- Easy fallback to other LLM providers if needed

**Implementation:** Install `portkey-ai` package and configure in Phase 4

---

## References

**Real-world examples:**
- **Stripe API**: [stripe.com/docs/api/versioning](https://stripe.com/docs/api/versioning)
- **GitHub API**: [docs.github.com/en/rest/overview/api-versions](https://docs.github.com/en/rest/overview/api-versions)
- **Flask Blueprints**: [flask.palletsprojects.com/blueprints](https://flask.palletsprojects.com/en/2.3.x/blueprints/)

**Learning resources:**
- Flask Application Factory: [flask.palletsprojects.com/patterns/appfactories](https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/)
- Blueprint URL Prefixes: [flask.palletsprojects.com/blueprints/#url-prefix](https://flask.palletsprojects.com/en/2.3.x/blueprints/#url-prefix)

---

**End of Phase 1 Spec**
