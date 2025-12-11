#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Sensory Vocabulary Architecture
============================================

Per MASTER_PLAN.md: "The reader does not merely read; the reader's body simulates."

This module provides the sensory vocabulary that creates embodied simulation
in the reader. Every motif carries visual, auditory, and tactile seeds that
accumulate across thousands of pages, creating bodily memory.

THE NARRATIVE ENDS AT THE CROSS.
When the reader reaches John 19:30, their body already knows:
- the weight of wood on shoulder
- the sound of silence before sacrifice
- the warmth of blood flowing
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# SENSORY MODALITIES
# ============================================================================

class SensoryModality(Enum):
    """The five sensory channels plus proprioception."""
    VISUAL = "visual"
    AUDITORY = "auditory"
    TACTILE = "tactile"
    OLFACTORY = "olfactory"
    GUSTATORY = "gustatory"
    PROPRIOCEPTIVE = "proprioceptive"  # Body position, weight, movement


@dataclass
class SensorySeed:
    """A single sensory vocabulary item."""
    term: str
    modality: SensoryModality
    intensity: float  # 0.0 (subtle) to 1.0 (overwhelming)
    hebrew_connection: Optional[str] = None
    greek_connection: Optional[str] = None
    temporal_folding: Optional[str] = None  # Phrase this plants/echoes


# ============================================================================
# MOTIF SENSORY VOCABULARIES
# ============================================================================

@dataclass
class MotifSensory:
    """Complete sensory vocabulary for a motif."""
    motif_name: str
    visual: Tuple[SensorySeed, ...]
    auditory: Tuple[SensorySeed, ...]
    tactile: Tuple[SensorySeed, ...]
    olfactory: Tuple[SensorySeed, ...]
    gustatory: Tuple[SensorySeed, ...]
    proprioceptive: Tuple[SensorySeed, ...]
    forbidden_terms: Tuple[str, ...]  # Never use these (modern, breaking period)
    
    # Class-level constant for sensory attribute names
    SENSORY_ATTRIBUTES = ('visual', 'auditory', 'tactile', 'olfactory', 'gustatory', 'proprioceptive')
    
    def get_all_seeds(self) -> List[SensorySeed]:
        """Get all sensory seeds from all modalities."""
        seeds: List[SensorySeed] = []
        for attr in self.SENSORY_ATTRIBUTES:
            seeds.extend(getattr(self, attr, ()))
        return seeds


LAMB_SENSORY = MotifSensory(
    motif_name="LAMB",
    visual=(
        SensorySeed("wool white against dark", SensoryModality.VISUAL, 0.6, "שֶׂה"),
        SensorySeed("blood spreading through fleece", SensoryModality.VISUAL, 0.9),
        SensorySeed("eyes of the lamb unblinking", SensoryModality.VISUAL, 0.8),
        SensorySeed("knife catching light", SensoryModality.VISUAL, 0.85),
        SensorySeed("crimson pooling beneath", SensoryModality.VISUAL, 0.95),
    ),
    auditory=(
        SensorySeed("bleating that ceases", SensoryModality.AUDITORY, 0.7),
        SensorySeed("silence where bleating was", SensoryModality.AUDITORY, 0.9, temporal_folding="silence of the Lamb"),
        SensorySeed("wool rustling", SensoryModality.AUDITORY, 0.3),
        SensorySeed("blood dripping", SensoryModality.AUDITORY, 0.6),
    ),
    tactile=(
        SensorySeed("wool beneath fingers", SensoryModality.TACTILE, 0.5),
        SensorySeed("warmth of living creature", SensoryModality.TACTILE, 0.6),
        SensorySeed("warmth draining away", SensoryModality.TACTILE, 0.85),
        SensorySeed("weight of small body", SensoryModality.TACTILE, 0.4),
        SensorySeed("stillness where struggle was", SensoryModality.TACTILE, 0.8),
    ),
    olfactory=(
        SensorySeed("lanolin and dust", SensoryModality.OLFACTORY, 0.4),
        SensorySeed("copper of blood", SensoryModality.OLFACTORY, 0.8),
        SensorySeed("burnt offering rising", SensoryModality.OLFACTORY, 0.7),
    ),
    gustatory=(
        SensorySeed("paschal meat between teeth", SensoryModality.GUSTATORY, 0.5),
        SensorySeed("bitter herbs", SensoryModality.GUSTATORY, 0.6),
    ),
    proprioceptive=(
        SensorySeed("lamb held to chest", SensoryModality.PROPRIOCEPTIVE, 0.5),
        SensorySeed("arm raised with knife", SensoryModality.PROPRIOCEPTIVE, 0.9),
        SensorySeed("kneeling to apply blood", SensoryModality.PROPRIOCEPTIVE, 0.7),
    ),
    forbidden_terms=("livestock", "sheep farming", "wool industry", "slaughterhouse"),
)


