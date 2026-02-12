# Phase 5: V2 Features Implementation

**Status:** Ready
**Created:** 2026-02-12
**Duration:** 3-4 sessions
**Dependencies:** Phase 4 (LLM Integration & Bulk Entry) must be complete

---

## Overview

Phase 5 brings V2 to life by implementing the three core learning features: Create (with full CRUD), Study (flashcard learning), and Revise (AI-powered practice). This phase transforms the scaffolded UI from Phase 2 into a fully functional vocabulary learning system.

**Learning Objectives:**
- Build complete CRUD operations for vocabulary management
- Implement on-demand AI generation with caching
- Create interactive flashcard study interface
- Design AI-powered feedback system for writing practice
- Add filtering and search capabilities
- Master frontend-backend integration with fetch API

---

## User Experience Goals

### Create Page
- **Full CRUD Operations:** Add, edit, delete words with inline editing
- **Search & Filter:** Find words by Spanish/English text, filter by type/theme
- **Bulk Entry:** Already implemented in Phase 4
- **Word Management:** Clean, dictionary-style card layout (already styled)

### Study Page
- **Flashcard Learning:** Show word with AI-generated example sentences
- **On-Demand Generation:** Generate examples when first viewed, cache for future
- **Progress Tracking:** Mark words as learned
- **Navigation:** Next/Previous word, random selection
- **Filters:** Study specific themes or word types

### Revise Page
- **Practice Writing:** User writes sentences using learned words
- **AI Feedback:** Detailed grammar analysis, corrections, and suggestions
- **Tip System:** Show English translation if user needs help
- **Progress Tracking:** Store practice attempts with feedback
- **Filters:** Practice specific themes or word types

---

## Architecture Decisions

### 1. AI Example Generation Strategy
**Decision:** On-demand generation with caching (from user feedback)

**Implementation:**
- Generate 3 example sentences when word is first viewed in Study page
- Store examples in `v2_generated_examples` table
- Reuse cached examples on subsequent views
- Add "Regenerate" button to create new examples if user dislikes them

**Why:**
- Lower API costs (only generate for words actually studied)
- Faster bulk word entry (no generation delay)
- Database acts as cache layer

### 2. Edit Functionality Scope
**Decision:** Full field editing (from user feedback)

**Implementation:**
- Edit modal allows changing: Spanish word, English translation, word type, themes
- Duplicate detection on Spanish word changes
- Client-side validation before submission

**Why:**
- Users can correct AI mistakes from bulk entry
- Flexibility for manual word adjustments
- Better user control over their vocabulary

### 3. AI Feedback Detail Level
**Decision:** Detailed feedback with grammar explanations (from user feedback)

**Implementation:**
- Correctness assessment (correct/partially correct/incorrect)
- Specific grammar corrections
- Vocabulary suggestions
- Native-speaker tips
- Structured JSON response from LLM

**Why:**
- Educational value (users learn from mistakes)
- Clear guidance for improvement
- Matches learning-focused product goal

### 4. Filter Implementation
**Decision:** Add filters in Phase 5 (from user feedback)

**Implementation:**
- Filter by theme (dropdown with multi-select)
- Filter by word type (dropdown)
- Filter by learned status (Study: unlearned, Revise: learned)
- Filters persist in session storage

**Why:**
- Focused learning (study cooking vocabulary before travel)
- Better UX for users with large vocabularies
- Essential feature for scaling beyond 20-30 words

---

## Implementation Steps

### Step 1: Create Page - Edit Modal

**Goal:** Allow inline editing of words with full field control

#### 1.1 Create Edit Modal Component

**Update `app/v2/templates/v2/create.html`:**

Add modal HTML before closing `</div>` of main content:

```html
<!-- Edit Modal (hidden by default) -->
<div id="edit-modal" class="hidden fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-full max-w-2xl shadow-lg rounded-lg bg-white">
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-2xl font-bold text-gray-900">Edit Word</h3>
            <button onclick="closeEditModal()" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>

        <form id="edit-form" class="space-y-4">
            <input type="hidden" id="edit-word-id">

            <!-- Spanish Word -->
            <div>
                <label for="edit-spanish" class="block text-sm font-medium text-gray-700 mb-1">
                    Spanish Word
                </label>
                <input type="text" id="edit-spanish" required
                       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
            </div>

            <!-- English Translation -->
            <div>
                <label for="edit-english" class="block text-sm font-medium text-gray-700 mb-1">
                    English Translation
                </label>
                <input type="text" id="edit-english" required
                       class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
            </div>

            <!-- Word Type -->
            <div>
                <label for="edit-word-type" class="block text-sm font-medium text-gray-700 mb-1">
                    Word Type
                </label>
                <select id="edit-word-type" required
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
                    <option value="verb">Verb</option>
                    <option value="noun">Noun</option>
                    <option value="adjective">Adjective</option>
                    <option value="adverb">Adverb</option>
                    <option value="phrase">Phrase</option>
                    <option value="function_word">Function Word</option>
                    <option value="number">Number</option>
                    <option value="other">Other</option>
                </select>
            </div>

            <!-- Themes (multi-select with checkboxes) -->
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Themes (select 1-3)
                </label>
                <div class="grid grid-cols-2 md:grid-cols-3 gap-2">
                    <label class="flex items-center space-x-2 p-2 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer">
                        <input type="checkbox" name="edit-themes" value="weather" class="form-checkbox text-primary-600">
                        <span class="text-sm">Weather</span>
                    </label>
                    <label class="flex items-center space-x-2 p-2 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer">
                        <input type="checkbox" name="edit-themes" value="food" class="form-checkbox text-primary-600">
                        <span class="text-sm">Food</span>
                    </label>
                    <label class="flex items-center space-x-2 p-2 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer">
                        <input type="checkbox" name="edit-themes" value="work" class="form-checkbox text-primary-600">
                        <span class="text-sm">Work</span>
                    </label>
                    <label class="flex items-center space-x-2 p-2 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer">
                        <input type="checkbox" name="edit-themes" value="travel" class="form-checkbox text-primary-600">
                        <span class="text-sm">Travel</span>
                    </label>
                    <label class="flex items-center space-x-2 p-2 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer">
                        <input type="checkbox" name="edit-themes" value="family" class="form-checkbox text-primary-600">
                        <span class="text-sm">Family</span>
                    </label>
                    <label class="flex items-center space-x-2 p-2 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer">
                        <input type="checkbox" name="edit-themes" value="emotions" class="form-checkbox text-primary-600">
                        <span class="text-sm">Emotions</span>
                    </label>
                    <label class="flex items-center space-x-2 p-2 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer">
                        <input type="checkbox" name="edit-themes" value="sports" class="form-checkbox text-primary-600">
                        <span class="text-sm">Sports</span>
                    </label>
                    <label class="flex items-center space-x-2 p-2 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer">
                        <input type="checkbox" name="edit-themes" value="home" class="form-checkbox text-primary-600">
                        <span class="text-sm">Home</span>
                    </label>
                    <label class="flex items-center space-x-2 p-2 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer">
                        <input type="checkbox" name="edit-themes" value="health" class="form-checkbox text-primary-600">
                        <span class="text-sm">Health</span>
                    </label>
                    <label class="flex items-center space-x-2 p-2 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer">
                        <input type="checkbox" name="edit-themes" value="other" class="form-checkbox text-primary-600">
                        <span class="text-sm">Other</span>
                    </label>
                </div>
                <p class="mt-2 text-sm text-gray-500">Select 1-3 themes</p>
            </div>

            <!-- Action Buttons -->
            <div class="flex justify-end space-x-3 pt-4">
                <button type="button" onclick="closeEditModal()"
                        class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition">
                    Cancel
                </button>
                <button type="submit"
                        class="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">
                    Save Changes
                </button>
            </div>
        </form>
    </div>
</div>
```

