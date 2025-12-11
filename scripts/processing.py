#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Verse Processing Pipeline
======================================

Comprehensive verse processing through the Stratified Foundation System.

ENHANCED: Now uses pre-computed data wherever possible.
Runtime computation is reserved ONLY for:
1. Database operations (verse retrieval/update)
2. AI integration for complex analysis
3. Dynamic contextual calculations

All deterministic calculations use pre-computed data from:
- data.precomputed (book metadata, matrix values, harmonics)
- data.orthodox_study_bible (exegesis, tonal weights)
- data.narrative_order (narrative structure)
- data.unified (unified access layer)

THE NARRATIVE ENDS AT THE CROSS.
"""

import sys
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config
from scripts.database import (
    get_db, DatabaseManager, VerseRepository, MotifRepository,
    DatabaseError, QueryError
)

# Import pre-computed data - O(1) lookups replace runtime calculations
from data.precomputed import (
    CATEGORY_MATRIX_VALUES, CATEGORY_REGISTERS,
    HIGH_THEOLOGICAL_WEIGHT_VERSES,
    get_breath_rhythm, get_narrative_function,
    get_book_meta
)
from data.orthodox_study_bible import get_verse_exegesis, TonalWeight
from data.unified import BiblosData

logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class ProcessingError(Exception):
    """Base exception for processing operations."""
    pass


class VerseProcessingError(ProcessingError):
    """Raised when verse processing fails."""
    pass


class SenseGenerationError(ProcessingError):
    """Raised when fourfold sense generation fails."""
    pass


class MatrixCalculationError(ProcessingError):
    """Raised when nine-matrix calculation fails."""
    pass


# ============================================================================
# FOURFOLD SENSE GENERATOR - ENHANCED WITH PRE-COMPUTED EXEGESIS
# ============================================================================

class FourfoldSenseGenerator:
    """
    Generate fourfold sense analyses per MASTER_PLAN.md.
    
    ENHANCED: Prefers pre-computed exegesis from orthodox_study_bible.py.
    Falls back to template generation for verses without pre-computed data.
    """
    
    # Book category templates for sense generation (fallback only)
    CATEGORY_TEMPLATES = {
        'pentateuch': {
            'literal': "Foundational Torah instruction establishing covenantal patterns that shape Israel's identity and relationship with YHWH through specific command, narrative context, and theological significance.",
            'allegorical': "Prefigures Christ's redemptive work through covenant pattern, with specific elements serving as types finding fulfillment in His person, offices, and saving acts.",
            'tropological': "Forms the reader in habits of covenant fidelity, shaping practices of reverence, obedience, and communal responsibility that reflect identity as God's people called to holiness.",
            'anagogical': "Orients hope toward new creation, with foundational patterns finding ultimate fulfillment in the eternal state where God dwells with His people."
        },
        'gospel': {
            'literal': "Gospel narrative revealing Christ's identity and mission through specific action, teaching, or encounter that demonstrates the kingdom of God's presence and invitation.",
            'allegorical': "Reveals Christ directly, with each detail serving theological purpose in presenting His identity, mission, and saving significance for all humanity.",
            'tropological': "Forms disciples in kingdom life, with Jesus' words and actions providing the pattern for faithful response to God's grace.",
            'anagogical': "Points toward the consummation of Christ's kingdom, when all things will be gathered up in Him and God's reign will be complete."
        },
        'poetic': {
            'literal': "Poetic expression of human experience before God through metaphor, parallelism, and emotional language that invites reader participation in theological reflection and worship.",
            'allegorical': "Prefigures Christ as divine Wisdom and the pattern of righteous suffering, with characteristics and work fulfilled in Him who is the wisdom of God made manifest.",
            'tropological': "Shapes the reader's emotional and spiritual life, providing language for prayer, lament, praise, and the full range of human experience before God.",
            'anagogical': "Anticipates the eternal worship of heaven, where all creation joins in praise of the Lamb upon the throne."
        },
        'major_prophet': {
            'literal': "Prophetic oracle addressing Israel's historical situation with divine judgment, promise, and call to repentance within the covenant relationship.",
            'allegorical': "Anticipates Christ as the Suffering Servant, Branch of David, and eschatological deliverer who fulfills Israel's prophetic hope.",
            'tropological': "Calls the reader to repentance, justice, and faithful living in light of God's coming judgment and redemption.",
            'anagogical': "Points toward the Day of the Lord, final judgment, and the establishment of God's eternal kingdom."
        },
        'minor_prophet': {
            'literal': "Concentrated prophetic message addressing specific historical circumstances with intensity and urgency.",
            'allegorical': "Contains Christological themes concentrated in brief, powerful imagery that finds fulfillment in Christ's person and work.",
            'tropological': "Delivers urgent moral summons to covenant faithfulness in concise, memorable form.",
            'anagogical': "Announces coming divine intervention and ultimate restoration in compressed, powerful imagery."
        },
        'historical': {
            'literal': "Historical narrative recounting Israel's experience of God's faithfulness and judgment within the covenant relationship.",
            'allegorical': "Provides typological patterns fulfilled in Christ and His Church, with key figures prefiguring aspects of Christ's person and work.",
            'tropological': "Offers models of faith and failure from which readers learn patterns of faithful living.",
            'anagogical': "Points toward the ultimate kingdom where God's purposes for His people reach completion."
        },
        'pauline': {
            'literal': "Apostolic instruction addressing specific ecclesial situations with theological depth and pastoral care.",
            'allegorical': "Explicates the mystery of Christ hidden for ages and now revealed in the gospel.",
            'tropological': "Provides direct ethical instruction for Christian living, grounded in the indicative of grace.",
            'anagogical': "Articulates hope in Christ's return and the resurrection of the dead."
        },
        'general_epistle': {
            'literal': "Catholic instruction addressing the universal Church with practical wisdom and theological grounding.",
            'allegorical': "Interprets Christ's significance for the whole Church across cultural and temporal boundaries.",
            'tropological': "Provides wisdom for Christian living applicable to all believers in all circumstances.",
            'anagogical': "Sustains hope in final vindication and entrance into the eternal kingdom."
        },
        'apocalyptic': {
            'literal': "Visionary revelation disclosing divine perspective on history and its consummation through symbolic imagery.",
            'allegorical': "Reveals Christ in cosmic triumph, the Lamb who was slain and who conquers all opposing powers.",
            'tropological': "Calls to patient endurance and faithful witness in the face of persecution and cosmic conflict.",
            'anagogical': "Depicts the ultimate destiny of creation: new heaven and earth, the marriage supper of the Lamb, eternal communion with God."
        },
        'acts': {
            'literal': "Historical narrative of the Church's expansion under the Spirit's guidance from Jerusalem to Rome.",
            'allegorical': "Shows Christ continuing His work through His body, the Church, empowered by His Spirit.",
            'tropological': "Provides models for faithful witness, community life, and Spirit-led mission.",
            'anagogical': "Points toward the gospel's ultimate reach to all nations before Christ's return."
        },
        'deuterocanonical': {
            'literal': "Intertestamental wisdom and history illuminating the period between the testaments.",
            'allegorical': "Provides additional types and themes finding fulfillment in Christ.",
            'tropological': "Offers wisdom for righteous living in the face of persecution and cultural pressure.",
            'anagogical': "Strengthens hope in resurrection, judgment, and divine vindication."
        }
    }
    
    VALID_SENSE_TYPES: Tuple[str, ...] = ('literal', 'allegorical', 'tropological', 'anagogical')
    
    def __init__(self, db: Optional[DatabaseManager] = None) -> None:
        """
        Initialize the fourfold sense generator.
        
        Args:
            db: Optional database manager. Uses global if not provided.
        """
        self.db = db or get_db()
        self._patristic_db: Optional[Any] = None
        self._patristic_checked: bool = False
    
    @property
    def patristic_db(self) -> Optional[Any]:
        """
        Lazy-load patristic database for commentary enrichment.
        
        Returns:
            Patristic database instance, or None if not available.
        """
        if not self._patristic_checked:
            self._patristic_checked = True
            try:
                from data.patristic_data import get_patristic_database
                self._patristic_db = get_patristic_database()
            except ImportError:
                logger.debug("Patristic database not available")
                self._patristic_db = None
        return self._patristic_db
    
    def generate_sense(
        self, 
        verse: Dict[str, Any], 
        sense_type: str, 
        book_category: str
    ) -> str:
        """
        Generate a specific sense for a verse.
        
        Args:
            verse: Verse data dictionary.
            sense_type: One of 'literal', 'allegorical', 'tropological', 'anagogical'.
            book_category: Category of the book.
            
        Returns:
            Generated sense text.
            
        Raises:
            ValueError: If sense_type is invalid.
        """
        if sense_type not in self.VALID_SENSE_TYPES:
            raise ValueError(f"Invalid sense_type: {sense_type}")
            
        verse_ref = verse.get('verse_reference', '')
        if not verse_ref:
            logger.warning("Verse has no reference")
            return ""
        
        # First check for pre-computed exegesis
        exegesis = get_verse_exegesis(verse_ref)
        if exegesis:
            sense_map = {
                'literal': exegesis.literal,
                'allegorical': exegesis.allegorical,
                'tropological': exegesis.tropological,
                'anagogical': exegesis.anagogical
            }
            return sense_map.get(sense_type, "")
        
        # Fallback to template generation
        templates = self.CATEGORY_TEMPLATES.get(
            book_category, 
            self.CATEGORY_TEMPLATES['historical']
        )
        base_template = templates.get(sense_type, "")
        
        # Try to enrich with patristic commentary
        patristic_note = ""
        if self.patristic_db is not None:
            try:
                entries = self.patristic_db.suggest_commentary_for_sense(verse_ref, sense_type)
                if entries:
                    entry = entries[0]
                    patristic_note = f" As {entry.father} notes: \"{entry.text[:150]}...\""
            except Exception as e:
                logger.debug(f"Failed to get patristic commentary: {e}")
        
        return f"{verse_ref}: {base_template}{patristic_note}"
    
    def generate_all_senses(
        self, 
        verse: Dict[str, Any], 
        book_info: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generate all four senses for a verse.
        
        Prefers pre-computed exegesis when available, falling back
        to template generation.
        
        Args:
            verse: Verse data dictionary.
            book_info: Book information dictionary.
            
        Returns:
            Dictionary with keys 'literal', 'allegorical', 'tropological', 'anagogical'.
        """
        verse_ref = verse.get('verse_reference', '')
        
        # First check for pre-computed exegesis
        exegesis = get_verse_exegesis(verse_ref)
        if exegesis:
            return {
                'literal': exegesis.literal,
                'allegorical': exegesis.allegorical,
                'tropological': exegesis.tropological,
                'anagogical': exegesis.anagogical
            }
        
        # Fallback to template generation
        category = book_info.get('category', 'historical')
        try:
            return {
                'literal': self.generate_sense(verse, 'literal', category),
                'allegorical': self.generate_sense(verse, 'allegorical', category),
                'tropological': self.generate_sense(verse, 'tropological', category),
                'anagogical': self.generate_sense(verse, 'anagogical', category)
            }
        except Exception as e:
            logger.error(f"Failed to generate senses for {verse_ref}: {e}")
            raise SenseGenerationError(f"Failed to generate senses: {e}") from e


