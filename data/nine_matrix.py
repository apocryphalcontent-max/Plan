#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Nine-Matrix Specification System
=============================================

The Nine-Matrix is the analytical foundation for generating working prose.
Each verse receives a complete specification that governs how it will be rendered.

Per MASTER_PLAN.md Part Four:
1. Fourfold Sense Distribution (literal, allegorical, tropological, anagogical)
2. Active Motifs (with ULTRA/MAJOR/sustain weights)
3. Breath Rhythm (7-7-3 syllable patterns)
4. Negative Motifs (vacuum pressure)
5. Sentence Architecture (compound minimum to Miltonic depth)
6. Typological Density (number of active types)
7. Orbital Resonance (position in harmonic trajectory)
8. Liturgical Calendar (feast/fast resonance)
9. Character Voice (which of seven registers controls)

THE NARRATIVE ENDS AT THE CROSS.
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# FOURFOLD SENSE DISTRIBUTION
# ============================================================================

@dataclass(frozen=True)
class FourfoldDistribution:
    """Distribution of the four senses for a verse."""
    literal: int       # Percentage (0-100)
    allegorical: int   # Percentage
    tropological: int  # Percentage
    anagogical: int    # Percentage
    
    def __post_init__(self):
        if self.literal + self.allegorical + self.tropological + self.anagogical != 100:
            raise ValueError("Fourfold distribution must sum to 100%")


# Pre-computed distributions by context
FOURFOLD_PRESETS: Dict[str, FourfoldDistribution] = {
    'historical_narrative': FourfoldDistribution(55, 20, 18, 7),
    'gospel_cosmic': FourfoldDistribution(45, 30, 18, 7),
    'apocalyptic_vision': FourfoldDistribution(35, 8, 2, 55),
    'wisdom_ethical': FourfoldDistribution(15, 2, 75, 8),
    'prophetic_oracular': FourfoldDistribution(40, 35, 10, 15),
    'passion_narrative': FourfoldDistribution(60, 25, 10, 5),
    'creation_account': FourfoldDistribution(50, 30, 10, 10),
    'psalm_lament': FourfoldDistribution(45, 20, 25, 10),
    'epistle_doctrinal': FourfoldDistribution(35, 25, 30, 10),
}


# ============================================================================
# MOTIF WEIGHT SYSTEM
# ============================================================================

class MotifWeight(Enum):
    """Weight levels for motifs per MASTER_PLAN.md"""
    ULTRA = 10     # Maximum weight - central to entire work (LAMB, SILENCE, WOOD)
    ICONIC = 9     # Near-maximum - iconic moments
    MAJOR = 8      # High importance - structural motifs
    SUSTAINED = 7  # Sustained presence
    MODERATE = 5   # Regular motif
    MINOR = 3      # Background motif
    PLANT = 2      # Newly planted seed


@dataclass
class ActiveMotif:
    """A motif active in a verse."""
    name: str
    weight: MotifWeight
    hebrew: Optional[str] = None
    greek: Optional[str] = None
    action: str = "sustain"  # sustain, plant, echo, intensify


# Pre-computed ULTRA-weight motifs (central to entire work)
ULTRA_MOTIFS: Dict[str, Dict[str, Any]] = {
    'LAMB': {
        'hebrew': 'שֶׂה / כֶּבֶשׂ',
        'greek': 'ἀρνίον / ἀμνός',
        'planting_page': 50,
        'convergence_page': 2400,
        'sensory_vocabulary': ('wool beneath hand', 'bleating', 'bloodied fleece'),
    },
    'WOOD': {
        'hebrew': 'עֵץ',
        'greek': 'ξύλον',
        'planting_page': 20,
        'convergence_page': 2200,
        'sensory_vocabulary': ('grain of wood', 'splinters', 'weight on shoulder'),
    },
    'SILENCE': {
        'hebrew': 'דּוּמִיָּה / חָרַשׁ',
        'greek': 'σιγή / σιωπή',
        'planting_page': 100,
        'convergence_page': 2200,
        'sensory_vocabulary': ('absence of sound', 'held breath', 'stillness'),
    },
    'BLOOD': {
        'hebrew': 'דָּם',
        'greek': 'αἷμα',
        'planting_page': 50,
        'convergence_page': 2200,
        'sensory_vocabulary': ('copper taste', 'warmth flowing', 'crimson spreading'),
    },
    'BREATH': {
        'hebrew': 'נְשָׁמָה / רוּחַ',
        'greek': 'πνεῦμα',
        'planting_page': 10,
        'convergence_page': 2400,
        'sensory_vocabulary': ('air entering lungs', 'last exhalation', 'spirit departing'),
    },
}


