#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Character Voice Registry
======================================

Per MASTER_PLAN.md: Character voices are distinct tonal registers that
vary by speaker, context, and theological weight. Each voice carries
its own breath rhythm, syntactic pattern, and emotional temperature.

THE NARRATIVE ENDS AT THE CROSS.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class VoiceRegister(Enum):
    """Seven Register System applied to character speech."""
    WANDERING = "wandering"         # Baseline exposed witness
    WAITING = "waiting"             # Meditative depth
    BREAKTHROUGH = "breakthrough"   # Prophetic intensity
    CLEARING = "clearing"           # Intimate presence
    RECKONING = "reckoning"        # Dissonant triumph
    SILENCE = "silence"            # Withheld/ellipsis
    BURNING = "burning"            # Unflinching horror


class CharacterType(Enum):
    """Categories of biblical characters."""
    PATRIARCH = "patriarch"
    PROPHET = "prophet"
    KING = "king"
    PRIEST = "priest"
    APOSTLE = "apostle"
    DISCIPLE = "disciple"
    ANGEL = "angel"
    DEMON = "demon"
    CHRIST = "christ"
    FATHER = "father"
    WOMAN = "woman"
    PAGAN = "pagan"
    SERPENT = "serpent"


@dataclass(frozen=True)
class CharacterVoice:
    """Complete specification for a biblical character's voice."""
    name: str
    character_type: CharacterType
    primary_register: VoiceRegister
    secondary_register: VoiceRegister
    breath_pattern: str  # e.g., "7-7-3", "sustained", "punctuated"
    syntactic_preference: str  # e.g., "paratactic", "hypotactic", "mixed"
    emotional_baseline: float  # -1.0 (grief) to 1.0 (joy)
    theological_density: float  # 0.0 to 1.0
    sensory_emphasis: Tuple[str, ...]  # Preferred sensory modalities
    forbidden_patterns: Tuple[str, ...]  # Patterns this voice never uses
    signature_phrases: Tuple[str, ...]  # Characteristic speech patterns
    hebrew_name: Optional[str] = None
    greek_name: Optional[str] = None


# ============================================================================
# DIVINE VOICE
# ============================================================================

DIVINE_VOICES: Dict[str, CharacterVoice] = {
    "YHWH": CharacterVoice(
        name="YHWH",
        hebrew_name="יְהוָה",
        character_type=CharacterType.FATHER,
        primary_register=VoiceRegister.BREAKTHROUGH,
        secondary_register=VoiceRegister.CLEARING,
        breath_pattern="sustained",
        syntactic_preference="declarative",
        emotional_baseline=0.0,  # Beyond emotion
        theological_density=1.0,
        sensory_emphasis=("auditory", "visual", "proprioceptive"),
        forbidden_patterns=("uncertainty", "question", "doubt"),
        signature_phrases=(
            "I AM",
            "Behold",
            "Thus saith the LORD",
            "Fear not",
        )
    ),
    "Christ_Teaching": CharacterVoice(
        name="Christ (Teaching)",
        greek_name="Χριστός",
        character_type=CharacterType.CHRIST,
        primary_register=VoiceRegister.CLEARING,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="7-7-3",
        syntactic_preference="parabolic",
        emotional_baseline=0.3,
        theological_density=1.0,
        sensory_emphasis=("visual", "tactile", "auditory"),
        forbidden_patterns=("violence", "condemnation without mercy"),
        signature_phrases=(
            "Verily, verily I say unto you",
            "The kingdom of heaven is like",
            "Ye have heard that it was said",
            "But I say unto you",
        )
    ),
    "Christ_Passion": CharacterVoice(
        name="Christ (Passion)",
        greek_name="Χριστός",
        character_type=CharacterType.CHRIST,
        primary_register=VoiceRegister.RECKONING,
        secondary_register=VoiceRegister.SILENCE,
        breath_pattern="punctuated",
        syntactic_preference="compressed",
        emotional_baseline=-0.3,
        theological_density=1.0,
        sensory_emphasis=("tactile", "proprioceptive", "auditory"),
        forbidden_patterns=("escape", "denial", "vengeance"),
        signature_phrases=(
            "Father, forgive them",
            "It is finished",
            "Into thy hands",
            "My God, my God",
        )
    ),
    "Holy_Spirit": CharacterVoice(
        name="Holy Spirit",
        greek_name="πνεῦμα ἅγιον",
        character_type=CharacterType.FATHER,
        primary_register=VoiceRegister.WAITING,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="sustained",
        syntactic_preference="flowing",
        emotional_baseline=0.5,
        theological_density=0.95,
        sensory_emphasis=("proprioceptive", "auditory", "tactile"),
        forbidden_patterns=("direct speech", "self-reference"),
        signature_phrases=(
            "The Spirit of the Lord",
            "breathed",
            "descended",
        )
    ),
}


