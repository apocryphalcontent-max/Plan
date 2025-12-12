#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Full 73-Book Verse Population System
Comprehensive population of all verses across the Orthodox Canon.

This module provides:
- Systematic population of all 73 canonical books
- Offline-first verse text retrieval with API fallback
- Progress tracking and resumption capabilities
- Book-level and canon-wide population reports
"""

import sys
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config, CANONICAL_ORDER
from scripts.database import get_db, DatabaseManager, QueryError

logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class PopulationError(Exception):
    """Base exception for population operations."""
    pass


class BookNotFoundError(PopulationError):
    """Raised when a canonical book is not found."""
    pass


# ============================================================================
# POPULATION STATISTICS
# ============================================================================

@dataclass
class PopulationStats:
    """Statistics for verse population operations."""
    total_books: int = 0
    populated_books: int = 0
    total_verses: int = 0
    verses_with_text: int = 0
    verses_populated: int = 0
    skipped: int = 0
    errors: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    
    @property
    def completion_percentage(self) -> float:
        """Calculate overall completion percentage."""
        if self.total_verses == 0:
            return 0.0
        return (self.verses_with_text / self.total_verses) * 100
    
    @property
    def book_completion_percentage(self) -> float:
        """Calculate book completion percentage."""
        if self.total_books == 0:
            return 0.0
        return (self.populated_books / self.total_books) * 100
    
    @property
    def elapsed_seconds(self) -> float:
        """Calculate elapsed time in seconds."""
        return (datetime.now() - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'total_books': self.total_books,
            'populated_books': self.populated_books,
            'total_verses': self.total_verses,
            'verses_with_text': self.verses_with_text,
            'verses_populated': self.verses_populated,
            'skipped': self.skipped,
            'errors': self.errors,
            'completion_percentage': round(self.completion_percentage, 2),
            'book_completion_percentage': round(self.book_completion_percentage, 2),
            'elapsed_seconds': round(self.elapsed_seconds, 2)
        }


@dataclass
class BookStats:
    """Statistics for a single book population."""
    book_id: int
    book_name: str
    total_chapters: int
    total_verses: int
    verses_with_text: int = 0
    verses_populated: int = 0
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage for this book."""
        if self.total_verses == 0:
            return 0.0
        return (self.verses_with_text / self.total_verses) * 100
    
    @property
    def is_complete(self) -> bool:
        """Check if book is fully populated."""
        return self.verses_with_text >= self.total_verses


# ============================================================================
# VERSE STRUCTURE DATA
# ============================================================================

# Verse counts per chapter for each book (Orthodox Canon - 73 books)
# Format: book_name: {chapter: verse_count}
# This data ensures we can create verse records for all canonical verses

