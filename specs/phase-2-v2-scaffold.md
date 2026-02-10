# Phase 2: Build V2 Scaffold & Route Structure

**Status:** Ready to implement
**Created:** 2026-02-10
**Duration:** 1-2 sessions
**Dependencies:** Phase 1 (Version Restructure) - COMPLETE

---

## Overview

Phase 2 builds out the foundational structure for V2's three-page learning flow: Create, Study, and Revise. We'll implement the route handlers, basic HTML templates, and navigation - but WITHOUT backend functionality or database operations yet. This is pure scaffolding to establish the UI structure.

**Learning Objectives:**
- Design multi-page user flows in Flask
- Build clean, semantic HTML templates with Tailwind CSS
- Implement navigation patterns for feature-based routes
- Practice UI/UX design for learning applications

---

## V2 Learning Flow (Target UX)

### The Three-Page Journey

```
┌─────────────────────────────────────────────────────┐
│  Dashboard (Shared)                                 │
│  - Overview of learning progress                    │
│  - Stats from both V1 and V2                        │
│  - Quick access to Create/Study/Revise              │
└─────────────────────────────────────────────────────┘
                      ↓
        ┌─────────────┴─────────────┐
        ↓                           ↓
┌───────────────┐           ┌───────────────┐
│  1. CREATE    │  →  →  →  │  2. STUDY     │
│               │           │               │
│ Add new words │           │ Flashcard     │
│ with Spanish  │           │ learning with │
│ + English     │           │ AI examples   │
│               │           │               │
│ Tag by theme  │           │ Mark learned  │
│ and type      │           │               │
└───────────────┘           └───────────────┘
                                    ↓
                            ┌───────────────┐
                            │  3. REVISE    │
                            │               │
                            │ Write Spanish │
                            │ sentences     │
                            │               │
                            │ Get AI        │
                            │ feedback      │
                            └───────────────┘
```

### User Story

> "As a learner, I want to:
> 1. **Create** my own word database with translations and tags
> 2. **Study** those words with AI-generated example sentences (flashcard style)
> 3. **Revise** by writing my own sentences and getting instant feedback"

---

## Current State (After Phase 1)

### URLs
```
/v2/                        # Placeholder "Coming Soon" page
```

### Files
```
app/v2/
├── __init__.py             # Blueprint factory with placeholder route
├── routes/__init__.py      # Single placeholder route
└── templates/v2/
    └── index.html          # "Coming Soon" message
```

---

## Target State (After Phase 2)

### URL Structure
```
/v2/                        # Dashboard (overview page)
/v2/create                  # Add/edit words
/v2/study                   # Flashcard learning
/v2/revise                  # Practice with feedback
```

### Directory Structure
```
app/v2/
├── __init__.py             # UPDATED: Blueprint factory
├── routes/
│   ├── __init__.py         # UPDATED: All route handlers
│   ├── dashboard.py        # NEW: Dashboard route
│   ├── create.py           # NEW: Create route
│   ├── study.py            # NEW: Study route
│   └── revise.py           # NEW: Revise route
└── templates/v2/
    ├── base.html           # NEW: V2 base template (inherits from app/templates/base.html)
    ├── dashboard.html      # UPDATED: Main V2 page
    ├── create.html         # NEW: Word creation page
    ├── study.html          # NEW: Flashcard study page
    └── revise.html         # NEW: Practice page
```

---

## Implementation Steps

### Step 1: Reorganize V2 Routes

**Goal:** Split routes into separate files by feature

#### 1.1 Create Route Files

Create these new files:

**`app/v2/routes/dashboard.py`**
```python
"""
V2 Dashboard Route
Shows overview of learning progress and quick links
"""
from flask import render_template
from flask_login import login_required

def register_dashboard_routes(bp):
    """Register dashboard routes"""

    @bp.route('/')
    @login_required
    def dashboard():
        """V2 Dashboard - Overview page"""
        # TODO Phase 3: Query user's word count, learned count, etc.
        stats = {
            'total_words': 0,  # Placeholder
            'learned_words': 0,
            'practice_count': 0
        }

        return render_template('v2/dashboard.html', stats=stats)
```

