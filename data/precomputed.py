#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Pre-computed Data Module
All calculations that can be done ahead of time ARE done ahead of time.
Zero runtime computation for deterministic operations.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# PRE-COMPUTED VERSE COUNTS PER CHAPTER
# No need to query or calculate at runtime
# ============================================================================

VERSE_COUNTS = {
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
    'Matthew': {
        1: 25, 2: 23, 3: 17, 4: 25, 5: 48, 6: 34, 7: 29, 8: 34, 9: 38, 10: 42,
        11: 30, 12: 50, 13: 58, 14: 36, 15: 39, 16: 28, 17: 27, 18: 35, 19: 30, 20: 34,
        21: 46, 22: 46, 23: 39, 24: 51, 25: 46, 26: 75, 27: 66, 28: 20
    },
    'John': {
        1: 51, 2: 25, 3: 36, 4: 54, 5: 47, 6: 71, 7: 53, 8: 59, 9: 41, 10: 42,
        11: 57, 12: 50, 13: 38, 14: 31, 15: 27, 16: 33, 17: 26, 18: 40, 19: 42, 20: 31, 21: 25
    },
    'Romans': {
        1: 32, 2: 29, 3: 31, 4: 25, 5: 21, 6: 23, 7: 25, 8: 39, 9: 33, 10: 21,
        11: 36, 12: 21, 13: 14, 14: 23, 15: 33, 16: 27
    },
    'Revelation': {
        1: 20, 2: 29, 3: 22, 4: 11, 5: 14, 6: 17, 7: 17, 8: 13, 9: 21, 10: 11,
        11: 19, 12: 17, 13: 18, 14: 20, 15: 8, 16: 21, 17: 18, 18: 24, 19: 21, 20: 15,
        21: 27, 22: 21
    },
}


# ============================================================================
# PRE-COMPUTED BOOK METADATA
# ============================================================================

@dataclass(frozen=True)
class BookMeta:
    """Immutable book metadata."""
    name: str
    canonical_order: int
    testament: str
    category: str
    chapters: int
    total_verses: int


