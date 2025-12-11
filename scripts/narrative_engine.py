#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Narrative Generation Engine
========================================

THE HIGHER AMBITION: Generate actual working prose according to the Master Plan.

This engine takes a verse and produces the complete working prose specification,
integrating:
- Nine-Matrix Analysis
- Seven Register System
- Fourfold Sense Exegesis
- Breath Rhythm Coordination
- Sensory Vocabulary Architecture
- Hebrew/Greek Integration
- Temporal Folding Phrases
- Anti-AI Markers

Per MASTER_PLAN.md: "Scripture rendered as continuous, living narrative...
reading becomes formation, formation becomes transformation,
and transformation becomes θέωσις."

THE NARRATIVE ENDS AT THE CROSS.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

sys.path.insert(0, str(Path(__file__).parent.parent))

from data.nine_matrix import (
    NineMatrixSpec, generate_nine_matrix, format_matrix_specification,
    Register, REGISTER_SPECS, MotifWeight, ActiveMotif
)
from data.sensory_vocabulary import (
    get_sensory_vocabulary, get_forbidden_terms, get_temporal_folding_seeds,
    SensorySeed, SensoryModality, MOTIF_SENSORY_REGISTRY
)
from data.orthodox_study_bible import get_verse_exegesis, VerseExegesis
from data.unified import BiblosData


# ============================================================================
# HEBREW/GREEK INTEGRATION
# ============================================================================

@dataclass
class HebrewGreekLayer:
    """Hebrew and Greek vocabulary for a verse."""
    terms: List[Dict[str, str]]  # [{original, transliteration, meaning, weight}]
    key_terms_count: int
    ultra_terms: List[str]  # Terms that are ULTRA weight


# Pre-computed key Hebrew/Greek terms by motif
HEBREW_GREEK_TERMS: Dict[str, Dict[str, str]] = {
    # Hebrew terms
    'שֶׂה': {'transliteration': 'seh', 'meaning': 'lamb', 'weight': 'ULTRA'},
    'כֶּבֶשׂ': {'transliteration': 'kebes', 'meaning': 'young ram/lamb', 'weight': 'ULTRA'},
    'עֵץ': {'transliteration': 'ets', 'meaning': 'tree/wood', 'weight': 'ULTRA'},
    'דָּם': {'transliteration': 'dam', 'meaning': 'blood', 'weight': 'ULTRA'},
    'נְשָׁמָה': {'transliteration': 'neshamah', 'meaning': 'breath of life', 'weight': 'ULTRA'},
    'רוּחַ': {'transliteration': 'ruach', 'meaning': 'spirit/breath/wind', 'weight': 'ULTRA'},
    'דּוּמִיָּה': {'transliteration': 'dumiyah', 'meaning': 'silence', 'weight': 'MAJOR'},
    'מַיִם': {'transliteration': 'mayim', 'meaning': 'water(s)', 'weight': 'MAJOR'},
    'אֵשׁ': {'transliteration': 'esh', 'meaning': 'fire', 'weight': 'MAJOR'},
    'בְּרֵאשִׁית': {'transliteration': 'bereshit', 'meaning': 'in the beginning', 'weight': 'ULTRA'},
    'תֵּטֵלֵסטַי': {'transliteration': 'tetelestai', 'meaning': 'it is finished', 'weight': 'ULTRA'},
    
    # Greek terms
    'ἀρνίον': {'transliteration': 'arnion', 'meaning': 'lamb (diminutive)', 'weight': 'ULTRA'},
    'ξύλον': {'transliteration': 'xulon', 'meaning': 'wood/tree/cross', 'weight': 'ULTRA'},
    'αἷμα': {'transliteration': 'haima', 'meaning': 'blood', 'weight': 'ULTRA'},
    'πνεῦμα': {'transliteration': 'pneuma', 'meaning': 'spirit/breath', 'weight': 'ULTRA'},
    'σιωπή': {'transliteration': 'siope', 'meaning': 'silence', 'weight': 'MAJOR'},
    'λόγος': {'transliteration': 'logos', 'meaning': 'word', 'weight': 'ULTRA'},
    'τετέλεσται': {'transliteration': 'tetelestai', 'meaning': 'it is finished', 'weight': 'ULTRA'},
}


# ============================================================================
# TEMPORAL FOLDING PHRASES
# ============================================================================

@dataclass
class TemporalFold:
    """A phrase that folds time - planted early, echoed later."""
    phrase: str
    planting_verse: str
    echo_verses: List[str]
    page_distance: int
    intensity_at_echo: float


