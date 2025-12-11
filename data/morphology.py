#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Extended Hebrew/Greek Morphology
=============================================

Comprehensive morphological data for biblical languages.
Includes grammatical analysis, semantic range, and theological weight.

Per MASTER_PLAN.md: Hebrew/Greek integration creates embodied simulation
through original language resonance.

THE NARRATIVE ENDS AT THE CROSS.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Language(Enum):
    """Biblical language."""
    HEBREW = "hebrew"
    ARAMAIC = "aramaic"
    GREEK = "greek"


class PartOfSpeech(Enum):
    """Grammatical part of speech."""
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PREPOSITION = "preposition"
    CONJUNCTION = "conjunction"
    PARTICLE = "particle"
    INTERJECTION = "interjection"
    PRONOUN = "pronoun"
    ARTICLE = "article"


class VerbStem(Enum):
    """Hebrew verb stems (binyanim)."""
    QAL = "qal"           # Simple active
    NIPHAL = "niphal"     # Simple passive/reflexive
    PIEL = "piel"         # Intensive active
    PUAL = "pual"         # Intensive passive
    HIPHIL = "hiphil"     # Causative active
    HOPHAL = "hophal"     # Causative passive
    HITHPAEL = "hithpael" # Reflexive/reciprocal


class GreekVoice(Enum):
    """Greek voice."""
    ACTIVE = "active"
    MIDDLE = "middle"
    PASSIVE = "passive"


class GreekTense(Enum):
    """Greek tense/aspect."""
    PRESENT = "present"
    IMPERFECT = "imperfect"
    FUTURE = "future"
    AORIST = "aorist"
    PERFECT = "perfect"
    PLUPERFECT = "pluperfect"


class TheologicalWeight(Enum):
    """Weight in theological significance."""
    ULTRA = "ULTRA"     # Highest theological significance
    MAJOR = "MAJOR"     # Major theological term
    STANDARD = "standard"  # Normal significance
    MINOR = "minor"     # Lesser significance


@dataclass(frozen=True)
class HebrewTerm:
    """Complete Hebrew term entry."""
    term: str
    transliteration: str
    strongs: str
    meaning: str
    semantic_range: Tuple[str, ...]
    part_of_speech: PartOfSpeech
    verb_stem: Optional[VerbStem]
    root: Optional[str]
    theological_weight: TheologicalWeight
    key_verses: Tuple[str, ...]
    lxx_equivalent: Optional[str]
    cognates: Tuple[str, ...]
    motif_associations: Tuple[str, ...]


@dataclass(frozen=True)
class GreekTerm:
    """Complete Greek term entry."""
    term: str
    transliteration: str
    strongs: str
    meaning: str
    semantic_range: Tuple[str, ...]
    part_of_speech: PartOfSpeech
    voice: Optional[GreekVoice]
    tense: Optional[GreekTense]
    theological_weight: TheologicalWeight
    key_verses: Tuple[str, ...]
    hebrew_equivalent: Optional[str]
    cognates: Tuple[str, ...]
    motif_associations: Tuple[str, ...]


# ============================================================================
# HEBREW VOCABULARY - ULTRA WEIGHT
# ============================================================================