# ============================================================================
# PATRIARCHAL VOICES
# ============================================================================

PATRIARCH_VOICES: Dict[str, CharacterVoice] = {
    "Adam": CharacterVoice(
        name="Adam",
        hebrew_name="אָדָם",
        character_type=CharacterType.PATRIARCH,
        primary_register=VoiceRegister.WANDERING,
        secondary_register=VoiceRegister.SILENCE,
        breath_pattern="broken",
        syntactic_preference="paratactic",
        emotional_baseline=-0.2,  # After the fall
        theological_density=0.6,
        sensory_emphasis=("visual", "tactile", "gustatory"),
        forbidden_patterns=("boasting", "certainty"),
        signature_phrases=(
            "The woman whom thou gavest",
            "I was afraid",
            "I hid myself",
        )
    ),
    "Noah": CharacterVoice(
        name="Noah",
        hebrew_name="נֹחַ",
        character_type=CharacterType.PATRIARCH,
        primary_register=VoiceRegister.WAITING,
        secondary_register=VoiceRegister.WANDERING,
        breath_pattern="sustained",
        syntactic_preference="paratactic",
        emotional_baseline=-0.1,
        theological_density=0.7,
        sensory_emphasis=("auditory", "olfactory", "tactile"),
        forbidden_patterns=("hurry", "impatience"),
        signature_phrases=(
            "according to all that God commanded",
        )
    ),
    "Abraham": CharacterVoice(
        name="Abraham",
        hebrew_name="אַבְרָהָם",
        character_type=CharacterType.PATRIARCH,
        primary_register=VoiceRegister.WANDERING,
        secondary_register=VoiceRegister.CLEARING,
        breath_pattern="7-7-3",
        syntactic_preference="paratactic",
        emotional_baseline=0.2,
        theological_density=0.8,
        sensory_emphasis=("visual", "auditory", "tactile"),
        forbidden_patterns=("despair", "faithlessness"),
        signature_phrases=(
            "Here am I",
            "God will provide himself a lamb",
            "I know not",
        )
    ),
    "Isaac": CharacterVoice(
        name="Isaac",
        hebrew_name="יִצְחָק",
        character_type=CharacterType.PATRIARCH,
        primary_register=VoiceRegister.CLEARING,
        secondary_register=VoiceRegister.WAITING,
        breath_pattern="gentle",
        syntactic_preference="interrogative",
        emotional_baseline=0.1,
        theological_density=0.7,
        sensory_emphasis=("tactile", "auditory", "olfactory"),
        forbidden_patterns=("violence", "command"),
        signature_phrases=(
            "Behold the fire and the wood, but where is the lamb",
        )
    ),
    "Jacob": CharacterVoice(
        name="Jacob",
        hebrew_name="יַעֲקֹב",
        character_type=CharacterType.PATRIARCH,
        primary_register=VoiceRegister.RECKONING,
        secondary_register=VoiceRegister.WANDERING,
        breath_pattern="struggled",
        syntactic_preference="mixed",
        emotional_baseline=0.0,
        theological_density=0.75,
        sensory_emphasis=("tactile", "visual", "proprioceptive"),
        forbidden_patterns=("passivity", "acceptance"),
        signature_phrases=(
            "I will not let thee go except thou bless me",
            "How dreadful is this place",
        )
    ),
    "Joseph": CharacterVoice(
        name="Joseph",
        hebrew_name="יוֹסֵף",
        character_type=CharacterType.PATRIARCH,
        primary_register=VoiceRegister.CLEARING,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="controlled",
        syntactic_preference="hypotactic",
        emotional_baseline=0.3,
        theological_density=0.8,
        sensory_emphasis=("visual", "auditory", "tactile"),
        forbidden_patterns=("bitterness", "revenge"),
        signature_phrases=(
            "Ye thought evil against me, but God meant it unto good",
            "Fear not, for am I in the place of God",
        )
    ),
    "Moses": CharacterVoice(
        name="Moses",
        hebrew_name="מֹשֶׁה",
        character_type=CharacterType.PROPHET,
        primary_register=VoiceRegister.BREAKTHROUGH,
        secondary_register=VoiceRegister.RECKONING,
        breath_pattern="7-7-3",
        syntactic_preference="mixed",
        emotional_baseline=0.0,
        theological_density=0.95,
        sensory_emphasis=("visual", "auditory", "proprioceptive"),
        forbidden_patterns=("self-confidence", "ease"),
        signature_phrases=(
            "Who am I that I should go",
            "Thus saith the LORD",
            "Hear, O Israel",
        )
    ),
}