#### 1.2 Add Edit/Delete JavaScript

**Update JavaScript in `v2_scripts` block:**

```javascript
// Edit Modal Functions
function openEditModal(wordId, spanish, english, wordType, themes) {
    document.getElementById('edit-word-id').value = wordId;
    document.getElementById('edit-spanish').value = spanish;
    document.getElementById('edit-english').value = english;
    document.getElementById('edit-word-type').value = wordType;

    // Uncheck all themes first
    document.querySelectorAll('input[name="edit-themes"]').forEach(cb => cb.checked = false);

    // Check selected themes
    themes.forEach(theme => {
        const checkbox = document.querySelector(`input[name="edit-themes"][value="${theme}"]`);
        if (checkbox) checkbox.checked = true;
    });

    document.getElementById('edit-modal').classList.remove('hidden');
}

function closeEditModal() {
    document.getElementById('edit-modal').classList.add('hidden');
}

// Handle edit form submission
document.getElementById('edit-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const wordId = document.getElementById('edit-word-id').value;
    const spanish = document.getElementById('edit-spanish').value.trim();
    const english = document.getElementById('edit-english').value.trim();
    const wordType = document.getElementById('edit-word-type').value;

    // Get selected themes
    const themes = Array.from(document.querySelectorAll('input[name="edit-themes"]:checked'))
        .map(cb => cb.value);

    // Validate themes count
    if (themes.length === 0 || themes.length > 3) {
        alert('Please select 1-3 themes');
        return;
    }

    try {
        const response = await fetch(`/v2/api/words/${wordId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                spanish,
                english,
                word_type: wordType,
                themes
            })
        });

        const data = await response.json();

        if (data.success) {
            closeEditModal();
            window.location.reload();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to update word. Please try again.');
    }
});