# ============================================================================
# BREATH RHYTHM PATTERNS
# ============================================================================

class BreathPhase(Enum):
    """Breath rhythm phases."""
    INHALE = "inhale"      # Reception, intake (7 syllables default)
    EXHALE = "exhale"      # Release, surrender (7 syllables default)
    HESYCHAST = "hesychast"  # Contemplative pause (3 syllables default)


@dataclass
class BreathPattern:
    """Breath rhythm specification for a verse."""
    phase: BreathPhase
    syllables: Tuple[int, int, int]  # (inhale, exhale, hesychast)
    note: str = ""


# Pre-computed breath patterns by narrative function
BREATH_PATTERNS: Dict[str, BreathPattern] = {
    'scene_setting': BreathPattern(BreathPhase.INHALE, (7, 7, 3), "Balanced reception"),
    'exposition': BreathPattern(BreathPhase.INHALE, (8, 6, 3), "Extended intake"),
    'development': BreathPattern(BreathPhase.INHALE, (7, 7, 3), "Sustained rhythm"),
    'intensification': BreathPattern(BreathPhase.INHALE, (9, 5, 2), "Building pressure"),
    'climax': BreathPattern(BreathPhase.EXHALE, (10, 5, 0), "Maximum tension, no rest"),
    'resolution': BreathPattern(BreathPhase.HESYCHAST, (6, 6, 5), "Extended contemplation"),
    'apocalyptic': BreathPattern(BreathPhase.INHALE, (10, 10, 0), "Relentless accumulation"),
}


# ============================================================================
# THE SEVEN REGISTER SYSTEM
# ============================================================================

class Register(Enum):
    """The Seven Registers per MASTER_PLAN.md Section XIII"""
    ONE_WANDERING = 1    # Baseline (60-70%), paratactic, vigilant witness-voice
    TWO_WAITING = 2      # Meditative depth, deep subordination
    THREE_BREAKTHROUGH = 3  # Prophetic intensity for theophanies
    FOUR_CLEARING = 4    # Intimate presence, consolation
    FIVE_RECKONING = 5   # Dissonant triumph, victory + tragedy
    SIX_SILENCE = 6      # Withholding, subliminal unease
    SEVEN_BURNING = 7    # Unflinching witness of horror


@dataclass
class RegisterSpec:
    """Specification for a register."""
    name: str
    description: str
    percentage_typical: int  # Typical percentage of narrative
    syntactic_style: str
    vocabulary_register: str
    breath_emphasis: str
    fourfold_modulation: Dict[str, float]  # Multipliers for fourfold distribution