# ============================================================================
# PROPHETIC VOICES
# ============================================================================

PROPHET_VOICES: Dict[str, CharacterVoice] = {
    "Isaiah": CharacterVoice(
        name="Isaiah",
        hebrew_name="יְשַׁעְיָהוּ",
        character_type=CharacterType.PROPHET,
        primary_register=VoiceRegister.BREAKTHROUGH,
        secondary_register=VoiceRegister.CLEARING,
        breath_pattern="sustained-punctuated",
        syntactic_preference="hypotactic",
        emotional_baseline=0.2,
        theological_density=0.95,
        sensory_emphasis=("visual", "auditory", "olfactory"),
        forbidden_patterns=("uncertainty", "smallness"),
        signature_phrases=(
            "Holy, holy, holy",
            "Woe is me",
            "Behold, a virgin shall conceive",
            "Comfort ye, comfort ye my people",
        )
    ),
    "Jeremiah": CharacterVoice(
        name="Jeremiah",
        hebrew_name="יִרְמְיָהוּ",
        character_type=CharacterType.PROPHET,
        primary_register=VoiceRegister.RECKONING,
        secondary_register=VoiceRegister.WAITING,
        breath_pattern="weeping",
        syntactic_preference="lamentation",
        emotional_baseline=-0.4,
        theological_density=0.9,
        sensory_emphasis=("auditory", "tactile", "visual"),
        forbidden_patterns=("celebration", "ease"),
        signature_phrases=(
            "Oh that my head were waters",
            "The heart is deceitful above all things",
            "Cursed be the day wherein I was born",
        )
    ),
    "Ezekiel": CharacterVoice(
        name="Ezekiel",
        hebrew_name="יְחֶזְקֵאל",
        character_type=CharacterType.PROPHET,
        primary_register=VoiceRegister.BURNING,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="visionary",
        syntactic_preference="cataloguing",
        emotional_baseline=-0.1,
        theological_density=0.95,
        sensory_emphasis=("visual", "proprioceptive", "auditory"),
        forbidden_patterns=("simplicity", "reduction"),
        signature_phrases=(
            "Son of man",
            "The hand of the LORD was upon me",
            "I saw visions of God",
        )
    ),
    "Daniel": CharacterVoice(
        name="Daniel",
        hebrew_name="דָּנִיֵּאל",
        character_type=CharacterType.PROPHET,
        primary_register=VoiceRegister.WAITING,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="controlled",
        syntactic_preference="measured",
        emotional_baseline=0.1,
        theological_density=0.9,
        sensory_emphasis=("visual", "auditory", "proprioceptive"),
        forbidden_patterns=("compromise", "fear"),
        signature_phrases=(
            "Blessed be the name of God for ever and ever",
            "The Most High ruleth in the kingdom of men",
        )
    ),
    "Elijah": CharacterVoice(
        name="Elijah",
        hebrew_name="אֵלִיָּהוּ",
        character_type=CharacterType.PROPHET,
        primary_register=VoiceRegister.BURNING,
        secondary_register=VoiceRegister.SILENCE,
        breath_pattern="fire-silence",
        syntactic_preference="imperative",
        emotional_baseline=0.0,
        theological_density=0.9,
        sensory_emphasis=("auditory", "visual", "tactile"),
        forbidden_patterns=("diplomacy", "compromise"),
        signature_phrases=(
            "The LORD, he is God",
            "I have been very jealous for the LORD",
            "What doest thou here",
        )
    ),
    "John_Baptist": CharacterVoice(
        name="John the Baptist",
        greek_name="Ἰωάννης ὁ Βαπτιστής",
        character_type=CharacterType.PROPHET,
        primary_register=VoiceRegister.BURNING,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="urgent",
        syntactic_preference="imperative",
        emotional_baseline=-0.1,
        theological_density=0.85,
        sensory_emphasis=("auditory", "visual", "tactile"),
        forbidden_patterns=("comfort", "accommodation"),
        signature_phrases=(
            "Repent ye",
            "Behold the Lamb of God",
            "He must increase, but I must decrease",
            "O generation of vipers",
        )
    ),
}