// Delete Word Function
async function deleteWord(wordId, spanish) {
    if (!confirm(`Delete "${spanish}"? This cannot be undone.`)) {
        return;
    }

    try {
        const response = await fetch(`/v2/api/words/${wordId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            window.location.reload();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to delete word. Please try again.');
    }
}
```

#### 1.3 Update Word Card Buttons

**Update the Edit and Delete buttons in the word list to call the functions:**

```html
<button onclick="openEditModal({{ word.id }}, '{{ word.spanish }}', '{{ word.english }}', '{{ word.word_type }}', {{ word.themes.split(',') | tojson }})"
        class="px-5 py-2.5 text-base font-medium text-primary-600 bg-primary-50 hover:bg-primary-100 rounded-lg transition duration-200 flex items-center justify-start gap-2">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
    </svg>
    <span>Edit</span>
</button>
<button onclick="deleteWord({{ word.id }}, '{{ word.spanish }}')"
        class="px-5 py-2.5 text-base font-medium text-gray-900 bg-gray-100 hover:bg-gray-200 rounded-lg transition duration-200 flex items-center justify-start gap-2">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
    </svg>
    <span>Delete</span>
</button>
```

---

### Step 2: Create Page - Search & Filter

**Goal:** Add search box and filters for word management

#### 2.1 Add Filter UI

**Add before the word list in `create.html`:**

```html
<!-- Search and Filter Bar -->
<div class="bg-white rounded-lg shadow p-4 mb-6">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- Search Box -->
        <div class="md:col-span-2">
            <label for="search-input" class="sr-only">Search</label>
            <input type="text" id="search-input" placeholder="Search words..."
                   class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
        </div>

        <!-- Word Type Filter -->
        <div>
            <select id="filter-type" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
                <option value="">All Types</option>
                <option value="verb">Verbs</option>
                <option value="noun">Nouns</option>
                <option value="adjective">Adjectives</option>
                <option value="adverb">Adverbs</option>
                <option value="phrase">Phrases</option>
                <option value="function_word">Function Words</option>
                <option value="number">Numbers</option>
                <option value="other">Other</option>
            </select>
        </div>

        <!-- Theme Filter -->
        <div>
            <select id="filter-theme" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent">
                <option value="">All Themes</option>
                <option value="weather">Weather</option>
                <option value="food">Food</option>
                <option value="work">Work</option>
                <option value="travel">Travel</option>
                <option value="family">Family</option>
                <option value="emotions">Emotions</option>
                <option value="sports">Sports</option>
                <option value="home">Home</option>
                <option value="health">Health</option>
                <option value="other">Other</option>
            </select>
        </div>
    </div>
</div>
```

#### 2.2 Add Client-Side Filtering

**Add to JavaScript:**

```javascript
// Client-side search and filter
const searchInput = document.getElementById('search-input');
const filterType = document.getElementById('filter-type');
const filterTheme = document.getElementById('filter-theme');

function applyFilters() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedType = filterType.value;
    const selectedTheme = filterTheme.value;

    const wordCards = document.querySelectorAll('.word-card');

    wordCards.forEach(card => {
        const spanish = card.dataset.spanish.toLowerCase();
        const english = card.dataset.english.toLowerCase();
        const type = card.dataset.type;
        const themes = card.dataset.themes.split(',');

        // Check search match
        const searchMatch = !searchTerm ||
                          spanish.includes(searchTerm) ||
                          english.includes(searchTerm);

        // Check type match
        const typeMatch = !selectedType || type === selectedType;

        // Check theme match
        const themeMatch = !selectedTheme || themes.includes(selectedTheme);

        // Show/hide card
        if (searchMatch && typeMatch && themeMatch) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

searchInput.addEventListener('input', applyFilters);
filterType.addEventListener('change', applyFilters);
filterTheme.addEventListener('change', applyFilters);
```

**Update word card HTML to add data attributes:**

```html
<div class="word-card bg-white border-b border-gray-200 p-6 hover:bg-gray-50 transition"
     data-spanish="{{ word.spanish }}"
     data-english="{{ word.english }}"
     data-type="{{ word.word_type }}"
     data-themes="{{ word.themes }}">
    <!-- existing card content -->
</div>
```

---

### Step 3: Create API Routes

**Goal:** Implement backend endpoints for CRUD operations

#### 3.1 Add CRUD Routes to `app/v2/routes/api.py`

```python
@api_bp.route('/api/words/<int:word_id>', methods=['PUT'])
@login_required
def update_word(word_id):
    """
    Update a word's details.

    Request:
        {
            "spanish": "cocinar",
            "english": "to cook",
            "word_type": "verb",
            "themes": ["food", "home"]
        }
    """
    try:
        data = request.get_json()

        # Find word (ensure it belongs to current user)
        word = V2Word.query.filter_by(
            id=word_id,
            user_id=current_user.id
        ).first()

        if not word:
            return jsonify({
                'success': False,
                'error': 'Word not found'
            }), 404

        # Validate input
        spanish = data.get('spanish', '').strip()
        english = data.get('english', '').strip()
        word_type = data.get('word_type', '').strip()
        themes = data.get('themes', [])

        if not spanish or not english or not word_type:
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400

        if len(themes) == 0 or len(themes) > 3:
            return jsonify({
                'success': False,
                'error': 'Please select 1-3 themes'
            }), 400

        # Check for duplicates (if Spanish word changed)
        if word.spanish.lower() != spanish.lower():
            existing = V2Word.query.filter(
                V2Word.user_id == current_user.id,
                V2Word.id != word_id,
                db.func.lower(V2Word.spanish) == spanish.lower()
            ).first()

            if existing:
                return jsonify({
                    'success': False,
                    'error': f'Word "{spanish}" already exists'
                }), 400

        # Update word
        word.spanish = spanish
        word.english = english
        word.word_type = word_type
        word.themes = ','.join(themes)

        db.session.commit()

        return jsonify({
            'success': True,
            'word': word.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error updating word: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@api_bp.route('/api/words/<int:word_id>', methods=['DELETE'])
@login_required
def delete_word(word_id):
    """Delete a word (cascades to examples and practice attempts)."""
    try:
        # Find word (ensure it belongs to current user)
        word = V2Word.query.filter_by(
            id=word_id,
            user_id=current_user.id
        ).first()

        if not word:
            return jsonify({
                'success': False,
                'error': 'Word not found'
            }), 404

        # Delete (cascades automatically)
        db.session.delete(word)
        db.session.commit()

        return jsonify({
            'success': True
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting word: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
```

---

### Step 4: Study Page Implementation

**Goal:** Interactive flashcard learning with on-demand AI examples

#### 4.1 Update Study Route

**Update `app/v2/routes/study.py`:**

```python
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.v2.models import V2Word, V2GeneratedExample
from app.v2.services.llm_service import llm_service
from app.shared.extensions import db


def register_study_routes(bp):
    """Register study routes"""

    @bp.route('/study')
    @login_required
    def study():
        """Study page - Flashcard learning"""
        # Get filter parameters
        theme = request.args.get('theme', '')
        word_type = request.args.get('word_type', '')

        # Build query for unlearned words
        query = V2Word.query.filter_by(
            user_id=current_user.id,
            is_learned=False
        )

        # Apply filters
        if theme:
            query = query.filter(V2Word.themes.contains(theme))
        if word_type:
            query = query.filter_by(word_type=word_type)

        # Get random word
        word = query.order_by(db.func.random()).first()

        if not word:
            return render_template('v2/study.html', word=None, filters={'theme': theme, 'word_type': word_type})

        # Check if examples exist
        examples = V2GeneratedExample.query.filter_by(word_id=word.id).all()

        return render_template(
            'v2/study.html',
            word=word,
            examples=[ex.to_dict() for ex in examples],
            has_examples=len(examples) > 0,
            filters={'theme': theme, 'word_type': word_type}
        )


    @bp.route('/api/study/generate-examples/<int:word_id>', methods=['POST'])
    @login_required
    def generate_examples(word_id):
        """Generate AI examples for a word."""
        try:
            # Find word (ensure belongs to user)
            word = V2Word.query.filter_by(
                id=word_id,
                user_id=current_user.id
            ).first()

            if not word:
                return jsonify({
                    'success': False,
                    'error': 'Word not found'
                }), 404

            # Generate examples with LLM
            examples = llm_service.generate_examples(
                spanish=word.spanish,
                english=word.english,
                word_type=word.word_type,
                count=3
            )

            if not examples:
                return jsonify({
                    'success': False,
                    'error': 'Failed to generate examples'
                }), 500

            # Save to database
            for ex in examples:
                example = V2GeneratedExample(
                    word_id=word.id,
                    spanish_sentence=ex['spanish'],
                    english_translation=ex['english']
                )
                db.session.add(example)

            db.session.commit()

            return jsonify({
                'success': True,
                'examples': examples
            })

        except Exception as e:
            db.session.rollback()
            print(f"Error generating examples: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500


    @bp.route('/api/study/mark-learned/<int:word_id>', methods='POST'])
    @login_required
    def mark_learned(word_id):
        """Mark word as learned."""
        try:
            word = V2Word.query.filter_by(
                id=word_id,
                user_id=current_user.id
            ).first()

            if not word:
                return jsonify({
                    'success': False,
                    'error': 'Word not found'
                }), 404

            word.is_learned = True
            db.session.commit()

            return jsonify({'success': True})

        except Exception as e:
            db.session.rollback()
            print(f"Error marking word learned: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500
```

---

Due to length, I'll continue with the Study page template and remaining sections in my next response. Would you like me to continue with:
- Study page template
- Revise page implementation
- LLM service updates
- Testing plan
- Success criteria?
#### 4.2 Update Study Template

**Replace `app/v2/templates/v2/study.html` content:**

```html
{% extends "v2/base.html" %}

{% block title %}Study - V2{% endblock %}

{% block v2_content %}
<div class="max-w-3xl mx-auto">
    <!-- Filter Bar -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
        <h3 class="text-sm font-medium text-gray-700 mb-3">Filter Study Words</h3>
        <form method="GET" class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Theme Filter -->
            <select name="theme" onchange="this.form.submit()"
                    class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500">
                <option value="">All Themes</option>
                <option value="weather" {% if filters.theme == 'weather' %}selected{% endif %}>Weather</option>
                <option value="food" {% if filters.theme == 'food' %}selected{% endif %}>Food</option>
                <option value="work" {% if filters.theme == 'work' %}selected{% endif %}>Work</option>
                <option value="travel" {% if filters.theme == 'travel' %}selected{% endif %}>Travel</option>
                <option value="family" {% if filters.theme == 'family' %}selected{% endif %}>Family</option>
                <option value="emotions" {% if filters.theme == 'emotions' %}selected{% endif %}>Emotions</option>
                <option value="sports" {% if filters.theme == 'sports' %}selected{% endif %}>Sports</option>
                <option value="home" {% if filters.theme == 'home' %}selected{% endif %}>Home</option>
                <option value="health" {% if filters.theme == 'health' %}selected{% endif %}>Health</option>
                <option value="other" {% if filters.theme == 'other' %}selected{% endif %}>Other</option>
            </select>

            <!-- Type Filter -->
            <select name="word_type" onchange="this.form.submit()"
                    class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500">
                <option value="">All Types</option>
                <option value="verb" {% if filters.word_type == 'verb' %}selected{% endif %}>Verbs</option>
                <option value="noun" {% if filters.word_type == 'noun' %}selected{% endif %}>Nouns</option>
                <option value="adjective" {% if filters.word_type == 'adjective' %}selected{% endif %}>Adjectives</option>
                <option value="adverb" {% if filters.word_type == 'adverb' %}selected{% endif %}>Adverbs</option>
                <option value="phrase" {% if filters.word_type == 'phrase' %}selected{% endif %}>Phrases</option>
            </select>

            <!-- Clear Filters Button -->
            <a href="{{ url_for('v2.study') }}"
               class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 text-center transition">
                Clear Filters
            </a>
        </form>
    </div>

    {% if word %}
    <!-- Flashcard -->
    <div class="bg-white rounded-lg shadow-lg p-8 mb-6">
        <!-- Word Header -->
        <div class="text-center mb-6">
            <p class="text-4xl font-bold text-gray-900 mb-2">{{ word.spanish }}</p>
            <p class="text-xl text-gray-600">{{ word.english }}</p>
            <div class="mt-3 flex justify-center space-x-2">
                <span class="text-sm bg-primary-100 text-primary-800 px-3 py-1 rounded-full">{{ word.word_type.replace('_', ' ') }}</span>
                {% for theme in word.themes.split(',') %}
                <span class="text-sm bg-gray-100 text-gray-800 px-3 py-1 rounded-full">{{ theme }}</span>
                {% endfor %}
            </div>
        </div>

        <!-- Divider -->
        <div class="border-t border-gray-200 my-6"></div>

        <!-- Example Sentences Section -->
        <div id="examples-section">
            {% if has_examples %}
            <!-- Examples List -->
            <div class="space-y-4">
                <h3 class="text-lg font-semibold text-gray-900">Example Sentences:</h3>
                {% for example in examples %}
                <div class="bg-primary-50 border border-primary-200 rounded-lg p-4">
                    <p class="text-gray-800 mb-1">{{ example.spanish }}</p>
                    <p class="text-sm text-gray-600 italic">{{ example.english }}</p>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <!-- Generate Button -->
            <div class="text-center py-8">
                <p class="text-gray-600 mb-4">No examples yet for this word</p>
                <button id="generate-btn" onclick="generateExamples({{ word.id }})"
                        class="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium transition">
                    Generate Examples with AI
                </button>
                <div id="loading" class="hidden mt-4">
                    <svg class="animate-spin h-8 w-8 mx-auto text-primary-600" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <p class="text-sm text-gray-600 mt-2">Generating examples...</p>
                </div>
            </div>
            {% endif %}
        </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex justify-between items-center">
        <a href="{{ url_for('v2.study', theme=filters.theme, word_type=filters.word_type) }}"
           class="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-medium transition">
            Next Word →
        </a>

        <button onclick="markLearned({{ word.id }})"
                class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium transition">
             Mark as Learned
        </button>
    </div>

    {% else %}
    <!-- Empty State -->
    <div class="bg-white rounded-lg shadow-lg p-12 text-center">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">No words to study!</h3>
        <p class="text-gray-600 mb-6">
            {% if filters.theme or filters.word_type %}
            No unlearned words match your filters. Try clearing filters or adding more words.
            {% else %}
            You haven't added any words yet, or you've learned them all!
            {% endif %}
        </p>
        <div class="space-x-4">
            <a href="{{ url_for('v2.create') }}"
               class="inline-block px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium transition">
                Add Words
            </a>
            {% if filters.theme or filters.word_type %}
            <a href="{{ url_for('v2.study') }}"
               class="inline-block px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-medium transition">
                Clear Filters
            </a>
            {% endif %}
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}

{% block v2_scripts %}
<script>
async function generateExamples(wordId) {
    const btn = document.getElementById('generate-btn');
    const loading = document.getElementById('loading');

    btn.disabled = true;
    btn.classList.add('hidden');
    loading.classList.remove('hidden');

    try {
        const response = await fetch(`/v2/api/study/generate-examples/${wordId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            // Reload to show examples
            window.location.reload();
        } else {
            alert('Error: ' + data.error);
            btn.disabled = false;
            btn.classList.remove('hidden');
            loading.classList.add('hidden');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate examples. Please try again.');
        btn.disabled = false;
        btn.classList.remove('hidden');
        loading.classList.add('hidden');
    }
}

async function markLearned(wordId) {
    try {
        const response = await fetch(`/v2/api/study/mark-learned/${wordId}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            // Show success message and load next word
            alert('Word marked as learned!');
            window.location.reload();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to mark word as learned. Please try again.');
    }
}
</script>
{% endblock %}
```

---

### Step 5: LLM Service - Example Generation

**Goal:** Add method to generate example sentences

#### 5.1 Update `app/v2/services/llm_service.py`

Add this method to the `LLMService` class:

```python
def generate_examples(self, spanish: str, english: str, word_type: str, count: int = 3) -> List[Dict]:
    """
    Generate example sentences for a Spanish word.

    Args:
        spanish: Spanish word
        english: English translation
        word_type: Type of word (verb, noun, etc.)
        count: Number of examples to generate (default 3)

    Returns:
        List of dicts with structure:
        [
            {
                'spanish': 'Me gusta cocinar.',
                'english': 'I like to cook.'
            },
            ...
        ]
    """
    prompt = f"""Generate {count} natural Spanish example sentences using the word "{spanish}" ({english}).

Word type: {word_type}

Requirements:
- Use common, everyday contexts
- Vary sentence complexity (simple to intermediate)
- Show different uses of the word
- Each sentence should be 5-15 words long
- Include English translations

Return ONLY valid JSON (no markdown, no explanation):
[
  {{
    "spanish": "sentence in Spanish",
    "english": "sentence in English"
  }}
]"""

    try:
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini",
            max_tokens=800,
            temperature=0.7,  # Higher temp for variety
            timeout=30.0
        )

        result_text = response.choices[0].message.content

        # Parse JSON
        clean_text = result_text.strip()
        if clean_text.startswith('```'):
            clean_text = clean_text.split('```')[1]
            if clean_text.startswith('json'):
                clean_text = clean_text[4:]
            clean_text = clean_text.strip()

        examples = json.loads(clean_text)

        # Validate structure
        validated = []
        for ex in examples:
            if 'spanish' in ex and 'english' in ex:
                validated.append(ex)

        return validated[:count]  # Return exactly count examples

    except Exception as e:
        print(f"Error generating examples: {e}")
        return []
```

---

### Step 6: Revise Page Implementation

**Goal:** AI-powered practice with detailed feedback

#### 6.1 Update Revise Route

**Update `app/v2/routes/revise.py`:**

```python
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.v2.models import V2Word, V2PracticeAttempt
from app.v2.services.llm_service import llm_service
from app.shared.extensions import db


def register_revise_routes(bp):
    """Register revise routes"""

    @bp.route('/revise')
    @login_required
    def revise():
        """Revise page - Practice with feedback"""
        # Get filter parameters
        theme = request.args.get('theme', '')
        word_type = request.args.get('word_type', '')

        # Build query for learned words only
        query = V2Word.query.filter_by(
            user_id=current_user.id,
            is_learned=True
        )

        # Apply filters
        if theme:
            query = query.filter(V2Word.themes.contains(theme))
        if word_type:
            query = query.filter_by(word_type=word_type)

        # Get random word
        word = query.order_by(db.func.random()).first()

        return render_template(
            'v2/revise.html',
            word=word,
            filters={'theme': theme, 'word_type': word_type}
        )


    @bp.route('/api/revise/submit', methods=['POST'])
    @login_required
    def submit_practice():
        """Submit practice sentence for AI feedback."""
        try:
            data = request.get_json()
            word_id = data.get('word_id')
            user_sentence = data.get('sentence', '').strip()

            if not user_sentence:
                return jsonify({
                    'success': False,
                    'error': 'Please write a sentence'
                }), 400

            # Find word
            word = V2Word.query.filter_by(
                id=word_id,
                user_id=current_user.id
            ).first()

            if not word:
                return jsonify({
                    'success': False,
                    'error': 'Word not found'
                }), 404

            # Get AI feedback
            feedback = llm_service.analyze_sentence(
                user_sentence=user_sentence,
                target_word=word.spanish,
                word_english=word.english,
                word_type=word.word_type
            )

            if not feedback:
                return jsonify({
                    'success': False,
                    'error': 'Failed to generate feedback'
                }), 500

            # Save practice attempt
            attempt = V2PracticeAttempt(
                user_id=current_user.id,
                word_id=word.id,
                user_sentence=user_sentence,
                ai_feedback=feedback['feedback_text'],
                is_correct=feedback['is_correct']
            )
            db.session.add(attempt)
            db.session.commit()

            return jsonify({
                'success': True,
                'feedback': feedback
            })

        except Exception as e:
            db.session.rollback()
            print(f"Error submitting practice: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error'
            }), 500
```


#### 6.2 Add LLM Sentence Analysis Method

**Add to `LLMService` class in `llm_service.py`:**

```python
def analyze_sentence(self, user_sentence: str, target_word: str, word_english: str, word_type: str) -> Dict:
    """
    Analyze user's Spanish sentence and provide detailed feedback.

    Args:
        user_sentence: User's Spanish sentence
        target_word: The word they should be practicing
        word_english: English translation of target word
        word_type: Type of word (verb, noun, etc.)

    Returns:
        Dict with structure:
        {
            'is_correct': true/false,
            'level': 'correct' | 'partially_correct' | 'incorrect',
            'feedback_text': 'Full feedback string',
            'corrections': ['correction 1', 'correction 2'],
            'suggestions': ['suggestion 1'],
            'native_tip': 'Native speaker tip'
        }
    """
    prompt = f"""Analyze this Spanish sentence written by a learner:

**Sentence:** "{user_sentence}"

**Context:** The learner is practicing the word "{target_word}" ({word_english}, {word_type}).

Provide detailed feedback on:
1. **Correctness:** Is it grammatically correct and natural?
2. **Usage:** Did they use "{target_word}" correctly?
3. **Grammar:** Point out any grammar errors
4. **Vocabulary:** Suggest better word choices if applicable
5. **Native tip:** How would a native speaker say this?

Return ONLY valid JSON (no markdown, no explanation):
{{
  "level": "correct" or "partially_correct" or "incorrect",
  "is_correct": true or false,
  "feedback_text": "Brief summary of feedback",
  "corrections": ["specific correction 1", "specific correction 2"],
  "suggestions": ["vocabulary or structure suggestion"],
  "native_tip": "How a native speaker would say this naturally"
}}

Be encouraging and educational!"""

    try:
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-4o-mini",
            max_tokens=600,
            temperature=0.3,  # Lower temp for consistent feedback
            timeout=30.0
        )

        result_text = response.choices[0].message.content

        # Parse JSON
        clean_text = result_text.strip()
        if clean_text.startswith('```'):
            clean_text = clean_text.split('```')[1]
            if clean_text.startswith('json'):
                clean_text = clean_text[4:]
            clean_text = clean_text.strip()

        feedback = json.loads(clean_text)

        # Validate structure
        required_keys = ['level', 'is_correct', 'feedback_text']
        if not all(key in feedback for key in required_keys):
            return None

        # Ensure defaults for optional keys
        feedback.setdefault('corrections', [])
        feedback.setdefault('suggestions', [])
        feedback.setdefault('native_tip', '')

        return feedback

    except Exception as e:
        print(f"Error analyzing sentence: {e}")
        return None
```

---

### Step 7: Revise Page Template

**Create/replace `app/v2/templates/v2/revise.html`:**

```html
{% extends "v2/base.html" %}

{% block title %}Revise - V2{% endblock %}

{% block v2_content %}
<div class="max-w-3xl mx-auto">
    <!-- Filter Bar (same as Study page) -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
        <h3 class="text-sm font-medium text-gray-700 mb-3">Filter Practice Words</h3>
        <form method="GET" class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <select name="theme" onchange="this.form.submit()"
                    class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500">
                <option value="">All Themes</option>
                <option value="weather" {% if filters.theme == 'weather' %}selected{% endif %}>Weather</option>
                <option value="food" {% if filters.theme == 'food' %}selected{% endif %}>Food</option>
                <option value="work" {% if filters.theme == 'work' %}selected{% endif %}>Work</option>
                <option value="travel" {% if filters.theme == 'travel' %}selected{% endif %}>Travel</option>
                <option value="family" {% if filters.theme == 'family' %}selected{% endif %}>Family</option>
                <option value="emotions" {% if filters.theme == 'emotions' %}selected{% endif %}>Emotions</option>
                <option value="sports" {% if filters.theme == 'sports' %}selected{% endif %}>Sports</option>
                <option value="home" {% if filters.theme == 'home' %}selected{% endif %}>Home</option>
                <option value="health" {% if filters.theme == 'health' %}selected{% endif %}>Health</option>
                <option value="other" {% if filters.theme == 'other' %}selected{% endif %}>Other</option>
            </select>

            <select name="word_type" onchange="this.form.submit()"
                    class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500">
                <option value="">All Types</option>
                <option value="verb" {% if filters.word_type == 'verb' %}selected{% endif %}>Verbs</option>
                <option value="noun" {% if filters.word_type == 'noun' %}selected{% endif %}>Nouns</option>
                <option value="adjective" {% if filters.word_type == 'adjective' %}selected{% endif %}>Adjectives</option>
                <option value="adverb" {% if filters.word_type == 'adverb' %}selected{% endif %}>Adverbs</option>
                <option value="phrase" {% if filters.word_type == 'phrase' %}selected{% endif %}>Phrases</option>
            </select>

            <a href="{{ url_for('v2.revise') }}"
               class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 text-center transition">
                Clear Filters
            </a>
        </form>
    </div>

    {% if word %}
    <!-- Practice Card -->
    <div class="bg-white rounded-lg shadow-lg p-8 mb-6">
        <!-- Practice Word -->
        <div class="text-center mb-6">
            <p class="text-sm text-gray-500 mb-2">Write a sentence using:</p>
            <p class="text-3xl font-bold text-gray-900 mb-1">{{ word.spanish }}</p>
            <p id="word-translation" class="text-lg text-gray-600 hidden">({{ word.english }})</p>
            <div class="mt-3">
                <span class="text-sm bg-primary-100 text-primary-800 px-3 py-1 rounded-full">{{ word.word_type.replace('_', ' ') }}</span>
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
                      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-lg"
                      placeholder="Escribe tu oración aquí..."></textarea>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-between">
            <button id="tip-button" onclick="toggleTip()"
                    class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition">
                Show Translation
            </button>
            <button id="submit-button" onclick="submitPractice()"
                    class="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium transition">
                Check Answer
            </button>
        </div>
    </div>

    <!-- Feedback Section (hidden by default) -->
    <div id="feedback-section" class="bg-white rounded-lg shadow-lg p-8 mb-6 hidden">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">AI Feedback</h3>

        <!-- Correctness Indicator -->
        <div id="correctness" class="mb-4">
            <!-- Populated by JS -->
        </div>

        <!-- Feedback Text -->
        <div id="feedback-text" class="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
            <!-- Populated by JS -->
        </div>

        <!-- Corrections -->
        <div id="corrections" class="mb-4">
            <!-- Populated by JS -->
        </div>

        <!-- Suggestions -->
        <div id="suggestions" class="mb-4">
            <!-- Populated by JS -->
        </div>

        <!-- Native Tip -->
        <div id="native-tip" class="bg-primary-50 border border-primary-200 rounded-lg p-4 mb-4">
            <!-- Populated by JS -->
        </div>

        <!-- Next Word Button -->
        <div class="text-center">
            <a href="{{ url_for('v2.revise', theme=filters.theme, word_type=filters.word_type) }}"
               class="inline-block px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium transition">
                Next Word →
            </a>
        </div>
    </div>

    {% else %}
    <!-- Empty State -->
    <div class="bg-white rounded-lg shadow-lg p-12 text-center">
        <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">No words to practice!</h3>
        <p class="text-gray-600 mb-6">
            {% if filters.theme or filters.word_type %}
            No learned words match your filters. Try clearing filters.
            {% else %}
            You need to mark some words as "learned" in the Study page first.
            {% endif %}
        </p>
        <div class="space-x-4">
            <a href="{{ url_for('v2.study') }}"
               class="inline-block px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium transition">
                Go to Study
            </a>
            {% if filters.theme or filters.word_type %}
            <a href="{{ url_for('v2.revise') }}"
               class="inline-block px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-medium transition">
                Clear Filters
            </a>
            {% endif %}
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}

{% block v2_scripts %}
<script>
const wordId = {{ word.id if word else 'null' }};
const sentenceInput = document.getElementById('sentence');
const submitButton = document.getElementById('submit-button');
const feedbackSection = document.getElementById('feedback-section');

function toggleTip() {
    const translation = document.getElementById('word-translation');
    translation.classList.toggle('hidden');
}

async function submitPractice() {
    const sentence = sentenceInput.value.trim();

    if (!sentence) {
        alert('Please write a sentence first!');
        return;
    }

    // Show loading state
    submitButton.disabled = true;
    submitButton.textContent = 'Analyzing...';

    try {
        const response = await fetch('/v2/api/revise/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                word_id: wordId,
                sentence: sentence
            })
        });

        const data = await response.json();

        if (data.success) {
            displayFeedback(data.feedback);
        } else {
            alert('Error: ' + data.error);
            submitButton.disabled = false;
            submitButton.textContent = 'Check Answer';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to analyze sentence. Please try again.');
        submitButton.disabled = false;
        submitButton.textContent = 'Check Answer';
    }
}