BOOK_METADATA: Dict[str, BookMeta] = {
    'Genesis': BookMeta('Genesis', 1, 'old', 'pentateuch', 50, 1533),
    'Exodus': BookMeta('Exodus', 2, 'old', 'pentateuch', 40, 1213),
    'Leviticus': BookMeta('Leviticus', 3, 'old', 'pentateuch', 27, 859),
    'Numbers': BookMeta('Numbers', 4, 'old', 'pentateuch', 36, 1288),
    'Deuteronomy': BookMeta('Deuteronomy', 5, 'old', 'pentateuch', 34, 959),
    'Joshua': BookMeta('Joshua', 6, 'old', 'historical', 24, 658),
    'Judges': BookMeta('Judges', 7, 'old', 'historical', 21, 618),
    'Ruth': BookMeta('Ruth', 8, 'old', 'historical', 4, 85),
    '1 Samuel': BookMeta('1 Samuel', 9, 'old', 'historical', 31, 810),
    '2 Samuel': BookMeta('2 Samuel', 10, 'old', 'historical', 24, 695),
    '1 Kings': BookMeta('1 Kings', 11, 'old', 'historical', 22, 816),
    '2 Kings': BookMeta('2 Kings', 12, 'old', 'historical', 25, 719),
    '1 Chronicles': BookMeta('1 Chronicles', 13, 'old', 'historical', 29, 942),
    '2 Chronicles': BookMeta('2 Chronicles', 14, 'old', 'historical', 36, 822),
    'Ezra': BookMeta('Ezra', 15, 'old', 'historical', 10, 280),
    'Nehemiah': BookMeta('Nehemiah', 16, 'old', 'historical', 13, 406),
    'Esther': BookMeta('Esther', 17, 'old', 'historical', 10, 167),
    'Job': BookMeta('Job', 18, 'old', 'poetic', 42, 1070),
    'Psalms': BookMeta('Psalms', 19, 'old', 'poetic', 150, 2461),
    'Proverbs': BookMeta('Proverbs', 20, 'old', 'poetic', 31, 915),
    'Ecclesiastes': BookMeta('Ecclesiastes', 21, 'old', 'poetic', 12, 222),
    'Song of Solomon': BookMeta('Song of Solomon', 22, 'old', 'poetic', 8, 117),
    'Isaiah': BookMeta('Isaiah', 23, 'old', 'major_prophet', 66, 1292),
    'Jeremiah': BookMeta('Jeremiah', 24, 'old', 'major_prophet', 52, 1364),
    'Lamentations': BookMeta('Lamentations', 25, 'old', 'poetic', 5, 154),
    'Ezekiel': BookMeta('Ezekiel', 26, 'old', 'major_prophet', 48, 1273),
    'Daniel': BookMeta('Daniel', 27, 'old', 'major_prophet', 12, 357),
    'Hosea': BookMeta('Hosea', 28, 'old', 'minor_prophet', 14, 197),
    'Joel': BookMeta('Joel', 29, 'old', 'minor_prophet', 3, 73),
    'Amos': BookMeta('Amos', 30, 'old', 'minor_prophet', 9, 146),
    'Obadiah': BookMeta('Obadiah', 31, 'old', 'minor_prophet', 1, 21),
    'Jonah': BookMeta('Jonah', 32, 'old', 'minor_prophet', 4, 48),
    'Micah': BookMeta('Micah', 33, 'old', 'minor_prophet', 7, 105),
    'Nahum': BookMeta('Nahum', 34, 'old', 'minor_prophet', 3, 47),
    'Habakkuk': BookMeta('Habakkuk', 35, 'old', 'minor_prophet', 3, 56),
    'Zephaniah': BookMeta('Zephaniah', 36, 'old', 'minor_prophet', 3, 53),
    'Haggai': BookMeta('Haggai', 37, 'old', 'minor_prophet', 2, 38),
    'Zechariah': BookMeta('Zechariah', 38, 'old', 'minor_prophet', 14, 211),
    'Malachi': BookMeta('Malachi', 39, 'old', 'minor_prophet', 4, 55),
    # Deuterocanonical
    'Tobit': BookMeta('Tobit', 40, 'deuterocanonical', 'deuterocanonical', 14, 244),
    'Judith': BookMeta('Judith', 41, 'deuterocanonical', 'deuterocanonical', 16, 340),
    'Wisdom': BookMeta('Wisdom', 42, 'deuterocanonical', 'deuterocanonical', 19, 435),
    'Sirach': BookMeta('Sirach', 43, 'deuterocanonical', 'deuterocanonical', 51, 1388),
    'Baruch': BookMeta('Baruch', 44, 'deuterocanonical', 'deuterocanonical', 6, 213),
    '1 Maccabees': BookMeta('1 Maccabees', 45, 'deuterocanonical', 'deuterocanonical', 16, 924),
    '2 Maccabees': BookMeta('2 Maccabees', 46, 'deuterocanonical', 'deuterocanonical', 15, 555),
    # New Testament
    'Matthew': BookMeta('Matthew', 47, 'new', 'gospel', 28, 1071),
    'Mark': BookMeta('Mark', 48, 'new', 'gospel', 16, 678),
    'Luke': BookMeta('Luke', 49, 'new', 'gospel', 24, 1151),
    'John': BookMeta('John', 50, 'new', 'gospel', 21, 879),
    'Acts': BookMeta('Acts', 51, 'new', 'acts', 28, 1007),
    'Romans': BookMeta('Romans', 52, 'new', 'pauline', 16, 433),
    '1 Corinthians': BookMeta('1 Corinthians', 53, 'new', 'pauline', 16, 437),
    '2 Corinthians': BookMeta('2 Corinthians', 54, 'new', 'pauline', 13, 257),
    'Galatians': BookMeta('Galatians', 55, 'new', 'pauline', 6, 149),
    'Ephesians': BookMeta('Ephesians', 56, 'new', 'pauline', 6, 155),
    'Philippians': BookMeta('Philippians', 57, 'new', 'pauline', 4, 104),
    'Colossians': BookMeta('Colossians', 58, 'new', 'pauline', 4, 95),
    '1 Thessalonians': BookMeta('1 Thessalonians', 59, 'new', 'pauline', 5, 89),
    '2 Thessalonians': BookMeta('2 Thessalonians', 60, 'new', 'pauline', 3, 47),
    '1 Timothy': BookMeta('1 Timothy', 61, 'new', 'pauline', 6, 113),
    '2 Timothy': BookMeta('2 Timothy', 62, 'new', 'pauline', 4, 83),
    'Titus': BookMeta('Titus', 63, 'new', 'pauline', 3, 46),
    'Philemon': BookMeta('Philemon', 64, 'new', 'pauline', 1, 25),
    'Hebrews': BookMeta('Hebrews', 65, 'new', 'general_epistle', 13, 303),
    'James': BookMeta('James', 66, 'new', 'general_epistle', 5, 108),
    '1 Peter': BookMeta('1 Peter', 67, 'new', 'general_epistle', 5, 105),
    '2 Peter': BookMeta('2 Peter', 68, 'new', 'general_epistle', 3, 61),
    '1 John': BookMeta('1 John', 69, 'new', 'general_epistle', 5, 105),
    '2 John': BookMeta('2 John', 70, 'new', 'general_epistle', 1, 13),
    '3 John': BookMeta('3 John', 71, 'new', 'general_epistle', 1, 14),
    'Jude': BookMeta('Jude', 72, 'new', 'general_epistle', 1, 25),
    'Revelation': BookMeta('Revelation', 73, 'new', 'apocalyptic', 22, 404),
}