REGISTER_SPECS: Dict[Register, RegisterSpec] = {
    Register.ONE_WANDERING: RegisterSpec(
        name="Wandering Variance",
        description="Baseline exposed, vigilant witness-voice through paratactic chaining and sensory concreteness",
        percentage_typical=65,
        syntactic_style="paratactic, compound sentences",
        vocabulary_register="concrete Anglo-Saxon",
        breath_emphasis="balanced 7-7-3",
        fourfold_modulation={'literal': 1.1, 'allegorical': 0.9, 'tropological': 1.0, 'anagogical': 0.8}
    ),
    Register.TWO_WAITING: RegisterSpec(
        name="Waiting/Tangle Variance",
        description="Meditative depth through deep subordination, suspending between promise and fulfillment",
        percentage_typical=10,
        syntactic_style="complex subordination, suspensive periods",
        vocabulary_register="mixed, tending abstract",
        breath_emphasis="extended 9-7-5",
        fourfold_modulation={'literal': 0.9, 'allegorical': 1.2, 'tropological': 0.9, 'anagogical': 1.1}
    ),
    Register.THREE_BREAKTHROUGH: RegisterSpec(
        name="Breakthrough Variance",
        description="Prophetic intensity for theophanies and divine ruptures",
        percentage_typical=5,
        syntactic_style="elevated periodic, Miltonic subordination",
        vocabulary_register="Latinate, liturgical",
        breath_emphasis="explosive 10-5-0",
        fourfold_modulation={'literal': 0.7, 'allegorical': 1.0, 'tropological': 0.6, 'anagogical': 1.8}
    ),
    Register.FOUR_CLEARING: RegisterSpec(
        name="Clearing Variance",
        description="Intimate presence for moments of consolation and tenderness",
        percentage_typical=8,
        syntactic_style="simple declarative, direct address",
        vocabulary_register="tender, personal",
        breath_emphasis="soft 6-8-4",
        fourfold_modulation={'literal': 1.0, 'allegorical': 0.8, 'tropological': 1.3, 'anagogical': 0.9}
    ),
    Register.FIVE_RECKONING: RegisterSpec(
        name="Reckoning Variance",
        description="Dissonant triumph where victory and tragedy coexist",
        percentage_typical=5,
        syntactic_style="antithetical, balanced oppositions",
        vocabulary_register="judicial, covenantal",
        breath_emphasis="sharp 7-3-7",
        fourfold_modulation={'literal': 1.0, 'allegorical': 1.1, 'tropological': 1.1, 'anagogical': 1.0}
    ),
    Register.SIX_SILENCE: RegisterSpec(
        name="Silence Variance",
        description="Withholding to create subliminal unease through absence and ellipsis",
        percentage_typical=4,
        syntactic_style="elliptical, fragmentary",
        vocabulary_register="sparse, withheld",
        breath_emphasis="broken 4-0-8",
        fourfold_modulation={'literal': 0.8, 'allegorical': 1.0, 'tropological': 1.0, 'anagogical': 1.2}
    ),
    Register.SEVEN_BURNING: RegisterSpec(
        name="Burning Variance",
        description="Removes all filters for unflinching witness of horror and destruction",
        percentage_typical=3,
        syntactic_style="relentless accumulation, asyndeton",
        vocabulary_register="raw, visceral",
        breath_emphasis="no rest 12-0-0",
        fourfold_modulation={'literal': 1.4, 'allegorical': 0.5, 'tropological': 1.0, 'anagogical': 0.6}
    ),
}


# ============================================================================
# NINE-MATRIX SPECIFICATION
# ============================================================================

@dataclass
class NineMatrixSpec:
    """Complete Nine-Matrix specification for a verse."""
    # 1. Fourfold Sense Distribution
    fourfold: FourfoldDistribution
    
    # 2. Active Motifs
    active_motifs: List[ActiveMotif]
    
    # 3. Breath Rhythm
    breath: BreathPattern
    
    # 4. Negative Motifs (vacuum pressure)
    negative_motifs: List[str]
    pages_since_appearance: Dict[str, int]
    
    # 5. Sentence Architecture
    sentence_style: str
    syntactic_complexity: float  # 0.0 (simple) to 1.0 (Miltonic)
    
    # 6. Typological Density
    typological_count: int
    explicit_percentage: int
    type_references: List[str]
    
    # 7. Orbital Resonance
    orbital_position: float  # 0.0 to 1.0
    intensity: float
    approaching_perihelion: bool
    harmonic_page: Optional[int]
    
    # 8. Liturgical Calendar
    liturgical_season: Optional[str]
    feast_resonance: Optional[str]
    
    # 9. Character Voice / Register
    primary_register: Register
    secondary_register: Optional[Register]
    register_percentage: Tuple[int, int]  # (primary%, secondary%)


# ============================================================================
# SPECIFICATION GENERATOR
# ============================================================================