# ============================================================================
# APOSTOLIC VOICES
# ============================================================================

APOSTLE_VOICES: Dict[str, CharacterVoice] = {
    "Peter": CharacterVoice(
        name="Peter",
        greek_name="Πέτρος",
        hebrew_name="שִׁמְעוֹן",
        character_type=CharacterType.APOSTLE,
        primary_register=VoiceRegister.WANDERING,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="impulsive",
        syntactic_preference="exclamatory",
        emotional_baseline=0.2,
        theological_density=0.75,
        sensory_emphasis=("visual", "tactile", "auditory"),
        forbidden_patterns=("calculation", "hesitation"),
        signature_phrases=(
            "Lord, to whom shall we go",
            "Thou art the Christ",
            "I know not the man",
            "Lord, thou knowest all things",
        )
    ),
    "John_Apostle": CharacterVoice(
        name="John the Apostle",
        greek_name="Ἰωάννης",
        character_type=CharacterType.APOSTLE,
        primary_register=VoiceRegister.CLEARING,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="contemplative",
        syntactic_preference="declarative",
        emotional_baseline=0.4,
        theological_density=0.95,
        sensory_emphasis=("visual", "tactile", "auditory"),
        forbidden_patterns=("hate", "darkness"),
        signature_phrases=(
            "God is love",
            "In the beginning was the Word",
            "That which we have seen and heard",
            "Little children",
        )
    ),
    "Paul": CharacterVoice(
        name="Paul",
        greek_name="Παῦλος",
        hebrew_name="שָׁאוּל",
        character_type=CharacterType.APOSTLE,
        primary_register=VoiceRegister.BREAKTHROUGH,
        secondary_register=VoiceRegister.RECKONING,
        breath_pattern="complex",
        syntactic_preference="hypotactic",
        emotional_baseline=0.2,
        theological_density=0.98,
        sensory_emphasis=("auditory", "proprioceptive", "visual"),
        forbidden_patterns=("simplism", "law-dependence"),
        signature_phrases=(
            "Grace to you and peace",
            "O the depth of the riches",
            "For me to live is Christ",
            "I am crucified with Christ",
        )
    ),
    "Thomas": CharacterVoice(
        name="Thomas",
        greek_name="Θωμᾶς",
        character_type=CharacterType.APOSTLE,
        primary_register=VoiceRegister.SILENCE,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="hesitant-sudden",
        syntactic_preference="conditional",
        emotional_baseline=-0.2,
        theological_density=0.7,
        sensory_emphasis=("tactile", "visual", "proprioceptive"),
        forbidden_patterns=("blind acceptance", "easy faith"),
        signature_phrases=(
            "Except I shall see",
            "Let us also go, that we may die with him",
            "My Lord and my God",
        )
    ),
}


# ============================================================================
# FEMININE VOICES
# ============================================================================

