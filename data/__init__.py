#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Data Module
========================

Offline biblical data for the Orthodox Exegetical Commentary System.

THE NARRATIVE ENDS AT THE CROSS.

This module provides pre-computed, hardcoded data to:
1. Eliminate API dependencies
2. Ensure O(1) lookups for deterministic operations
3. Support temporal folding through planted/echoed phrases
4. Maintain local emotional honesty while building global dread architecture

Primary Access Point: BiblosData (from unified.py)
"""

# Legacy providers (for backwards compatibility)
from .offline_bible import OfflineBibleProvider, get_offline_provider
from .liturgical_calendar import LiturgicalCalendar, get_liturgical_calendar
from .patristic_data import PatristicDatabase, get_patristic_database

# New pre-computed data modules
from .precomputed import (
    BOOK_METADATA, BookMeta, CANONICAL_ORDER, VERSE_COUNTS,
    HIGH_THEOLOGICAL_WEIGHT_VERSES, CATEGORY_MATRIX_VALUES,
    get_book_meta, normalize_book_name, is_high_theological_weight
)

from .orthodox_study_bible import (
    VerseExegesis, TonalWeight, 
    get_verse_exegesis, get_book_exegesis, get_statistics as get_exegesis_stats
)

from .narrative_order import (
    NarrativeEvent, NarrativePart,
    get_narrative_order, get_terminal_event, get_events_by_part,
    find_echoes, find_plantings
)

# Enhanced modules
from .character_voices import (
    CharacterVoice, VoiceRegister, CharacterType,
    get_voice, get_voices_by_type, get_voices_by_register,
    ALL_VOICES
)

from .morphology import (
    HebrewTerm, GreekTerm, Language, TheologicalWeight,
    get_hebrew_term, get_greek_term, get_terms_by_motif, get_ultra_terms,
    ALL_HEBREW, ALL_GREEK
)

from .cross_references import (
    TypologicalCorrespondence, TypeCategory, CorrespondenceStrength,
    get_antitype, get_type, get_by_category, get_explicit, get_sensory_network,
    ALL_CORRESPONDENCES
)

from .unified import BiblosData

__all__ = [
    # Legacy providers
    'OfflineBibleProvider', 'get_offline_provider',
    'LiturgicalCalendar', 'get_liturgical_calendar',
    'PatristicDatabase', 'get_patristic_database',
    
    # Book metadata
    'BOOK_METADATA', 'BookMeta', 'CANONICAL_ORDER', 'VERSE_COUNTS',
    'get_book_meta', 'normalize_book_name',
    
    # Verse data
    'HIGH_THEOLOGICAL_WEIGHT_VERSES', 'is_high_theological_weight',
    'CATEGORY_MATRIX_VALUES',
    
    # Exegesis
    'VerseExegesis', 'TonalWeight',
    'get_verse_exegesis', 'get_book_exegesis', 'get_exegesis_stats',
    
    # Narrative order
    'NarrativeEvent', 'NarrativePart',
    'get_narrative_order', 'get_terminal_event', 'get_events_by_part',
    'find_echoes', 'find_plantings',
    
    # Character voices
    'CharacterVoice', 'VoiceRegister', 'CharacterType',
    'get_voice', 'get_voices_by_type', 'get_voices_by_register',
    'ALL_VOICES',
    
    # Hebrew/Greek morphology
    'HebrewTerm', 'GreekTerm', 'Language', 'TheologicalWeight',
    'get_hebrew_term', 'get_greek_term', 'get_terms_by_motif', 'get_ultra_terms',
    'ALL_HEBREW', 'ALL_GREEK',
    
    # Cross-references / Typology
    'TypologicalCorrespondence', 'TypeCategory', 'CorrespondenceStrength',
    'get_antitype', 'get_type', 'get_by_category', 'get_explicit', 'get_sensory_network',
    'ALL_CORRESPONDENCES',
    
    # Unified access (primary entry point)
    'BiblosData',
]