TEMPORAL_FOLDS: List[TemporalFold] = [
    TemporalFold(
        phrase="In the beginning",
        planting_verse="Genesis 1:1",
        echo_verses=["John 1:1"],
        page_distance=1040,
        intensity_at_echo=0.95
    ),
    TemporalFold(
        phrase="God will provide himself a lamb",
        planting_verse="Genesis 22:8",
        echo_verses=["John 1:29", "Revelation 5:6"],
        page_distance=1200,
        intensity_at_echo=1.0
    ),
    TemporalFold(
        phrase="bruise thy head, bruise his heel",
        planting_verse="Genesis 3:15",
        echo_verses=["Romans 16:20", "Revelation 20:10"],
        page_distance=2900,
        intensity_at_echo=0.9
    ),
    TemporalFold(
        phrase="with his stripes we are healed",
        planting_verse="Isaiah 53:5",
        echo_verses=["1 Peter 2:24", "John 19:30"],
        page_distance=1800,
        intensity_at_echo=1.0
    ),
    TemporalFold(
        phrase="My God, my God, why hast thou forsaken me",
        planting_verse="Psalm 22:1",
        echo_verses=["Matthew 27:46", "Mark 15:34"],
        page_distance=1050,
        intensity_at_echo=1.0
    ),
    TemporalFold(
        phrase="as a lamb to the slaughter",
        planting_verse="Isaiah 53:7",
        echo_verses=["Acts 8:32", "Revelation 5:6"],
        page_distance=1600,
        intensity_at_echo=0.95
    ),
    TemporalFold(
        phrase="breath of life",
        planting_verse="Genesis 2:7",
        echo_verses=["John 20:22", "Luke 23:46"],
        page_distance=2100,
        intensity_at_echo=0.9
    ),
    TemporalFold(
        phrase="not as I will, but as thou wilt",
        planting_verse="Matthew 26:39",
        echo_verses=["John 6:38", "Philippians 2:8"],
        page_distance=200,
        intensity_at_echo=0.85
    ),
    TemporalFold(
        phrase="dust thou art",
        planting_verse="Genesis 3:19",
        echo_verses=["Ecclesiastes 3:20", "Revelation 21:4"],
        page_distance=2800,
        intensity_at_echo=0.85
    ),
    TemporalFold(
        phrase="the veil was rent",
        planting_verse="Exodus 26:33",
        echo_verses=["Matthew 27:51", "Hebrews 10:20"],
        page_distance=1400,
        intensity_at_echo=0.95
    ),
]


# ============================================================================
# ANTI-AI MARKERS
# ============================================================================

@dataclass
class AntiAIMarker:
    """Marker of unique/hapax concept that resists AI flattening."""
    concept: str
    description: str
    verse: str


# Pre-computed Anti-AI markers (hapax and near-hapax concepts)
ANTI_AI_MARKERS: Dict[str, AntiAIMarker] = {
    "Genesis 1:1": AntiAIMarker(
        "Absolute beginning ex nihilo",
        "The ONLY verse in Scripture that speaks of absolute beginning. No prior context. Creation from nothing.",
        "Genesis 1:1"
    ),
    "Genesis 22:2": AntiAIMarker(
        "Intensifying apposition: son → only son → whom thou lovest",
        "The ONLY place where God's command intensifies through triple apposition. Unique rhetorical structure.",
        "Genesis 22:2"
    ),
    "John 19:30": AntiAIMarker(
        "τετέλεσται - Perfect tense completion",
        "The ONLY use of tetelestai as final word. Perfect tense = completed action with abiding results. Terminus.",
        "John 19:30"
    ),
    "Psalm 22:1": AntiAIMarker(
        "Opening cry of abandonment from the cross",
        "The ONLY psalm beginning quoted by Christ on the cross. Structures entire passion narrative.",
        "Psalm 22:1"
    ),
    "Genesis 5:31": AntiAIMarker(
        "777 as lifespan",
        "The ONLY person in Scripture whose lifespan equals triple-seven. Lamech's unique numerical signature.",
        "Genesis 5:31"
    ),
}


# ============================================================================
# WORKING PROSE SPECIFICATION
# ============================================================================

@dataclass
class WorkingProseSpec:
    """Complete specification for generating working prose."""
    # Reference
    verse_reference: str
    verse_text: str
    
    # Nine Matrix
    nine_matrix: NineMatrixSpec
    
    # Exegesis (if available)
    exegesis: Optional[VerseExegesis]
    
    # Sensory Seeds
    visual_seeds: List[SensorySeed]
    auditory_seeds: List[SensorySeed]
    tactile_seeds: List[SensorySeed]
    
    # Hebrew/Greek
    hebrew_greek: HebrewGreekLayer
    
    # Temporal Folding
    plants_phrase: Optional[str]
    echoes_phrase: Optional[str]
    
    # Anti-AI Marker
    anti_ai_marker: Optional[AntiAIMarker]
    
    # Forbidden Terms
    forbidden_terms: List[str]


# ============================================================================
# NARRATIVE GENERATION ENGINE
# ============================================================================