**`app/v2/routes/create.py`**
```python
"""
V2 Create Route
Allows users to add/edit words in their vocabulary database
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required

def register_create_routes(bp):
    """Register create routes"""

    @bp.route('/create', methods=['GET', 'POST'])
    @login_required
    def create():
        """Create/edit words page"""

        if request.method == 'POST':
            # TODO Phase 5: Handle word creation
            flash('Word creation will be implemented in Phase 5', 'info')
            return redirect(url_for('v2.create'))

        # TODO Phase 5: Load user's existing words
        words = []  # Placeholder

        return render_template('v2/create.html', words=words)
```

**`app/v2/routes/study.py`**
```python
"""
V2 Study Route
Flashcard-style learning with AI-generated examples
"""
from flask import render_template, request, jsonify
from flask_login import login_required

def register_study_routes(bp):
    """Register study routes"""

    @bp.route('/study')
    @login_required
    def study():
        """Study page - Flashcard learning"""
        # TODO Phase 5: Load a random unlearned word with examples

        # Placeholder data
        current_word = {
            'id': 1,
            'spanish': 'cocinar',
            'english': 'to cook',
            'word_type': 'verb',
            'theme': 'cooking',
            'examples': [
                'Me gusta cocinar con mi familia.',
                'Ella sabe cocinar muy bien.',
                'Voy a cocinar pasta esta noche.'
            ]
        }

        return render_template('v2/study.html', word=current_word)
```

**`app/v2/routes/revise.py`**
```python
"""
V2 Revise Route
Practice writing sentences with AI feedback
"""
from flask import render_template, request, jsonify
from flask_login import login_required

def register_revise_routes(bp):
    """Register revise routes"""

    @bp.route('/revise')
    @login_required
    def revise():
        """Revise page - Practice with feedback"""
        # TODO Phase 5: Load a random learned word to practice

        # Placeholder data
        practice_word = {
            'id': 1,
            'spanish': 'cocinar',
            'english': 'to cook',
            'word_type': 'verb',
            'theme': 'cooking'
        }

        return render_template('v2/revise.html', word=practice_word)

    @bp.route('/revise/submit', methods=['POST'])
    @login_required
    def revise_submit():
        """Handle practice sentence submission"""
        # TODO Phase 4: Send to LLM for feedback

        user_sentence = request.json.get('sentence', '')

        # Placeholder response
        return jsonify({
            'feedback': 'AI feedback will be implemented in Phase 4',
            'is_correct': True,
            'suggestions': []
        })
```

#### 1.2 Update Route Registration

**Update `app/v2/routes/__init__.py`:**
```python
"""
V2 Route Registration
Registers all v2 routes on the blueprint
"""

def register_routes(bp):
    """Register all v2 routes"""
    from .dashboard import register_dashboard_routes
    from .create import register_create_routes
    from .study import register_study_routes
    from .revise import register_revise_routes

    # Register all route modules
    register_dashboard_routes(bp)
    register_create_routes(bp)
    register_study_routes(bp)
    register_revise_routes(bp)
```

---

### Step 2: Create V2 Base Template

**Goal:** Establish consistent layout for all V2 pages