# ============================================================================
# PRE-COMPUTED CANONICAL ORDER (Fast Lookup)
# ============================================================================

CANONICAL_ORDER: Dict[str, int] = {book: meta.canonical_order for book, meta in BOOK_METADATA.items()}


# ============================================================================
# PRE-COMPUTED BOOK ALIASES (Normalized Lookup)
# ============================================================================

BOOK_ALIASES: Dict[str, str] = {
    # Common abbreviations
    'gen': 'Genesis', 'ge': 'Genesis', 'gn': 'Genesis',
    'exod': 'Exodus', 'ex': 'Exodus', 'exo': 'Exodus',
    'lev': 'Leviticus', 'le': 'Leviticus', 'lv': 'Leviticus',
    'num': 'Numbers', 'nu': 'Numbers', 'nm': 'Numbers',
    'deut': 'Deuteronomy', 'de': 'Deuteronomy', 'dt': 'Deuteronomy',
    'josh': 'Joshua', 'jos': 'Joshua',
    'judg': 'Judges', 'jdg': 'Judges', 'jg': 'Judges',
    'ru': 'Ruth', 'rth': 'Ruth',
    '1sam': '1 Samuel', '1sa': '1 Samuel', '1 sam': '1 Samuel',
    '2sam': '2 Samuel', '2sa': '2 Samuel', '2 sam': '2 Samuel',
    '1kgs': '1 Kings', '1ki': '1 Kings', '1 kings': '1 Kings',
    '2kgs': '2 Kings', '2ki': '2 Kings', '2 kings': '2 Kings',
    '1chr': '1 Chronicles', '1ch': '1 Chronicles',
    '2chr': '2 Chronicles', '2ch': '2 Chronicles',
    'ezr': 'Ezra',
    'neh': 'Nehemiah', 'ne': 'Nehemiah',
    'est': 'Esther', 'esth': 'Esther',
    'jb': 'Job',
    'ps': 'Psalms', 'psa': 'Psalms', 'psalm': 'Psalms',
    'prov': 'Proverbs', 'pr': 'Proverbs', 'prv': 'Proverbs',
    'eccl': 'Ecclesiastes', 'ecc': 'Ecclesiastes', 'ec': 'Ecclesiastes',
    'song': 'Song of Solomon', 'sos': 'Song of Solomon', 'ss': 'Song of Solomon',
    'canticles': 'Song of Solomon',
    'isa': 'Isaiah', 'is': 'Isaiah',
    'jer': 'Jeremiah', 'je': 'Jeremiah',
    'lam': 'Lamentations', 'la': 'Lamentations',
    'ezek': 'Ezekiel', 'eze': 'Ezekiel', 'ezk': 'Ezekiel',
    'dan': 'Daniel', 'da': 'Daniel', 'dn': 'Daniel',
    'hos': 'Hosea', 'ho': 'Hosea',
    'joe': 'Joel', 'jl': 'Joel',
    'am': 'Amos', 'amo': 'Amos',
    'ob': 'Obadiah', 'oba': 'Obadiah', 'obad': 'Obadiah',
    'jon': 'Jonah', 'jnh': 'Jonah',
    'mic': 'Micah', 'mi': 'Micah',
    'nah': 'Nahum', 'na': 'Nahum',
    'hab': 'Habakkuk', 'hb': 'Habakkuk',
    'zeph': 'Zephaniah', 'zep': 'Zephaniah', 'zp': 'Zephaniah',
    'hag': 'Haggai', 'hg': 'Haggai',
    'zech': 'Zechariah', 'zec': 'Zechariah', 'zc': 'Zechariah',
    'mal': 'Malachi', 'ml': 'Malachi',
    # Deuterocanonical
    'tob': 'Tobit', 'tb': 'Tobit',
    'jdt': 'Judith', 'jdth': 'Judith',
    'wis': 'Wisdom', 'ws': 'Wisdom', 'wisdom of solomon': 'Wisdom',
    'sir': 'Sirach', 'ecclesiasticus': 'Sirach',
    'bar': 'Baruch',
    '1macc': '1 Maccabees', '1mac': '1 Maccabees', '1 macc': '1 Maccabees',
    '2macc': '2 Maccabees', '2mac': '2 Maccabees', '2 macc': '2 Maccabees',
    # New Testament
    'matt': 'Matthew', 'mt': 'Matthew', 'mat': 'Matthew',
    'mk': 'Mark', 'mr': 'Mark', 'mrk': 'Mark',
    'lk': 'Luke', 'lu': 'Luke',
    'jn': 'John', 'joh': 'John',
    'ac': 'Acts', 'act': 'Acts',
    'rom': 'Romans', 'ro': 'Romans', 'rm': 'Romans',
    '1cor': '1 Corinthians', '1co': '1 Corinthians',
    '2cor': '2 Corinthians', '2co': '2 Corinthians',
    'gal': 'Galatians', 'ga': 'Galatians',
    'eph': 'Ephesians', 'ephes': 'Ephesians',
    'phil': 'Philippians', 'php': 'Philippians',
    'col': 'Colossians',
    '1thess': '1 Thessalonians', '1th': '1 Thessalonians',
    '2thess': '2 Thessalonians', '2th': '2 Thessalonians',
    '1tim': '1 Timothy', '1ti': '1 Timothy',
    '2tim': '2 Timothy', '2ti': '2 Timothy',
    'tit': 'Titus', 'ti': 'Titus',
    'phm': 'Philemon', 'philem': 'Philemon',
    'heb': 'Hebrews',
    'jas': 'James', 'jm': 'James',
    '1pet': '1 Peter', '1pe': '1 Peter', '1pt': '1 Peter',
    '2pet': '2 Peter', '2pe': '2 Peter', '2pt': '2 Peter',
    '1jn': '1 John', '1jo': '1 John', '1john': '1 John',
    '2jn': '2 John', '2jo': '2 John', '2john': '2 John',
    '3jn': '3 John', '3jo': '3 John', '3john': '3 John',
    'jud': 'Jude', 'jude': 'Jude',
    'rev': 'Revelation', 're': 'Revelation', 'apocalypse': 'Revelation',
}