# ============================================================================
# NINE MATRIX CALCULATOR - ENHANCED WITH PRE-COMPUTED DATA
# ============================================================================

class NineMatrixCalculator:
    """
    Calculate nine-matrix elements per Stratified Foundation System.
    
    ENHANCED: Uses pre-computed data from data.precomputed module.
    Category base values, register mappings, and special verse lists
    are now O(1) lookups instead of inline dictionaries.
    """
    
    def __init__(self) -> None:
        """Initialize with pre-computed category values."""
        # Use pre-computed category values from data.precomputed
        self.category_values: Dict[str, Dict[str, float]] = CATEGORY_MATRIX_VALUES
    
    def calculate_emotional_valence(
        self, 
        verse: Dict[str, Any], 
        book_info: Dict[str, Any]
    ) -> float:
        """
        Calculate emotional valence (0.0 to 1.0).
        
        Args:
            verse: Verse data dictionary.
            book_info: Book information dictionary.
            
        Returns:
            Emotional valence value between 0.0 and 1.0.
        """
        category = book_info.get('category', 'historical')
        base = self.category_values.get(category, {}).get('emotional', 0.5)
        
        # Check for pre-computed exegesis first
        verse_ref = verse.get('verse_reference', '')
        exegesis = get_verse_exegesis(verse_ref)
        if exegesis:
            return exegesis.emotional_valence
        
        # Fallback to position-based calculation
        verse_num = verse.get('verse_number', 1)
        chapter = verse.get('chapter', 1)
        if not isinstance(verse_num, int):
            verse_num = 1
        if not isinstance(chapter, int):
            chapter = 1
            
        verse_mod = (verse_num % 5) * 0.02
        chapter_mod = (chapter % 10) * 0.01
        return min(1.0, max(0.0, base + verse_mod + chapter_mod - 0.05))
    
    def calculate_theological_weight(
        self, 
        verse: Dict[str, Any], 
        book_info: Dict[str, Any]
    ) -> float:
        """
        Calculate theological weight.
        
        Uses pre-computed high-weight verse set for O(1) lookup.
        
        Args:
            verse: Verse data dictionary.
            book_info: Book information dictionary.
            
        Returns:
            Theological weight value between 0.0 and 1.0.
        """
        category = book_info.get('category', 'historical')
        base = self.category_values.get(category, {}).get('theological', 0.5)
        
        verse_ref = verse.get('verse_reference', '')
        
        # Check for pre-computed exegesis first
        exegesis = get_verse_exegesis(verse_ref)
        if exegesis:
            return exegesis.theological_weight
        
        # Use pre-computed high theological weight set (O(1) lookup)
        if verse_ref in HIGH_THEOLOGICAL_WEIGHT_VERSES:
            base = min(1.0, base + 0.15)
        
        return base
    
    def calculate_sensory_intensity(
        self, 
        verse: Dict[str, Any], 
        book_info: Dict[str, Any]
    ) -> float:
        """
        Calculate sensory intensity.
        
        Args:
            verse: Verse data dictionary.
            book_info: Book information dictionary.
            
        Returns:
            Sensory intensity value between 0.0 and 1.0.
        """
        category = book_info.get('category', 'historical')
        
        # Check for pre-computed exegesis first
        verse_ref = verse.get('verse_reference', '')
        exegesis = get_verse_exegesis(verse_ref)
        if exegesis:
            return exegesis.sensory_intensity
        
        return self.category_values.get(category, {}).get('sensory', 0.5)
    
    def determine_narrative_function(self, verse: Dict[str, Any]) -> str:
        """
        Determine narrative function.
        
        Args:
            verse: Verse data dictionary.
            
        Returns:
            Narrative function string.
        """
        verse_ref = verse.get('verse_reference', '')
        exegesis = get_verse_exegesis(verse_ref)
        if exegesis:
            return exegesis.narrative_function.value
        
        # Use pre-computed function from data.precomputed
        verse_num = verse.get('verse_number', 1)
        if not isinstance(verse_num, int):
            verse_num = 1
        return get_narrative_function(verse_num)
    
    def determine_breath_rhythm(self, verse: Dict[str, Any]) -> str:
        """
        Determine breath rhythm.
        
        Args:
            verse: Verse data dictionary.
            
        Returns:
            Breath rhythm string.
        """
        verse_ref = verse.get('verse_reference', '')
        exegesis = get_verse_exegesis(verse_ref)
        if exegesis:
            return exegesis.breath_rhythm
        
        # Use pre-computed function from data.precomputed
        verse_num = verse.get('verse_number', 1)
        if not isinstance(verse_num, int):
            verse_num = 1
        return get_breath_rhythm(verse_num)
    
    def determine_register(self, book_info: Dict[str, Any]) -> str:
        """
        Determine register using pre-computed mapping.
        
        Args:
            book_info: Book information dictionary.
            
        Returns:
            Register string.
        """
        category = book_info.get('category', 'historical')
        # Use pre-computed register mapping (O(1) lookup)
        return CATEGORY_REGISTERS.get(category, 'narrative-standard')
    
    def calculate_all(
        self, 
        verse: Dict[str, Any], 
        book_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate all nine matrix elements.
        
        Prefers pre-computed data when available.
        
        Args:
            verse: Verse data dictionary.
            book_info: Book information dictionary.
            
        Returns:
            Dictionary with all matrix element values.
            
        Raises:
            MatrixCalculationError: If calculation fails.
        """
        verse_ref = verse.get('verse_reference', '')
        
        try:
            # Try to get fully pre-computed exegesis first
            exegesis = get_verse_exegesis(verse_ref)
            if exegesis:
                verse_num = verse.get('verse_number', 1)
                if not isinstance(verse_num, int):
                    verse_num = 1
                return {
                    'emotional_valence': exegesis.emotional_valence,
                    'theological_weight': exegesis.theological_weight,
                    'narrative_function': exegesis.narrative_function.value,
                    'sensory_intensity': exegesis.sensory_intensity,
                    'grammatical_complexity': round(0.5 + (verse_num % 3) * 0.1, 2),
                    'lexical_rarity': round(0.3 + (hash(verse_ref) % 40) / 100, 2),
                    'breath_rhythm': exegesis.breath_rhythm,
                    'register_baseline': self.determine_register(book_info)
                }
            
            # Fallback to computed values
            verse_num = verse.get('verse_number', 1)
            if not isinstance(verse_num, int):
                verse_num = 1
            return {
                'emotional_valence': round(self.calculate_emotional_valence(verse, book_info), 2),
                'theological_weight': round(self.calculate_theological_weight(verse, book_info), 2),
                'narrative_function': self.determine_narrative_function(verse),
                'sensory_intensity': round(self.calculate_sensory_intensity(verse, book_info), 2),
                'grammatical_complexity': round(0.5 + (verse_num % 3) * 0.1, 2),
                'lexical_rarity': round(0.3 + (hash(verse_ref) % 40) / 100, 2),
                'breath_rhythm': self.determine_breath_rhythm(verse),
                'register_baseline': self.determine_register(book_info)
            }
        except Exception as e:
            logger.error(f"Failed to calculate matrix for {verse_ref}: {e}")
            raise MatrixCalculationError(f"Matrix calculation failed: {e}") from e


# ============================================================================
# TONAL ADJUSTER
# ============================================================================

class TonalAdjuster:
    """
    Apply Hermeneutical.txt tonal principles.
    
    Analyzes and adjusts the tonal character of verses while
    preserving their native emotional honesty.
    """
    
    # Word lists for mood analysis
    JOY_WORDS: Tuple[str, ...] = (
        'rejoice', 'praise', 'blessed', 'glory', 'love', 'peace', 'joy', 'glad'
    )
    TERROR_WORDS: Tuple[str, ...] = (
        'death', 'destroy', 'wrath', 'judgment', 'curse', 'plague', 'fear', 'perish'
    )
    HEAVY_WORDS: Tuple[str, ...] = (
        'crucified', 'death', 'slaughter', 'destroy', 'perish'
    )
    TRANSCENDENT_WORDS: Tuple[str, ...] = (
        'resurrection', 'glory', 'throne', 'heaven', 'eternal'
    )
    
    def __init__(self, db: Optional[DatabaseManager] = None) -> None:
        """
        Initialize the tonal adjuster.
        
        Args:
            db: Optional database manager.
        """
        self.db = db or get_db()
    
    def _analyze_native_mood(self, text: str) -> str:
        """
        Analyze the native mood of verse text.
        
        Args:
            text: Verse text.
            
        Returns:
            Mood category string.
        """
        if not text:
            return 'neutral/expository'
        
        text_lower = text.lower()
        
        joy_count = sum(1 for w in self.JOY_WORDS if w in text_lower)
        terror_count = sum(1 for w in self.TERROR_WORDS if w in text_lower)
        
        if joy_count > terror_count:
            return 'joyful/celebratory'
        elif terror_count > joy_count:
            return 'fearful/solemn'
        else:
            return 'neutral/expository'
    
    def _determine_tonal_weight(self, text: str) -> str:
        """
        Determine tonal weight category.
        
        Args:
            text: Verse text.
            
        Returns:
            Tonal weight category string.
        """
        if not text:
            return 'neutral'
        
        text_lower = text.lower()
        
        if any(w in text_lower for w in self.HEAVY_WORDS):
            return 'heavy'
        elif any(w in text_lower for w in self.TRANSCENDENT_WORDS):
            return 'transcendent'
        elif any(w in text_lower for w in ('rejoice', 'praise', 'blessed', 'joy', 'glad')):
            return 'light'
        elif any(w in text_lower for w in ('warning', 'flee', 'fear', 'tremble', 'beware')):
            return 'unsettling'
        else:
            return 'neutral'
    
    def calculate_dread_amplification(self, verse: Dict[str, Any]) -> float:
        """
        Calculate dread amplification based on context.
        
        Args:
            verse: Verse data dictionary.
            
        Returns:
            Dread amplification value.
        """
        base = config.hermeneutical.base_dread_level
        
        text = verse.get('text_kjv', '') or ''
        text_lower = text.lower()
        
        # Heavy words increase dread
        heavy_words = ('death', 'judgment', 'wrath', 'curse', 'destroy', 'perish')
        heavy_count = sum(1 for w in heavy_words if w in text_lower)
        
        amplification = base + (heavy_count * 0.1)
        return min(config.hermeneutical.max_dread_amplification, amplification)
    
    def apply_tonal_adjustments(
        self, 
        verse: Dict[str, Any], 
        book_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply all tonal adjustments to a verse.
        
        Args:
            verse: Verse data dictionary.
            book_info: Book information dictionary.
            
        Returns:
            Dictionary with tonal adjustment values.
        """
        text = verse.get('text_kjv', '') or ''
        native_mood = self._analyze_native_mood(text)
        
        return {
            'tonal_weight': self._determine_tonal_weight(text),
            'dread_amplification': round(self.calculate_dread_amplification(verse), 2),
            'local_emotional_honesty': (
                f"Native emotional character preserved: {native_mood}. "
                f"This passage maintains its intrinsic mood while contributing "
                f"to the larger tonal architecture through contextual placement."
            ),
            'temporal_dislocation_offset': 0  # Default: no dislocation
        }


# ============================================================================
# ORBITAL RESONANCE CALCULATOR
# ============================================================================

class OrbitalResonanceCalculator:
    """
    Calculate orbital resonance positions per MASTER_PLAN.md.
    
    Manages motif tracking and activation across the narrative arc.
    """
    
    def __init__(self):
        self.ratios = config.orbital_resonance.harmonic_ratios
    
    def calculate_harmonic_positions(self, planting_page: int, 
                                     convergence_page: int) -> List[int]:
        """Calculate harmonic reinforcement positions"""
        distance = convergence_page - planting_page
        return [planting_page + int(distance * r) for r in self.ratios]
    
    def calculate_orbital_position(self, planting_page: int, 
                                   convergence_page: int,
                                   current_page: int) -> float:
        """Calculate current position in orbital trajectory (0.0 to 1.0)"""
        if convergence_page == planting_page:
            return 1.0
        
        return (current_page - planting_page) / (convergence_page - planting_page)
    
    def calculate_intensity_at_position(self, orbital_position: float) -> float:
        """Calculate intensity at current orbital position"""
        curve = config.orbital_resonance.intensity_curve
        
        if orbital_position <= 0.1:
            return curve['planting']
        elif orbital_position <= 0.3:
            return curve['early_reinforcement']
        elif orbital_position <= 0.6:
            return curve['mid_trajectory']
        elif orbital_position <= 0.85:
            return curve['low_point']
        else:
            return curve['convergence']
    
    def is_at_resonance_point(self, current_page: int, 
                              harmonic_positions: List[int],
                              tolerance: int = 25) -> Optional[int]:
        """Check if current page is at a resonance point"""
        for i, pos in enumerate(harmonic_positions):
            if abs(current_page - pos) <= tolerance:
                return i
        return None


# ============================================================================
# THREAD DENSITY MANAGER
# ============================================================================

class ThreadDensityManager:
    """Manage thread density per Stratified Foundation System"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.config = config.thread_density
    
    def calculate_density_at_page(self, page: int) -> Dict[str, Any]:
        """Calculate thread density at a specific page"""
        # Count active elements at this page
        layer_counts = {}
        
        # Query motifs by layer
        query = """
            SELECT foundation_layer, COUNT(*) as count
            FROM motifs
            WHERE %s BETWEEN planting_page AND convergence_page
            GROUP BY foundation_layer
        """
        
        rows = self.db.fetch_all(query, (page,))
        for row in rows:
            layer_counts[row['foundation_layer']] = row['count']
        
        # Calculate weighted total
        weights = self.config.layer_weights
        total = 0.0
        
        total += layer_counts.get('layer_one', 0) * weights.get('layer_one', 1.0)
        total += layer_counts.get('layer_two', 0) * weights.get('layer_two', 1.0)
        total += layer_counts.get('layer_three', 0) * weights.get('layer_three', 1.0)
        total += layer_counts.get('layer_four', 0) * weights.get('layer_four_approach', 1.0)
        total += layer_counts.get('layer_five', 0) * weights.get('layer_five_resonance', 3.0)
        
        within_bounds = self.config.target_minimum <= total <= self.config.target_maximum
        
        return {
            'page': page,
            'layer_counts': layer_counts,
            'total_density': total,
            'within_bounds': within_bounds,
            'recommendation': self._get_recommendation(total)
        }
    
    def _get_recommendation(self, density: float) -> str:
        """Get recommendation based on density"""
        if density < self.config.target_minimum:
            deficit = self.config.target_minimum - density
            return f"Density under minimum. Can add {deficit:.1f} thread-points."
        elif density > self.config.target_maximum:
            excess = density - self.config.target_maximum
            return f"Density over maximum. Must suspend {excess:.1f} thread-points."
        else:
            return "Density optimal."


# ============================================================================
# MAIN VERSE PROCESSOR
# ============================================================================

class VerseProcessor:
    """Main processor that coordinates all refinement operations"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.verse_repo = VerseRepository(self.db)
        self.motif_repo = MotifRepository(self.db)
        
        self.fourfold_generator = FourfoldSenseGenerator(self.db)
        self.matrix_calculator = NineMatrixCalculator()
        self.tonal_adjuster = TonalAdjuster(self.db)
        self.orbital_calculator = OrbitalResonanceCalculator()
        self.density_manager = ThreadDensityManager(self.db)
        
        self.stats = {
            'processed': 0,
            'success': 0,
            'failed': 0
        }
    
    def process_verse(self, verse_id: int) -> bool:
        """Process a single verse through the complete pipeline"""
        try:
            # Load verse with book info
            verse = self.db.fetch_one("""
                SELECT v.*, cb.name as book_name, cb.category, cb.canonical_order
                FROM verses v
                JOIN canonical_books cb ON v.book_id = cb.id
                WHERE v.id = %s
            """, (verse_id,))
            
            if not verse:
                return False
            
            book_info = {
                'name': verse['book_name'],
                'category': verse['category'],
                'canonical_order': verse['canonical_order']
            }
            
            # Generate fourfold senses
            senses = self.fourfold_generator.generate_all_senses(verse, book_info)
            
            # Calculate nine-matrix
            matrix = self.matrix_calculator.calculate_all(verse, book_info)
            
            # Apply tonal adjustments
            tonal = self.tonal_adjuster.apply_tonal_adjustments(verse, book_info)
            
            # Generate refined explication
            refined = self._generate_refined_explication(verse, senses, matrix, tonal)
            
            # Update verse in database
            self._update_verse(verse_id, senses, matrix, tonal, refined)
            
            self.stats['processed'] += 1
            self.stats['success'] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error processing verse {verse_id}: {e}")
            self.verse_repo.update_verse_status(verse_id, 'failed', str(e))
            self.stats['processed'] += 1
            self.stats['failed'] += 1
            return False
    
    def _generate_refined_explication(self, verse: Dict, senses: Dict, 
                                      matrix: Dict, tonal: Dict) -> str:
        """Generate the final refined explication"""
        return f"""
{senses['literal']}

Christologically, this passage {senses['allegorical'].lower() if senses['allegorical'] else 'reveals Christ hidden in the text.'}

For the reader's formation, this text {senses['tropological'].lower() if senses['tropological'] else 'shapes virtue and practice.'}

Looking toward the eschaton, we see how {senses['anagogical'].lower() if senses['anagogical'] else 'all things move toward consummation.'}

[Matrix: Emotional {matrix['emotional_valence']:.2f}, Theological {matrix['theological_weight']:.2f}, 
Sensory {matrix['sensory_intensity']:.2f}, Register: {matrix['register_baseline']}]
        """.strip()
    
    def _update_verse(self, verse_id: int, senses: Dict, matrix: Dict, 
                      tonal: Dict, refined: str):
        """Update verse with all calculated values"""
        query = """
            UPDATE verses SET
                sense_literal = %s,
                sense_allegorical = %s,
                sense_tropological = %s,
                sense_anagogical = %s,
                emotional_valence = %s,
                theological_weight = %s,
                narrative_function = %s,
                sensory_intensity = %s,
                grammatical_complexity = %s,
                lexical_rarity = %s,
                breath_rhythm = %s,
                register_baseline = %s,
                tonal_weight = %s,
                dread_amplification = %s,
                local_emotional_honesty = %s,
                temporal_dislocation_offset = %s,
                refined_explication = %s,
                status = 'refined',
                last_processed_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        
        self.db.execute(query, (
            senses['literal'],
            senses['allegorical'],
            senses['tropological'],
            senses['anagogical'],
            matrix['emotional_valence'],
            matrix['theological_weight'],
            matrix['narrative_function'],
            matrix['sensory_intensity'],
            matrix['grammatical_complexity'],
            matrix['lexical_rarity'],
            matrix['breath_rhythm'],
            matrix['register_baseline'],
            tonal['tonal_weight'],
            tonal['dread_amplification'],
            tonal['local_emotional_honesty'],
            tonal['temporal_dislocation_offset'],
            refined,
            verse_id
        ))
    
    def process_batch(self, batch_size: int = None) -> Dict[str, int]:
        """Process a batch of verses"""
        batch_size = batch_size or config.processing.batch_size
        
        verses = self.verse_repo.get_unprocessed_verses(batch_size)
        
        for verse in verses:
            self.process_verse(verse['id'])
            time.sleep(0.01)  # Small delay to prevent overwhelming
        
        logger.info(f"Batch complete: {self.stats['success']} success, {self.stats['failed']} failed")
        return self.stats.copy()
    
    def run_continuous(self, cooldown: int = 2):
        """Run continuous processing"""
        logger.info("Starting continuous verse processing...")
        
        while True:
            # Check remaining
            stats = self.verse_repo.get_completion_stats()
            unprocessed = stats.get('raw', 0) + stats.get('parsed', 0)
            
            if unprocessed == 0:
                logger.info("All verses processed!")
                break
            
            logger.info(f"Remaining unprocessed verses: {unprocessed}")
            self.process_batch()
            time.sleep(cooldown)
        
        return self.stats


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Main entry point for processing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Verse Processing')
    parser.add_argument('--batch', type=int, default=100, help='Batch size')
    parser.add_argument('--continuous', action='store_true', help='Run continuously')
    parser.add_argument('--verse-id', type=int, help='Process specific verse ID')
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    from scripts.database import init_db
    if not init_db():
        logger.error("Failed to initialize database")
        return 1
    
    processor = VerseProcessor()
    
    if args.verse_id:
        success = processor.process_verse(args.verse_id)
        return 0 if success else 1
    elif args.continuous:
        processor.run_continuous()
    else:
        processor.process_batch(args.batch)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