**Create `app/v2/templates/v2/base.html`:**
```html
{% extends "base.html" %}

{% block content %}
<!-- V2 Navigation Tabs -->
<div class="bg-white border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav class="flex space-x-8" aria-label="V2 Navigation">
            <!-- Dashboard Tab -->
            <a href="{{ url_for('v2.dashboard') }}"
               class="{% if request.endpoint == 'v2.dashboard' %}border-blue-500 text-blue-600{% else %}border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700{% endif %} inline-flex items-center px-1 pt-4 pb-3 border-b-2 text-sm font-medium">
                <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                Dashboard
            </a>

            <!-- Create Tab -->
            <a href="{{ url_for('v2.create') }}"
               class="{% if request.endpoint == 'v2.create' %}border-blue-500 text-blue-600{% else %}border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700{% endif %} inline-flex items-center px-1 pt-4 pb-3 border-b-2 text-sm font-medium">
                <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Create
            </a>

            <!-- Study Tab -->
            <a href="{{ url_for('v2.study') }}"
               class="{% if request.endpoint == 'v2.study' %}border-blue-500 text-blue-600{% else %}border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700{% endif %} inline-flex items-center px-1 pt-4 pb-3 border-b-2 text-sm font-medium">
                <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                Study
            </a>

            <!-- Revise Tab -->
            <a href="{{ url_for('v2.revise') }}"
               class="{% if request.endpoint == 'v2.revise' %}border-blue-500 text-blue-600{% else %}border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700{% endif %} inline-flex items-center px-1 pt-4 pb-3 border-b-2 text-sm font-medium">
                <svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Revise
            </a>
        </nav>
    </div>
</div>

<!-- Page Content -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {% block v2_content %}{% endblock %}
</div>
{% endblock %}

{% block scripts %}
    {% block v2_scripts %}{% endblock %}
{% endblock %}
```

**Why This Design:**
- Inherits from main `base.html` (gets version switcher navbar)
- Adds V2-specific tab navigation (Dashboard/Create/Study/Revise)
- Active tab highlighting with Tailwind CSS
- SVG icons for visual clarity
- Responsive design (mobile-friendly)

---

### Step 3: Build Dashboard Template

**Goal:** Create welcoming overview page with quick actions

**Update `app/v2/templates/v2/dashboard.html`:**
```html
{% extends "v2/base.html" %}

{% block title %}Dashboard - V2{% endblock %}

{% block v2_content %}
<!-- Welcome Section -->
<div class="mb-8">
    <h1 class="text-3xl font-bold text-gray-900">Welcome to V2</h1>
    <p class="mt-2 text-gray-600">
        Build your vocabulary with AI-powered learning
    </p>
</div>

<!-- Stats Cards -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
    <!-- Total Words Card -->
    <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
            <div class="flex-shrink-0 bg-blue-100 rounded-md p-3">
                <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
            </div>
            <div class="ml-5">
                <p class="text-sm font-medium text-gray-500">Total Words</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.total_words }}</p>
            </div>
        </div>
    </div>

    <!-- Learned Words Card -->
    <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
            <div class="flex-shrink-0 bg-green-100 rounded-md p-3">
                <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
            </div>
            <div class="ml-5">
                <p class="text-sm font-medium text-gray-500">Learned</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.learned_words }}</p>
            </div>
        </div>
    </div>

    <!-- Practice Count Card -->
    <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
            <div class="flex-shrink-0 bg-purple-100 rounded-md p-3">
                <svg class="h-6 w-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
            </div>
            <div class="ml-5">
                <p class="text-sm font-medium text-gray-500">Practice Sessions</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.practice_count }}</p>
            </div>
        </div>
    </div>
</div>

<!-- Quick Actions -->
<div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Create Button -->
        <a href="{{ url_for('v2.create') }}"
           class="flex items-center justify-center px-4 py-6 bg-blue-50 border-2 border-blue-200 rounded-lg hover:bg-blue-100 transition">
            <div class="text-center">
                <svg class="mx-auto h-12 w-12 text-blue-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <p class="text-lg font-medium text-blue-900">Add Words</p>
                <p class="text-sm text-blue-700">Build your database</p>
            </div>
        </a>

        <!-- Study Button -->
        <a href="{{ url_for('v2.study') }}"
           class="flex items-center justify-center px-4 py-6 bg-green-50 border-2 border-green-200 rounded-lg hover:bg-green-100 transition">
            <div class="text-center">
                <svg class="mx-auto h-12 w-12 text-green-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                <p class="text-lg font-medium text-green-900">Study</p>
                <p class="text-sm text-green-700">Learn with flashcards</p>
            </div>
        </a>

        <!-- Revise Button -->
        <a href="{{ url_for('v2.revise') }}"
           class="flex items-center justify-center px-4 py-6 bg-purple-50 border-2 border-purple-200 rounded-lg hover:bg-purple-100 transition">
            <div class="text-center">
                <svg class="mx-auto h-12 w-12 text-purple-600 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <p class="text-lg font-medium text-purple-900">Revise</p>
                <p class="text-sm text-purple-700">Practice writing</p>
            </div>
        </a>
    </div>
</div>

<!-- How V2 Works Section -->
<div class="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-3">How V2 Works</h3>
    <div class="space-y-3 text-gray-700">
        <div class="flex items-start">
            <span class="flex-shrink-0 bg-blue-600 text-white rounded-full h-6 w-6 flex items-center justify-center text-sm font-medium mr-3">1</span>
            <p><strong>Create:</strong> Add Spanish words with English translations. Tag them by type (verb, noun, adj) and theme (cooking, work, etc.)</p>
        </div>
        <div class="flex items-start">
            <span class="flex-shrink-0 bg-blue-600 text-white rounded-full h-6 w-6 flex items-center justify-center text-sm font-medium mr-3">2</span>
            <p><strong>Study:</strong> See your words in flashcard format with AI-generated example sentences. Mark words as "learned" when ready.</p>
        </div>
        <div class="flex items-start">
            <span class="flex-shrink-0 bg-blue-600 text-white rounded-full h-6 w-6 flex items-center justify-center text-sm font-medium mr-3">3</span>
            <p><strong>Revise:</strong> Practice using learned words by writing your own sentences. Get instant AI feedback and suggestions.</p>
        </div>
    </div>
</div>
{% endblock %}
```

