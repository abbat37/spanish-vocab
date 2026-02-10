"""
LLM Service for V2
Handles all OpenAI API calls for vocabulary processing
"""
import os
import json
from typing import List, Dict
from openai import OpenAI
from flask import current_app


class LLMService:
    """Service for OpenAI API calls"""

    # Predefined theme options
    THEMES = [
        'weather',      # Weather & climate
        'food',         # Food & cooking
        'work',         # Work & business
        'travel',       # Travel & transportation
        'family',       # Family & relationships
        'emotions',     # Emotions & feelings
        'sports',       # Sports & activities
        'home',         # Home & daily life
        'health',       # Health & body
        'other'         # Other topics
    ]

    # Word type options (8 types from Phase 3 spec)
    WORD_TYPES = [
        'verb',           # Action words (cocinar, hablar)
        'noun',           # Things/people (casa, amigo)
        'adjective',      # Descriptive (frío, grande)
        'adverb',         # Manner/degree (rápidamente, muy)
        'phrase',         # Multi-word expressions (por cierto)
        'function_word',  # Grammar words (el, en, y, pero)
        'number',         # Numbers (primero, cinco, cien)
        'other'           # Everything else
    ]

    def __init__(self):
        """Initialize OpenAI client"""
        api_key = current_app.config.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not configured")

        self.client = OpenAI(api_key=api_key)
        self.model = current_app.config.get('OPENAI_MODEL', 'gpt-4o-mini')

    def process_words_bulk(self, raw_words: List[str]) -> tuple[List[Dict], str]:
        """
        Process multiple Spanish words/phrases with LLM.

        Args:
            raw_words: List of Spanish words/phrases (already cleaned)

        Returns:
            Tuple of (processed_words, error_message)
            - processed_words: List of dicts with spanish, english, word_type, themes
            - error_message: Empty string if success, error description if failure
        """
        if not raw_words:
            return [], ""

        # Build prompt
        prompt = self._build_bulk_processing_prompt(raw_words)

        try:
            # Call OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4000,
                temperature=0.3  # Low temp for consistent structured output
            )

            # Parse response
            result_text = response.choices[0].message.content
            processed_words = self._parse_llm_response(result_text)

            if not processed_words:
                error_msg = "AI couldn't translate the words. They may not be valid Spanish."
                return [], error_msg

            return processed_words, ""

        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)

            # Provide user-friendly error messages
            if "rate_limit" in error_msg.lower():
                friendly_msg = "AI service rate limit reached. Please wait a moment and try again."
            elif "authentication" in error_msg.lower() or "api_key" in error_msg.lower():
                friendly_msg = "AI service authentication error. Please contact support."
            elif "timeout" in error_msg.lower():
                friendly_msg = "AI service timed out. Please try again with fewer words."
            elif "connection" in error_msg.lower() or "network" in error_msg.lower():
                friendly_msg = "Network error connecting to AI service. Please check your connection and try again."
            else:
                friendly_msg = f"Translation service error ({error_type}). Please try again."

            print(f"LLM processing error: {error_type} - {error_msg}")
            return [], friendly_msg

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
                # Remove code fence
                parts = clean_text.split('```')
                if len(parts) >= 2:
                    clean_text = parts[1]
                    # Remove 'json' language identifier if present
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
            print(f"Response text: {response_text[:200]}")
            return []

    def _validate_word_structure(self, word: Dict) -> bool:
        """
        Validate that word has required fields and correct format.

        Modifies word dict in-place to fix invalid values.

        Returns:
            True if valid (after corrections), False if fundamentally invalid
        """
        required = ['spanish', 'english', 'word_type', 'themes']

        # Check all required fields exist
        if not all(key in word for key in required):
            return False

        # Check non-empty values
        if not word.get('spanish') or not word.get('english'):
            return False

        # Check translation isn't same as Spanish (LLM error)
        if word['spanish'].lower() == word['english'].lower():
            return False

        # Length checks
        if len(word['spanish']) > 50 or len(word['english']) > 200:
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

# Singleton-like helper function
def get_llm_service() -> LLMService:
    """Get LLM service instance"""
    return LLMService()
