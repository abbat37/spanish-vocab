"""
Validation Utilities for V2
Deterministic validation before LLM calls
"""
import re
from typing import Tuple
from app.v2.models import V2Word


def is_reasonable_length(word: str) -> bool:
    """
    Check if word has reasonable length.

    Args:
        word: Word to check

    Returns:
        True if 2-50 characters
    """
    return 2 <= len(word.strip()) <= 50


def contains_valid_characters(word: str) -> bool:
    """
    Check if word contains only valid characters.

    Allows:
    - Letters (a-z, A-Z)
    - Spanish accents (á, é, í, ó, ú, ñ, ü, etc.)
    - Spaces (for phrases)
    - Forward slash (for gender: lejo/a)

    Rejects:
    - Numbers (0-9)
    - Special characters (@, #, $, etc.)
    - Emojis

    Args:
        word: Word to validate

    Returns:
        True if only valid characters
    """
    # Check for numbers
    if re.search(r'\d', word):
        return False

    # Check for special characters (except space and /)
    # Allow: letters, spaces, /, Spanish accents
    if not re.match(r'^[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ¿¡\s/]+$', word):
        return False

    return True


def is_likely_spanish(word: str) -> bool:
    """
    Heuristic check if word is likely Spanish.

    Checks for:
    - Spanish-specific characters (ñ, á, é, í, ó, ú, ü, ¿, ¡)
    - Common Spanish verb endings (-ar, -er, -ir)
    - Common Spanish noun endings (-ción, -dad, -mente)
    - Common English words (for rejection)

    Args:
        word: Word to check

    Returns:
        True if likely Spanish, False if likely not
    """
    word_lower = word.lower().strip()

    # Check for Spanish-specific characters
    spanish_chars = ['ñ', 'á', 'é', 'í', 'ó', 'ú', 'ü', '¿', '¡']
    if any(char in word_lower for char in spanish_chars):
        return True

    # Common English words that should be rejected
    common_english = [
        'the', 'and', 'is', 'are', 'hello', 'world', 'computer',
        'phone', 'email', 'internet', 'website', 'password',
        'you', 'your', 'this', 'that', 'with', 'from', 'they'
    ]
    if word_lower in common_english:
        return False

    # Check for common Spanish patterns
    spanish_patterns = [
        r'ar$',      # verb ending: cocinar, hablar
        r'er$',      # verb ending: comer, beber
        r'ir$',      # verb ending: vivir, escribir
        r'ción$',    # noun ending: nación, canción
        r'dad$',     # noun ending: ciudad, verdad
        r'mente$',   # adverb ending: rápidamente
        r'oso$',     # adjective: hermoso
        r'osa$',     # adjective: hermosa
        r'^de\s',    # phrase starting with 'de'
        r'^por\s',   # phrase starting with 'por'
        r'^para\s',  # phrase starting with 'para'
    ]

    for pattern in spanish_patterns:
        if re.search(pattern, word_lower):
            return True

    # Check for obvious gibberish patterns
    # 1. Repeated same letter (xxx, aaaa)
    if len(set(word_lower.replace(' ', ''))) <= 3 and len(word_lower) > 5:
        return False

    # 2. Keyboard mashing patterns (common sequences)
    gibberish_patterns = [
        r'zxc',      # keyboard row
        r'qwe',      # keyboard row
        r'asd',      # keyboard row
        r'fgh',      # keyboard row
        r'jkl',      # keyboard row
        r'xxx',      # repeated chars
        r'yyy',      # repeated chars
        r'zzz',      # repeated chars
    ]
    for pattern in gibberish_patterns:
        if pattern in word_lower:
            return False

    # 3. No vowels at all (except for very short function words)
    if len(word_lower) > 3:
        vowels = 'aeiouáéíóú'
        if not any(v in word_lower for v in vowels):
            return False

    # If no Spanish indicators found but it's a reasonable word, allow it
    # (LLM will do final validation)
    if len(word_lower) >= 3:
        return True

    return False


def is_duplicate_in_db(word: str, user_id: int) -> bool:
    """
    Check if word already exists for user (case-insensitive).

    Args:
        word: Word to check
        user_id: User ID

    Returns:
        True if duplicate exists
    """
    existing = V2Word.query.filter(
        V2Word.user_id == user_id,
        V2Word.spanish.ilike(word)
    ).first()

    return existing is not None


def validate_word_before_llm(word: str, user_id: int) -> Tuple[bool, str]:
    """
    Comprehensive validation before sending to LLM.

    Runs all deterministic checks to catch invalid inputs early.

    Args:
        word: Word to validate
        user_id: User ID for duplicate check

    Returns:
        (is_valid, error_message)
    """
    word = word.strip()

    # Empty check
    if not word:
        return False, "Word is empty"

    # Length check
    if not is_reasonable_length(word):
        return False, "Word too short or too long (must be 2-50 characters)"

    # Character validation
    if not contains_valid_characters(word):
        return False, "Contains invalid characters (numbers or special characters not allowed)"

    # Duplicate check
    if is_duplicate_in_db(word, user_id):
        return False, "Word already exists in your vocabulary"

    # Spanish language check
    if not is_likely_spanish(word):
        return False, "Does not appear to be Spanish"

    return True, ""