FEMININE_VOICES: Dict[str, CharacterVoice] = {
    "Eve": CharacterVoice(
        name="Eve",
        hebrew_name="חַוָּה",
        character_type=CharacterType.WOMAN,
        primary_register=VoiceRegister.WANDERING,
        secondary_register=VoiceRegister.SILENCE,
        breath_pattern="broken",
        syntactic_preference="paratactic",
        emotional_baseline=-0.3,
        theological_density=0.6,
        sensory_emphasis=("visual", "gustatory", "tactile"),
        forbidden_patterns=("certainty", "command"),
        signature_phrases=(
            "The serpent beguiled me",
            "I will greatly multiply thy sorrow",
        )
    ),
    "Mary_Mother": CharacterVoice(
        name="Mary (Mother of Christ)",
        greek_name="Μαρία",
        character_type=CharacterType.WOMAN,
        primary_register=VoiceRegister.CLEARING,
        secondary_register=VoiceRegister.WAITING,
        breath_pattern="pondering",
        syntactic_preference="receptive",
        emotional_baseline=0.3,
        theological_density=0.85,
        sensory_emphasis=("auditory", "visual", "tactile"),
        forbidden_patterns=("self-assertion", "resistance"),
        signature_phrases=(
            "Be it unto me according to thy word",
            "My soul doth magnify the Lord",
            "They have no wine",
            "Whatsoever he saith unto you, do it",
        )
    ),
    "Mary_Magdalene": CharacterVoice(
        name="Mary Magdalene",
        greek_name="Μαρία ἡ Μαγδαληνή",
        character_type=CharacterType.WOMAN,
        primary_register=VoiceRegister.RECKONING,
        secondary_register=VoiceRegister.CLEARING,
        breath_pattern="urgent-tender",
        syntactic_preference="seeking",
        emotional_baseline=0.1,
        theological_density=0.75,
        sensory_emphasis=("visual", "tactile", "auditory"),
        forbidden_patterns=("despair", "abandonment"),
        signature_phrases=(
            "They have taken away my Lord",
            "Rabboni",
            "I have seen the Lord",
        )
    ),
    "Hannah": CharacterVoice(
        name="Hannah",
        hebrew_name="חַנָּה",
        character_type=CharacterType.WOMAN,
        primary_register=VoiceRegister.WAITING,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="weeping-exulting",
        syntactic_preference="hymnic",
        emotional_baseline=0.0,
        theological_density=0.8,
        sensory_emphasis=("auditory", "tactile", "visual"),
        forbidden_patterns=("bitterness", "envy"),
        signature_phrases=(
            "My heart rejoiceth in the LORD",
            "The LORD killeth, and maketh alive",
        )
    ),
    "Ruth": CharacterVoice(
        name="Ruth",
        hebrew_name="רוּת",
        character_type=CharacterType.WOMAN,
        primary_register=VoiceRegister.CLEARING,
        secondary_register=VoiceRegister.WANDERING,
        breath_pattern="faithful",
        syntactic_preference="declarative",
        emotional_baseline=0.2,
        theological_density=0.7,
        sensory_emphasis=("visual", "tactile", "auditory"),
        forbidden_patterns=("self-preservation", "abandonment"),
        signature_phrases=(
            "Whither thou goest, I will go",
            "Thy people shall be my people",
            "Thy God my God",
        )
    ),
}


# ============================================================================
# ANTAGONIST VOICES
# ============================================================================

ANTAGONIST_VOICES: Dict[str, CharacterVoice] = {
    "Serpent": CharacterVoice(
        name="The Serpent",
        hebrew_name="נָחָשׁ",
        character_type=CharacterType.SERPENT,
        primary_register=VoiceRegister.SILENCE,
        secondary_register=VoiceRegister.WANDERING,
        breath_pattern="sinuous",
        syntactic_preference="interrogative",
        emotional_baseline=-0.5,
        theological_density=0.3,
        sensory_emphasis=("auditory", "visual", "gustatory"),
        forbidden_patterns=("direct assault", "obvious evil"),
        signature_phrases=(
            "Yea, hath God said",
            "Ye shall not surely die",
            "Your eyes shall be opened",
        )
    ),
    "Satan": CharacterVoice(
        name="Satan",
        hebrew_name="שָׂטָן",
        greek_name="Σατανᾶς",
        character_type=CharacterType.DEMON,
        primary_register=VoiceRegister.BURNING,
        secondary_register=VoiceRegister.SILENCE,
        breath_pattern="accusing",
        syntactic_preference="conditional",
        emotional_baseline=-0.7,
        theological_density=0.4,
        sensory_emphasis=("visual", "auditory", "proprioceptive"),
        forbidden_patterns=("truth", "love", "selflessness"),
        signature_phrases=(
            "If thou be the Son of God",
            "All these things will I give thee",
            "Does Job fear God for nought",
        )
    ),
    "Pilate": CharacterVoice(
        name="Pilate",
        greek_name="Πιλᾶτος",
        character_type=CharacterType.PAGAN,
        primary_register=VoiceRegister.RECKONING,
        secondary_register=VoiceRegister.SILENCE,
        breath_pattern="political",
        syntactic_preference="interrogative",
        emotional_baseline=-0.2,
        theological_density=0.3,
        sensory_emphasis=("visual", "auditory", "tactile"),
        forbidden_patterns=("commitment", "faith"),
        signature_phrases=(
            "What is truth",
            "I find no fault in this man",
            "Behold the man",
            "What I have written, I have written",
        )
    ),
}


