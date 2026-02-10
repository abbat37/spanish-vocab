# Phase 4: LLM Integration & Bulk Word Entry

**Status:** Ready to implement (after Phase 3)
**Created:** 2026-02-10
**Duration:** 2-3 sessions
**Dependencies:** Phase 3 (V2 Database Schema) must be complete

---

## Overview

Phase 4 transforms the V2 word creation experience from manual entry to intelligent bulk processing. Users can paste raw word lists, and the LLM automatically translates, categorizes, and tags them - making vocabulary building effortless.

**Learning Objectives:**
- Production LLM integration with Claude via Portkey SDK
- Prompt engineering for structured data extraction
- Bulk text processing and validation
- Error handling for API failures
- Cost management and rate limiting

---

## User Workflow

### Before (Phase 2 - Manual Entry)
```
User enters ONE word at a time:
1. Type Spanish word: "cocinar"
2. Type English: "to cook"
3. Select type: "verb"
4. Select theme: "cooking"
5. Click "Add Word"
6. Repeat 100 times... 😰
```

### After (Phase 4 - Bulk Entry with LLM)
```
User pastes entire list:
1. Paste:
   Frío
   Sol
   Viento
   por cierto
   que va!

2. Click "Process Words"
3. Wait 2-3 seconds (loading state)
4. Review auto-tagged results in table
5. Make manual adjustments if needed
6. Done! ✨
```

---

## Technical Design

### Architecture

```
┌─────────────────────────────────────────────────────┐
│  Frontend (Create Page)                             │
│  - Textarea for bulk input                          │
│  - "Process Words" button                           │
│  - Loading spinner during processing                │
└─────────────────┬───────────────────────────────────┘
                  │ POST /v2/api/process-words
                  │ { "raw_text": "Frío\nSol..." }
                  ↓
┌─────────────────────────────────────────────────────┐
│  Backend (Flask Route)                              │
│  1. Parse & clean raw text                          │
│  2. Extract individual words/phrases                │
│  3. Call LLM service                                │
└─────────────────┬───────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────┐
│  LLM Service (Claude via Portkey)                   │
│  - Translate Spanish → English                      │
│  - Identify word type (verb/noun/phrase)            │
│  - Assign 1-3 relevant themes                       │
│  - Return structured JSON                           │
└─────────────────┬───────────────────────────────────┘
                  │ JSON response
                  ↓
┌─────────────────────────────────────────────────────┐
│  Backend (Flask Route)                              │
│  4. Validate LLM response                           │
│  5. Store in database (V2Word model)                │
│  6. Return processed words to frontend              │
└─────────────────┬───────────────────────────────────┘
                  │ JSON: [{ spanish, english, type, themes }]
                  ↓
┌─────────────────────────────────────────────────────┐
│  Frontend (Create Page)                             │
│  - Display table with processed words               │
│  - Allow inline editing                             │
│  - Show delete buttons                              │
└─────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Step 1: Install Portkey SDK

**Why Portkey?**
- Wraps Claude API with analytics and cost tracking
- Built-in rate limiting and retries
- Multi-LLM fallback support
- Request/response logging

**Install:**
```bash
pip install portkey-ai
```

**Add to requirements.txt:**
```
portkey-ai==1.0.0
```

---

### Step 2: Configure Environment Variables

**Add to `.env`:**
```bash
# Portkey Configuration
PORTKEY_API_KEY=your_portkey_api_key_here
PORTKEY_VIRTUAL_KEY=your_claude_virtual_key_here

# Optional: Portkey project tracking
PORTKEY_PROJECT_ID=spanish-vocab-v2
```

**Why two keys?**
- `PORTKEY_API_KEY`: Your Portkey account key
- `PORTKEY_VIRTUAL_KEY`: Virtual key that routes to Claude (configured in Portkey dashboard)

---

### Step 3: Create LLM Service

**Create `app/v2/services/llm_service.py`:**

```python
"""
LLM Service for V2
Handles all Claude API calls via Portkey SDK
"""
import os
import json
from portkey_ai import Portkey
from typing import List, Dict, Optional