---

### Step 4: Build Create Template

**Create `app/v2/templates/v2/create.html`:**
```html
{% extends "v2/base.html" %}

{% block title %}Create - V2{% endblock %}

{% block v2_content %}
<div class="max-w-4xl mx-auto">
    <!-- Page Header -->
    <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Create Words</h1>
        <p class="mt-1 text-gray-600">Add new vocabulary to your database</p>
    </div>

    <!-- Add Word Form -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Add New Word</h2>

        <form method="POST" class="space-y-4">
            <!-- Spanish Word -->
            <div>
                <label for="spanish" class="block text-sm font-medium text-gray-700 mb-1">
                    Spanish Word
                </label>
                <input type="text" id="spanish" name="spanish" required
                       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                       placeholder="e.g., cocinar">
            </div>

            <!-- English Translation -->
            <div>
                <label for="english" class="block text-sm font-medium text-gray-700 mb-1">
                    English Translation
                </label>
                <input type="text" id="english" name="english" required
                       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                       placeholder="e.g., to cook">
            </div>

            <!-- Word Type -->
            <div>
                <label for="word_type" class="block text-sm font-medium text-gray-700 mb-1">
                    Word Type
                </label>
                <select id="word_type" name="word_type" required
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Select type...</option>
                    <option value="verb">Verb</option>
                    <option value="noun">Noun</option>
                    <option value="adj">Adjective</option>
                    <option value="adverb">Adverb</option>
                    <option value="phrase">Phrase</option>
                </select>
            </div>

            <!-- Theme -->
            <div>
                <label for="theme" class="block text-sm font-medium text-gray-700 mb-1">
                    Theme
                </label>
                <select id="theme" name="theme" required
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <option value="">Select theme...</option>
                    <option value="cooking">Cooking</option>
                    <option value="work">Work</option>
                    <option value="sports">Sports</option>
                    <option value="restaurant">Restaurant</option>
                    <option value="travel">Travel</option>
                    <option value="family">Family</option>
                    <option value="other">Other</option>
                </select>
            </div>

            <!-- Submit Button -->
            <div class="pt-2">
                <button type="submit"
                        class="w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 font-medium transition">
                    Add Word
                </button>
            </div>
        </form>
    </div>

    <!-- Word List -->
    <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Your Words</h2>

        {% if words %}
        <div class="space-y-2">
            {% for word in words %}
            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                    <p class="font-medium text-gray-900">{{ word.spanish }}</p>
                    <p class="text-sm text-gray-600">{{ word.english }}</p>
                    <div class="mt-1 flex space-x-2">
                        <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">{{ word.word_type }}</span>
                        <span class="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded">{{ word.theme }}</span>
                    </div>
                </div>
                <div class="flex space-x-2">
                    <button class="text-blue-600 hover:text-blue-800">Edit</button>
                    <button class="text-red-600 hover:text-red-800">Delete</button>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <p class="mt-4 text-gray-600">No words yet. Add your first word above!</p>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

---

### Step 5: Build Study Template

**Create `app/v2/templates/v2/study.html`:**
```html
{% extends "v2/base.html" %}