WOOD_SENSORY = MotifSensory(
    motif_name="WOOD",
    visual=(
        SensorySeed("grain of wood running", SensoryModality.VISUAL, 0.5),
        SensorySeed("splinters catching skin", SensoryModality.VISUAL, 0.7),
        SensorySeed("wood laid on young shoulders", SensoryModality.VISUAL, 0.9, "עֵץ", temporal_folding="wood on shoulder"),
        SensorySeed("crossbeam silhouetted", SensoryModality.VISUAL, 0.95),
        SensorySeed("tree of knowledge", SensoryModality.VISUAL, 0.8, "עֵץ הַדַּעַת"),
        SensorySeed("tree of life", SensoryModality.VISUAL, 0.85, "עֵץ הַחַיִּים"),
    ),
    auditory=(
        SensorySeed("wood creaking under weight", SensoryModality.AUDITORY, 0.7),
        SensorySeed("nail driven through grain", SensoryModality.AUDITORY, 0.95),
        SensorySeed("dragging of beam", SensoryModality.AUDITORY, 0.8),
    ),
    tactile=(
        SensorySeed("rough bark beneath palm", SensoryModality.TACTILE, 0.5),
        SensorySeed("splinter entering flesh", SensoryModality.TACTILE, 0.85),
        SensorySeed("weight of beam on shoulder", SensoryModality.TACTILE, 0.9, temporal_folding="burden on shoulder"),
        SensorySeed("smoothness of worked wood", SensoryModality.TACTILE, 0.3),
    ),
    olfactory=(
        SensorySeed("cedar and cypress", SensoryModality.OLFACTORY, 0.4),
        SensorySeed("sap weeping from cut", SensoryModality.OLFACTORY, 0.5),
    ),
    gustatory=(),  # Wood has no gustatory associations
    proprioceptive=(
        SensorySeed("staggering under beam", SensoryModality.PROPRIOCEPTIVE, 0.9),
        SensorySeed("arms spread against wood", SensoryModality.PROPRIOCEPTIVE, 0.95),
        SensorySeed("climbing tree", SensoryModality.PROPRIOCEPTIVE, 0.4),
    ),
    forbidden_terms=("lumber", "timber industry", "deforestation", "carpentry shop"),
)


BLOOD_SENSORY = MotifSensory(
    motif_name="BLOOD",
    visual=(
        SensorySeed("crimson spreading", SensoryModality.VISUAL, 0.9),
        SensorySeed("blood on doorpost", SensoryModality.VISUAL, 0.85, "דָּם"),
        SensorySeed("pool forming beneath", SensoryModality.VISUAL, 0.95),
        SensorySeed("drops falling from wound", SensoryModality.VISUAL, 0.8),
        SensorySeed("blood and water mingling", SensoryModality.VISUAL, 0.95, temporal_folding="blood and water"),
    ),
    auditory=(
        SensorySeed("blood dripping to stone", SensoryModality.AUDITORY, 0.7),
        SensorySeed("cry of blood from ground", SensoryModality.AUDITORY, 0.9, "קוֹל דְּמֵי"),
    ),
    tactile=(
        SensorySeed("warmth of blood on hands", SensoryModality.TACTILE, 0.8),
        SensorySeed("stickiness between fingers", SensoryModality.TACTILE, 0.7),
        SensorySeed("blood drying, stiffening", SensoryModality.TACTILE, 0.6),
    ),
    olfactory=(
        SensorySeed("copper scent of blood", SensoryModality.OLFACTORY, 0.9),
        SensorySeed("iron-tang in air", SensoryModality.OLFACTORY, 0.8),
    ),
    gustatory=(
        SensorySeed("blood on lips", SensoryModality.GUSTATORY, 0.7),
        SensorySeed("wine become blood", SensoryModality.GUSTATORY, 0.95, "αἷμα", temporal_folding="cup of blood"),
    ),
    proprioceptive=(
        SensorySeed("life draining", SensoryModality.PROPRIOCEPTIVE, 0.95),
        SensorySeed("weakness spreading through limbs", SensoryModality.PROPRIOCEPTIVE, 0.9),
    ),
    forbidden_terms=("bloodshed", "bloody", "gore", "hemorrhage"),
)