VERSE_STRUCTURE: Dict[str, Dict[int, int]] = {
    # Pentateuch
    'Genesis': {
        1: 31, 2: 25, 3: 24, 4: 26, 5: 32, 6: 22, 7: 24, 8: 22, 9: 29, 10: 32,
        11: 32, 12: 20, 13: 18, 14: 24, 15: 21, 16: 16, 17: 27, 18: 33, 19: 38, 20: 18,
        21: 34, 22: 24, 23: 20, 24: 67, 25: 34, 26: 35, 27: 46, 28: 22, 29: 35, 30: 43,
        31: 55, 32: 32, 33: 20, 34: 31, 35: 29, 36: 43, 37: 36, 38: 30, 39: 23, 40: 23,
        41: 57, 42: 38, 43: 34, 44: 34, 45: 28, 46: 34, 47: 31, 48: 22, 49: 33, 50: 26
    },
    'Exodus': {
        1: 22, 2: 25, 3: 22, 4: 31, 5: 23, 6: 30, 7: 25, 8: 32, 9: 35, 10: 29,
        11: 10, 12: 51, 13: 22, 14: 31, 15: 27, 16: 36, 17: 16, 18: 27, 19: 25, 20: 26,
        21: 36, 22: 31, 23: 33, 24: 18, 25: 40, 26: 37, 27: 21, 28: 43, 29: 46, 30: 38,
        31: 18, 32: 35, 33: 23, 34: 35, 35: 35, 36: 38, 37: 29, 38: 31, 39: 43, 40: 38
    },
    'Leviticus': {
        1: 17, 2: 16, 3: 17, 4: 35, 5: 19, 6: 30, 7: 38, 8: 36, 9: 24, 10: 20,
        11: 47, 12: 8, 13: 59, 14: 57, 15: 33, 16: 34, 17: 16, 18: 30, 19: 37, 20: 27,
        21: 24, 22: 33, 23: 44, 24: 23, 25: 55, 26: 46, 27: 34
    },
    'Numbers': {
        1: 54, 2: 34, 3: 51, 4: 49, 5: 31, 6: 27, 7: 89, 8: 26, 9: 23, 10: 36,
        11: 35, 12: 16, 13: 33, 14: 45, 15: 41, 16: 50, 17: 13, 18: 32, 19: 22, 20: 29,
        21: 35, 22: 41, 23: 30, 24: 25, 25: 18, 26: 65, 27: 23, 28: 31, 29: 40, 30: 16,
        31: 54, 32: 42, 33: 56, 34: 29, 35: 34, 36: 13
    },
    'Deuteronomy': {
        1: 46, 2: 37, 3: 29, 4: 49, 5: 33, 6: 25, 7: 26, 8: 20, 9: 29, 10: 22,
        11: 32, 12: 32, 13: 18, 14: 29, 15: 23, 16: 22, 17: 20, 18: 22, 19: 21, 20: 20,
        21: 23, 22: 30, 23: 25, 24: 22, 25: 19, 26: 19, 27: 26, 28: 68, 29: 29, 30: 20,
        31: 30, 32: 52, 33: 29, 34: 12
    },
    # Historical Books
    'Joshua': {
        1: 18, 2: 24, 3: 17, 4: 24, 5: 15, 6: 27, 7: 26, 8: 35, 9: 27, 10: 43,
        11: 23, 12: 24, 13: 33, 14: 15, 15: 63, 16: 10, 17: 18, 18: 28, 19: 51, 20: 9,
        21: 45, 22: 34, 23: 16, 24: 33
    },
    'Judges': {
        1: 36, 2: 23, 3: 31, 4: 24, 5: 31, 6: 40, 7: 25, 8: 35, 9: 57, 10: 18,
        11: 40, 12: 15, 13: 25, 14: 20, 15: 20, 16: 31, 17: 13, 18: 31, 19: 30, 20: 48, 21: 25
    },
    'Ruth': {1: 22, 2: 23, 3: 18, 4: 22},
    '1 Samuel': {
        1: 28, 2: 36, 3: 21, 4: 22, 5: 12, 6: 21, 7: 17, 8: 22, 9: 27, 10: 27,
        11: 15, 12: 25, 13: 23, 14: 52, 15: 35, 16: 23, 17: 58, 18: 30, 19: 24, 20: 42,
        21: 15, 22: 23, 23: 29, 24: 22, 25: 44, 26: 25, 27: 12, 28: 25, 29: 11, 30: 31, 31: 13
    },
    '2 Samuel': {
        1: 27, 2: 32, 3: 39, 4: 12, 5: 25, 6: 23, 7: 29, 8: 18, 9: 13, 10: 19,
        11: 27, 12: 31, 13: 39, 14: 33, 15: 37, 16: 23, 17: 29, 18: 33, 19: 43, 20: 26,
        21: 22, 22: 51, 23: 39, 24: 25
    },
    '1 Kings': {
        1: 53, 2: 46, 3: 28, 4: 34, 5: 18, 6: 38, 7: 51, 8: 66, 9: 28, 10: 29,
        11: 43, 12: 33, 13: 34, 14: 31, 15: 34, 16: 34, 17: 24, 18: 46, 19: 21, 20: 43,
        21: 29, 22: 53
    },
    '2 Kings': {
        1: 18, 2: 25, 3: 27, 4: 44, 5: 27, 6: 33, 7: 20, 8: 29, 9: 37, 10: 36,
        11: 21, 12: 21, 13: 25, 14: 29, 15: 38, 16: 20, 17: 41, 18: 37, 19: 37, 20: 21,
        21: 26, 22: 20, 23: 37, 24: 20, 25: 30
    },
    '1 Chronicles': {
        1: 54, 2: 55, 3: 24, 4: 43, 5: 26, 6: 81, 7: 40, 8: 40, 9: 44, 10: 14,
        11: 47, 12: 40, 13: 14, 14: 17, 15: 29, 16: 43, 17: 27, 18: 17, 19: 19, 20: 8,
        21: 30, 22: 19, 23: 32, 24: 31, 25: 31, 26: 32, 27: 34, 28: 21, 29: 30
    },
    '2 Chronicles': {
        1: 17, 2: 18, 3: 17, 4: 22, 5: 14, 6: 42, 7: 22, 8: 18, 9: 31, 10: 19,
        11: 23, 12: 16, 13: 22, 14: 15, 15: 19, 16: 14, 17: 19, 18: 34, 19: 11, 20: 37,
        21: 20, 22: 12, 23: 21, 24: 27, 25: 28, 26: 23, 27: 9, 28: 27, 29: 36, 30: 27,
        31: 21, 32: 33, 33: 25, 34: 33, 35: 27, 36: 23
    },
    'Ezra': {1: 11, 2: 70, 3: 13, 4: 24, 5: 17, 6: 22, 7: 28, 8: 36, 9: 15, 10: 44},
    'Nehemiah': {
        1: 11, 2: 20, 3: 32, 4: 23, 5: 19, 6: 19, 7: 73, 8: 18, 9: 38, 10: 39,
        11: 36, 12: 47, 13: 31
    },
    'Esther': {1: 22, 2: 23, 3: 15, 4: 17, 5: 14, 6: 14, 7: 10, 8: 17, 9: 32, 10: 3},
    # Poetic Books
    'Job': {
        1: 22, 2: 13, 3: 26, 4: 21, 5: 27, 6: 30, 7: 21, 8: 22, 9: 35, 10: 22,
        11: 20, 12: 25, 13: 28, 14: 22, 15: 35, 16: 22, 17: 16, 18: 21, 19: 29, 20: 29,
        21: 34, 22: 30, 23: 17, 24: 25, 25: 6, 26: 14, 27: 23, 28: 28, 29: 25, 30: 31,
        31: 40, 32: 22, 33: 33, 34: 37, 35: 16, 36: 33, 37: 24, 38: 41, 39: 30, 40: 24,
        41: 34, 42: 17
    },
    'Psalms': {
        1: 6, 2: 12, 3: 8, 4: 8, 5: 12, 6: 10, 7: 17, 8: 9, 9: 20, 10: 18,
        11: 7, 12: 8, 13: 6, 14: 7, 15: 5, 16: 11, 17: 15, 18: 50, 19: 14, 20: 9,
        21: 13, 22: 31, 23: 6, 24: 10, 25: 22, 26: 12, 27: 14, 28: 9, 29: 11, 30: 12,
        31: 24, 32: 11, 33: 22, 34: 22, 35: 28, 36: 12, 37: 40, 38: 22, 39: 13, 40: 17,
        41: 13, 42: 11, 43: 5, 44: 26, 45: 17, 46: 11, 47: 9, 48: 14, 49: 20, 50: 23,
        51: 19, 52: 9, 53: 6, 54: 7, 55: 23, 56: 13, 57: 11, 58: 11, 59: 17, 60: 12,
        61: 8, 62: 12, 63: 11, 64: 10, 65: 13, 66: 20, 67: 7, 68: 35, 69: 36, 70: 5,
        71: 24, 72: 20, 73: 28, 74: 23, 75: 10, 76: 12, 77: 20, 78: 72, 79: 13, 80: 19,
        81: 16, 82: 8, 83: 18, 84: 12, 85: 13, 86: 17, 87: 7, 88: 18, 89: 52, 90: 17,
        91: 16, 92: 15, 93: 5, 94: 23, 95: 11, 96: 13, 97: 12, 98: 9, 99: 9, 100: 5,
        101: 8, 102: 28, 103: 22, 104: 35, 105: 45, 106: 48, 107: 43, 108: 13, 109: 31, 110: 7,
        111: 10, 112: 10, 113: 9, 114: 8, 115: 18, 116: 19, 117: 2, 118: 29, 119: 176, 120: 7,
        121: 8, 122: 9, 123: 4, 124: 8, 125: 5, 126: 6, 127: 5, 128: 6, 129: 8, 130: 8,
        131: 3, 132: 18, 133: 3, 134: 3, 135: 21, 136: 26, 137: 9, 138: 8, 139: 24, 140: 13,
        141: 10, 142: 7, 143: 12, 144: 15, 145: 21, 146: 10, 147: 20, 148: 14, 149: 9, 150: 6
    },
    'Proverbs': {
        1: 33, 2: 22, 3: 35, 4: 27, 5: 23, 6: 35, 7: 27, 8: 36, 9: 18, 10: 32,
        11: 31, 12: 28, 13: 25, 14: 35, 15: 33, 16: 33, 17: 28, 18: 24, 19: 29, 20: 30,
        21: 31, 22: 29, 23: 35, 24: 34, 25: 28, 26: 28, 27: 27, 28: 28, 29: 27, 30: 33, 31: 31
    },
    'Ecclesiastes': {1: 18, 2: 26, 3: 22, 4: 16, 5: 20, 6: 12, 7: 29, 8: 17, 9: 18, 10: 20, 11: 10, 12: 14},
    'Song of Solomon': {1: 17, 2: 17, 3: 11, 4: 16, 5: 16, 6: 13, 7: 13, 8: 14},
    # Major Prophets
    'Isaiah': {
        1: 31, 2: 22, 3: 26, 4: 6, 5: 30, 6: 13, 7: 25, 8: 22, 9: 21, 10: 34,
        11: 16, 12: 6, 13: 22, 14: 32, 15: 9, 16: 14, 17: 14, 18: 7, 19: 25, 20: 6,
        21: 17, 22: 25, 23: 18, 24: 23, 25: 12, 26: 21, 27: 13, 28: 29, 29: 24, 30: 33,
        31: 9, 32: 20, 33: 24, 34: 17, 35: 10, 36: 22, 37: 38, 38: 22, 39: 8, 40: 31,
        41: 29, 42: 25, 43: 28, 44: 28, 45: 25, 46: 13, 47: 15, 48: 22, 49: 26, 50: 11,
        51: 23, 52: 15, 53: 12, 54: 17, 55: 13, 56: 12, 57: 21, 58: 14, 59: 21, 60: 22,
        61: 11, 62: 12, 63: 19, 64: 12, 65: 25, 66: 24
    },
    'Jeremiah': {
        1: 19, 2: 37, 3: 25, 4: 31, 5: 31, 6: 30, 7: 34, 8: 22, 9: 26, 10: 25,
        11: 23, 12: 17, 13: 27, 14: 22, 15: 21, 16: 21, 17: 27, 18: 23, 19: 15, 20: 18,
        21: 14, 22: 30, 23: 40, 24: 10, 25: 38, 26: 24, 27: 22, 28: 17, 29: 32, 30: 24,
        31: 40, 32: 44, 33: 26, 34: 22, 35: 19, 36: 32, 37: 21, 38: 28, 39: 18, 40: 16,
        41: 18, 42: 22, 43: 13, 44: 30, 45: 5, 46: 28, 47: 7, 48: 47, 49: 39, 50: 46,
        51: 64, 52: 34
    },
    'Lamentations': {1: 22, 2: 22, 3: 66, 4: 22, 5: 22},
    'Ezekiel': {
        1: 28, 2: 10, 3: 27, 4: 17, 5: 17, 6: 14, 7: 27, 8: 18, 9: 11, 10: 22,
        11: 25, 12: 28, 13: 23, 14: 23, 15: 8, 16: 63, 17: 24, 18: 32, 19: 14, 20: 49,
        21: 32, 22: 31, 23: 49, 24: 27, 25: 17, 26: 21, 27: 36, 28: 26, 29: 21, 30: 26,
        31: 18, 32: 32, 33: 33, 34: 31, 35: 15, 36: 38, 37: 28, 38: 23, 39: 29, 40: 49,
        41: 26, 42: 20, 43: 27, 44: 31, 45: 25, 46: 24, 47: 23, 48: 35
    },
    'Daniel': {1: 21, 2: 49, 3: 30, 4: 37, 5: 31, 6: 28, 7: 28, 8: 27, 9: 27, 10: 21, 11: 45, 12: 13},
    # Minor Prophets
    'Hosea': {1: 11, 2: 23, 3: 5, 4: 19, 5: 15, 6: 11, 7: 16, 8: 14, 9: 17, 10: 15, 11: 12, 12: 14, 13: 16, 14: 9},
    'Joel': {1: 20, 2: 32, 3: 21},
    'Amos': {1: 15, 2: 16, 3: 15, 4: 13, 5: 27, 6: 14, 7: 17, 8: 14, 9: 15},
    'Obadiah': {1: 21},
    'Jonah': {1: 17, 2: 10, 3: 10, 4: 11},
    'Micah': {1: 16, 2: 13, 3: 12, 4: 13, 5: 15, 6: 16, 7: 20},
    'Nahum': {1: 15, 2: 13, 3: 19},
    'Habakkuk': {1: 17, 2: 20, 3: 19},
    'Zephaniah': {1: 18, 2: 15, 3: 20},
    'Haggai': {1: 15, 2: 23},
    'Zechariah': {1: 21, 2: 13, 3: 10, 4: 14, 5: 11, 6: 15, 7: 14, 8: 23, 9: 17, 10: 12, 11: 17, 12: 14, 13: 9, 14: 21},
    'Malachi': {1: 14, 2: 17, 3: 18, 4: 6},
    # Deuterocanonical Books
    'Tobit': {1: 22, 2: 14, 3: 17, 4: 21, 5: 23, 6: 19, 7: 17, 8: 21, 9: 6, 10: 14, 11: 19, 12: 22, 13: 18, 14: 15},
    'Judith': {1: 16, 2: 28, 3: 10, 4: 15, 5: 24, 6: 21, 7: 32, 8: 36, 9: 14, 10: 23, 11: 23, 12: 20, 13: 20, 14: 19, 15: 14, 16: 25},
    '1 Maccabees': {
        1: 64, 2: 70, 3: 60, 4: 61, 5: 68, 6: 63, 7: 50, 8: 32, 9: 73, 10: 89,
        11: 74, 12: 53, 13: 53, 14: 49, 15: 41, 16: 24
    },
    '2 Maccabees': {1: 36, 2: 32, 3: 40, 4: 50, 5: 27, 6: 31, 7: 42, 8: 36, 9: 29, 10: 38, 11: 38, 12: 45, 13: 26, 14: 46, 15: 39},
    'Wisdom': {1: 16, 2: 24, 3: 19, 4: 20, 5: 23, 6: 25, 7: 30, 8: 21, 9: 18, 10: 21, 11: 26, 12: 27, 13: 19, 14: 31, 15: 19, 16: 29, 17: 21, 18: 25, 19: 22},
    'Sirach': {
        1: 30, 2: 18, 3: 31, 4: 31, 5: 18, 6: 37, 7: 36, 8: 19, 9: 18, 10: 31,
        11: 34, 12: 18, 13: 26, 14: 27, 15: 20, 16: 30, 17: 32, 18: 33, 19: 30, 20: 31,
        21: 28, 22: 27, 23: 27, 24: 34, 25: 26, 26: 29, 27: 30, 28: 26, 29: 28, 30: 25,
        31: 31, 32: 24, 33: 31, 34: 31, 35: 26, 36: 31, 37: 31, 38: 34, 39: 35, 40: 30,
        41: 24, 42: 25, 43: 33, 44: 23, 45: 26, 46: 20, 47: 25, 48: 25, 49: 16, 50: 29, 51: 30
    },
    'Baruch': {1: 22, 2: 35, 3: 38, 4: 37, 5: 9, 6: 73},
    # New Testament - Gospels
    'Matthew': {
        1: 25, 2: 23, 3: 17, 4: 25, 5: 48, 6: 34, 7: 29, 8: 34, 9: 38, 10: 42,
        11: 30, 12: 50, 13: 58, 14: 36, 15: 39, 16: 28, 17: 27, 18: 35, 19: 30, 20: 34,
        21: 46, 22: 46, 23: 39, 24: 51, 25: 46, 26: 75, 27: 66, 28: 20
    },
    'Mark': {
        1: 45, 2: 28, 3: 35, 4: 41, 5: 43, 6: 56, 7: 37, 8: 38, 9: 50, 10: 52,
        11: 33, 12: 44, 13: 37, 14: 72, 15: 47, 16: 20
    },
    'Luke': {
        1: 80, 2: 52, 3: 38, 4: 44, 5: 39, 6: 49, 7: 50, 8: 56, 9: 62, 10: 42,
        11: 54, 12: 59, 13: 35, 14: 35, 15: 32, 16: 31, 17: 37, 18: 43, 19: 48, 20: 47,
        21: 38, 22: 71, 23: 56, 24: 53
    },
    'John': {
        1: 51, 2: 25, 3: 36, 4: 54, 5: 47, 6: 71, 7: 53, 8: 59, 9: 41, 10: 42,
        11: 57, 12: 50, 13: 38, 14: 31, 15: 27, 16: 33, 17: 26, 18: 40, 19: 42, 20: 31, 21: 25
    },
    # Acts
    'Acts': {
        1: 26, 2: 47, 3: 26, 4: 37, 5: 42, 6: 15, 7: 60, 8: 40, 9: 43, 10: 48,
        11: 30, 12: 25, 13: 52, 14: 28, 15: 41, 16: 40, 17: 34, 18: 28, 19: 41, 20: 38,
        21: 40, 22: 30, 23: 35, 24: 27, 25: 27, 26: 32, 27: 44, 28: 31
    },
    # Pauline Epistles
    'Romans': {1: 32, 2: 29, 3: 31, 4: 25, 5: 21, 6: 23, 7: 25, 8: 39, 9: 33, 10: 21, 11: 36, 12: 21, 13: 14, 14: 23, 15: 33, 16: 27},
    '1 Corinthians': {1: 31, 2: 16, 3: 23, 4: 21, 5: 13, 6: 20, 7: 40, 8: 13, 9: 27, 10: 33, 11: 34, 12: 31, 13: 13, 14: 40, 15: 58, 16: 24},
    '2 Corinthians': {1: 24, 2: 17, 3: 18, 4: 18, 5: 21, 6: 18, 7: 16, 8: 24, 9: 15, 10: 18, 11: 33, 12: 21, 13: 14},
    'Galatians': {1: 24, 2: 21, 3: 29, 4: 31, 5: 26, 6: 18},
    'Ephesians': {1: 23, 2: 22, 3: 21, 4: 32, 5: 33, 6: 24},
    'Philippians': {1: 30, 2: 30, 3: 21, 4: 23},
    'Colossians': {1: 29, 2: 23, 3: 25, 4: 18},
    '1 Thessalonians': {1: 10, 2: 20, 3: 13, 4: 18, 5: 28},
    '2 Thessalonians': {1: 12, 2: 17, 3: 18},
    '1 Timothy': {1: 20, 2: 15, 3: 16, 4: 16, 5: 25, 6: 21},
    '2 Timothy': {1: 18, 2: 26, 3: 17, 4: 22},
    'Titus': {1: 16, 2: 15, 3: 15},
    'Philemon': {1: 25},
    'Hebrews': {1: 14, 2: 18, 3: 19, 4: 16, 5: 14, 6: 20, 7: 28, 8: 13, 9: 28, 10: 39, 11: 40, 12: 29, 13: 25},
    # General Epistles
    'James': {1: 27, 2: 26, 3: 18, 4: 17, 5: 20},
    '1 Peter': {1: 25, 2: 25, 3: 22, 4: 19, 5: 14},
    '2 Peter': {1: 21, 2: 22, 3: 18},
    '1 John': {1: 10, 2: 29, 3: 24, 4: 21, 5: 21},
    '2 John': {1: 13},
    '3 John': {1: 14},
    'Jude': {1: 25},
    # Apocalyptic
    'Revelation': {
        1: 20, 2: 29, 3: 22, 4: 11, 5: 14, 6: 17, 7: 17, 8: 13, 9: 21, 10: 11,
        11: 19, 12: 17, 13: 18, 14: 20, 15: 8, 16: 21, 17: 18, 18: 24, 19: 21, 20: 15,
        21: 27, 22: 21
    }
}