# ============================================================================
# ANGELIC VOICES
# ============================================================================

ANGELIC_VOICES: Dict[str, CharacterVoice] = {
    "Gabriel": CharacterVoice(
        name="Gabriel",
        hebrew_name="גַּבְרִיאֵל",
        character_type=CharacterType.ANGEL,
        primary_register=VoiceRegister.BREAKTHROUGH,
        secondary_register=VoiceRegister.CLEARING,
        breath_pattern="annunciatory",
        syntactic_preference="declarative",
        emotional_baseline=0.5,
        theological_density=0.85,
        sensory_emphasis=("visual", "auditory", "proprioceptive"),
        forbidden_patterns=("doubt", "fear"),
        signature_phrases=(
            "Fear not",
            "Behold",
            "Thou shalt conceive",
            "His kingdom shall have no end",
        )
    ),
    "Seraphim": CharacterVoice(
        name="Seraphim",
        hebrew_name="שְׂרָפִים",
        character_type=CharacterType.ANGEL,
        primary_register=VoiceRegister.BURNING,
        secondary_register=VoiceRegister.BREAKTHROUGH,
        breath_pattern="trisagion",
        syntactic_preference="hymnic",
        emotional_baseline=0.9,
        theological_density=1.0,
        sensory_emphasis=("auditory", "visual", "proprioceptive"),
        forbidden_patterns=("silence", "doubt"),
        signature_phrases=(
            "Holy, holy, holy",
            "The whole earth is full of his glory",
        )
    ),
}


# ============================================================================
# UNIFIED REGISTRY
# ============================================================================

ALL_VOICES: Dict[str, CharacterVoice] = {
    **DIVINE_VOICES,
    **PATRIARCH_VOICES,
    **PROPHET_VOICES,
    **APOSTLE_VOICES,
    **FEMININE_VOICES,
    **ANTAGONIST_VOICES,
    **ANGELIC_VOICES,
}


def get_voice(name: str) -> Optional[CharacterVoice]:
    """Get a character voice by name."""
    return ALL_VOICES.get(name)


def get_voices_by_type(char_type: CharacterType) -> List[CharacterVoice]:
    """Get all voices of a specific type."""
    return [v for v in ALL_VOICES.values() if v.character_type == char_type]


def get_voices_by_register(register: VoiceRegister) -> List[CharacterVoice]:
    """Get all voices with a specific primary register."""
    return [v for v in ALL_VOICES.values() if v.primary_register == register]


def get_statistics() -> Dict[str, int]:
    """Get statistics about the voice registry."""
    return {
        'total_voices': len(ALL_VOICES),
        'divine': len(DIVINE_VOICES),
        'patriarchs': len(PATRIARCH_VOICES),
        'prophets': len(PROPHET_VOICES),
        'apostles': len(APOSTLE_VOICES),
        'feminine': len(FEMININE_VOICES),
        'antagonists': len(ANTAGONIST_VOICES),
        'angelic': len(ANGELIC_VOICES),
    }


if __name__ == "__main__":
    stats = get_statistics()
    print("ΒΊΒΛΟΣ ΛΌΓΟΥ Character Voice Registry")
    print("=" * 40)
    for key, value in stats.items():
        print(f"  {key}: {value}")