# Add lowercase canonical names
for book in BOOK_METADATA:
    BOOK_ALIASES[book.lower()] = book


# ============================================================================
# PRE-COMPUTED HARMONIC RATIOS FOR ORBITAL RESONANCE
# ============================================================================

HARMONIC_RATIOS: Tuple[float, ...] = (0.5, 0.833, 0.9375)  # 1/2, 5/6, 15/16

def precompute_harmonic_pages(planting: int, convergence: int) -> Tuple[int, ...]:
    """Pre-compute harmonic reinforcement pages for a motif."""
    distance = convergence - planting
    return tuple(planting + int(distance * r) for r in HARMONIC_RATIOS)


# Pre-computed for all primary motifs
MOTIF_HARMONICS: Dict[str, Tuple[int, ...]] = {
    'The Lamb': precompute_harmonic_pages(50, 2400),      # (1225, 2006, 2253)
    'Wood': precompute_harmonic_pages(20, 2200),          # (1110, 1836, 2063)
    'Silence': precompute_harmonic_pages(100, 2200),      # (1150, 1850, 2069)
    'The Binding': precompute_harmonic_pages(700, 2200),  # (1450, 1950, 2106)
    'Water': precompute_harmonic_pages(10, 1800),         # (905, 1500, 1688)
    'Fire': precompute_harmonic_pages(300, 2050),         # (1175, 1758, 1941)
    'Blood': precompute_harmonic_pages(50, 2200),         # (1125, 1842, 2069)
    'Bread': precompute_harmonic_pages(400, 2100),        # (1250, 1817, 1994)
    'Shepherd': precompute_harmonic_pages(50, 1900),      # (975, 1592, 1784)
    'Stone': precompute_harmonic_pages(750, 2000),        # (1375, 1792, 1922)
}