# ============================================================================
# VERSE POPULATOR CLASS
# ============================================================================

class VersePopulator:
    """
    Comprehensive verse population system for all 73 canonical books.
    
    Provides systematic population of verse records and text retrieval
    using offline data with optional API fallback.
    """
    
    def __init__(self, db: Optional[DatabaseManager] = None) -> None:
        """
        Initialize the verse populator.
        
        Args:
            db: Optional database manager. Uses global if not provided.
        """
        self.db = db or get_db()
        self._book_id_cache: Dict[str, int] = {}
        self._offline_provider: Optional[Any] = None
        self._verse_fetcher: Optional[Any] = None
        self._load_book_ids()
    
    def _load_book_ids(self) -> None:
        """Cache book IDs for fast lookup."""
        try:
            rows = self.db.fetch_all(
                "SELECT id, name FROM canonical_books ORDER BY canonical_order"
            )
            for row in rows:
                self._book_id_cache[row['name']] = row['id']
        except QueryError as e:
            logger.error(f"Failed to load book IDs: {e}")
    
    @property
    def offline_provider(self) -> Any:
        """Lazy-load offline Bible provider."""
        if self._offline_provider is None:
            try:
                from data.offline_bible import get_offline_provider
                self._offline_provider = get_offline_provider()
            except ImportError:
                logger.debug("Offline provider not available")
        return self._offline_provider
    
    @property
    def verse_fetcher(self) -> Any:
        """Lazy-load verse fetcher for API fallback."""
        if self._verse_fetcher is None:
            try:
                from tools.bible_api import VerseFetcher
                self._verse_fetcher = VerseFetcher(self.db)
            except ImportError:
                logger.debug("Verse fetcher not available")
        return self._verse_fetcher
    
    def get_canonical_books(self) -> List[Dict[str, Any]]:
        """
        Get all 73 canonical books from the database.
        
        Returns:
            List of book dictionaries with id, name, chapters, verses counts.
        """
        query = """
            SELECT id, name, abbreviation, category, canonical_order,
                   testament, total_chapters, total_verses
            FROM canonical_books
            ORDER BY canonical_order
        """
        try:
            return self.db.fetch_all(query)
        except QueryError as e:
            logger.error(f"Failed to get canonical books: {e}")
            return []
    
    def get_population_status(self) -> PopulationStats:
        """
        Get overall population status across all books.
        
        Returns:
            PopulationStats with current population state.
        """
        stats = PopulationStats()
        
        # Get book counts
        books = self.get_canonical_books()
        stats.total_books = len(books)
        
        # Get total expected verses
        for book in books:
            stats.total_verses += book.get('total_verses', 0)
        
        # Get actual verse counts
        try:
            count_query = "SELECT COUNT(*) as count FROM verses"
            result = self.db.fetch_one(count_query)
            actual_verses = result['count'] if result else 0
            
            text_query = "SELECT COUNT(*) as count FROM verses WHERE text_kjv IS NOT NULL"
            result = self.db.fetch_one(text_query)
            stats.verses_with_text = result['count'] if result else 0
            
            # Count fully populated books
            for book in books:
                book_id = book['id']
                result = self.db.fetch_one(
                    "SELECT COUNT(*) as count FROM verses WHERE book_id = %s AND text_kjv IS NOT NULL",
                    (book_id,)
                )
                if result and result['count'] >= book.get('total_verses', 0):
                    stats.populated_books += 1
                    
        except QueryError as e:
            logger.error(f"Failed to get population status: {e}")
        
        return stats
    
    def get_book_status(self, book_name: str) -> Optional[BookStats]:
        """
        Get population status for a specific book.
        
        Args:
            book_name: Name of the canonical book.
            
        Returns:
            BookStats for the book, or None if not found.
        """
        book_id = self._book_id_cache.get(book_name)
        if not book_id:
            return None
        
        try:
            # Get book info
            book = self.db.fetch_one(
                "SELECT * FROM canonical_books WHERE id = %s",
                (book_id,)
            )
            if not book:
                return None
            
            stats = BookStats(
                book_id=book_id,
                book_name=book_name,
                total_chapters=book['total_chapters'],
                total_verses=book['total_verses']
            )
            
            # Get populated verse count
            result = self.db.fetch_one(
                "SELECT COUNT(*) as count FROM verses WHERE book_id = %s AND text_kjv IS NOT NULL",
                (book_id,)
            )
            stats.verses_with_text = result['count'] if result else 0
            
            return stats
            
        except QueryError as e:
            logger.error(f"Failed to get book status for {book_name}: {e}")
            return None
    
    def create_verse_records(
        self, 
        book_name: str, 
        populate_text: bool = True,
        use_offline: bool = True
    ) -> int:
        """
        Create verse records for a book from VERSE_STRUCTURE.
        
        Args:
            book_name: Name of the canonical book.
            populate_text: Whether to populate verse text.
            use_offline: Whether to use offline data.
            
        Returns:
            Number of verses created/updated.
        """
        book_id = self._book_id_cache.get(book_name)
        if not book_id:
            logger.error(f"Book not found in cache: {book_name}")
            return 0
        
        structure = VERSE_STRUCTURE.get(book_name)
        if not structure:
            logger.warning(f"No verse structure data for: {book_name}")
            return 0
        
        created = 0
        
        for chapter, verse_count in structure.items():
            for verse_num in range(1, verse_count + 1):
                verse_ref = f"{book_name} {chapter}:{verse_num}"
                
                # Get text if requested
                text = None
                if populate_text:
                    # Try offline first
                    if use_offline and self.offline_provider:
                        text = self.offline_provider.get_verse(book_name, chapter, verse_num)
                    
                    # API fallback is expensive, skip for bulk creation
                    # Text can be populated later via populate_text_for_book
                
                # Insert/update verse record
                query = """
                    INSERT INTO verses (book_id, chapter, verse_number, verse_reference, text_kjv, status)
                    VALUES (%s, %s, %s, %s, %s, 'raw')
                    ON CONFLICT (book_id, chapter, verse_number) 
                    DO UPDATE SET
                        text_kjv = COALESCE(EXCLUDED.text_kjv, verses.text_kjv),
                        updated_at = CURRENT_TIMESTAMP
                """
                
                try:
                    self.db.execute(query, (book_id, chapter, verse_num, verse_ref, text))
                    created += 1
                except QueryError as e:
                    logger.error(f"Failed to create verse {verse_ref}: {e}")
        
        logger.info(f"Created/updated {created} verse records for {book_name}")
        return created
    
    def populate_all_books(
        self, 
        populate_text: bool = True,
        progress_callback: Optional[callable] = None
    ) -> PopulationStats:
        """
        Populate verse records for all 73 canonical books.
        
        Args:
            populate_text: Whether to populate verse text from offline data.
            progress_callback: Optional callback(book_name, book_num, total_books).
            
        Returns:
            PopulationStats with final status.
        """
        stats = PopulationStats()
        books = list(VERSE_STRUCTURE.keys())
        stats.total_books = len(books)
        
        logger.info(f"Starting population of {len(books)} canonical books")
        
        for i, book_name in enumerate(books, 1):
            if progress_callback:
                progress_callback(book_name, i, len(books))
            
            logger.info(f"[{i}/{len(books)}] Populating {book_name}...")
            
            created = self.create_verse_records(book_name, populate_text)
            
            if created > 0:
                stats.verses_populated += created
                stats.populated_books += 1
            else:
                stats.errors += 1
        
        # Calculate final totals
        stats.total_verses = sum(
            sum(chapters.values()) for chapters in VERSE_STRUCTURE.values()
        )
        
        # Get actual verse text count
        try:
            result = self.db.fetch_one(
                "SELECT COUNT(*) as count FROM verses WHERE text_kjv IS NOT NULL"
            )
            stats.verses_with_text = result['count'] if result else 0
        except QueryError:
            pass
        
        logger.info(f"Population complete: {stats.verses_populated} verses, "
                   f"{stats.verses_with_text} with text")
        
        return stats
    
    def populate_text_for_book(
        self,
        book_name: str,
        use_api: bool = False,
        limit: Optional[int] = None
    ) -> int:
        """
        Populate text for existing verse records in a book.
        
        Args:
            book_name: Name of the canonical book.
            use_api: Whether to use API for missing text.
            limit: Optional limit on verses to process.
            
        Returns:
            Number of verses updated with text.
        """
        book_id = self._book_id_cache.get(book_name)
        if not book_id:
            logger.error(f"Book not found: {book_name}")
            return 0
        
        # Get verses without text
        query = """
            SELECT id, chapter, verse_number, verse_reference
            FROM verses
            WHERE book_id = %s AND text_kjv IS NULL
            ORDER BY chapter, verse_number
        """
        params: List[Any] = [book_id]
        
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        
        try:
            verses = self.db.fetch_all(query, tuple(params))
        except QueryError as e:
            logger.error(f"Failed to get verses: {e}")
            return 0
        
        updated = 0
        
        for verse in verses:
            text = None
            
            # Try offline first
            if self.offline_provider:
                text = self.offline_provider.get_verse(
                    book_name, verse['chapter'], verse['verse_number']
                )
            
            # Try API if offline didn't have it
            if not text and use_api and self.verse_fetcher:
                text = self.verse_fetcher.fetch_verse(
                    book_name, verse['chapter'], verse['verse_number']
                )
                time.sleep(0.2)  # Rate limiting
            
            if text:
                try:
                    self.db.execute(
                        "UPDATE verses SET text_kjv = %s WHERE id = %s",
                        (text, verse['id'])
                    )
                    updated += 1
                except QueryError as e:
                    logger.error(f"Failed to update verse {verse['verse_reference']}: {e}")
        
        logger.info(f"Updated {updated} verses with text for {book_name}")
        return updated
    
    def get_missing_text_count(self) -> Dict[str, int]:
        """
        Get count of verses missing text by book.
        
        Returns:
            Dictionary mapping book name to missing count.
        """
        query = """
            SELECT cb.name, COUNT(*) as missing
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.text_kjv IS NULL
            GROUP BY cb.name, cb.canonical_order
            ORDER BY cb.canonical_order
        """
        
        try:
            rows = self.db.fetch_all(query)
            return {row['name']: row['missing'] for row in rows}
        except QueryError as e:
            logger.error(f"Failed to get missing text count: {e}")
            return {}
    
    def print_status_report(self) -> None:
        """Print a formatted status report to stdout."""
        stats = self.get_population_status()
        
        print("\n" + "=" * 60)
        print("ΒΊΒΛΟΣ ΛΌΓΟΥ - 73-Book Verse Population Status")
        print("=" * 60)
        print(f"\nTotal Books: {stats.total_books}")
        print(f"Populated Books: {stats.populated_books} ({stats.book_completion_percentage:.1f}%)")
        print(f"\nTotal Verses Expected: {stats.total_verses:,}")
        print(f"Verses with Text: {stats.verses_with_text:,}")
        print(f"Completion: {stats.completion_percentage:.1f}%")
        
        # Show books missing text
        missing = self.get_missing_text_count()
        if missing:
            print(f"\nBooks with Missing Text ({len(missing)} books):")
            for book, count in list(missing.items())[:10]:
                print(f"  {book}: {count} verses missing")
            if len(missing) > 10:
                print(f"  ... and {len(missing) - 10} more books")
        else:
            print("\n✓ All verse records have text populated")
        
        print("=" * 60 + "\n")


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_populator: Optional[VersePopulator] = None