SILENCE_SENSORY = MotifSensory(
    motif_name="SILENCE",
    visual=(
        SensorySeed("mouths closed", SensoryModality.VISUAL, 0.6),
        SensorySeed("stillness of held breath", SensoryModality.VISUAL, 0.7),
        SensorySeed("absence where voice should be", SensoryModality.VISUAL, 0.8),
    ),
    auditory=(
        SensorySeed("silence where there was sound", SensoryModality.AUDITORY, 0.9, "דּוּמִיָּה"),
        SensorySeed("breath held, no sound escaping", SensoryModality.AUDITORY, 0.85),
        SensorySeed("wind that is not wind", SensoryModality.AUDITORY, 0.7),
        SensorySeed("silence heavier than sound", SensoryModality.AUDITORY, 0.95, "σιωπή", temporal_folding="silence of the Lamb"),
        SensorySeed("no answer coming", SensoryModality.AUDITORY, 0.9),
    ),
    tactile=(
        SensorySeed("pressure of unspoken words", SensoryModality.TACTILE, 0.6),
        SensorySeed("weight of silence", SensoryModality.TACTILE, 0.75),
    ),
    olfactory=(),  # Silence has no smell
    gustatory=(),  # Silence has no taste
    proprioceptive=(
        SensorySeed("stillness in the body", SensoryModality.PROPRIOCEPTIVE, 0.5),
        SensorySeed("frozen in position", SensoryModality.PROPRIOCEPTIVE, 0.7),
    ),
    forbidden_terms=("mute", "speechless", "quiet", "hush"),
)


BREATH_SENSORY = MotifSensory(
    motif_name="BREATH",
    visual=(
        SensorySeed("chest rising and falling", SensoryModality.VISUAL, 0.5),
        SensorySeed("mist of breath in cold", SensoryModality.VISUAL, 0.4),
        SensorySeed("last breath escaping", SensoryModality.VISUAL, 0.95),
    ),
    auditory=(
        SensorySeed("whisper of breath", SensoryModality.AUDITORY, 0.4, "נְשָׁמָה"),
        SensorySeed("labored breathing", SensoryModality.AUDITORY, 0.7),
        SensorySeed("breath given up", SensoryModality.AUDITORY, 0.95, "πνεῦμα", temporal_folding="gave up the ghost"),
        SensorySeed("wind of spirit", SensoryModality.AUDITORY, 0.8, "רוּחַ"),
    ),
    tactile=(
        SensorySeed("breath on skin", SensoryModality.TACTILE, 0.4),
        SensorySeed("wind touching face", SensoryModality.TACTILE, 0.5),
        SensorySeed("breath entering nostrils", SensoryModality.TACTILE, 0.7, temporal_folding="breath of life"),
    ),
    olfactory=(
        SensorySeed("breath of the living", SensoryModality.OLFACTORY, 0.3),
    ),
    gustatory=(),
    proprioceptive=(
        SensorySeed("lungs expanding", SensoryModality.PROPRIOCEPTIVE, 0.5),
        SensorySeed("chest constricted", SensoryModality.PROPRIOCEPTIVE, 0.8),
        SensorySeed("final exhalation", SensoryModality.PROPRIOCEPTIVE, 0.95),
    ),
    forbidden_terms=("respiration", "breathing exercises", "respiratory"),
)