# ============================================================================
# PRE-COMPUTED INTENSITY CURVE VALUES
# ============================================================================

INTENSITY_CURVE: Dict[str, float] = {
    'planting': 0.7,
    'early_reinforcement': 0.5,
    'mid_trajectory': 0.3,
    'low_point': 0.2,
    'convergence': 1.0,
}

def get_intensity_for_position(orbital_position: float) -> float:
    """Get intensity based on orbital position (0.0 to 1.0). Pre-computed thresholds."""
    if orbital_position <= 0.1:
        return INTENSITY_CURVE['planting']
    elif orbital_position <= 0.3:
        return INTENSITY_CURVE['early_reinforcement']
    elif orbital_position <= 0.6:
        return INTENSITY_CURVE['mid_trajectory']
    elif orbital_position <= 0.85:
        return INTENSITY_CURVE['low_point']
    else:
        return INTENSITY_CURVE['convergence']


# ============================================================================
# PRE-COMPUTED CATEGORY BASE VALUES FOR NINE-MATRIX
# ============================================================================

CATEGORY_MATRIX_VALUES: Dict[str, Dict[str, float]] = {
    'pentateuch': {'emotional': 0.55, 'theological': 0.75, 'sensory': 0.65},
    'gospel': {'emotional': 0.70, 'theological': 0.85, 'sensory': 0.75},
    'poetic': {'emotional': 0.80, 'theological': 0.60, 'sensory': 0.70},
    'major_prophet': {'emotional': 0.75, 'theological': 0.80, 'sensory': 0.70},
    'minor_prophet': {'emotional': 0.70, 'theological': 0.75, 'sensory': 0.65},
    'historical': {'emotional': 0.50, 'theological': 0.55, 'sensory': 0.55},
    'pauline': {'emotional': 0.45, 'theological': 0.90, 'sensory': 0.35},
    'general_epistle': {'emotional': 0.50, 'theological': 0.80, 'sensory': 0.40},
    'apocalyptic': {'emotional': 0.85, 'theological': 0.90, 'sensory': 0.90},
    'acts': {'emotional': 0.60, 'theological': 0.70, 'sensory': 0.60},
    'deuterocanonical': {'emotional': 0.55, 'theological': 0.65, 'sensory': 0.55},
}


