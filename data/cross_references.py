#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Cross-Reference Network
====================================

Comprehensive typological correspondence system mapping Old Testament
shadows to New Testament fulfillments.

Per MASTER_PLAN.md: "Types are established through concrete sensory
and structural correspondence, not through verbal coincidence."

THE NARRATIVE ENDS AT THE CROSS.
"""

from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class TypeCategory(Enum):
    """Categories of typological correspondence."""
    PERSON = "person"           # Person prefigures person
    EVENT = "event"             # Event prefigures event  
    INSTITUTION = "institution" # Institution prefigures institution
    OBJECT = "object"           # Object prefigures object
    PLACE = "place"             # Place prefigures place
    RITUAL = "ritual"           # Ritual prefigures ritual
    OFFICE = "office"           # Office prefigures office


class CorrespondenceStrength(Enum):
    """Strength of typological correspondence."""
    EXPLICIT = "explicit"       # NT explicitly identifies the type
    STRONG = "strong"           # Clear correspondence widely recognized
    MODERATE = "moderate"       # Valid correspondence, less explicit
    SUBTLE = "subtle"           # Recognized by close reading


@dataclass(frozen=True)
class TypologicalCorrespondence:
    """A single typological correspondence between OT and NT."""
    type_reference: str         # OT passage/figure
    antitype_reference: str     # NT fulfillment
    type_description: str       # Brief description of OT element
    antitype_description: str   # Brief description of NT fulfillment
    category: TypeCategory
    strength: CorrespondenceStrength
    sensory_links: Tuple[str, ...] # Shared sensory vocabulary
    structural_links: Tuple[str, ...] # Shared structural elements
    patristic_support: Tuple[str, ...] # Church Fathers who taught this


# ============================================================================
# EXPLICIT CORRESPONDENCES (NT-identified)
# ============================================================================

EXPLICIT_TYPES: List[TypologicalCorrespondence] = [
    # LAMB TYPES
    TypologicalCorrespondence(
        type_reference="Exodus 12:3-13",
        antitype_reference="1 Corinthians 5:7",
        type_description="Passover lamb slain",
        antitype_description="Christ our Passover sacrificed",
        category=TypeCategory.RITUAL,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("blood", "doorpost", "lamb", "bone unbroken"),
        structural_links=("deliverance from death", "blood marks the saved"),
        patristic_support=("Chrysostom", "Cyril of Alexandria"),
    ),
    TypologicalCorrespondence(
        type_reference="Isaiah 53:7",
        antitype_reference="Acts 8:32-35",
        type_description="Led as a lamb to slaughter",
        antitype_description="Philip identifies lamb as Jesus",
        category=TypeCategory.PERSON,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("lamb", "silent", "slaughter"),
        structural_links=("innocent suffering", "silence before accusers"),
        patristic_support=("Justin Martyr", "Irenaeus"),
    ),
    TypologicalCorrespondence(
        type_reference="Genesis 22:1-14",
        antitype_reference="Hebrews 11:17-19",
        type_description="Abraham offering Isaac",
        antitype_description="Abraham received Isaac back as type",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("wood", "fire", "knife", "lamb", "mountain"),
        structural_links=("only son offered", "third day", "substitute provided"),
        patristic_support=("Origen", "Augustine", "Chrysostom"),
    ),
    
    # SERPENT TYPES
    TypologicalCorrespondence(
        type_reference="Numbers 21:8-9",
        antitype_reference="John 3:14-15",
        type_description="Bronze serpent lifted up",
        antitype_description="Son of Man must be lifted up",
        category=TypeCategory.OBJECT,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("lifted up", "pole", "look", "live"),
        structural_links=("healing through looking", "lifted on wood"),
        patristic_support=("Justin Martyr", "Cyril of Jerusalem"),
    ),
    
    # ADAM/CHRIST TYPES
    TypologicalCorrespondence(
        type_reference="Genesis 2:7",
        antitype_reference="1 Corinthians 15:45",
        type_description="First Adam, living soul",
        antitype_description="Last Adam, life-giving spirit",
        category=TypeCategory.PERSON,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("breath", "dust", "living"),
        structural_links=("head of humanity", "source of life/death"),
        patristic_support=("Irenaeus", "Athanasius"),
    ),
    TypologicalCorrespondence(
        type_reference="Genesis 3:15",
        antitype_reference="Romans 16:20",
        type_description="Seed of woman crushes serpent",
        antitype_description="God will crush Satan under your feet",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("foot", "head", "crush"),
        structural_links=("enmity", "victory through suffering"),
        patristic_support=("Irenaeus", "Chrysostom"),
    ),
    
    # MELCHIZEDEK TYPE
    TypologicalCorrespondence(
        type_reference="Genesis 14:18-20",
        antitype_reference="Hebrews 7:1-17",
        type_description="Melchizedek, priest-king",
        antitype_description="Christ priest forever after Melchizedek",
        category=TypeCategory.OFFICE,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("bread", "wine", "blessing"),
        structural_links=("no genealogy", "priest-king", "tithing"),
        patristic_support=("Clement of Alexandria", "Origen"),
    ),
    
    # TEMPLE/TABERNACLE TYPES
    TypologicalCorrespondence(
        type_reference="Exodus 25-27",
        antitype_reference="Hebrews 9:1-14",
        type_description="Tabernacle structure",
        antitype_description="Greater and more perfect tabernacle",
        category=TypeCategory.INSTITUTION,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("curtain", "blood", "holy", "sanctuary"),
        structural_links=("separation", "access through blood"),
        patristic_support=("Origen", "Gregory of Nyssa"),
    ),
    TypologicalCorrespondence(
        type_reference="Exodus 26:31-33",
        antitype_reference="Hebrews 10:19-20",
        type_description="Veil separating Holy of Holies",
        antitype_description="Veil is Christ's flesh",
        category=TypeCategory.OBJECT,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("veil", "torn", "flesh", "entry"),
        structural_links=("barrier removed", "access opened"),
        patristic_support=("Chrysostom", "Cyril of Alexandria"),
    ),
    
    # JONAH TYPE
    TypologicalCorrespondence(
        type_reference="Jonah 1:17",
        antitype_reference="Matthew 12:40",
        type_description="Jonah three days in fish",
        antitype_description="Son of Man three days in earth",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("three days", "belly", "depths"),
        structural_links=("descent", "emergence", "preaching"),
        patristic_support=("Jerome", "Augustine"),
    ),
    
    # MOSES TYPES
    TypologicalCorrespondence(
        type_reference="Exodus 17:6",
        antitype_reference="1 Corinthians 10:4",
        type_description="Water from the rock",
        antitype_description="Rock was Christ",
        category=TypeCategory.OBJECT,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("rock", "water", "struck"),
        structural_links=("life from stone", "provision in wilderness"),
        patristic_support=("Origen", "Augustine"),
    ),
    TypologicalCorrespondence(
        type_reference="Exodus 16:4-15",
        antitype_reference="John 6:31-35",
        type_description="Manna from heaven",
        antitype_description="True bread from heaven",
        category=TypeCategory.OBJECT,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("bread", "heaven", "eating", "life"),
        structural_links=("divine provision", "sustenance in wilderness"),
        patristic_support=("Cyril of Alexandria", "Augustine"),
    ),
    
    # DAVID TYPE
    TypologicalCorrespondence(
        type_reference="2 Samuel 7:12-16",
        antitype_reference="Luke 1:32-33",
        type_description="David's throne established",
        antitype_description="Christ on David's throne forever",
        category=TypeCategory.OFFICE,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("throne", "house", "kingdom"),
        structural_links=("son of David", "eternal kingdom"),
        patristic_support=("Justin Martyr", "Irenaeus"),
    ),
]


# ============================================================================
# STRONG CORRESPONDENCES (widely recognized)
# ============================================================================

STRONG_TYPES: List[TypologicalCorrespondence] = [
    # JOSEPH AS TYPE OF CHRIST
    TypologicalCorrespondence(
        type_reference="Genesis 37-50",
        antitype_reference="(Multiple NT passages)",
        type_description="Joseph rejected, exalted, saves family",
        antitype_description="Christ rejected, exalted, saves His people",
        category=TypeCategory.PERSON,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("pit", "garment", "bread", "prison", "throne"),
        structural_links=(
            "beloved son", "sold for silver", "falsely accused",
            "exalted to right hand", "saves through suffering"
        ),
        patristic_support=("Ambrose", "Augustine", "Ephrem"),
    ),
    
    # CREATION/NEW CREATION
    TypologicalCorrespondence(
        type_reference="Genesis 1:1-3",
        antitype_reference="2 Corinthians 4:6",
        type_description="Light in primordial darkness",
        antitype_description="Light in hearts through Christ",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("light", "darkness", "word", "creation"),
        structural_links=("divine fiat", "new beginning"),
        patristic_support=("Basil", "Gregory of Nyssa"),
    ),
    
    # ARK/CHURCH
    TypologicalCorrespondence(
        type_reference="Genesis 6-8",
        antitype_reference="1 Peter 3:20-21",
        type_description="Noah's ark saves through water",
        antitype_description="Baptism now saves you",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("water", "wood", "eight souls", "saved"),
        structural_links=("judgment through water", "salvation through ark"),
        patristic_support=("Justin Martyr", "Cyprian", "Augustine"),
    ),
    
    # RED SEA/BAPTISM
    TypologicalCorrespondence(
        type_reference="Exodus 14",
        antitype_reference="1 Corinthians 10:1-2",
        type_description="Israel through Red Sea",
        antitype_description="Baptized into Moses in cloud and sea",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("water", "cloud", "passage", "deliverance"),
        structural_links=("death of enemies", "new life", "wilderness journey"),
        patristic_support=("Origen", "Cyril of Jerusalem", "Gregory of Nyssa"),
    ),
    
    # GARDEN/GETHSEMANE/EDEN
    TypologicalCorrespondence(
        type_reference="Genesis 3",
        antitype_reference="Matthew 26:36-46",
        type_description="Adam's fall in garden",
        antitype_description="Christ's obedience in garden",
        category=TypeCategory.PLACE,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("garden", "tree", "sweat", "will"),
        structural_links=("temptation", "choice", "consequences for humanity"),
        patristic_support=("Irenaeus", "Cyril of Jerusalem"),
    ),
    
    # TREE OF LIFE/CROSS
    TypologicalCorrespondence(
        type_reference="Genesis 2:9; 3:22-24",
        antitype_reference="Revelation 22:2",
        type_description="Tree of life in Eden",
        antitype_description="Tree of life in New Jerusalem",
        category=TypeCategory.OBJECT,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("tree", "fruit", "life", "healing"),
        structural_links=("access denied", "access restored", "cross as tree"),
        patristic_support=("Irenaeus", "Ephrem", "Cyril of Jerusalem"),
    ),
    
    # FLOOD/JUDGMENT
    TypologicalCorrespondence(
        type_reference="Genesis 7",
        antitype_reference="Matthew 24:37-39",
        type_description="Days of Noah, flood judgment",
        antitype_description="Coming of Son of Man like Noah's days",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("water", "destruction", "ark", "eating drinking"),
        structural_links=("sudden judgment", "few saved", "new beginning"),
        patristic_support=("Chrysostom", "Jerome"),
    ),
    
    # RAHAB/CHURCH
    TypologicalCorrespondence(
        type_reference="Joshua 2",
        antitype_reference="Hebrews 11:31",
        type_description="Rahab saved by scarlet cord",
        antitype_description="Rahab saved by faith",
        category=TypeCategory.PERSON,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("scarlet", "cord", "window", "wall"),
        structural_links=("Gentile saved", "faith before Israel's victory"),
        patristic_support=("Clement of Rome", "Justin Martyr"),
    ),
    
    # HIGH PRIEST/CHRIST
    TypologicalCorrespondence(
        type_reference="Leviticus 16",
        antitype_reference="Hebrews 9:7-12",
        type_description="High priest enters Holy of Holies",
        antitype_description="Christ entered heaven itself",
        category=TypeCategory.OFFICE,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("blood", "curtain", "incense", "mercy seat"),
        structural_links=("once a year / once for all", "atonement made"),
        patristic_support=("Origen", "Chrysostom", "Cyril of Alexandria"),
    ),
    
    # DAY OF ATONEMENT
    TypologicalCorrespondence(
        type_reference="Leviticus 16:20-22",
        antitype_reference="Isaiah 53:4-6; John 1:29",
        type_description="Scapegoat bears sins away",
        antitype_description="Christ bears away sin of world",
        category=TypeCategory.RITUAL,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("goat", "wilderness", "sin", "bear"),
        structural_links=("sin transferred", "removed from people"),
        patristic_support=("Justin Martyr", "Cyril of Alexandria"),
    ),
]


# ============================================================================
# PSALM 22 FULFILLMENTS (Special category: Passion predictions)
# ============================================================================

PSALM_22_FULFILLMENTS: List[TypologicalCorrespondence] = [
    TypologicalCorrespondence(
        type_reference="Psalm 22:1",
        antitype_reference="Matthew 27:46",
        type_description="My God, my God, why hast thou forsaken me",
        antitype_description="Jesus cries same words from cross",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("cry", "forsaken", "God"),
        structural_links=("opening cry", "abandonment"),
        patristic_support=("All Church Fathers",),
    ),
    TypologicalCorrespondence(
        type_reference="Psalm 22:7-8",
        antitype_reference="Matthew 27:39-43",
        type_description="They mock, they shake heads",
        antitype_description="Passers-by mock, shake heads",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("mock", "wag heads", "let him deliver"),
        structural_links=("derision", "challenge to God"),
        patristic_support=("Augustine", "Chrysostom"),
    ),
    TypologicalCorrespondence(
        type_reference="Psalm 22:16",
        antitype_reference="John 20:25",
        type_description="They pierced my hands and my feet",
        antitype_description="Print of nails in hands",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.STRONG,
        sensory_links=("pierced", "hands", "feet"),
        structural_links=("crucifixion method"),
        patristic_support=("Justin Martyr", "Tertullian"),
    ),
    TypologicalCorrespondence(
        type_reference="Psalm 22:18",
        antitype_reference="John 19:23-24",
        type_description="They part my garments, cast lots",
        antitype_description="Soldiers divide garments, cast lots",
        category=TypeCategory.EVENT,
        strength=CorrespondenceStrength.EXPLICIT,
        sensory_links=("garments", "lots", "divide"),
        structural_links=("stripping", "gambling"),
        patristic_support=("Jerome", "Augustine"),
    ),
]


# ============================================================================
# UNIFIED ACCESS
# ============================================================================

ALL_CORRESPONDENCES: List[TypologicalCorrespondence] = (
    EXPLICIT_TYPES + STRONG_TYPES + PSALM_22_FULFILLMENTS
)


def get_antitype(ot_reference: str) -> List[TypologicalCorrespondence]:
    """Get all correspondences where OT reference is the type."""
    return [c for c in ALL_CORRESPONDENCES if ot_reference in c.type_reference]


def get_type(nt_reference: str) -> List[TypologicalCorrespondence]:
    """Get all correspondences where NT reference is the antitype."""
    return [c for c in ALL_CORRESPONDENCES if nt_reference in c.antitype_reference]


def get_by_category(category: TypeCategory) -> List[TypologicalCorrespondence]:
    """Get all correspondences of a specific category."""
    return [c for c in ALL_CORRESPONDENCES if c.category == category]


def get_explicit() -> List[TypologicalCorrespondence]:
    """Get all explicit (NT-identified) correspondences."""
    return [c for c in ALL_CORRESPONDENCES 
            if c.strength == CorrespondenceStrength.EXPLICIT]


def get_sensory_network(sensory_term: str) -> List[TypologicalCorrespondence]:
    """Get all correspondences sharing a sensory link."""
    return [c for c in ALL_CORRESPONDENCES if sensory_term in c.sensory_links]


def build_cross_reference_index() -> Dict[str, Set[str]]:
    """Build bidirectional index of cross-references."""
    index: Dict[str, Set[str]] = {}
    
    for corr in ALL_CORRESPONDENCES:
        # Add type -> antitype
        if corr.type_reference not in index:
            index[corr.type_reference] = set()
        index[corr.type_reference].add(corr.antitype_reference)
        
        # Add antitype -> type
        if corr.antitype_reference not in index:
            index[corr.antitype_reference] = set()
        index[corr.antitype_reference].add(corr.type_reference)
    
    return index


def get_statistics() -> Dict[str, int]:
    """Get statistics about the cross-reference network."""
    return {
        'total_correspondences': len(ALL_CORRESPONDENCES),
        'explicit': len([c for c in ALL_CORRESPONDENCES 
                        if c.strength == CorrespondenceStrength.EXPLICIT]),
        'strong': len([c for c in ALL_CORRESPONDENCES 
                      if c.strength == CorrespondenceStrength.STRONG]),
        'person_types': len([c for c in ALL_CORRESPONDENCES 
                           if c.category == TypeCategory.PERSON]),
        'event_types': len([c for c in ALL_CORRESPONDENCES 
                          if c.category == TypeCategory.EVENT]),
        'ritual_types': len([c for c in ALL_CORRESPONDENCES 
                           if c.category == TypeCategory.RITUAL]),
        'object_types': len([c for c in ALL_CORRESPONDENCES 
                           if c.category == TypeCategory.OBJECT]),
        'psalm_22_fulfillments': len(PSALM_22_FULFILLMENTS),
    }


if __name__ == "__main__":
    stats = get_statistics()
    print("ΒΊΒΛΟΣ ΛΌΓΟΥ Cross-Reference Network")
    print("=" * 40)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 40)
    print("Explicit Types (NT-identified):")
    for corr in get_explicit()[:5]:
        print(f"  {corr.type_description} → {corr.antitype_description}")
