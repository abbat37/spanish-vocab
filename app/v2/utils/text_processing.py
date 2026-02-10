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
        Input: "Frío    \\n\\nSol, Viento,,\\npor cierto\\nlejo/a"
        Output: ['Frío', 'Sol', 'Viento', 'por cierto', 'lejo/a']
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

        # Remove special characters EXCEPT '/' (for gender: lejo/a)
        # Keep: letters, spaces, slash, Spanish accents
        word = re.sub(r'[^\w\s/áéíóúñüÁÉÍÓÚÑÜ¿¡]', '', word)

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
        True if valid length (2-50 chars)
    """
    return 2 <= len(word) <= 50


def truncate_if_needed(words: List[str], max_words: int = 50) -> tuple[List[str], bool]:
    """
    Truncate word list if too long (cost control).

    Args:
        words: List of words
        max_words: Maximum number of words to process

    Returns:
        (truncated_words, was_truncated)
    """
    if len(words) <= max_words:
        return words, False

    return words[:max_words], True