# ============================================================================
# PRE-COMPUTED SPECIAL VERSES (High Theological Weight)
# ============================================================================

HIGH_THEOLOGICAL_WEIGHT_VERSES: frozenset = frozenset({
    'Genesis 1:1', 'Genesis 1:26', 'Genesis 1:27', 'Genesis 3:15', 'Genesis 22:8',
    'Exodus 3:14', 'Exodus 12:13', 'Exodus 20:2', 'Exodus 20:3',
    'Deuteronomy 6:4', 'Deuteronomy 6:5',
    'Psalm 22:1', 'Psalm 23:1', 'Psalm 51:10', 'Psalm 110:1', 'Psalm 118:22',
    'Isaiah 7:14', 'Isaiah 9:6', 'Isaiah 53:5', 'Isaiah 53:6', 'Isaiah 53:7',
    'Jeremiah 31:31',
    'Ezekiel 37:14',
    'Daniel 7:13',
    'Micah 5:2',
    'Zechariah 9:9',
    'Malachi 3:1',
    'Matthew 1:21', 'Matthew 3:17', 'Matthew 16:16', 'Matthew 28:19', 'Matthew 28:20',
    'Mark 10:45',
    'Luke 1:35', 'Luke 2:11', 'Luke 24:6',
    'John 1:1', 'John 1:14', 'John 1:29', 'John 3:16', 'John 6:35', 'John 8:58',
    'John 10:11', 'John 11:25', 'John 14:6', 'John 17:3', 'John 19:30', 'John 20:28',
    'Acts 2:38', 'Acts 4:12',
    'Romans 1:16', 'Romans 3:23', 'Romans 5:8', 'Romans 6:23', 'Romans 8:1',
    'Romans 8:28', 'Romans 8:38', 'Romans 8:39',
    '1 Corinthians 15:3', '1 Corinthians 15:4', '1 Corinthians 15:55',
    '2 Corinthians 5:17', '2 Corinthians 5:21',
    'Galatians 2:20', 'Galatians 3:13',
    'Ephesians 2:8', 'Ephesians 2:9',
    'Philippians 2:6', 'Philippians 2:7', 'Philippians 2:8', 'Philippians 2:10', 'Philippians 2:11',
    'Colossians 1:15', 'Colossians 1:16', 'Colossians 1:17', 'Colossians 2:9',
    'Hebrews 1:3', 'Hebrews 4:12', 'Hebrews 11:1', 'Hebrews 12:2', 'Hebrews 13:8',
    '1 Peter 2:24', '1 Peter 3:18',
    '1 John 1:9', '1 John 4:8',
    'Revelation 1:8', 'Revelation 5:12', 'Revelation 21:4', 'Revelation 22:20',
})


# ============================================================================
# PRE-COMPUTED PASCHA DATES (2020-2050)
# ============================================================================

ORTHODOX_PASCHA_DATES: Dict[int, Tuple[int, int]] = {
    # Year: (month, day) - Gregorian calendar
    2020: (4, 19), 2021: (5, 2), 2022: (4, 24), 2023: (4, 16), 2024: (5, 5),
    2025: (4, 20), 2026: (4, 12), 2027: (5, 2), 2028: (4, 16), 2029: (4, 8),
    2030: (4, 28), 2031: (4, 13), 2032: (5, 2), 2033: (4, 24), 2034: (4, 9),
    2035: (4, 29), 2036: (4, 20), 2037: (4, 5), 2038: (4, 25), 2039: (4, 17),
    2040: (5, 6), 2041: (4, 21), 2042: (4, 6), 2043: (4, 26), 2044: (4, 17),
    2045: (5, 7), 2046: (4, 22), 2047: (4, 14), 2048: (5, 3), 2049: (4, 18),
    2050: (4, 10),
}


# ============================================================================
# PRE-COMPUTED REGISTER MAPPINGS
# ============================================================================