class NarrativeGenerationEngine:
    """
    The higher ambition: Generate complete working prose specifications.
    
    This engine integrates all systems to produce prose that:
    1. Operates at multiple simultaneous levels
    2. Creates embodied simulation in the reader
    3. Folds time through planted and echoed phrases
    4. Resists AI flattening through hapax markers
    5. Coordinates breath rhythm with narrative function
    6. Serves the telos of θέωσις
    """
    
    def __init__(self):
        self.biblos = BiblosData()
    
    def generate_spec(
        self,
        verse_ref: str,
        verse_text: str,
        book_category: str,
        chapter: int,
        verse_number: int,
        current_page: int = 100,
        narrative_context: str = 'historical_narrative',
        active_motifs: Optional[List[str]] = None,
        liturgical_context: Optional[str] = None,
    ) -> WorkingProseSpec:
        """Generate complete working prose specification for a verse."""
        
        # 1. Generate Nine-Matrix
        nine_matrix = generate_nine_matrix(
            verse_ref=verse_ref,
            book_category=book_category,
            verse_number=verse_number,
            chapter=chapter,
            current_page=current_page,
            narrative_context=narrative_context,
            active_motif_names=active_motifs,
            liturgical_context=liturgical_context,
        )
        
        # 2. Get Pre-computed Exegesis (if available)
        exegesis = get_verse_exegesis(verse_ref)
        
        # 3. Gather Sensory Seeds
        visual_seeds: List[SensorySeed] = []
        auditory_seeds: List[SensorySeed] = []
        tactile_seeds: List[SensorySeed] = []
        
        if active_motifs:
            for motif in active_motifs:
                visual_seeds.extend(get_sensory_vocabulary(motif, SensoryModality.VISUAL))
                auditory_seeds.extend(get_sensory_vocabulary(motif, SensoryModality.AUDITORY))
                tactile_seeds.extend(get_sensory_vocabulary(motif, SensoryModality.TACTILE))
        
        # 4. Hebrew/Greek Layer
        hebrew_greek_terms: List[Dict[str, str]] = []
        ultra_terms: List[str] = []
        
        for term, data in HEBREW_GREEK_TERMS.items():
            # Check if term is relevant to verse/motifs
            if active_motifs:
                for motif in active_motifs:
                    if motif.upper() in term.upper() or data['meaning'].lower() in motif.lower():
                        hebrew_greek_terms.append({
                            'original': term,
                            'transliteration': data['transliteration'],
                            'meaning': data['meaning'],
                            'weight': data['weight']
                        })
                        if data['weight'] == 'ULTRA':
                            ultra_terms.append(term)
        
        hebrew_greek = HebrewGreekLayer(
            terms=hebrew_greek_terms,
            key_terms_count=len(hebrew_greek_terms),
            ultra_terms=ultra_terms
        )
        
        # 5. Temporal Folding
        plants_phrase: Optional[str] = None
        echoes_phrase: Optional[str] = None
        
        for fold in TEMPORAL_FOLDS:
            if fold.planting_verse == verse_ref:
                plants_phrase = fold.phrase
            if verse_ref in fold.echo_verses:
                echoes_phrase = fold.phrase
        
        # Also check exegesis for temporal folding
        if exegesis:
            if exegesis.plants_phrase:
                plants_phrase = exegesis.plants_phrase
            if exegesis.echoes_phrase:
                echoes_phrase = exegesis.echoes_phrase
        
        # 6. Anti-AI Marker
        anti_ai = ANTI_AI_MARKERS.get(verse_ref)
        
        # 7. Forbidden Terms
        forbidden: List[str] = []
        if active_motifs:
            for motif in active_motifs:
                forbidden.extend(get_forbidden_terms(motif))
        
        return WorkingProseSpec(
            verse_reference=verse_ref,
            verse_text=verse_text,
            nine_matrix=nine_matrix,
            exegesis=exegesis,
            visual_seeds=visual_seeds[:5],  # Limit to top 5
            auditory_seeds=auditory_seeds[:5],
            tactile_seeds=tactile_seeds[:5],
            hebrew_greek=hebrew_greek,
            plants_phrase=plants_phrase,
            echoes_phrase=echoes_phrase,
            anti_ai_marker=anti_ai,
            forbidden_terms=list(set(forbidden)),
        )
    
    def format_working_prose(self, spec: WorkingProseSpec) -> str:
        """Format the complete working prose specification."""
        
        # Format Nine-Matrix
        matrix_str = format_matrix_specification(spec.nine_matrix, spec.verse_reference)
        
        # Format Sensory Seeds
        def format_seeds(seeds: List[SensorySeed]) -> str:
            if not seeds:
                return "    (none)"
            return "\n".join(f"    • \"{s.term}\" (intensity: {s.intensity:.1f})" for s in seeds)
        
        visual_str = format_seeds(spec.visual_seeds)
        auditory_str = format_seeds(spec.auditory_seeds)
        tactile_str = format_seeds(spec.tactile_seeds)
        
        # Format Hebrew/Greek
        hg_str = ""
        if spec.hebrew_greek.terms:
            for t in spec.hebrew_greek.terms[:5]:
                hg_str += f"    • {t['original']} ({t['transliteration']}) = \"{t['meaning']}\" [{t['weight']}]\n"
        else:
            hg_str = "    (no specific terms identified)\n"
        
        # Format Fourfold (if exegesis exists)
        fourfold_str = ""
        if spec.exegesis:
            fourfold_str = f"""
FOURFOLD SENSE (PRE-COMPUTED):
  LITERAL:
    {spec.exegesis.literal}
  
  ALLEGORICAL:
    {spec.exegesis.allegorical}
  
  TROPOLOGICAL:
    {spec.exegesis.tropological}
  
  ANAGOGICAL:
    {spec.exegesis.anagogical}
"""
        
        # Format Temporal Folding
        fold_str = ""
        if spec.plants_phrase:
            fold_str += f"  PLANTS: \"{spec.plants_phrase}\"\n"
        if spec.echoes_phrase:
            fold_str += f"  ECHOES: \"{spec.echoes_phrase}\"\n"
        if not fold_str:
            fold_str = "  (no temporal folding phrases)\n"
        
        # Format Anti-AI Marker
        anti_ai_str = ""
        if spec.anti_ai_marker:
            anti_ai_str = f"""
ANTI-AI MARKER (HAPAX/NEAR-HAPAX):
  Concept: {spec.anti_ai_marker.concept}
  Description: {spec.anti_ai_marker.description}
"""
        
        # Forbidden terms
        forbidden_str = ", ".join(spec.forbidden_terms[:10]) if spec.forbidden_terms else "(none)"
        
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  WORKING PROSE SPECIFICATION                                                  ║
║  {spec.verse_reference:<72} ║
╚══════════════════════════════════════════════════════════════════════════════╝