def generate_nine_matrix(
    verse_ref: str,
    book_category: str,
    verse_number: int,
    chapter: int,
    current_page: int,
    narrative_context: str = 'historical_narrative',
    active_motif_names: Optional[List[str]] = None,
    liturgical_context: Optional[str] = None,
) -> NineMatrixSpec:
    """
    Generate a complete Nine-Matrix specification for a verse.
    
    This is the analytical foundation for prose generation.
    """
    
    # 1. Fourfold Sense Distribution
    fourfold = FOURFOLD_PRESETS.get(
        narrative_context, 
        FOURFOLD_PRESETS['historical_narrative']
    )
    
    # 2. Active Motifs
    active_motifs = []
    if active_motif_names:
        for name in active_motif_names:
            if name.upper() in ULTRA_MOTIFS:
                motif_data = ULTRA_MOTIFS[name.upper()]
                active_motifs.append(ActiveMotif(
                    name=name.upper(),
                    weight=MotifWeight.ULTRA,
                    hebrew=motif_data.get('hebrew'),
                    greek=motif_data.get('greek'),
                    action='sustain'
                ))
            else:
                active_motifs.append(ActiveMotif(
                    name=name,
                    weight=MotifWeight.MODERATE,
                    action='sustain'
                ))
    
    # 3. Breath Rhythm
    if verse_number <= 3:
        breath = BREATH_PATTERNS['scene_setting']
    elif verse_number <= 8:
        breath = BREATH_PATTERNS['exposition']
    elif verse_number <= 15:
        breath = BREATH_PATTERNS['development']
    elif verse_number <= 20:
        breath = BREATH_PATTERNS['intensification']
    elif verse_number <= 25:
        breath = BREATH_PATTERNS['climax']
    else:
        breath = BREATH_PATTERNS['resolution']
    
    # 4. Negative Motifs (vacuum pressure calculation)
    negative_motifs: List[str] = []
    pages_since: Dict[str, int] = {}
    
    # 5. Sentence Architecture
    complexity = min(1.0, 0.3 + (chapter / 50) + (verse_number / 100))
    if narrative_context in ('apocalyptic_vision', 'prophetic_oracular'):
        complexity = min(1.0, complexity + 0.2)
    
    sentence_style = "paratactic compound" if complexity < 0.4 else \
                     "balanced complex" if complexity < 0.7 else \
                     "elevated periodic"
    
    # 6. Typological Density
    typological_count = 0
    type_refs: List[str] = []
    if book_category in ('pentateuch', 'major_prophet'):
        typological_count = min(100, 20 + verse_number * 2)
    elif book_category == 'gospel':
        typological_count = min(100, 40 + verse_number)
    else:
        typological_count = min(100, 10 + verse_number)
    
    # 7. Orbital Resonance
    # For LAMB motif (example calculation)
    lamb_data = ULTRA_MOTIFS['LAMB']
    planting = lamb_data['planting_page']
    convergence = lamb_data['convergence_page']
    if current_page >= planting:
        orbital_position = min(1.0, (current_page - planting) / (convergence - planting))
    else:
        orbital_position = 0.0
    
    from data.precomputed import get_intensity_for_position
    intensity = get_intensity_for_position(orbital_position)
    
    # 8. Liturgical Calendar
    liturgical_season = liturgical_context
    feast_resonance = None
    if liturgical_context == 'pascha':
        feast_resonance = "Paschal Victory"
    elif liturgical_context == 'great_lent':
        feast_resonance = "Penitential Preparation"
    
    # 9. Register Determination
    if book_category == 'apocalyptic':
        primary_register = Register.THREE_BREAKTHROUGH
        secondary_register = Register.SEVEN_BURNING
        register_pct = (70, 30)
    elif book_category == 'poetic':
        primary_register = Register.TWO_WAITING
        secondary_register = Register.ONE_WANDERING
        register_pct = (60, 40)
    elif narrative_context == 'passion_narrative':
        primary_register = Register.SEVEN_BURNING
        secondary_register = Register.SIX_SILENCE
        register_pct = (65, 35)
    else:
        primary_register = Register.ONE_WANDERING
        secondary_register = Register.FOUR_CLEARING
        register_pct = (75, 25)
    
    return NineMatrixSpec(
        fourfold=fourfold,
        active_motifs=active_motifs,
        breath=breath,
        negative_motifs=negative_motifs,
        pages_since_appearance=pages_since,
        sentence_style=sentence_style,
        syntactic_complexity=complexity,
        typological_count=typological_count,
        explicit_percentage=min(100, 60 + typological_count // 5),
        type_references=type_refs,
        orbital_position=orbital_position,
        intensity=intensity,
        approaching_perihelion=orbital_position > 0.85,
        harmonic_page=None,
        liturgical_season=liturgical_season,
        feast_resonance=feast_resonance,
        primary_register=primary_register,
        secondary_register=secondary_register,
        register_percentage=register_pct,
    )


# ============================================================================
# PROSE SPECIFICATION OUTPUT
# ============================================================================

def format_matrix_specification(spec: NineMatrixSpec, verse_ref: str) -> str:
    """Format the Nine-Matrix specification as a prose generation guide."""
    
    # Format motifs
    motif_lines = []
    for m in spec.active_motifs:
        hebrew = f" ({m.hebrew})" if m.hebrew else ""
        motif_lines.append(f"    {m.name}{hebrew} — {m.weight.name} {m.weight.value}/10, {m.action}")
    motif_str = "\n".join(motif_lines) if motif_lines else "    None active"
    
    # Get register specs
    primary_spec = REGISTER_SPECS[spec.primary_register]
    secondary_spec = REGISTER_SPECS[spec.secondary_register] if spec.secondary_register else None
    
    return f"""
╔══════════════════════════════════════════════════════════════════╗
║  NINE-MATRIX SPECIFICATION: {verse_ref:<34} ║
╚══════════════════════════════════════════════════════════════════╝

1. FOURFOLD SENSE DISTRIBUTION
   ├── Literal:      {spec.fourfold.literal}%
   ├── Allegorical:  {spec.fourfold.allegorical}%
   ├── Tropological: {spec.fourfold.tropological}%
   └── Anagogical:   {spec.fourfold.anagogical}%

2. ACTIVE MOTIFS
{motif_str}

3. BREATH RHYTHM
   ├── Phase: {spec.breath.phase.value}
   ├── Pattern: {spec.breath.syllables[0]}-{spec.breath.syllables[1]}-{spec.breath.syllables[2]}
   └── Note: {spec.breath.note}

4. NEGATIVE MOTIFS (Vacuum Pressure)
   └── {', '.join(spec.negative_motifs) if spec.negative_motifs else 'None currently absent'}

5. SENTENCE ARCHITECTURE
   ├── Style: {spec.sentence_style}
   └── Complexity: {spec.syntactic_complexity:.2f} (0=simple, 1=Miltonic)

6. TYPOLOGICAL DENSITY
   ├── Active Types: {spec.typological_count}
   ├── Explicit: {spec.explicit_percentage}%
   └── References: {', '.join(spec.type_references) if spec.type_references else 'See canonical connections'}

7. ORBITAL RESONANCE
   ├── Position: {spec.orbital_position:.3f}
   ├── Intensity: {spec.intensity:.2f}
   ├── Approaching Perihelion: {'YES' if spec.approaching_perihelion else 'No'}
   └── Harmonic Page: {spec.harmonic_page if spec.harmonic_page else 'N/A'}

8. LITURGICAL CALENDAR
   ├── Season: {spec.liturgical_season or 'Ordinary time'}
   └── Feast Resonance: {spec.feast_resonance or 'None'}

9. REGISTER SPECIFICATION
   ├── Primary: Register {spec.primary_register.value} ({primary_spec.name}) [{spec.register_percentage[0]}%]
   │   ├── Syntax: {primary_spec.syntactic_style}
   │   ├── Vocabulary: {primary_spec.vocabulary_register}
   │   └── Breath: {primary_spec.breath_emphasis}
   └── Secondary: {f"Register {spec.secondary_register.value} ({secondary_spec.name}) [{spec.register_percentage[1]}%]" if secondary_spec else "None"}

══════════════════════════════════════════════════════════════════════
"""


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Nine-Matrix Specification')
    parser.add_argument('--verse', type=str, default='Genesis 1:1', help='Verse reference')
    parser.add_argument('--page', type=int, default=10, help='Current page number')
    parser.add_argument('--context', type=str, default='creation_account', 
                       help='Narrative context')
    parser.add_argument('--motifs', type=str, nargs='*', help='Active motif names')
    
    args = parser.parse_args()
    
    # Parse verse reference
    parts = args.verse.replace(':', ' ').split()
    book = parts[0] if len(parts) >= 1 else 'Genesis'
    chapter = int(parts[1]) if len(parts) >= 2 else 1
    verse = int(parts[2]) if len(parts) >= 3 else 1
    
    spec = generate_nine_matrix(
        verse_ref=args.verse,
        book_category='pentateuch' if book == 'Genesis' else 'historical',
        verse_number=verse,
        chapter=chapter,
        current_page=args.page,
        narrative_context=args.context,
        active_motif_names=args.motifs,
    )
    
    print(format_matrix_specification(spec, args.verse))