HEBREW_ULTRA: Dict[str, HebrewTerm] = {
    "בְּרֵאשִׁית": HebrewTerm(
        term="בְּרֵאשִׁית",
        transliteration="bereshit",
        strongs="H7225",
        meaning="in the beginning",
        semantic_range=("beginning", "first", "chief", "head"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="ראש",
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Genesis 1:1", "John 1:1"),
        lxx_equivalent="ἐν ἀρχῇ",
        cognates=("ראש", "ראשון"),
        motif_associations=("CREATION", "WORD"),
    ),
    "יְהוָה": HebrewTerm(
        term="יְהוָה",
        transliteration="YHWH",
        strongs="H3068",
        meaning="the LORD, the self-existent One",
        semantic_range=("LORD", "I AM", "the Existing One"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="הוה",
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Exodus 3:14", "Exodus 6:3", "Isaiah 42:8"),
        lxx_equivalent="κύριος",
        cognates=("היה",),
        motif_associations=("SILENCE", "FIRE", "BREATH"),
    ),
    "שֶׂה": HebrewTerm(
        term="שֶׂה",
        transliteration="seh",
        strongs="H7716",
        meaning="lamb, sheep, goat",
        semantic_range=("lamb", "sheep", "young sheep", "goat"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Genesis 22:7-8", "Exodus 12:3", "Isaiah 53:7"),
        lxx_equivalent="πρόβατον, ἀρνίον",
        cognates=(),
        motif_associations=("LAMB",),
    ),
    "כֶּבֶשׂ": HebrewTerm(
        term="כֶּבֶשׂ",
        transliteration="kebes",
        strongs="H3532",
        meaning="young ram, lamb",
        semantic_range=("lamb", "young ram", "sheep"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Exodus 12:5", "Leviticus 1:10", "Numbers 28:3"),
        lxx_equivalent="ἀμνός",
        cognates=(),
        motif_associations=("LAMB",),
    ),
    "דָּם": HebrewTerm(
        term="דָּם",
        transliteration="dam",
        strongs="H1818",
        meaning="blood",
        semantic_range=("blood", "bloodshed", "guilt of bloodshed"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Genesis 4:10", "Exodus 12:13", "Leviticus 17:11"),
        lxx_equivalent="αἷμα",
        cognates=("אדם",),
        motif_associations=("BLOOD",),
    ),
    "עֵץ": HebrewTerm(
        term="עֵץ",
        transliteration="ets",
        strongs="H6086",
        meaning="tree, wood",
        semantic_range=("tree", "wood", "timber", "gallows", "staff"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Genesis 2:9", "Genesis 22:6", "Deuteronomy 21:23"),
        lxx_equivalent="ξύλον",
        cognates=(),
        motif_associations=("WOOD",),
    ),
    "נְשָׁמָה": HebrewTerm(
        term="נְשָׁמָה",
        transliteration="neshamah",
        strongs="H5397",
        meaning="breath, breath of life",
        semantic_range=("breath", "blast", "spirit", "soul"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="נשם",
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Genesis 2:7", "Job 33:4", "Isaiah 42:5"),
        lxx_equivalent="πνοή",
        cognates=("נשם",),
        motif_associations=("BREATH",),
    ),
    "רוּחַ": HebrewTerm(
        term="רוּחַ",
        transliteration="ruach",
        strongs="H7307",
        meaning="spirit, wind, breath",
        semantic_range=("spirit", "wind", "breath", "mind", "disposition"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Genesis 1:2", "Ezekiel 37:9", "Joel 2:28"),
        lxx_equivalent="πνεῦμα",
        cognates=(),
        motif_associations=("BREATH", "FIRE"),
    ),
    "מַיִם": HebrewTerm(
        term="מַיִם",
        transliteration="mayim",
        strongs="H4325",
        meaning="water, waters",
        semantic_range=("water", "flood", "sea", "spring"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Genesis 1:2", "Exodus 14:21", "Ezekiel 47:1"),
        lxx_equivalent="ὕδωρ",
        cognates=(),
        motif_associations=("WATER",),
    ),
    "אֵשׁ": HebrewTerm(
        term="אֵשׁ",
        transliteration="esh",
        strongs="H784",
        meaning="fire",
        semantic_range=("fire", "flame", "burning"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Exodus 3:2", "Deuteronomy 4:24", "1 Kings 18:38"),
        lxx_equivalent="πῦρ",
        cognates=(),
        motif_associations=("FIRE",),
    ),
}


# ============================================================================
# HEBREW VOCABULARY - MAJOR WEIGHT
# ============================================================================

HEBREW_MAJOR: Dict[str, HebrewTerm] = {
    "דּוּמִיָּה": HebrewTerm(
        term="דּוּמִיָּה",
        transliteration="dumiyah",
        strongs="H1747",
        meaning="silence, stillness",
        semantic_range=("silence", "rest", "stillness", "waiting"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="דמם",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Psalm 62:1", "Psalm 65:1"),
        lxx_equivalent="σιωπή",
        cognates=("דום", "דמם"),
        motif_associations=("SILENCE",),
    ),
    "חֶסֶד": HebrewTerm(
        term="חֶסֶד",
        transliteration="chesed",
        strongs="H2617",
        meaning="steadfast love, lovingkindness, mercy",
        semantic_range=("mercy", "kindness", "faithfulness", "covenant love"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Exodus 34:6", "Psalm 136:1", "Hosea 6:6"),
        lxx_equivalent="ἔλεος",
        cognates=(),
        motif_associations=(),
    ),
    "כָּבוֹד": HebrewTerm(
        term="כָּבוֹד",
        transliteration="kabod",
        strongs="H3519",
        meaning="glory, honor, weight",
        semantic_range=("glory", "honor", "splendor", "abundance"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="כבד",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Exodus 33:18", "Isaiah 6:3", "Ezekiel 1:28"),
        lxx_equivalent="δόξα",
        cognates=("כבד",),
        motif_associations=("FIRE",),
    ),
    "עֹלָה": HebrewTerm(
        term="עֹלָה",
        transliteration="olah",
        strongs="H5930",
        meaning="burnt offering, whole burnt offering",
        semantic_range=("burnt offering", "ascent offering"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="עלה",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Genesis 22:2", "Leviticus 1:3", "Psalm 51:16"),
        lxx_equivalent="ὁλοκαύτωμα",
        cognates=("עלה",),
        motif_associations=("LAMB", "FIRE"),
    ),
    "כַּפָּרָה": HebrewTerm(
        term="כַּפָּרָה",
        transliteration="kapparah",
        strongs="H3724",
        meaning="atonement, covering",
        semantic_range=("atonement", "ransom", "covering"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="כפר",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Leviticus 17:11", "Numbers 5:8"),
        lxx_equivalent="ἱλασμός",
        cognates=("כפר", "כפרת"),
        motif_associations=("BLOOD", "LAMB"),
    ),
    "גָּאַל": HebrewTerm(
        term="גָּאַל",
        transliteration="gaal",
        strongs="H1350",
        meaning="to redeem, act as kinsman",
        semantic_range=("redeem", "ransom", "avenge", "act as kinsman"),
        part_of_speech=PartOfSpeech.VERB,
        verb_stem=VerbStem.QAL,
        root="גאל",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Ruth 4:4", "Isaiah 41:14", "Isaiah 63:16"),
        lxx_equivalent="λυτρόω",
        cognates=("גאלה", "גאל"),
        motif_associations=("BLOOD",),
    ),
    "נֹחַ": HebrewTerm(
        term="נֹחַ",
        transliteration="noach",
        strongs="H5146",
        meaning="rest, comfort (name: Noah)",
        semantic_range=("rest", "comfort", "settle"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="נוח",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Genesis 5:29", "Genesis 6:8"),
        lxx_equivalent="Νῶε",
        cognates=("נוח", "נחם"),
        motif_associations=("WATER",),
    ),
    "שָׁלוֹם": HebrewTerm(
        term="שָׁלוֹם",
        transliteration="shalom",
        strongs="H7965",
        meaning="peace, completeness, welfare",
        semantic_range=("peace", "wholeness", "welfare", "safety"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="שלם",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Numbers 6:26", "Isaiah 9:6", "Isaiah 53:5"),
        lxx_equivalent="εἰρήνη",
        cognates=("שלם",),
        motif_associations=(),
    ),
}


# ============================================================================
# GREEK VOCABULARY - ULTRA WEIGHT
# ============================================================================

GREEK_ULTRA: Dict[str, GreekTerm] = {
    "λόγος": GreekTerm(
        term="λόγος",
        transliteration="logos",
        strongs="G3056",
        meaning="word, reason, account",
        semantic_range=("word", "message", "reason", "account", "matter"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("John 1:1", "John 1:14", "Revelation 19:13"),
        hebrew_equivalent="דָּבָר",
        cognates=("λέγω", "λογίζομαι"),
        motif_associations=("WORD",),
    ),
    "ἀρνίον": GreekTerm(
        term="ἀρνίον",
        transliteration="arnion",
        strongs="G721",
        meaning="lamb (diminutive)",
        semantic_range=("lamb", "little lamb"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("John 21:15", "Revelation 5:6", "Revelation 5:12"),
        hebrew_equivalent="שֶׂה",
        cognates=("ἀμνός",),
        motif_associations=("LAMB",),
    ),
    "ἀμνός": GreekTerm(
        term="ἀμνός",
        transliteration="amnos",
        strongs="G286",
        meaning="lamb",
        semantic_range=("lamb",),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("John 1:29", "John 1:36", "Acts 8:32"),
        hebrew_equivalent="כֶּבֶשׂ",
        cognates=("ἀρνίον",),
        motif_associations=("LAMB",),
    ),
    "αἷμα": GreekTerm(
        term="αἷμα",
        transliteration="haima",
        strongs="G129",
        meaning="blood",
        semantic_range=("blood", "bloodshed"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Matthew 26:28", "Romans 5:9", "Hebrews 9:22"),
        hebrew_equivalent="דָּם",
        cognates=(),
        motif_associations=("BLOOD",),
    ),
    "σταυρός": GreekTerm(
        term="σταυρός",
        transliteration="stauros",
        strongs="G4716",
        meaning="cross, stake",
        semantic_range=("cross", "stake", "crucifixion"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Matthew 27:32", "1 Corinthians 1:18", "Galatians 6:14"),
        hebrew_equivalent="עֵץ",
        cognates=("σταυρόω",),
        motif_associations=("WOOD",),
    ),
    "ξύλον": GreekTerm(
        term="ξύλον",
        transliteration="xulon",
        strongs="G3586",
        meaning="wood, tree, cross",
        semantic_range=("wood", "tree", "club", "cross"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Acts 5:30", "Galatians 3:13", "1 Peter 2:24"),
        hebrew_equivalent="עֵץ",
        cognates=(),
        motif_associations=("WOOD",),
    ),
    "πνεῦμα": GreekTerm(
        term="πνεῦμα",
        transliteration="pneuma",
        strongs="G4151",
        meaning="spirit, breath, wind",
        semantic_range=("spirit", "breath", "wind", "ghost", "disposition"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("John 3:8", "Romans 8:16", "Galatians 5:22"),
        hebrew_equivalent="רוּחַ",
        cognates=("πνέω",),
        motif_associations=("BREATH",),
    ),
    "τετέλεσται": GreekTerm(
        term="τετέλεσται",
        transliteration="tetelestai",
        strongs="G5055",
        meaning="it is finished, it has been completed",
        semantic_range=("complete", "accomplish", "fulfill", "pay"),
        part_of_speech=PartOfSpeech.VERB,
        voice=GreekVoice.PASSIVE,
        tense=GreekTense.PERFECT,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("John 19:30",),
        hebrew_equivalent=None,
        cognates=("τέλος", "τελέω"),
        motif_associations=("SILENCE",),
    ),
    "ἀγάπη": GreekTerm(
        term="ἀγάπη",
        transliteration="agape",
        strongs="G26",
        meaning="love (unconditional)",
        semantic_range=("love", "charity", "affection"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("John 3:16", "1 Corinthians 13:4", "1 John 4:8"),
        hebrew_equivalent="אַהֲבָה",
        cognates=("ἀγαπάω",),
        motif_associations=(),
    ),
}


# ============================================================================
# GREEK VOCABULARY - MAJOR WEIGHT  
# ============================================================================

GREEK_MAJOR: Dict[str, GreekTerm] = {
    "δόξα": GreekTerm(
        term="δόξα",
        transliteration="doxa",
        strongs="G1391",
        meaning="glory, honor, splendor",
        semantic_range=("glory", "honor", "praise", "brightness"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("John 1:14", "Romans 8:18", "2 Corinthians 3:18"),
        hebrew_equivalent="כָּבוֹד",
        cognates=("δοξάζω",),
        motif_associations=("FIRE",),
    ),
    "χάρις": GreekTerm(
        term="χάρις",
        transliteration="charis",
        strongs="G5485",
        meaning="grace, favor, kindness",
        semantic_range=("grace", "favor", "thanks", "gift"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("John 1:14", "Romans 5:20", "Ephesians 2:8"),
        hebrew_equivalent="חֵן",
        cognates=("χαρίζομαι",),
        motif_associations=(),
    ),
    "ἱλασμός": GreekTerm(
        term="ἱλασμός",
        transliteration="hilasmos",
        strongs="G2434",
        meaning="propitiation, atoning sacrifice",
        semantic_range=("propitiation", "expiation", "atonement"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Romans 3:25", "1 John 2:2", "1 John 4:10"),
        hebrew_equivalent="כַּפָּרָה",
        cognates=("ἱλάσκομαι",),
        motif_associations=("BLOOD", "LAMB"),
    ),
    "σιωπή": GreekTerm(
        term="σιωπή",
        transliteration="siope",
        strongs="G4602",
        meaning="silence",
        semantic_range=("silence", "quiet"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Revelation 8:1",),
        hebrew_equivalent="דּוּמִיָּה",
        cognates=("σιωπάω",),
        motif_associations=("SILENCE",),
    ),
    "ὕδωρ": GreekTerm(
        term="ὕδωρ",
        transliteration="hudor",
        strongs="G5204",
        meaning="water",
        semantic_range=("water", "rain"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("John 4:14", "John 7:38", "Revelation 22:1"),
        hebrew_equivalent="מַיִם",
        cognates=(),
        motif_associations=("WATER",),
    ),
    "πῦρ": GreekTerm(
        term="πῦρ",
        transliteration="pur",
        strongs="G4442",
        meaning="fire",
        semantic_range=("fire", "lightning"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Matthew 3:11", "Acts 2:3", "Hebrews 12:29"),
        hebrew_equivalent="אֵשׁ",
        cognates=("πυρόω",),
        motif_associations=("FIRE",),
    ),
    "εἰρήνη": GreekTerm(
        term="εἰρήνη",
        transliteration="eirene",
        strongs="G1515",
        meaning="peace",
        semantic_range=("peace", "harmony", "tranquility"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("John 14:27", "Romans 5:1", "Philippians 4:7"),
        hebrew_equivalent="שָׁלוֹם",
        cognates=(),
        motif_associations=(),
    ),
}


# ============================================================================
# ADDITIONAL HEBREW VOCABULARY
# ============================================================================

HEBREW_ADDITIONAL: Dict[str, HebrewTerm] = {
    "קָדוֹשׁ": HebrewTerm(
        term="קָדוֹשׁ",
        transliteration="qadosh",
        strongs="H6918",
        meaning="holy, sacred, set apart",
        semantic_range=("holy", "sacred", "consecrated", "saint"),
        part_of_speech=PartOfSpeech.ADJECTIVE,
        verb_stem=None,
        root="קדש",
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Isaiah 6:3", "Leviticus 19:2", "Psalm 99:9"),
        lxx_equivalent="ἅγιος",
        cognates=("קדש", "קְדֻשָּׁה"),
        motif_associations=("FIRE",),
    ),
    "בָּרָא": HebrewTerm(
        term="בָּרָא",
        transliteration="bara",
        strongs="H1254",
        meaning="to create (divine creation)",
        semantic_range=("create", "shape", "form", "make new"),
        part_of_speech=PartOfSpeech.VERB,
        verb_stem=VerbStem.QAL,
        root="ברא",
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Genesis 1:1", "Genesis 1:27", "Isaiah 65:17"),
        lxx_equivalent="κτίζω",
        cognates=(),
        motif_associations=("CREATION",),
    ),
    "יָשַׁע": HebrewTerm(
        term="יָשַׁע",
        transliteration="yasha",
        strongs="H3467",
        meaning="to save, deliver, rescue",
        semantic_range=("save", "deliver", "rescue", "help", "preserve"),
        part_of_speech=PartOfSpeech.VERB,
        verb_stem=VerbStem.HIPHIL,
        root="ישע",
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Exodus 14:30", "Psalm 106:21", "Isaiah 43:11"),
        lxx_equivalent="σῴζω",
        cognates=("יֵשׁוּעַ", "יְשׁוּעָה"),
        motif_associations=(),
    ),
    "צֶדֶק": HebrewTerm(
        term="צֶדֶק",
        transliteration="tsedeq",
        strongs="H6664",
        meaning="righteousness, justice",
        semantic_range=("righteousness", "justice", "rightness", "vindication"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="צדק",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Genesis 15:6", "Psalm 85:10", "Isaiah 45:8"),
        lxx_equivalent="δικαιοσύνη",
        cognates=("צַדִּיק", "צְדָקָה"),
        motif_associations=(),
    ),
    "אֱמוּנָה": HebrewTerm(
        term="אֱמוּנָה",
        transliteration="emunah",
        strongs="H530",
        meaning="faithfulness, steadfastness",
        semantic_range=("faithfulness", "truth", "steadfastness", "trust"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="אמן",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Habakkuk 2:4", "Psalm 36:5", "Lamentations 3:23"),
        lxx_equivalent="πίστις",
        cognates=("אָמֵן", "אֱמֶת"),
        motif_associations=(),
    ),
    "תְּשׁוּבָה": HebrewTerm(
        term="תְּשׁוּבָה",
        transliteration="teshuvah",
        strongs="H8666",
        meaning="repentance, return",
        semantic_range=("repentance", "return", "turning back", "answer"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="שוב",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Hosea 14:2", "Joel 2:12"),
        lxx_equivalent="μετάνοια",
        cognates=("שׁוּב",),
        motif_associations=(),
    ),
    "מָשִׁיחַ": HebrewTerm(
        term="מָשִׁיחַ",
        transliteration="mashiach",
        strongs="H4899",
        meaning="anointed one, Messiah",
        semantic_range=("anointed", "Messiah", "Christ"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="משח",
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Daniel 9:25-26", "Psalm 2:2", "1 Samuel 2:10"),
        lxx_equivalent="Χριστός",
        cognates=("משח",),
        motif_associations=("LAMB",),
    ),
    "בְּרִית": HebrewTerm(
        term="בְּרִית",
        transliteration="berit",
        strongs="H1285",
        meaning="covenant, treaty",
        semantic_range=("covenant", "agreement", "treaty", "alliance"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Genesis 15:18", "Exodus 24:8", "Jeremiah 31:31"),
        lxx_equivalent="διαθήκη",
        cognates=(),
        motif_associations=("BLOOD",),
    ),
    "עֶבֶד": HebrewTerm(
        term="עֶבֶד",
        transliteration="ebed",
        strongs="H5650",
        meaning="servant, slave",
        semantic_range=("servant", "slave", "worshiper"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root="עבד",
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Isaiah 52:13", "Isaiah 53:11", "Psalm 113:1"),
        lxx_equivalent="δοῦλος, παῖς",
        cognates=("עָבַד",),
        motif_associations=("LAMB",),
    ),
    "נֶפֶשׁ": HebrewTerm(
        term="נֶפֶשׁ",
        transliteration="nephesh",
        strongs="H5315",
        meaning="soul, life, self",
        semantic_range=("soul", "life", "person", "self", "appetite"),
        part_of_speech=PartOfSpeech.NOUN,
        verb_stem=None,
        root=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Genesis 2:7", "Leviticus 17:11", "Psalm 42:1"),
        lxx_equivalent="ψυχή",
        cognates=(),
        motif_associations=("BREATH",),
    ),
}


# ============================================================================
# ADDITIONAL GREEK VOCABULARY
# ============================================================================

GREEK_ADDITIONAL: Dict[str, GreekTerm] = {
    "ἅγιος": GreekTerm(
        term="ἅγιος",
        transliteration="hagios",
        strongs="G40",
        meaning="holy, sacred, set apart",
        semantic_range=("holy", "sacred", "saint"),
        part_of_speech=PartOfSpeech.ADJECTIVE,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Revelation 4:8", "1 Peter 1:16", "Matthew 6:9"),
        hebrew_equivalent="קָדוֹשׁ",
        cognates=("ἁγιάζω", "ἁγιασμός"),
        motif_associations=("FIRE",),
    ),
    "σῴζω": GreekTerm(
        term="σῴζω",
        transliteration="sozo",
        strongs="G4982",
        meaning="to save, rescue, deliver",
        semantic_range=("save", "rescue", "heal", "preserve"),
        part_of_speech=PartOfSpeech.VERB,
        voice=GreekVoice.ACTIVE,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Matthew 1:21", "Romans 10:9", "Ephesians 2:8"),
        hebrew_equivalent="יָשַׁע",
        cognates=("σωτήρ", "σωτηρία"),
        motif_associations=(),
    ),
    "δικαιοσύνη": GreekTerm(
        term="δικαιοσύνη",
        transliteration="dikaiosune",
        strongs="G1343",
        meaning="righteousness, justice",
        semantic_range=("righteousness", "justice", "justification"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Romans 3:21", "Matthew 5:6", "Philippians 3:9"),
        hebrew_equivalent="צֶדֶק",
        cognates=("δίκαιος", "δικαιόω"),
        motif_associations=(),
    ),
    "πίστις": GreekTerm(
        term="πίστις",
        transliteration="pistis",
        strongs="G4102",
        meaning="faith, trust, belief",
        semantic_range=("faith", "trust", "belief", "faithfulness"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Romans 1:17", "Hebrews 11:1", "Galatians 2:20"),
        hebrew_equivalent="אֱמוּנָה",
        cognates=("πιστεύω", "πιστός"),
        motif_associations=(),
    ),
    "μετάνοια": GreekTerm(
        term="μετάνοια",
        transliteration="metanoia",
        strongs="G3341",
        meaning="repentance, change of mind",
        semantic_range=("repentance", "change of mind", "conversion"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Matthew 3:8", "Acts 2:38", "2 Corinthians 7:10"),
        hebrew_equivalent="תְּשׁוּבָה",
        cognates=("μετανοέω",),
        motif_associations=(),
    ),
    "Χριστός": GreekTerm(
        term="Χριστός",
        transliteration="Christos",
        strongs="G5547",
        meaning="Christ, Anointed One, Messiah",
        semantic_range=("Christ", "Messiah", "Anointed"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Matthew 16:16", "John 1:41", "Acts 2:36"),
        hebrew_equivalent="מָשִׁיחַ",
        cognates=("χρίω",),
        motif_associations=("LAMB",),
    ),
    "διαθήκη": GreekTerm(
        term="διαθήκη",
        transliteration="diatheke",
        strongs="G1242",
        meaning="covenant, testament",
        semantic_range=("covenant", "testament", "will"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Matthew 26:28", "Hebrews 9:15", "2 Corinthians 3:6"),
        hebrew_equivalent="בְּרִית",
        cognates=(),
        motif_associations=("BLOOD",),
    ),
    "κύριος": GreekTerm(
        term="κύριος",
        transliteration="kurios",
        strongs="G2962",
        meaning="Lord, master",
        semantic_range=("Lord", "master", "sir", "owner"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("Romans 10:9", "Philippians 2:11", "Revelation 19:16"),
        hebrew_equivalent="יְהוָה, אֲדֹנָי",
        cognates=("κυριεύω",),
        motif_associations=(),
    ),
    "ἀνάστασις": GreekTerm(
        term="ἀνάστασις",
        transliteration="anastasis",
        strongs="G386",
        meaning="resurrection, rising",
        semantic_range=("resurrection", "rising up", "raising"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("John 11:25", "Romans 6:5", "1 Corinthians 15:42"),
        hebrew_equivalent=None,
        cognates=("ἀνίστημι",),
        motif_associations=("BREATH",),
    ),
    "ψυχή": GreekTerm(
        term="ψυχή",
        transliteration="psuche",
        strongs="G5590",
        meaning="soul, life, self",
        semantic_range=("soul", "life", "self", "person"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Matthew 16:26", "Luke 12:20", "1 Peter 2:25"),
        hebrew_equivalent="נֶפֶשׁ",
        cognates=(),
        motif_associations=("BREATH",),
    ),
    "θάνατος": GreekTerm(
        term="θάνατος",
        transliteration="thanatos",
        strongs="G2288",
        meaning="death",
        semantic_range=("death", "mortality"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.MAJOR,
        key_verses=("Romans 6:23", "1 Corinthians 15:26", "Revelation 21:4"),
        hebrew_equivalent="מָוֶת",
        cognates=("θνῄσκω",),
        motif_associations=("SILENCE",),
    ),
    "ζωή": GreekTerm(
        term="ζωή",
        transliteration="zoe",
        strongs="G2222",
        meaning="life",
        semantic_range=("life", "living", "vitality"),
        part_of_speech=PartOfSpeech.NOUN,
        voice=None,
        tense=None,
        theological_weight=TheologicalWeight.ULTRA,
        key_verses=("John 1:4", "John 14:6", "1 John 5:12"),
        hebrew_equivalent="חַיִּים",
        cognates=("ζάω",),
        motif_associations=("BREATH",),
    ),
}


# ============================================================================
# UNIFIED REGISTRY
# ============================================================================

ALL_HEBREW: Dict[str, HebrewTerm] = {**HEBREW_ULTRA, **HEBREW_MAJOR, **HEBREW_ADDITIONAL}
ALL_GREEK: Dict[str, GreekTerm] = {**GREEK_ULTRA, **GREEK_MAJOR, **GREEK_ADDITIONAL}


def get_hebrew_term(term: str) -> Optional[HebrewTerm]:
    """Get a Hebrew term by its Hebrew text."""
    return ALL_HEBREW.get(term)


def get_greek_term(term: str) -> Optional[GreekTerm]:
    """Get a Greek term by its Greek text."""
    return ALL_GREEK.get(term)


def get_terms_by_motif(motif: str) -> Tuple[List[HebrewTerm], List[GreekTerm]]:
    """Get all Hebrew and Greek terms associated with a motif."""
    hebrew = [t for t in ALL_HEBREW.values() if motif in t.motif_associations]
    greek = [t for t in ALL_GREEK.values() if motif in t.motif_associations]
    return hebrew, greek


def get_ultra_terms() -> Tuple[List[HebrewTerm], List[GreekTerm]]:
    """Get all ULTRA weight terms."""
    return list(HEBREW_ULTRA.values()), list(GREEK_ULTRA.values())


def get_statistics() -> Dict[str, int]:
    """Get statistics about the morphology database."""
    return {
        'total_hebrew': len(ALL_HEBREW),
        'total_greek': len(ALL_GREEK),
        'hebrew_ultra': len(HEBREW_ULTRA),
        'hebrew_major': len(HEBREW_MAJOR),
        'greek_ultra': len(GREEK_ULTRA),
        'greek_major': len(GREEK_MAJOR),
    }


if __name__ == "__main__":
    stats = get_statistics()
    print("ΒΊΒΛΟΣ ΛΌΓΟΥ Hebrew/Greek Morphology")
    print("=" * 40)
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 40)
    print("ULTRA Weight Hebrew Terms:")
    for term in HEBREW_ULTRA.values():
        print(f"  {term.term} ({term.transliteration}) = {term.meaning}")
    
    print("\nULTRA Weight Greek Terms:")
    for term in GREEK_ULTRA.values():
        print(f"  {term.term} ({term.transliteration}) = {term.meaning}")