{% block title %}Study - V2{% endblock %}

{% block v2_content %}
<div class="max-w-3xl mx-auto">
    <!-- Page Header -->
    <div class="mb-6 text-center">
        <h1 class="text-2xl font-bold text-gray-900">Study Flashcards</h1>
        <p class="mt-1 text-gray-600">Learn vocabulary with AI-generated examples</p>
    </div>

    <!-- Flashcard -->
    <div class="bg-white rounded-lg shadow-lg p-8 mb-6">
        <!-- Word Header -->
        <div class="text-center mb-6">
            <p class="text-4xl font-bold text-gray-900 mb-2">{{ word.spanish }}</p>
            <p class="text-xl text-gray-600">{{ word.english }}</p>
            <div class="mt-3 flex justify-center space-x-2">
                <span class="text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded-full">{{ word.word_type }}</span>
                <span class="text-sm bg-gray-100 text-gray-800 px-3 py-1 rounded-full">{{ word.theme }}</span>
            </div>
        </div>

        <!-- Divider -->
        <div class="border-t border-gray-200 my-6"></div>

        <!-- Example Sentences -->
        <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-900">Example Sentences:</h3>
            {% for example in word.examples %}
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p class="text-gray-800">{{ example }}</p>
            </div>
            {% endfor %}
        </div>

        <!-- Regenerate Button -->
        <div class="mt-6 text-center">
            <button class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                🔄 Regenerate Examples
            </button>
        </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex justify-between items-center">
        <button class="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-medium transition">
            ← Previous
        </button>

        <button class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium transition">
            ✓ Mark as Learned
        </button>

        <button class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition">
            Next →
        </button>
    </div>

    <!-- Progress Indicator -->
    <div class="mt-6 text-center text-sm text-gray-600">
        <p>Word 1 of X | X words remaining</p>
    </div>
</div>
{% endblock %}
```

---

### Step 6: Build Revise Template

**Create `app/v2/templates/v2/revise.html`:**
```html
{% extends "v2/base.html" %}

{% block title %}Revise - V2{% endblock %}