class LLMService:
    """Service for Claude API calls via Portkey"""

    # Predefined theme options
    THEMES = [
        'weather',      # Weather & climate (tiempo)
        'food',         # Food & cooking (comida)
        'work',         # Work & business (trabajo)
        'travel',       # Travel & transportation (viajes)
        'family',       # Family & relationships (familia)
        'emotions',     # Emotions & feelings (emociones)
        'sports',       # Sports & activities (deportes)
        'home',         # Home & daily life (hogar)
        'health',       # Health & body (salud)
        'other'         # Other topics
    ]

    # Word type options
    WORD_TYPES = ['verb', 'noun', 'adj', 'adverb', 'phrase']

    def __init__(self):
        """Initialize Portkey client"""
        self.client = Portkey(
            api_key=os.getenv('PORTKEY_API_KEY'),
            virtual_key=os.getenv('PORTKEY_VIRTUAL_KEY')
        )

    def process_words_bulk(self, raw_words: List[str]) -> List[Dict]:
        """
        Process multiple Spanish words/phrases with LLM.

        Args:
            raw_words: List of Spanish words/phrases (already cleaned)

        Returns:
            List of dicts with structure:
            [
                {
                    'spanish': 'cocinar',
                    'english': 'to cook',
                    'word_type': 'verb',
                    'themes': ['food', 'home']
                },
                ...
            ]
        """
        if not raw_words:
            return []

        # Build prompt
        prompt = self._build_bulk_processing_prompt(raw_words)

        try:
            # Call Claude via Portkey
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="claude-sonnet-4",  # Use Sonnet for cost/speed balance
                max_tokens=4000,
                temperature=0.3  # Low temp for consistent structured output
            )

            # Parse response
            result_text = response.choices[0].message.content
            processed_words = self._parse_llm_response(result_text)

            return processed_words

        except Exception as e:
            print(f"LLM processing error: {e}")
            # Fallback: return words with minimal processing
            return self._fallback_processing(raw_words)

    def _build_bulk_processing_prompt(self, words: List[str]) -> str:
        """Build prompt for bulk word processing"""

        word_list = "\n".join([f"{i+1}. {word}" for i, word in enumerate(words)])

        prompt = f"""You are a Spanish-English vocabulary processing assistant.

For each Spanish word or phrase below, provide:
1. English translation
2. Word type: {', '.join(self.WORD_TYPES)}
3. 1-3 relevant themes from: {', '.join(self.THEMES)}

Spanish words to process:
{word_list}

Return ONLY valid JSON in this exact format (no markdown, no explanation):
[
  {{
    "spanish": "word",
    "english": "translation",
    "word_type": "type",
    "themes": ["theme1", "theme2"]
  }}
]

Rules:
- Keep original Spanish text exactly as provided (including / for gender variations)
- Provide natural English translations
- For phrases (2+ words), use word_type "phrase"
- Assign 1-3 most relevant themes (max 3)
- If unsure about theme, use "other"
- Return results in same order as input"""

        return prompt

    def _parse_llm_response(self, response_text: str) -> List[Dict]:
        """Parse LLM JSON response"""
        try:
            # Remove markdown code blocks if present
            clean_text = response_text.strip()
            if clean_text.startswith('```'):
                clean_text = clean_text.split('```')[1]
                if clean_text.startswith('json'):
                    clean_text = clean_text[4:]
                clean_text = clean_text.strip()

            # Parse JSON
            words = json.loads(clean_text)

            # Validate structure
            validated = []
            for word in words:
                if self._validate_word_structure(word):
                    validated.append(word)

            return validated

        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            return []

    def _validate_word_structure(self, word: Dict) -> bool:
        """Validate that word has required fields"""
        required = ['spanish', 'english', 'word_type', 'themes']

        if not all(key in word for key in required):
            return False

        # Validate word_type
        if word['word_type'] not in self.WORD_TYPES:
            word['word_type'] = 'other'

        # Validate themes (must be list)
        if not isinstance(word['themes'], list):
            word['themes'] = ['other']

        # Limit to 3 themes
        if len(word['themes']) > 3:
            word['themes'] = word['themes'][:3]

        # Ensure themes are valid
        word['themes'] = [t for t in word['themes'] if t in self.THEMES]
        if not word['themes']:
            word['themes'] = ['other']

        return True

    def _fallback_processing(self, raw_words: List[str]) -> List[Dict]:
        """Fallback if LLM fails - return minimal structure"""
        return [
            {
                'spanish': word,
                'english': '(translation needed)',
                'word_type': 'other',
                'themes': ['other']
            }
            for word in raw_words
        ]


