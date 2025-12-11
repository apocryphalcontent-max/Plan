#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Unified Data Access Layer
======================================

This module provides a single, unified interface to ALL pre-computed data.
Every lookup is O(1). Every calculation that can be pre-computed IS pre-computed.

The system is designed around the core principle:
THE NARRATIVE ENDS AT THE CROSS.

All data serves this terminus. All lookups return data oriented toward
the blood-red sky that emerges from arrangement, not from repainting.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from our pre-computed modules
from data.precomputed import (
    BOOK_METADATA, BookMeta, BOOK_ALIASES, CANONICAL_ORDER,
    VERSE_COUNTS, HIGH_THEOLOGICAL_WEIGHT_VERSES,
    CATEGORY_MATRIX_VALUES, CATEGORY_REGISTERS,
    MOTIF_HARMONICS, INTENSITY_CURVE, HARMONIC_RATIOS,
    ORTHODOX_PASCHA_DATES, BREATH_PATTERNS,
    get_book_meta, normalize_book_name, get_verse_count,
    is_high_theological_weight, get_motif_harmonics,
    get_intensity_for_position, get_breath_rhythm, get_narrative_function
)

from data.orthodox_study_bible import (
    VerseExegesis, TonalWeight, NarrativeFunction as ExegesisNarrativeFunction,
    get_verse_exegesis, get_book_exegesis, get_statistics as get_exegesis_stats
)

from data.narrative_order import (
    NarrativeEvent, NarrativePart,
    get_narrative_order, get_terminal_event, get_events_by_part,
    find_echoes, find_plantings
)


# ============================================================================
# UNIFIED ACCESS CLASS
# ============================================================================