{% block v2_content %}
<div class="max-w-3xl mx-auto">
    <!-- Page Header -->
    <div class="mb-6 text-center">
        <h1 class="text-2xl font-bold text-gray-900">Practice Writing</h1>
        <p class="mt-1 text-gray-600">Write sentences using your learned words</p>
    </div>

    <!-- Practice Card -->
    <div class="bg-white rounded-lg shadow-lg p-8 mb-6">
        <!-- Practice Word -->
        <div class="text-center mb-6">
            <p class="text-sm text-gray-500 mb-2">Write a sentence using:</p>
            <p class="text-3xl font-bold text-gray-900 mb-1">{{ word.spanish }}</p>
            <p class="text-lg text-gray-600">({{ word.english }})</p>
            <div class="mt-3">
                <span class="text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded-full">{{ word.word_type }}</span>
            </div>
        </div>

        <!-- Divider -->
        <div class="border-t border-gray-200 my-6"></div>

        <!-- Sentence Input -->
        <div class="mb-6">
            <label for="sentence" class="block text-sm font-medium text-gray-700 mb-2">
                Your Spanish Sentence:
            </label>
            <textarea id="sentence" name="sentence" rows="4"
                      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
                      placeholder="Write your sentence here..."></textarea>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-between">
            <button id="tipButton" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition">
                💡 Show Translation
            </button>
            <button id="submitButton" class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition">
                Check Answer
            </button>
        </div>
    </div>

    <!-- Feedback Section (hidden by default) -->
    <div id="feedbackSection" class="bg-white rounded-lg shadow-lg p-8 mb-6 hidden">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">AI Feedback:</h3>

        <!-- Correctness Indicator -->
        <div id="correctnessIndicator" class="mb-4">
            <!-- Will be populated by JS -->
        </div>

        <!-- Feedback Text -->
        <div id="feedbackText" class="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
            <!-- Will be populated by JS -->
        </div>

        <!-- Suggestions -->
        <div id="suggestions" class="mb-4">
            <!-- Will be populated by JS -->
        </div>

        <!-- Next Word Button -->
        <div class="text-center">
            <button class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition">
                Next Word →
            </button>
        </div>
    </div>

    <!-- Tip Section (hidden by default) -->
    <div id="tipSection" class="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-6 hidden">
        <p class="text-sm font-medium text-gray-700 mb-2">Translation Tip:</p>
        <p class="text-gray-800">{{ word.english }}</p>
    </div>
</div>
{% endblock %}

{% block v2_scripts %}
<script>
    // Simple JavaScript for Phase 2 (will enhance in Phase 5)
    const submitButton = document.getElementById('submitButton');
    const tipButton = document.getElementById('tipButton');
    const feedbackSection = document.getElementById('feedbackSection');
    const tipSection = document.getElementById('tipSection');
    const sentenceInput = document.getElementById('sentence');

    tipButton.addEventListener('click', () => {
        tipSection.classList.toggle('hidden');
    });

    submitButton.addEventListener('click', async () => {
        const sentence = sentenceInput.value.trim();

        if (!sentence) {
            alert('Please write a sentence first!');
            return;
        }

        // TODO Phase 4: Send to backend for AI feedback
        // For now, show placeholder feedback
        document.getElementById('correctnessIndicator').innerHTML = `
            <div class="flex items-center text-green-600">
                <svg class="h-6 w-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="font-semibold">Good job!</span>
            </div>
        `;

        document.getElementById('feedbackText').textContent =
            'AI feedback will be implemented in Phase 4. Your sentence looks great!';

        feedbackSection.classList.remove('hidden');
    });