WATER_SENSORY = MotifSensory(
    motif_name="WATER",
    visual=(
        SensorySeed("waters deep and dark", SensoryModality.VISUAL, 0.7, "מַיִם"),
        SensorySeed("waters parted", SensoryModality.VISUAL, 0.9),
        SensorySeed("blood and water flowing", SensoryModality.VISUAL, 0.95, "ὕδωρ", temporal_folding="blood and water"),
        SensorySeed("baptismal waters", SensoryModality.VISUAL, 0.8),
    ),
    auditory=(
        SensorySeed("rush of many waters", SensoryModality.AUDITORY, 0.8),
        SensorySeed("dripping into stillness", SensoryModality.AUDITORY, 0.5),
        SensorySeed("voice like many waters", SensoryModality.AUDITORY, 0.9),
    ),
    tactile=(
        SensorySeed("water closing over", SensoryModality.TACTILE, 0.8),
        SensorySeed("coolness of spring", SensoryModality.TACTILE, 0.4),
        SensorySeed("immersion, burial in water", SensoryModality.TACTILE, 0.85),
    ),
    olfactory=(
        SensorySeed("salt of sea", SensoryModality.OLFACTORY, 0.5),
        SensorySeed("freshness of spring", SensoryModality.OLFACTORY, 0.3),
    ),
    gustatory=(
        SensorySeed("water from rock", SensoryModality.GUSTATORY, 0.6),
        SensorySeed("bitter water made sweet", SensoryModality.GUSTATORY, 0.7),
    ),
    proprioceptive=(
        SensorySeed("floating weightless", SensoryModality.PROPRIOCEPTIVE, 0.5),
        SensorySeed("drowning, sinking", SensoryModality.PROPRIOCEPTIVE, 0.9),
        SensorySeed("rising from water", SensoryModality.PROPRIOCEPTIVE, 0.85),
    ),
    forbidden_terms=("hydration", "H2O", "liquid", "fluid"),
)


FIRE_SENSORY = MotifSensory(
    motif_name="FIRE",
    visual=(
        SensorySeed("flame consuming", SensoryModality.VISUAL, 0.9, "אֵשׁ"),
        SensorySeed("fire not consuming", SensoryModality.VISUAL, 0.95),  # Burning bush
        SensorySeed("pillar of fire", SensoryModality.VISUAL, 0.85),
        SensorySeed("tongues of flame", SensoryModality.VISUAL, 0.9, "πῦρ"),
        SensorySeed("embers glowing", SensoryModality.VISUAL, 0.5),
    ),
    auditory=(
        SensorySeed("crackling of fire", SensoryModality.AUDITORY, 0.6),
        SensorySeed("roar of conflagration", SensoryModality.AUDITORY, 0.9),
    ),
    tactile=(
        SensorySeed("heat on face", SensoryModality.TACTILE, 0.7),
        SensorySeed("burning that does not burn", SensoryModality.TACTILE, 0.95),
        SensorySeed("fire beneath cauldron", SensoryModality.TACTILE, 0.5),
    ),
    olfactory=(
        SensorySeed("smoke rising", SensoryModality.OLFACTORY, 0.7),
        SensorySeed("pleasing aroma of burnt offering", SensoryModality.OLFACTORY, 0.8, "רֵיחַ נִיחֹחַ"),
    ),
    gustatory=(),
    proprioceptive=(
        SensorySeed("recoiling from heat", SensoryModality.PROPRIOCEPTIVE, 0.7),
        SensorySeed("standing in fire unharmed", SensoryModality.PROPRIOCEPTIVE, 0.95),
    ),
    forbidden_terms=("combustion", "ignition", "flammable", "inferno"),
)


# ============================================================================
# SENSORY VOCABULARY REGISTRY
# ============================================================================

MOTIF_SENSORY_REGISTRY: Dict[str, MotifSensory] = {
    'LAMB': LAMB_SENSORY,
    'WOOD': WOOD_SENSORY,
    'BLOOD': BLOOD_SENSORY,
    'SILENCE': SILENCE_SENSORY,
    'BREATH': BREATH_SENSORY,
    'WATER': WATER_SENSORY,
    'FIRE': FIRE_SENSORY,
}


# ============================================================================
# SENSORY SELECTION FUNCTIONS
# ============================================================================