class BiblosData:
    """
    Unified access to all pre-computed ΒΊΒΛΟΣ ΛΌΓΟΥ data.
    
    This is the single entry point for all data access in the system.
    All methods return pre-computed data with O(1) complexity.
    """
    
    # Terminal verse - the narrative ends here
    TERMINAL_REFERENCE = "John 19:30"
    TERMINAL_TEXT = "It is finished"
    
    # ========================================================================
    # BOOK DATA
    # ========================================================================
    
    @staticmethod
    def get_book(name: str) -> Optional[BookMeta]:
        """Get book metadata by name (canonical or alias)."""
        return get_book_meta(name)
    
    @staticmethod
    def normalize_book(name: str) -> Optional[str]:
        """Normalize any book name/alias to canonical form."""
        return normalize_book_name(name)
    
    @staticmethod
    def get_all_books() -> Dict[str, BookMeta]:
        """Get all book metadata."""
        return BOOK_METADATA.copy()
    
    @staticmethod
    def get_canonical_order(book: str) -> Optional[int]:
        """Get canonical order for a book."""
        return CANONICAL_ORDER.get(book)
    
    @staticmethod
    def get_category(book: str) -> Optional[str]:
        """Get category for a book."""
        meta = get_book_meta(book)
        return meta.category if meta else None
    
    # ========================================================================
    # VERSE DATA
    # ========================================================================
    
    @staticmethod
    def get_verse_count(book: str, chapter: int) -> Optional[int]:
        """Get verse count for a chapter."""
        return get_verse_count(book, chapter)
    
    @staticmethod
    def is_high_weight(reference: str) -> bool:
        """Check if a verse has high theological weight."""
        return is_high_theological_weight(reference)
    
    @staticmethod
    def get_exegesis(reference: str) -> Optional[VerseExegesis]:
        """Get pre-computed exegesis for a verse."""
        return get_verse_exegesis(reference)
    
    @staticmethod
    def get_fourfold_sense(reference: str) -> Optional[Dict[str, str]]:
        """Get fourfold sense for a verse if available."""
        ex = get_verse_exegesis(reference)
        if ex:
            return {
                'literal': ex.literal,
                'allegorical': ex.allegorical,
                'tropological': ex.tropological,
                'anagogical': ex.anagogical
            }
        return None
    
    # ========================================================================
    # NINE-MATRIX DATA
    # ========================================================================
    
    @staticmethod
    def get_matrix_base_values(category: str) -> Dict[str, float]:
        """Get base matrix values for a book category."""
        return CATEGORY_MATRIX_VALUES.get(category, CATEGORY_MATRIX_VALUES['historical'])
    
    @staticmethod
    def get_register(category: str) -> str:
        """Get register for a book category."""
        return CATEGORY_REGISTERS.get(category, 'narrative-standard')
    
    @staticmethod
    def get_breath_rhythm(verse_number: int) -> str:
        """Get breath rhythm for verse number."""
        return get_breath_rhythm(verse_number)
    
    @staticmethod
    def get_narrative_function(verse_number: int) -> str:
        """Get narrative function for verse number."""
        return get_narrative_function(verse_number)
    
    # ========================================================================
    # MOTIF DATA
    # ========================================================================
    
    @staticmethod
    def get_harmonics(motif: str) -> Optional[Tuple[int, ...]]:
        """Get pre-computed harmonic pages for a motif."""
        return get_motif_harmonics(motif)
    
    @staticmethod
    def get_all_motif_harmonics() -> Dict[str, Tuple[int, ...]]:
        """Get all pre-computed motif harmonics."""
        return MOTIF_HARMONICS.copy()
    
    @staticmethod
    def get_intensity(position: float) -> float:
        """Get intensity for orbital position (0.0-1.0)."""
        return get_intensity_for_position(position)
    
    # ========================================================================
    # NARRATIVE ORDER
    # ========================================================================
    
    @staticmethod
    def get_narrative_order() -> List[NarrativeEvent]:
        """Get the complete narrative ordering."""
        return get_narrative_order()
    
    @staticmethod
    def get_terminal() -> NarrativeEvent:
        """Get the terminal event (the Cross)."""
        return get_terminal_event()
    
    @staticmethod
    def get_events_for_part(part: NarrativePart) -> List[NarrativeEvent]:
        """Get events for a specific narrative part."""
        return get_events_by_part(part)
    
    @staticmethod
    def find_phrase_echoes(phrase: str) -> List[NarrativeEvent]:
        """Find events that echo a phrase."""
        return find_echoes(phrase)
    
    @staticmethod
    def find_phrase_plantings(phrase: str) -> List[NarrativeEvent]:
        """Find events that plant a phrase."""
        return find_plantings(phrase)
    
    # ========================================================================
    # TEMPORAL FOLDING
    # ========================================================================
    
    @staticmethod
    def get_planted_phrase(reference: str) -> Optional[str]:
        """Get phrase planted by a verse (if any)."""
        ex = get_verse_exegesis(reference)
        return ex.plants_phrase if ex else None
    
    @staticmethod
    def get_echoed_phrase(reference: str) -> Optional[str]:
        """Get phrase echoed by a verse (if any)."""
        ex = get_verse_exegesis(reference)
        return ex.echoes_phrase if ex else None
    
    # ========================================================================
    # TONAL ARCHITECTURE
    # ========================================================================
    
    @staticmethod
    def get_tonal_weight(reference: str) -> Optional[str]:
        """Get tonal weight for a verse."""
        ex = get_verse_exegesis(reference)
        return ex.tonal_weight.value if ex else None
    
    @staticmethod
    def get_native_mood(reference: str) -> Optional[str]:
        """Get native mood for a verse."""
        ex = get_verse_exegesis(reference)
        return ex.native_mood if ex else None
    
    @staticmethod
    def get_dread_amplification(reference: str) -> Optional[float]:
        """Get dread amplification for a verse."""
        ex = get_verse_exegesis(reference)
        return ex.dread_amplification if ex else None
    
    # ========================================================================
    # SENSORY VOCABULARY
    # ========================================================================
    
    @staticmethod
    def get_sensory_seeds(reference: str) -> Optional[Dict[str, Tuple[str, ...]]]:
        """Get sensory vocabulary seeds for a verse."""
        ex = get_verse_exegesis(reference)
        if ex:
            return {
                'visual': ex.visual_seeds,
                'auditory': ex.auditory_seeds,
                'tactile': ex.tactile_seeds
            }
        return None
    
    # ========================================================================
    # LITURGICAL CALENDAR
    # ========================================================================
    
    @staticmethod
    def get_pascha(year: int) -> Optional[Tuple[int, int]]:
        """Get pre-computed Pascha date for a year."""
        return ORTHODOX_PASCHA_DATES.get(year)
    
    # ========================================================================
    # CROSS REFERENCES
    # ========================================================================
    
    @staticmethod
    def get_cross_references(reference: str) -> Optional[Tuple[str, ...]]:
        """Get cross-references for a verse."""
        ex = get_verse_exegesis(reference)
        return ex.cross_references if ex else None
    
    @staticmethod
    def get_typological_shadows(reference: str) -> Optional[Tuple[str, ...]]:
        """Get OT shadows (antecedents) for a verse."""
        ex = get_verse_exegesis(reference)
        return ex.typological_shadows if ex else None
    
    @staticmethod
    def get_typological_fulfillments(reference: str) -> Optional[Tuple[str, ...]]:
        """Get typological fulfillments for a verse."""
        ex = get_verse_exegesis(reference)
        return ex.typological_fulfillments if ex else None
    
    # ========================================================================
    # STATISTICS
    # ========================================================================
    
    @staticmethod
    def get_statistics() -> Dict[str, Any]:
        """Get comprehensive statistics about all pre-computed data."""
        exegesis_stats = get_exegesis_stats()
        
        return {
            'books': {
                'total': len(BOOK_METADATA),
                'old_testament': sum(1 for m in BOOK_METADATA.values() if m.testament == 'old'),
                'new_testament': sum(1 for m in BOOK_METADATA.values() if m.testament == 'new'),
                'deuterocanonical': sum(1 for m in BOOK_METADATA.values() if m.testament == 'deuterocanonical'),
            },
            'verses': {
                'total': sum(m.total_verses for m in BOOK_METADATA.values()),
                'high_theological_weight': len(HIGH_THEOLOGICAL_WEIGHT_VERSES),
                'with_exegesis': exegesis_stats['total_verses'],
            },
            'motifs': {
                'with_harmonics': len(MOTIF_HARMONICS),
            },
            'narrative': {
                'total_events': len(get_narrative_order()),
                'terminal_event': BiblosData.TERMINAL_TEXT,
            },
            'aliases': len(BOOK_ALIASES),
        }