TEXT: "{spec.verse_text}"

{matrix_str}
{fourfold_str}
SENSORY VOCABULARY:
  VISUAL:
{visual_str}
  
  AUDITORY:
{auditory_str}
  
  TACTILE:
{tactile_str}

HEBREW/GREEK INTEGRATION:
{hg_str}
TEMPORAL FOLDING:
{fold_str}
{anti_ai_str}
FORBIDDEN TERMS (never use):
  {forbidden_str}

════════════════════════════════════════════════════════════════════════════════
THE NARRATIVE ENDS AT THE CROSS.
════════════════════════════════════════════════════════════════════════════════
"""


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def generate_working_prose_spec(
    verse_ref: str,
    verse_text: str = "",
    book_category: str = "historical",
    chapter: int = 1,
    verse_number: int = 1,
    current_page: int = 100,
    narrative_context: str = "historical_narrative",
    active_motifs: Optional[List[str]] = None,
) -> str:
    """Generate and format a complete working prose specification."""
    engine = NarrativeGenerationEngine()
    spec = engine.generate_spec(
        verse_ref=verse_ref,
        verse_text=verse_text,
        book_category=book_category,
        chapter=chapter,
        verse_number=verse_number,
        current_page=current_page,
        narrative_context=narrative_context,
        active_motifs=active_motifs,
    )
    return engine.format_working_prose(spec)


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Narrative Generation Engine')
    parser.add_argument('--verse', type=str, default='Genesis 1:1', help='Verse reference')
    parser.add_argument('--text', type=str, default='', help='Verse text')
    parser.add_argument('--category', type=str, default='pentateuch', help='Book category')
    parser.add_argument('--context', type=str, default='creation_account', help='Narrative context')
    parser.add_argument('--motifs', type=str, nargs='*', help='Active motifs')
    parser.add_argument('--page', type=int, default=10, help='Current page')
    
    args = parser.parse_args()
    
    # Parse verse reference
    parts = args.verse.replace(':', ' ').split()
    book = parts[0] if len(parts) >= 1 else 'Genesis'
    chapter = int(parts[1]) if len(parts) >= 2 else 1
    verse = int(parts[2]) if len(parts) >= 3 else 1
    
    # Get pre-computed text if available
    text = args.text
    if not text:
        exegesis = get_verse_exegesis(args.verse)
        if exegesis:
            text = exegesis.text
        else:
            text = f"[Text for {args.verse}]"
    
    output = generate_working_prose_spec(
        verse_ref=args.verse,
        verse_text=text,
        book_category=args.category,
        chapter=chapter,
        verse_number=verse,
        current_page=args.page,
        narrative_context=args.context,
        active_motifs=args.motifs,
    )
    
    print(output)