def get_sensory_vocabulary(
    motif_name: str,
    modality: Optional[SensoryModality] = None,
    intensity_threshold: float = 0.0,
) -> List[SensorySeed]:
    """Get sensory vocabulary for a motif."""
    motif = MOTIF_SENSORY_REGISTRY.get(motif_name.upper())
    if not motif:
        return []
    
    seeds: List[SensorySeed] = []
    
    if modality is None or modality == SensoryModality.VISUAL:
        seeds.extend(motif.visual)
    if modality is None or modality == SensoryModality.AUDITORY:
        seeds.extend(motif.auditory)
    if modality is None or modality == SensoryModality.TACTILE:
        seeds.extend(motif.tactile)
    if modality is None or modality == SensoryModality.OLFACTORY:
        seeds.extend(motif.olfactory)
    if modality is None or modality == SensoryModality.GUSTATORY:
        seeds.extend(motif.gustatory)
    if modality is None or modality == SensoryModality.PROPRIOCEPTIVE:
        seeds.extend(motif.proprioceptive)
    
    return [s for s in seeds if s.intensity >= intensity_threshold]


def get_forbidden_terms(motif_name: str) -> Tuple[str, ...]:
    """Get terms that must NEVER be used for a motif."""
    motif = MOTIF_SENSORY_REGISTRY.get(motif_name.upper())
    return motif.forbidden_terms if motif else ()


def get_temporal_folding_seeds(motif_name: str) -> List[SensorySeed]:
    """Get seeds that participate in temporal folding (plant/echo phrases)."""
    motif = MOTIF_SENSORY_REGISTRY.get(motif_name.upper())
    if not motif:
        return []
    
    # Use class method for cleaner code
    all_seeds = motif.get_all_seeds()
    return [s for s in all_seeds if s.temporal_folding]


def format_sensory_specification(motif_name: str) -> str:
    """Format sensory vocabulary as specification document."""
    motif = MOTIF_SENSORY_REGISTRY.get(motif_name.upper())
    if not motif:
        return f"No sensory vocabulary registered for motif: {motif_name}"
    
    def format_seeds(seeds: Tuple[SensorySeed, ...], indent: str = "    ") -> str:
        if not seeds:
            return f"{indent}(none)"
        lines = []
        for s in seeds:
            hebrew = f" [{s.hebrew_connection}]" if s.hebrew_connection else ""
            greek = f" [{s.greek_connection}]" if s.greek_connection else ""
            fold = f" → FOLDS: '{s.temporal_folding}'" if s.temporal_folding else ""
            lines.append(f"{indent}• \"{s.term}\" (intensity: {s.intensity:.1f}){hebrew}{greek}{fold}")
        return "\n".join(lines)
    
    return f"""
════════════════════════════════════════════════════════════════════
SENSORY VOCABULARY SPECIFICATION: {motif.motif_name}
════════════════════════════════════════════════════════════════════

VISUAL (what the reader's eyes simulate):
{format_seeds(motif.visual)}

AUDITORY (what the reader's ears simulate):
{format_seeds(motif.auditory)}

TACTILE (what the reader's body simulates):
{format_seeds(motif.tactile)}

OLFACTORY (what the reader smells):
{format_seeds(motif.olfactory)}

GUSTATORY (what the reader tastes):
{format_seeds(motif.gustatory)}

PROPRIOCEPTIVE (body position, weight, movement):
{format_seeds(motif.proprioceptive)}

FORBIDDEN TERMS (never use):
    {', '.join(motif.forbidden_terms) if motif.forbidden_terms else '(none)'}

TEMPORAL FOLDING PHRASES:
{format_seeds(tuple(get_temporal_folding_seeds(motif_name)))}

════════════════════════════════════════════════════════════════════
"""


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Sensory Vocabulary Architecture')
    parser.add_argument('--motif', type=str, default='LAMB', help='Motif name')
    parser.add_argument('--list', action='store_true', help='List all motifs')
    parser.add_argument('--modality', type=str, help='Filter by modality')
    
    args = parser.parse_args()
    
    if args.list:
        print("\nRegistered Motif Sensory Vocabularies:")
        for name in MOTIF_SENSORY_REGISTRY:
            motif = MOTIF_SENSORY_REGISTRY[name]
            total = (len(motif.visual) + len(motif.auditory) + len(motif.tactile) +
                    len(motif.olfactory) + len(motif.gustatory) + len(motif.proprioceptive))
            print(f"  • {name}: {total} sensory seeds")
    else:
        print(format_sensory_specification(args.motif))