</script>
{% endblock %}
```

---

## Testing Plan

### Manual Testing Checklist

#### Test 1: Navigation Flow
- [ ] Visit `/v2/` → Should see dashboard
- [ ] Click "Create" tab → Navigate to `/v2/create`
- [ ] Click "Study" tab → Navigate to `/v2/study`
- [ ] Click "Revise" tab → Navigate to `/v2/revise`
- [ ] Click "Dashboard" tab → Return to `/v2/`
- [ ] Verify active tab highlighting works correctly

#### Test 2: Dashboard
- [ ] Dashboard shows stats (all 0 for now)
- [ ] Three quick action cards displayed
- [ ] Click each quick action card → Navigate to correct page
- [ ] "How V2 Works" section visible

#### Test 3: Create Page
- [ ] Form displays with all fields
- [ ] Submit form → Flash message appears
- [ ] "No words yet" message displayed (since no DB yet)

#### Test 4: Study Page
- [ ] Flashcard displays with placeholder word
- [ ] Spanish word, English translation, and tags visible
- [ ] Three example sentences displayed
- [ ] Buttons displayed (Previous, Mark Learned, Next)

#### Test 5: Revise Page
- [ ] Practice word displayed
- [ ] Textarea for input visible
- [ ] Click "Show Translation" → Tip section appears
- [ ] Enter sentence and click "Check Answer" → Feedback appears
- [ ] Feedback section shows placeholder message

#### Test 6: Authentication
- [ ] All V2 pages require login
- [ ] Unauthenticated access redirects to `/login`
- [ ] After login, redirect works correctly

#### Test 7: Mobile Responsiveness
- [ ] Test on mobile viewport (360px width)
- [ ] Navigation tabs stack properly
- [ ] Cards display correctly
- [ ] Forms are usable

#### Test 8: Version Switching
- [ ] From V2, click "Back to V1" in navbar → Navigate to `/v1/`
- [ ] From V1, click "Try V2 Beta" → Navigate to `/v2/`

---

## Success Criteria

Phase 2 is complete when:

- [ ] All four V2 pages accessible (`/v2/`, `/v2/create`, `/v2/study`, `/v2/revise`)
- [ ] Navigation between pages works smoothly
- [ ] Active tab highlighting works correctly
- [ ] All templates use consistent styling (Tailwind CSS)
- [ ] Pages display placeholder data correctly
- [ ] All pages require authentication
- [ ] Mobile responsive design works
- [ ] No console errors in browser
- [ ] Version switcher works (V1 ↔ V2)
- [ ] Code is clean and follows project standards

---

## What's NOT in Phase 2

**Phase 2 is UI scaffolding only. These features come later:**

- ❌ Database operations (Phase 3)
- ❌ Word creation/editing (Phase 5)
- ❌ LLM integration (Phase 4)
- ❌ AI-generated examples (Phase 4)
- ❌ AI feedback (Phase 4)
- ❌ Real flashcard logic (Phase 5)
- ❌ Progress tracking (Phase 5)
- ❌ Mark as learned functionality (Phase 5)

---

## Design Decisions

### 1. Tab Navigation Pattern
**Decision:** Use horizontal tabs for V2 pages

**Why:**
- Clear visual hierarchy (Dashboard → Create → Study → Revise)
- Common pattern in learning apps (Duolingo, Anki)
- Easy to understand progression

**Implementation:** Tailwind CSS with active state styling

### 2. Placeholder Data in Templates
**Decision:** Show realistic placeholder content

**Why:**
- Helps visualize final product
- Makes testing easier
- Provides clear UX direction

**Example:** Study page shows 3 example sentences even though DB doesn't exist yet

### 3. Flash Messages for Form Submissions
**Decision:** Show "coming in Phase X" messages

**Why:**
- Confirms user actions are registered
- Sets expectations for future functionality
- Helps with testing (know form submission works)

---

## Deployment Strategy

### Local Development
1. Create branch: `git checkout -b phase-2-v2-scaffold`
2. Implement changes following this spec
3. Test locally using checklist
4. Commit: `git commit -m "feat: Implement Phase 2 - V2 Scaffold"`

### Production Deployment
1. Merge to main: `git push origin main`
2. CI/CD deploys automatically
3. Verify in production:
   - `https://spanish-vocab.duckdns.org/v2/` accessible
   - All navigation works
   - No errors in logs

---

## Next Phase Preview

**Phase 3 will add:**
- Database schema for V2
- Models: `V2Word`, `V2LearnedWord`, `V2Example`, `V2PracticeAttempt`
- Migrations to create new tables
- Database relationships

**Phase 4 will add:**
- LLM service integration (Claude via Portkey)
- Sentence generation
- Feedback generation
- Error handling for API calls

---

## Learning Objectives Recap

By completing Phase 2, you'll have learned:
- ✅ Organizing routes by feature (not by type)
- ✅ Building multi-page user flows
- ✅ Template inheritance patterns
- ✅ Navigation UX design
- ✅ Prototyping with placeholder data
- ✅ Mobile-first responsive design

---

## Estimated Time

**1-2 development sessions:**
- Session 1 (2-3 hours): Routes + Templates
- Session 2 (1-2 hours): Testing + Polish

---

**Ready to start Phase 2? Let's build the V2 scaffold! 🚀**