function displayFeedback(feedback) {
    // Correctness indicator
    const correctnessDiv = document.getElementById('correctness');
    let icon, color, text;

    if (feedback.level === 'correct') {
        icon = '';
        color = 'text-green-600';
        text = 'Excellent!';
    } else if (feedback.level === 'partially_correct') {
        icon = '⚠️';
        color = 'text-yellow-600';
        text = 'Good effort, but...';
    } else {
        icon = '❌';
        color = 'text-red-600';
        text = 'Needs improvement';
    }

    correctnessDiv.innerHTML = `
        <div class="flex items-center ${color}">
            <span class="text-3xl mr-3">${icon}</span>
            <span class="text-xl font-semibold">${text}</span>
        </div>
    `;

    // Feedback text
    document.getElementById('feedback-text').innerHTML = `
        <p class="text-gray-800">${feedback.feedback_text}</p>
    `;

    // Corrections
    const correctionsDiv = document.getElementById('corrections');
    if (feedback.corrections && feedback.corrections.length > 0) {
        correctionsDiv.innerHTML = `
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h4 class="font-semibold text-gray-900 mb-2">Corrections:</h4>
                <ul class="list-disc list-inside space-y-1 text-gray-800">
                    ${feedback.corrections.map(c => `<li>${c}</li>`).join('')}
                </ul>
            </div>
        `;
    } else {
        correctionsDiv.innerHTML = '';
    }

    // Suggestions
    const suggestionsDiv = document.getElementById('suggestions');
    if (feedback.suggestions && feedback.suggestions.length > 0) {
        suggestionsDiv.innerHTML = `
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 class="font-semibold text-gray-900 mb-2">Suggestions:</h4>
                <ul class="list-disc list-inside space-y-1 text-gray-800">
                    ${feedback.suggestions.map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
        `;
    } else {
        suggestionsDiv.innerHTML = '';
    }

    // Native tip
    const nativeTipDiv = document.getElementById('native-tip');
    if (feedback.native_tip) {
        nativeTipDiv.innerHTML = `
            <h4 class="font-semibold text-primary-900 mb-2">Native Speaker Tip:</h4>
            <p class="text-gray-800">${feedback.native_tip}</p>
        `;
    } else {
        nativeTipDiv.classList.add('hidden');
    }

    // Show feedback section
    feedbackSection.classList.remove('hidden');

    // Disable input
    sentenceInput.disabled = true;
}
</script>
{% endblock %}
```

---

## Testing Plan

### Manual Testing Checklist

#### Create Page Tests
- [ ] Edit modal opens with correct data
- [ ] All fields editable (Spanish, English, type, themes)
- [ ] Theme validation (1-3 themes required)
- [ ] Duplicate detection works on edit
- [ ] Changes save correctly
- [ ] Delete confirmation appears
- [ ] Delete removes word (cascades to examples/attempts)
- [ ] Search filters words correctly
- [ ] Type filter works
- [ ] Theme filter works
- [ ] Filters can be combined

#### Study Page Tests
- [ ] Shows random unlearned word
- [ ] Filter by theme works
- [ ] Filter by word type works
- [ ] Empty state shows when no words match filters
- [ ] "Generate Examples" button works
- [ ] Loading state shows during generation
- [ ] Examples display after generation
- [ ] Cached examples reused on reload
- [ ] "Mark as Learned" button works
- [ ] "Next Word" loads new random word
- [ ] Filters persist in URL params

#### Revise Page Tests
- [ ] Shows random learned word only
- [ ] Filter by theme works
- [ ] Filter by word type works
- [ ] Empty state shows when no learned words
- [ ] "Show Translation" toggle works
- [ ] Sentence submission works
- [ ] Loading state during AI feedback
- [ ] Feedback displays correctly
- [ ] Different feedback levels display (correct/partial/incorrect)
- [ ] Corrections, suggestions, and native tips show
- [ ] Practice attempt saved to database
- [ ] "Next Word" loads new random word

#### API Tests
- [ ] PUT /api/words/:id updates word
- [ ] DELETE /api/words/:id removes word
- [ ] POST /api/study/generate-examples creates examples
- [ ] POST /api/study/mark-learned updates word
- [ ] POST /api/revise/submit returns feedback

---

## Success Criteria

Phase 5 is complete when:

### Create Page
- [ ] Edit modal functional with all fields editable
- [ ] Delete functionality works with confirmation
- [ ] Search box filters words in real-time
- [ ] Type and theme filters work correctly
- [ ] All CRUD operations persist to database

### Study Page
- [ ] Random unlearned word selection works
- [ ] On-demand example generation functional
- [ ] Examples cached and reused
- [ ] "Mark as Learned" updates database
- [ ] Filters work (theme, type)
- [ ] Empty states handled gracefully

### Revise Page
- [ ] Random learned word selection works
- [ ] Sentence submission sends to AI
- [ ] Detailed feedback displays correctly
- [ ] Practice attempts saved to database
- [ ] Filters work (theme, type)
- [ ] Translation tip toggle works

### LLM Integration
- [ ] Example generation produces natural sentences
- [ ] Sentence analysis provides detailed feedback
- [ ] 30s timeouts on all AI calls
- [ ] Error handling works correctly

### Database
- [ ] All CRUD operations work
- [ ] Cascade deletes function properly
- [ ] Examples stored correctly
- [ ] Practice attempts recorded

### UX/Design
- [ ] Consistent design system (primary/calm colors)
- [ ] Mobile responsive on all pages
- [ ] Loading states for async operations
- [ ] Empty states provide clear guidance
- [ ] Transitions smooth and polished

---

## Deployment Checklist

- [ ] All templates updated
- [ ] Routes registered correctly
- [ ] API endpoints tested
- [ ] LLM service methods added
- [ ] Database migrations (if any schema changes)
- [ ] Environment variables set (OpenAI API key)
- [ ] Test in local environment
- [ ] Commit with descriptive message
- [ ] Push to main branch
- [ ] Verify production deployment
- [ ] Test all features in production
- [ ] Monitor for errors in logs
- [ ] Check API costs/usage

---

## Estimated Costs

**Phase 5 LLM Usage:**
- Example generation: ~200 tokens/request × 3 examples = 600 tokens
- Sentence analysis: ~400 tokens/request for feedback
- GPT-4o-mini pricing: $0.15/1M input, $0.60/1M output

**Estimated monthly cost (active user):**
- 50 words studied (example generation): $0.03
- 100 practice attempts (sentence analysis): $0.04
- **Total per active user:** ~$0.07/month

**Budget:** $5-10/month should support 70-140 active users

---

## Future Enhancements (Post-Phase 5)

### Phase 6: Polish & Optimization
- Rate limiting per user (prevent abuse)
- Cost tracking dashboard
- Batch example generation
- Improved caching strategies
- Performance profiling
- Comprehensive test suite

### Phase 7: Production Launch
- User onboarding flow
- Feature tutorials
- Analytics integration
- Feedback mechanism
- V2 promotion strategy

---

## Key Files Summary

### New/Updated Files

**Templates:**
- `app/v2/templates/v2/create.html` - Updated with edit modal, search/filters
- `app/v2/templates/v2/study.html` - Complete flashcard implementation
- `app/v2/templates/v2/revise.html` - Complete practice implementation

**Routes:**
- `app/v2/routes/create.py` - Already exists from Phase 4
- `app/v2/routes/study.py` - Updated with filters and example generation
- `app/v2/routes/revise.py` - Updated with sentence analysis
- `app/v2/routes/api.py` - New CRUD endpoints, generation endpoints

**Services:**
- `app/v2/services/llm_service.py` - Add generate_examples() and analyze_sentence()
- `app/v2/services/word_service.py` - Already exists from Phase 3

**Models:**
- No changes (all models from Phase 3)

---

## Design System Compliance

All pages use the established design system:

**Colors:**
- Primary: Indigo (`primary-50` to `primary-900`)
- Neutral: Slate (`calm-50` to `calm-900`)
- Success: Green (for "learned" states)
- Warning: Yellow (for partial correctness)
- Error: Red (for incorrect feedback)

**Components:**
- Consistent card shadows and rounded corners
- Button styles match base template
- Form inputs use primary color focus rings
- Empty states with helpful icons and CTAs

**Typography:**
- Headers: Bold, appropriate sizing
- Body text: Gray-600 for secondary text
- Consistent spacing and line heights

---

**Phase 5 Spec Complete! Ready for implementation.** 🚀