# Singleton instance
llm_service = LLMService()
```

---

### Step 4: Create Text Cleaning Utility

**Create `app/v2/utils/text_processing.py`:**

```python
"""
Text Processing Utilities for V2
Handles parsing and cleaning of bulk word input
"""
import re
from typing import List


def parse_bulk_word_input(raw_text: str) -> List[str]:
    """
    Parse bulk word input into clean list of words/phrases.

    Handles:
    - Newline separation
    - Comma separation
    - Extra whitespace
    - Empty lines
    - Special characters (except '/')

    Args:
        raw_text: Raw input from textarea

    Returns:
        List of cleaned words/phrases

    Example:
        Input:
            "Frío    \\n\\nSol, Viento,,\\npor cierto\\nLejo/a"

        Output:
            ['Frío', 'Sol', 'Viento', 'por cierto', 'Lejo/a']
    """
    if not raw_text or not raw_text.strip():
        return []

    # Step 1: Split by newlines and commas
    # Replace commas with newlines for uniform processing
    text = raw_text.replace(',', '\n')

    # Split by newlines
    lines = text.split('\n')

    # Step 2: Clean each line
    cleaned_words = []
    for line in lines:
        # Strip whitespace
        word = line.strip()

        # Skip empty lines
        if not word:
            continue

        # Remove special characters EXCEPT '/' (for gender: Lejo/a)
        # Keep: letters, spaces, slash, accents
        word = re.sub(r'[^\w\s/áéíóúñü¿¡]', '', word, flags=re.IGNORECASE)

        # Remove extra spaces (but keep single spaces for phrases)
        word = ' '.join(word.split())

        # Skip if empty after cleaning
        if word:
            cleaned_words.append(word)

    # Step 3: Remove duplicates while preserving order
    seen = set()
    unique_words = []
    for word in cleaned_words:
        word_lower = word.lower()
        if word_lower not in seen:
            seen.add(word_lower)
            unique_words.append(word)

    return unique_words


def validate_word_length(word: str) -> bool:
    """
    Validate that word is reasonable length.

    Args:
        word: Word or phrase to validate

    Returns:
        True if valid length (1-50 chars)
    """
    return 1 <= len(word) <= 50


def truncate_if_needed(words: List[str], max_words: int = 50) -> List[str]:
    """
    Truncate word list if too long (cost control).

    Args:
        words: List of words
        max_words: Maximum words to process in one batch

    Returns:
        Truncated list
    """
    if len(words) > max_words:
        print(f"Warning: Truncating from {len(words)} to {max_words} words")
        return words[:max_words]
    return words
```

---

### Step 5: Create API Route for Bulk Processing

**Create `app/v2/routes/api.py`:**

```python
"""
V2 API Routes
Handles AJAX requests for word processing and management
"""
from flask import request, jsonify
from flask_login import login_required, current_user
from app.v2.routes import api_bp
from app.v2.services.llm_service import llm_service
from app.v2.utils.text_processing import parse_bulk_word_input, truncate_if_needed
from app.shared.extensions import db
from app.v2.models import V2Word