# ============================================================================
# CONVENIENCE FUNCTIONS (Module-level access)
# ============================================================================

# Create singleton instance
_data = BiblosData()

# Export commonly used functions at module level
get_book = _data.get_book
get_exegesis = _data.get_exegesis
get_fourfold_sense = _data.get_fourfold_sense
get_narrative = _data.get_narrative_order
get_terminal = _data.get_terminal
get_statistics = _data.get_statistics


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI interface for exploring unified data."""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Unified Data Access')
    parser.add_argument('--verse', type=str, help='Get all data for a verse')
    parser.add_argument('--book', type=str, help='Get book metadata')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--terminal', action='store_true', help='Show terminal event')
    parser.add_argument('--phrase', type=str, help='Find phrase echoes and plantings')
    
    args = parser.parse_args()
    
    if args.verse:
        print(f"\n{'='*60}")
        print(f"Data for: {args.verse}")
        print(f"{'='*60}")
        
        ex = get_exegesis(args.verse)
        if ex:
            print(f"\nText: {ex.text}")
            print(f"\nLiteral: {ex.literal}")
            print(f"\nAllegorical: {ex.allegorical}")
            print(f"\nTropological: {ex.tropological}")
            print(f"\nAnagogical: {ex.anagogical}")
            print(f"\nTonal Weight: {ex.tonal_weight.value}")
            print(f"Native Mood: {ex.native_mood}")
            print(f"Dread Amplification: {ex.dread_amplification}")
            if ex.plants_phrase:
                print(f"Plants Phrase: '{ex.plants_phrase}'")
            if ex.echoes_phrase:
                print(f"Echoes Phrase: '{ex.echoes_phrase}'")
        else:
            print(f"No pre-computed exegesis for: {args.verse}")
            
            # Show what we do have
            high_weight = BiblosData.is_high_weight(args.verse)
            print(f"High Theological Weight: {high_weight}")
    
    elif args.book:
        meta = get_book(args.book)
        if meta:
            print(f"\nBook: {meta.name}")
            print(f"Canonical Order: {meta.canonical_order}")
            print(f"Testament: {meta.testament}")
            print(f"Category: {meta.category}")
            print(f"Chapters: {meta.chapters}")
            print(f"Verses: {meta.total_verses}")
        else:
            print(f"Unknown book: {args.book}")
    
    elif args.stats:
        stats = get_statistics()
        print("\n" + "="*60)
        print("ΒΊΒΛΟΣ ΛΌΓΟΥ Data Statistics")
        print("="*60)
        print(f"\nBooks:")
        print(f"  Total: {stats['books']['total']}")
        print(f"  Old Testament: {stats['books']['old_testament']}")
        print(f"  New Testament: {stats['books']['new_testament']}")
        print(f"  Deuterocanonical: {stats['books']['deuterocanonical']}")
        print(f"\nVerses:")
        print(f"  Total in Bible: {stats['verses']['total']:,}")
        print(f"  High Theological Weight: {stats['verses']['high_theological_weight']}")
        print(f"  With Full Exegesis: {stats['verses']['with_exegesis']}")
        print(f"\nNarrative:")
        print(f"  Total Events: {stats['narrative']['total_events']}")
        print(f"  Terminal: \"{stats['narrative']['terminal_event']}\"")
    
    elif args.terminal:
        terminal = get_terminal()
        print(f"\n{'='*60}")
        print("THE NARRATIVE ENDS HERE")
        print(f"{'='*60}")
        print(f"\nEvent: {terminal.event_text}")
        print(f"Reference: {terminal.verse_reference}")
        print(f"Part: {terminal.part.value}")
        print(f"Mood: {terminal.native_mood}")
        if terminal.echoes_phrase:
            print(f"Echoes: '{terminal.echoes_phrase}'")
        if terminal.breath_note:
            print(f"\n{terminal.breath_note}")
    
    elif args.phrase:
        print(f"\nSearching for phrase: '{args.phrase}'")
        
        plantings = BiblosData.find_phrase_plantings(args.phrase)
        echoes = BiblosData.find_phrase_echoes(args.phrase)
        
        if plantings:
            print(f"\nPlanted in:")
            for e in plantings:
                print(f"  {e.verse_reference}: {e.event_text[:50]}...")
        
        if echoes:
            print(f"\nEchoed in:")
            for e in echoes:
                print(f"  {e.verse_reference}: {e.event_text[:50]}...")
        
        if not plantings and not echoes:
            print("No matches found.")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