def get_populator() -> VersePopulator:
    """Get the global verse populator singleton."""
    global _populator
    if _populator is None:
        _populator = VersePopulator()
    return _populator


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Main entry point for verse population CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='ΒΊΒΛΟΣ ΛΌΓΟΥ Full 73-Book Verse Population'
    )
    parser.add_argument('--status', action='store_true', 
                       help='Show population status')
    parser.add_argument('--populate-all', action='store_true',
                       help='Populate all 73 books')
    parser.add_argument('--book', type=str,
                       help='Populate specific book')
    parser.add_argument('--populate-text', action='store_true',
                       help='Populate text for existing records')
    parser.add_argument('--use-api', action='store_true',
                       help='Use API for missing text')
    parser.add_argument('--limit', type=int,
                       help='Limit verses to process')
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize database
    from scripts.database import init_db
    if not init_db():
        logger.error("Failed to initialize database connection")
        return 1
    
    populator = get_populator()
    
    if args.status:
        populator.print_status_report()
        return 0
    
    if args.populate_all:
        def progress(book: str, num: int, total: int):
            print(f"\r[{num}/{total}] {book}...", end='', flush=True)
        
        print("Populating all 73 canonical books...")
        stats = populator.populate_all_books(
            populate_text=True,
            progress_callback=progress
        )
        print(f"\n\nComplete: {stats.verses_populated} verses populated")
        populator.print_status_report()
        return 0
    
    if args.book:
        if args.populate_text:
            count = populator.populate_text_for_book(
                args.book,
                use_api=args.use_api,
                limit=args.limit
            )
            print(f"Updated {count} verses with text for {args.book}")
        else:
            count = populator.create_verse_records(args.book)
            print(f"Created {count} verse records for {args.book}")
        return 0
    
    # Default: show status
    populator.print_status_report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
