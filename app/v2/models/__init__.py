"""
V2 Database Models
Isolated from V1 - new vocabulary learning system
"""
from .word import V2Word
from .example import V2GeneratedExample
from .practice import V2PracticeAttempt

__all__ = [
    'V2Word',
    'V2GeneratedExample',
    'V2PracticeAttempt'
]