@api_bp.route('/api/process-words', methods=['POST'])
@login_required
def process_words():
    """
    Process bulk word input with LLM.

    Request:
        { "raw_text": "Frío\nSol\nViento..." }

    Response:
        {
            "success": true,
            "words": [
                {
                    "spanish": "Frío",
                    "english": "cold",
                    "word_type": "adj",
                    "themes": ["weather"]
                },
                ...
            ],
            "count": 5
        }
    """
    try:
        data = request.get_json()
        raw_text = data.get('raw_text', '')

        if not raw_text or not raw_text.strip():
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400

        # Step 1: Parse and clean input
        cleaned_words = parse_bulk_word_input(raw_text)

        if not cleaned_words:
            return jsonify({
                'success': False,
                'error': 'No valid words found after cleaning'
            }), 400

        # Step 2: Truncate if too many (cost control)
        cleaned_words = truncate_if_needed(cleaned_words, max_words=50)

        # Step 3: Process with LLM
        processed_words = llm_service.process_words_bulk(cleaned_words)

        if not processed_words:
            return jsonify({
                'success': False,
                'error': 'LLM processing failed'
            }), 500

        # Step 4: Save to database
        saved_count = 0
        for word_data in processed_words:
            # Check for duplicates (case-insensitive)
            existing = V2Word.query.filter(
                V2Word.user_id == current_user.id,
                db.func.lower(V2Word.spanish) == word_data['spanish'].lower()
            ).first()

            if existing:
                # Skip duplicates
                continue

            # Create new word
            new_word = V2Word(
                user_id=current_user.id,
                spanish=word_data['spanish'],
                english=word_data['english'],
                word_type=word_data['word_type'],
                themes=','.join(word_data['themes'])  # Store as comma-separated
            )
            db.session.add(new_word)
            saved_count += 1

        db.session.commit()

        return jsonify({
            'success': True,
            'words': processed_words,
            'count': len(processed_words),
            'saved': saved_count,
            'skipped': len(processed_words) - saved_count
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error processing words: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
```

**Register API blueprint in `app/v2/routes/__init__.py`:**
```python
# Add to imports
api_bp = Blueprint('v2_api', __name__)

# In register_routes():
def register_routes(bp):
    # ... existing registrations ...
    from .api import register_api_routes
    register_api_routes(bp)
```

---

### Step 6: Update Create Page UI

**Update `app/v2/templates/v2/create.html`:**

Replace the form section with bulk entry UI:

```html
<!-- Bulk Entry Section -->
<div class="bg-white rounded-lg shadow p-6 mb-8">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Add Words (Bulk Entry)</h2>

    <div class="space-y-4">
        <!-- Instructions -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-gray-700">
            <p class="font-medium mb-2">📝 How to use bulk entry:</p>
            <ul class="list-disc list-inside space-y-1">
                <li>Paste your Spanish words (one per line or comma-separated)</li>
                <li>No English translation needed - AI will translate automatically</li>
                <li>AI will auto-tag word type and themes</li>
                <li>You can edit results before saving</li>
            </ul>
        </div>

        <!-- Textarea for bulk input -->
        <div>
            <label for="bulkInput" class="block text-sm font-medium text-gray-700 mb-2">
                Paste your Spanish words:
            </label>
            <textarea id="bulkInput" rows="10"
                      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                      placeholder="Frío&#10;Sol&#10;Viento&#10;por cierto&#10;que va!"></textarea>
            <p class="mt-1 text-sm text-gray-500">Max 50 words per batch</p>
        </div>

        <!-- Process Button -->
        <div class="flex items-center space-x-4">
            <button id="processButton" type="button"
                    class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition disabled:opacity-50 disabled:cursor-not-allowed">
                Process Words with AI
            </button>

            <!-- Loading indicator (hidden by default) -->
            <div id="loadingIndicator" class="hidden flex items-center text-gray-600">
                <svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
            </div>
        </div>
    </div>
</div>

<!-- Results Table (hidden until processing complete) -->
<div id="resultsSection" class="bg-white rounded-lg shadow p-6 hidden">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Processed Words</h2>

    <div class="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
        <p class="text-sm text-green-800">
            ✅ <span id="processedCount">0</span> words processed successfully!
            Review below and click "Save All" to add to your vocabulary.
        </p>
    </div>

    <!-- Results table will be populated by JavaScript -->
    <div id="resultsTable" class="overflow-x-auto">
        <!-- Table populated by JS -->
    </div>

    <div class="mt-6 flex justify-between">
        <button id="clearButton" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300">
            Clear & Start Over
        </button>
        <button id="saveAllButton" class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium">
            Save All to Vocabulary
        </button>
    </div>
</div>
```

---

### Step 7: Add JavaScript for Bulk Processing

**Add to `app/v2/templates/v2/create.html` (in v2_scripts block):**

```html
{% block v2_scripts %}
<script>
const bulkInput = document.getElementById('bulkInput');
const processButton = document.getElementById('processButton');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsSection = document.getElementById('resultsSection');
const resultsTable = document.getElementById('resultsTable');
const processedCount = document.getElementById('processedCount');
const saveAllButton = document.getElementById('saveAllButton');
const clearButton = document.getElementById('clearButton');

let processedWords = [];

// Process words with LLM
processButton.addEventListener('click', async () => {
    const rawText = bulkInput.value.trim();

    if (!rawText) {
        alert('Please enter some Spanish words first!');
        return;
    }

    // Show loading state
    processButton.disabled = true;
    loadingIndicator.classList.remove('hidden');
    resultsSection.classList.add('hidden');

    try {
        const response = await fetch('/v2/api/process-words', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ raw_text: rawText })
        });

        const data = await response.json();

        if (data.success) {
            processedWords = data.words;
            displayResults(data.words);
            processedCount.textContent = data.count;
            resultsSection.classList.remove('hidden');
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to process words. Please try again.');
    } finally {
        processButton.disabled = false;
        loadingIndicator.classList.add('hidden');
    }
});