CATEGORY_REGISTERS: Dict[str, str] = {
    'apocalyptic': 'elevated-liturgical',
    'poetic': 'elevated-poetic',
    'pauline': 'instructional-theological',
    'general_epistle': 'instructional-pastoral',
    'gospel': 'narrative-testimonial',
    'historical': 'narrative-historical',
    'pentateuch': 'narrative-covenantal',
    'major_prophet': 'prophetic-oracular',
    'minor_prophet': 'prophetic-condensed',
    'acts': 'narrative-missional',
    'deuterocanonical': 'wisdom-historical',
}


# ============================================================================
# PRE-COMPUTED BREATH RHYTHM PATTERNS
# ============================================================================

BREATH_PATTERNS: Tuple[str, ...] = ('sustained', 'punctuated', 'flowing', 'staccato', 'measured')

def get_breath_rhythm(verse_number: int) -> str:
    """Get breath rhythm for verse. Pre-computed pattern."""
    return BREATH_PATTERNS[verse_number % len(BREATH_PATTERNS)]


# ============================================================================
# PRE-COMPUTED NARRATIVE FUNCTION THRESHOLDS
# ============================================================================

def get_narrative_function(verse_number: int) -> str:
    """Determine narrative function. Pre-computed thresholds."""
    if verse_number <= 3:
        return 'scene-setting'
    elif verse_number <= 8:
        return 'exposition'
    elif verse_number <= 15:
        return 'development'
    elif verse_number <= 20:
        return 'intensification'
    elif verse_number <= 25:
        return 'climax'
    else:
        return 'resolution'


# ============================================================================
# LOOKUP FUNCTIONS (O(1) access to pre-computed data)
# ============================================================================

def get_book_meta(book_name: str) -> Optional[BookMeta]:
    """Get book metadata. O(1) lookup."""
    # Try direct lookup first
    if book_name in BOOK_METADATA:
        return BOOK_METADATA[book_name]
    
    # Try alias lookup
    normalized = BOOK_ALIASES.get(book_name.lower())
    if normalized:
        return BOOK_METADATA.get(normalized)
    
    return None


def normalize_book_name(name: str) -> Optional[str]:
    """Normalize book name to canonical form. O(1) lookup."""
    if name in BOOK_METADATA:
        return name
    return BOOK_ALIASES.get(name.lower())


def get_verse_count(book: str, chapter: int) -> Optional[int]:
    """Get verse count for a chapter. O(1) lookup."""
    book_counts = VERSE_COUNTS.get(book)
    if book_counts:
        return book_counts.get(chapter)
    return None


def is_high_theological_weight(verse_ref: str) -> bool:
    """Check if verse has high theological weight. O(1) lookup."""
    return verse_ref in HIGH_THEOLOGICAL_WEIGHT_VERSES


def get_motif_harmonics(motif_name: str) -> Optional[Tuple[int, ...]]:
    """Get pre-computed harmonic pages for a motif. O(1) lookup."""
    return MOTIF_HARMONICS.get(motif_name)


def get_pascha_date(year: int) -> Optional[Tuple[int, int]]:
    """Get pre-computed Pascha date. O(1) lookup."""
    return ORTHODOX_PASCHA_DATES.get(year)


# ============================================================================
# STATISTICS
# ============================================================================

def get_precomputed_stats() -> Dict[str, Any]:
    """Get statistics about pre-computed data."""
    return {
        'books': len(BOOK_METADATA),
        'aliases': len(BOOK_ALIASES),
        'verse_count_chapters': sum(len(chapters) for chapters in VERSE_COUNTS.values()),
        'motifs_with_harmonics': len(MOTIF_HARMONICS),
        'high_theological_verses': len(HIGH_THEOLOGICAL_WEIGHT_VERSES),
        'pascha_dates_cached': len(ORTHODOX_PASCHA_DATES),
        'total_bible_verses': sum(meta.total_verses for meta in BOOK_METADATA.values()),
    }