// Display results in table
function displayResults(words) {
    const tableHTML = `
        <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
                <tr>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Spanish</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">English</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Themes</th>
                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
                ${words.map((word, index) => `
                    <tr>
                        <td class="px-4 py-3 font-medium text-gray-900">${word.spanish}</td>
                        <td class="px-4 py-3 text-gray-700">${word.english}</td>
                        <td class="px-4 py-3">
                            <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">${word.word_type}</span>
                        </td>
                        <td class="px-4 py-3">
                            ${word.themes.map(theme =>
                                `<span class="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded mr-1">${theme}</span>`
                            ).join('')}
                        </td>
                        <td class="px-4 py-3">
                            <button onclick="editWord(${index})" class="text-blue-600 hover:text-blue-800 text-sm">Edit</button>
                            <button onclick="removeWord(${index})" class="text-red-600 hover:text-red-800 text-sm ml-2">Remove</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    resultsTable.innerHTML = tableHTML;
}

// Edit word (simplified for Phase 4 - full implementation in Phase 5)
function editWord(index) {
    alert('Edit functionality coming in Phase 5!');
}

// Remove word from results
function removeWord(index) {
    processedWords.splice(index, 1);
    displayResults(processedWords);
    processedCount.textContent = processedWords.length;

    if (processedWords.length === 0) {
        resultsSection.classList.add('hidden');
    }
}

// Save all words to database
saveAllButton.addEventListener('click', async () => {
    // In Phase 4, words are already saved during processing
    // This button just confirms and reloads
    alert(`${processedWords.length} words added to your vocabulary!`);
    window.location.reload();
});

// Clear and start over
clearButton.addEventListener('click', () => {
    bulkInput.value = '';
    processedWords = [];
    resultsSection.classList.add('hidden');
});
</script>
{% endblock %}
```

---

## Testing Plan

### Unit Tests

**Create `tests/test_phase4_llm.py`:**

```python
"""Tests for Phase 4 - LLM Integration and Bulk Entry"""
import pytest
from app.v2.utils.text_processing import parse_bulk_word_input


def test_parse_bulk_input_newlines():
    """Test parsing newline-separated words"""
    raw = "Frío\nSol\nViento"
    result = parse_bulk_word_input(raw)
    assert result == ['Frío', 'Sol', 'Viento']


def test_parse_bulk_input_commas():
    """Test parsing comma-separated words"""
    raw = "Frío, Sol, Viento"
    result = parse_bulk_word_input(raw)
    assert result == ['Frío', 'Sol', 'Viento']


def test_parse_bulk_input_mixed():
    """Test mixed separators"""
    raw = "Frío\nSol, Viento"
    result = parse_bulk_word_input(raw)
    assert result == ['Frío', 'Sol', 'Viento']


def test_parse_bulk_input_extra_whitespace():
    """Test handling extra whitespace"""
    raw = "  Frío    \n\n  Sol  "
    result = parse_bulk_word_input(raw)
    assert result == ['Frío', 'Sol']


def test_parse_bulk_input_special_chars():
    """Test removing special characters except /"""
    raw = "Frío--, Sol!!!, Lejo/a"
    result = parse_bulk_word_input(raw)
    assert result == ['Frío', 'Sol', 'Lejo/a']


def test_parse_bulk_input_phrases():
    """Test handling phrases with spaces"""
    raw = "por cierto\nque va"
    result = parse_bulk_word_input(raw)
    assert result == ['por cierto', 'que va']


def test_parse_bulk_input_duplicates():
    """Test removing duplicates"""
    raw = "Frío\nfrío\nFRÍO"
    result = parse_bulk_word_input(raw)
    assert len(result) == 1
    assert result[0] == 'Frío'  # Keeps first occurrence
```

### Integration Tests

**Test bulk processing endpoint:**

```python
def test_bulk_process_api_authenticated(auth_client):
    """Test bulk processing requires authentication"""
    response = auth_client.post('/v2/api/process-words',
                                json={'raw_text': 'Frío\nSol'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['words']) == 2


def test_bulk_process_api_empty_input(auth_client):
    """Test error handling for empty input"""
    response = auth_client.post('/v2/api/process-words',
                                json={'raw_text': ''})
    assert response.status_code == 400
```

---

## Success Criteria

Phase 4 is complete when:

- [ ] Portkey SDK installed and configured
- [ ] LLM service implemented with bulk processing
- [ ] Text parsing utility handles all edge cases
- [ ] API endpoint processes words and returns structured data
- [ ] Create page UI updated with bulk entry interface
- [ ] Loading states and error handling work correctly
- [ ] JavaScript displays results in table
- [ ] Words saved to database after processing
- [ ] All tests passing
- [ ] LLM costs tracked in Portkey dashboard

---

## Cost Management

**Estimated costs:**
- Claude Sonnet: ~$3 per million input tokens, $15 per million output tokens
- Processing 50 words: ~500 input tokens + 1000 output tokens = $0.015 per batch
- **Budget:** Set $10/month limit in Portkey

**Cost controls:**
- Max 50 words per batch (truncate if more)
- Rate limit: 10 requests per minute per user
- Use Sonnet (not Opus) for balance of speed/cost

---

## Next Phase Preview

**Phase 5 will add:**
- Edit word modal (inline editing from results table)
- Search functionality
- Filter by type and theme
- Delete words
- Pagination for large vocabularies
- Study/Revise filters

---

**Ready to implement Phase 4 after Phase 3 is complete! 🚀**