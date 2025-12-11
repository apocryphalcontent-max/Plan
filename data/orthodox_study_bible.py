#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Orthodox Study Bible - Pre-Computed Exegetical Data
===============================================================

The narrative ENDS at the Cross. Christ's final breath is the terminal point.
Everything else - resurrection, burial, Revelation, Pentecost - must come BEFORE
in the non-linear narrative order.

Per Hermeneutical.txt:
- Local emotional honesty preserved (each verse keeps its native mood)
- Global dread architecture (blood-red sky from arrangement, not repainting)
- Pattern pressure without visible machinery (recognition does the work)
- Temporal folding through planted phrases that echo
- No gimmicks - events presented as-is, arrangement does the work

TERMINAL POINT: "He bows his head and gives up his spirit"
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, NamedTuple
from dataclasses import dataclass, field
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent.parent))


class TonalWeight(Enum):
    """Tonal weight per Hermeneutical.txt"""
    LIGHT = "light"
    NEUTRAL = "neutral"
    UNSETTLING = "unsettling"
    HEAVY = "heavy"
    TRANSCENDENT = "transcendent"


class NarrativeFunction(Enum):
    """Narrative function within larger structure"""
    SCENE_SETTING = "scene-setting"
    EXPOSITION = "exposition"
    DEVELOPMENT = "development"
    INTENSIFICATION = "intensification"
    CLIMAX = "climax"
    RESOLUTION = "resolution"
    ECHO = "echo"
    SEED = "seed"


@dataclass(frozen=True)
class VerseExegesis:
    """Complete pre-computed exegesis for a single verse."""
    reference: str
    text: str
    literal: str
    allegorical: str
    tropological: str
    anagogical: str
    emotional_valence: float
    theological_weight: float
    sensory_intensity: float
    tonal_weight: TonalWeight
    native_mood: str
    dread_amplification: float
    narrative_function: NarrativeFunction
    breath_rhythm: str
    typological_shadows: Tuple[str, ...]
    typological_fulfillments: Tuple[str, ...]
    cross_references: Tuple[str, ...]
    visual_seeds: Tuple[str, ...]
    auditory_seeds: Tuple[str, ...]
    tactile_seeds: Tuple[str, ...]
    plants_phrase: Optional[str] = None
    echoes_phrase: Optional[str] = None


# ============================================================================
# GENESIS - THE FOUNDATION
# ============================================================================

GENESIS_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "Genesis 1:1": VerseExegesis(
        reference="Genesis 1:1",
        text="In the beginning God created the heaven and the earth.",
        literal="The absolute beginning of created existence. God (Elohim) creates ex nihilo. Heaven and earth constitute totality: invisible and visible realms. There was a beginning, and God was before it.",
        allegorical="'In the beginning was the Word' (John 1:1). The Father creates through the Son in the Spirit. This beginning anticipates the new beginning in Christ.",
        tropological="If God is Creator, I am creature—radically dependent. This recognition is the foundation of humility.",
        anagogical="'Behold, I make all things new' (Rev 21:5). The first creation points toward new heaven and new earth.",
        emotional_valence=0.85, theological_weight=1.0, sensory_intensity=0.70,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Majestic wonder at the threshold of being",
        dread_amplification=0.2,
        narrative_function=NarrativeFunction.SCENE_SETTING,
        breath_rhythm="sustained",
        typological_shadows=(),
        typological_fulfillments=("John 1:1-3", "Colossians 1:16", "Revelation 21:1"),
        cross_references=("Psalm 33:6", "Isaiah 42:5", "John 1:1"),
        visual_seeds=("primordial darkness giving way to light", "void pregnant with potential"),
        auditory_seeds=("silence before the first word", "voice that speaks worlds"),
        tactile_seeds=("weight of nothingness before creation",),
        plants_phrase="In the beginning"
    ),
    
    "Genesis 1:3": VerseExegesis(
        reference="Genesis 1:3",
        text="And God said, Let there be light: and there was light.",
        literal="The first divine speech-act. God speaks and reality obeys. Light exists because God wills it. Not the sun (Day 4) but light itself.",
        allegorical="'I am the light of the world' (John 8:12). The light that pierces darkness is Christ, the true Light.",
        tropological="'Walk as children of light' (Eph 5:8). God speaks His Word into the darkness of the heart.",
        anagogical="'The Lamb is the light thereof' (Rev 21:23). The light of Day One finds consummation in the Light of the Lamb.",
        emotional_valence=0.95, theological_weight=0.98, sensory_intensity=0.95,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Explosive joy as darkness shatters",
        dread_amplification=0.1,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="punctuated",
        typological_shadows=(),
        typological_fulfillments=("John 1:4-5", "John 8:12", "2 Corinthians 4:6"),
        cross_references=("Psalm 27:1", "Isaiah 9:2", "John 1:4-9"),
        visual_seeds=("light breaking through darkness", "first dawn"),
        auditory_seeds=("the word that creates", "divine fiat echoing through void"),
        tactile_seeds=("warmth of first light", "darkness giving way"),
        plants_phrase="Let there be light"
    ),
    
    "Genesis 2:7": VerseExegesis(
        reference="Genesis 2:7",
        text="And the LORD God formed man of the dust of the ground, and breathed into his nostrils the breath of life; and man became a living soul.",
        literal="YHWH Elohim forms (yatsar, like a potter) man from dust (adamah). Then the intimate act: God breathes into human nostrils. Body and soul united.",
        allegorical="Christ will breathe on disciples: 'Receive ye the Holy Ghost' (John 20:22). The first breath prefigures the second.",
        tropological="I am dust animated by divine breath. This guards against both pride and despair.",
        anagogical="The resurrection of the body fulfills what creation began. The dust will rise; the breath will return.",
        emotional_valence=0.85, theological_weight=0.95, sensory_intensity=0.90,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Intimate tenderness in the creative act",
        dread_amplification=0.1,
        narrative_function=NarrativeFunction.DEVELOPMENT,
        breath_rhythm="sustained",
        typological_shadows=(),
        typological_fulfillments=("John 20:22", "1 Corinthians 15:45"),
        cross_references=("Psalm 103:14", "Ecclesiastes 12:7", "Job 33:4"),
        visual_seeds=("divine hands shaping clay", "face bent close to breathe"),
        auditory_seeds=("first human breath", "whisper of life"),
        tactile_seeds=("dust becoming flesh", "breath entering nostrils"),
        plants_phrase="dust of the ground"
    ),
    
    "Genesis 3:15": VerseExegesis(
        reference="Genesis 3:15",
        text="And I will put enmity between thee and the woman, and between thy seed and her seed; it shall bruise thy head, and thou shalt bruise his heel.",
        literal="The protoevangelium. God curses the serpent but prophesies victory. The woman's seed will crush the serpent's head, though suffering a wounded heel. The war begins.",
        allegorical="Christ is the Seed of the woman. He crushes Satan's head at the Cross, though His heel is bruised—wounded but not destroyed.",
        tropological="The reader enters the enmity. Every temptation resisted is victory; every sin is siding with the enemy.",
        anagogical="'The devil was cast into the lake of fire' (Rev 20:10). The final crushing is certain.",
        emotional_valence=0.50, theological_weight=1.0, sensory_intensity=0.75,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Grim hope in the midst of curse",
        dread_amplification=0.7,
        narrative_function=NarrativeFunction.SEED,
        breath_rhythm="punctuated",
        typological_shadows=(),
        typological_fulfillments=("Romans 16:20", "Galatians 4:4", "Revelation 12:9", "Revelation 20:10"),
        cross_references=("Isaiah 7:14", "Revelation 12:17", "Hebrews 2:14"),
        visual_seeds=("serpent striking at heel", "head crushed beneath foot"),
        auditory_seeds=("curse pronounced", "enmity declared"),
        tactile_seeds=("bruised heel", "serpent writhing"),
        plants_phrase="bruise thy head, bruise his heel"
    ),
    
    "Genesis 22:2": VerseExegesis(
        reference="Genesis 22:2",
        text="And he said, Take now thy son, thine only son Isaac, whom thou lovest, and get thee into the land of Moriah; and offer him there for a burnt offering upon one of the mountains which I will tell thee of.",
        literal="The test of Abraham. God commands the unthinkable. Every word intensifies: 'thy son'—'thine only son'—'whom thou lovest.' Moriah is Jerusalem.",
        allegorical="'God so loved the world, that he gave his only begotten Son' (John 3:16). What God asked of Abraham, God performed. Isaac carrying wood prefigures Christ carrying the cross.",
        tropological="The call to radical surrender. What is my Isaac? God requires willingness. The knife must be raised before the ram appears.",
        anagogical="The Lamb slain from the foundation of the world (Rev 13:8). What Abraham glimpsed, heaven sees eternally.",
        emotional_valence=0.25, theological_weight=1.0, sensory_intensity=0.85,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Terrible command piercing paternal love",
        dread_amplification=0.95,
        narrative_function=NarrativeFunction.SEED,
        breath_rhythm="punctuated",
        typological_shadows=(),
        typological_fulfillments=("John 3:16", "Romans 8:32", "Hebrews 11:17-19"),
        cross_references=("2 Chronicles 3:1", "Hebrews 11:17", "James 2:21"),
        visual_seeds=("wood laid on young shoulders", "mountain rising ahead", "knife catching sun"),
        auditory_seeds=("terrible command", "silence of obedience"),
        tactile_seeds=("grain of wood against shoulder", "cold weight of knife"),
        plants_phrase="thine only son Isaac, whom thou lovest"
    ),
    
    "Genesis 22:8": VerseExegesis(
        reference="Genesis 22:8",
        text="And Abraham said, My son, God will provide himself a lamb for a burnt offering: so they went both of them together.",
        literal="Isaac's question pierces: 'Where is the lamb?' Abraham's answer is faith's prophecy: 'God will provide himself a lamb.' They walk together—both unaware how much walks with them.",
        allegorical="'Behold the Lamb of God' (John 1:29). Abraham spoke better than he knew. God did provide Himself as the Lamb.",
        tropological="Faith speaks before it sees. The soul that trusts walks with God even up the mountain of sacrifice.",
        anagogical="'Worthy is the Lamb that was slain' (Rev 5:12). The provision of Moriah becomes the worship of heaven.",
        emotional_valence=0.40, theological_weight=0.98, sensory_intensity=0.70,
        tonal_weight=TonalWeight.UNSETTLING,
        native_mood="Faith speaking through dread",
        dread_amplification=0.8,
        narrative_function=NarrativeFunction.INTENSIFICATION,
        breath_rhythm="sustained",
        typological_shadows=(),
        typological_fulfillments=("John 1:29", "1 Peter 1:19-20", "Revelation 5:6"),
        cross_references=("Genesis 22:14", "John 1:29", "Hebrews 11:17-19"),
        visual_seeds=("father and son walking together", "mountain slope ahead"),
        auditory_seeds=("child's question", "father's answer from somewhere deeper than knowledge"),
        tactile_seeds=("hand in hand ascending", "weight of wood, weight of silence"),
        plants_phrase="God will provide himself a lamb"
    ),
}


# ============================================================================
# ISAIAH - THE EVANGELICAL PROPHET
# ============================================================================

ISAIAH_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "Isaiah 53:5": VerseExegesis(
        reference="Isaiah 53:5",
        text="But he was wounded for our transgressions, he was bruised for our iniquities: the chastisement of our peace was upon him; and with his stripes we are healed.",
        literal="The Suffering Servant bears wounds for others' transgressions. He is bruised (crushed) for their iniquities. His stripes effect healing.",
        allegorical="Every word finds fulfillment in Christ's Passion. The scourging, thorns, nails, spear—all anticipated here.",
        tropological="Contemplation of Christ's wounds transforms the soul. His stripes become our healing through meditation and love.",
        anagogical="The wounds remain glorified. The risen Christ shows His hands and side. The Lamb stands 'as it had been slain.'",
        emotional_valence=0.30, theological_weight=1.0, sensory_intensity=0.95,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Grief and gratitude intertwined",
        dread_amplification=0.9,
        narrative_function=NarrativeFunction.SEED,
        breath_rhythm="punctuated",
        typological_shadows=("Genesis 22:8", "Exodus 12:13", "Leviticus 16:21"),
        typological_fulfillments=("Matthew 27:26", "1 Peter 2:24", "Hebrews 9:28"),
        cross_references=("Romans 4:25", "1 Corinthians 15:3", "2 Corinthians 5:21"),
        visual_seeds=("wounds opened by whip", "blood running down torn flesh"),
        auditory_seeds=("silence under the lash", "no cry escaping lips"),
        tactile_seeds=("stripes raised on back", "flesh torn by scourge"),
        plants_phrase="with his stripes we are healed"
    ),
    
    "Isaiah 53:7": VerseExegesis(
        reference="Isaiah 53:7",
        text="He was oppressed, and he was afflicted, yet he opened not his mouth: he is brought as a lamb to the slaughter, and as a sheep before her shearers is dumb, so he openeth not his mouth.",
        literal="The Servant's silence under affliction. Oppressed and afflicted, yet mute. Lamb to slaughter, sheep before shearers. Not struggling, not bleating. The silence is chosen.",
        allegorical="'He answered nothing' (Mark 15:5). Before Pilate, before Herod, Christ maintained the silence prophesied here.",
        tropological="The patience of the Lamb becomes the pattern for the Christian. The closed mouth under injustice is cruciform love.",
        anagogical="The Lamb who was silent at slaughter speaks from the throne. The mute One will judge.",
        emotional_valence=0.20, theological_weight=0.95, sensory_intensity=0.85,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Crushing weight of chosen silence",
        dread_amplification=0.95,
        narrative_function=NarrativeFunction.INTENSIFICATION,
        breath_rhythm="sustained",
        typological_shadows=("Genesis 22:7-8",),
        typological_fulfillments=("Mark 14:61", "Mark 15:5", "Acts 8:32-35", "1 Peter 2:23"),
        cross_references=("Matthew 26:63", "John 1:29", "1 Peter 2:21-24"),
        visual_seeds=("lamb led without resistance", "mouth closed under accusation"),
        auditory_seeds=("terrible silence where defense should be", "no bleat, no plea"),
        tactile_seeds=("rough hands pushing forward", "wool of lamb beneath knife"),
        plants_phrase="as a lamb to the slaughter"
    ),
}


# ============================================================================
# JOHN'S GOSPEL - THE SPIRITUAL GOSPEL
# ============================================================================

JOHN_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "John 1:1": VerseExegesis(
        reference="John 1:1",
        text="In the beginning was the Word, and the Word was with God, and the Word was God.",
        literal="En arche—echoing Genesis 1:1. The Logos existed in the beginning—eternally. Three affirmations: eternal existence, distinct person, divine nature.",
        allegorical="The eternal Son revealed in pre-incarnate glory. The Word who spoke creation is identified as a Person.",
        tropological="To know Christ is to know One who was before time, who is its Creator, who will be its Judge.",
        anagogical="The Logos who was in the beginning will be in the end. Alpha and Omega meet in the Logos.",
        emotional_valence=0.90, theological_weight=1.0, sensory_intensity=0.50,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Awe at eternity unveiled",
        dread_amplification=0.15,
        narrative_function=NarrativeFunction.SCENE_SETTING,
        breath_rhythm="sustained",
        typological_shadows=("Genesis 1:1",),
        typological_fulfillments=("Revelation 19:13",),
        cross_references=("Genesis 1:1", "Proverbs 8:22-31", "Colossians 1:15-17"),
        visual_seeds=("darkness before creation", "light dwelling with light"),
        auditory_seeds=("the Word before all words", "eternal conversation of Father and Son"),
        tactile_seeds=("weight of eternity",),
        echoes_phrase="In the beginning",
        plants_phrase="the Word was God"
    ),
    
    "John 1:14": VerseExegesis(
        reference="John 1:14",
        text="And the Word was made flesh, and dwelt among us, (and we beheld his glory, the glory as of the only begotten of the Father,) full of grace and truth.",
        literal="Ho Logos sarx egeneto—the Word became flesh. Eskēnōsen—tabernacled among us. Eyewitness testimony: 'we beheld.'",
        allegorical="The tabernacle fulfilled: God dwelling not in a tent but in human flesh. Glory once hidden behind curtains revealed in a face.",
        tropological="God became flesh that flesh might be divinized. Every body is potentially a temple.",
        anagogical="'The tabernacle of God is with men' (Rev 21:3). The tabernacling reaches consummation in the New Jerusalem.",
        emotional_valence=0.95, theological_weight=1.0, sensory_intensity=0.85,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Wonder at God entering flesh",
        dread_amplification=0.1,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="sustained",
        typological_shadows=("Exodus 40:34", "Isaiah 7:14"),
        typological_fulfillments=("Revelation 21:3",),
        cross_references=("Matthew 1:23", "Philippians 2:6-7", "1 Timothy 3:16"),
        visual_seeds=("glory veiled in flesh", "tabernacle become person"),
        auditory_seeds=("Word speaking with human voice", "baby's cry from eternal Logos"),
        tactile_seeds=("divine flesh that can be touched", "the Word handled"),
        echoes_phrase="the Word was God"
    ),
    
    "John 1:29": VerseExegesis(
        reference="John 1:29",
        text="The next day John seeth Jesus coming unto him, and saith, Behold the Lamb of God, which taketh away the sin of the world.",
        literal="The Baptist's proclamation: Behold the Lamb of God. Not merely a lamb for God's use but God's own Lamb. Airōn—taking away, lifting, bearing.",
        allegorical="Every lamb of sacrifice finds meaning here. Abraham's prophecy finally answered: here is the Lamb.",
        tropological="'Behold' is imperative: look, contemplate. The Christian life is beholding the Lamb.",
        anagogical="The Lamb of John 1 is the Lamb of Revelation 5—slain yet standing, worshiped by every creature.",
        emotional_valence=0.85, theological_weight=1.0, sensory_intensity=0.75,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Recognition of the Long-Awaited",
        dread_amplification=0.3,
        narrative_function=NarrativeFunction.ECHO,
        breath_rhythm="punctuated",
        typological_shadows=("Genesis 22:8", "Exodus 12:3-13", "Isaiah 53:7"),
        typological_fulfillments=("1 Corinthians 5:7", "1 Peter 1:19", "Revelation 5:6-14"),
        cross_references=("Isaiah 53:7", "Acts 8:32", "Revelation 5:6"),
        visual_seeds=("finger pointing across Jordan", "Lamb walking toward identifier"),
        auditory_seeds=("voice crying in wilderness now naming", "Behold!"),
        tactile_seeds=("approach of the One long awaited",),
        echoes_phrase="God will provide himself a lamb"
    ),
    
    "John 19:30": VerseExegesis(
        reference="John 19:30",
        text="When Jesus therefore had received the vinegar, he said, It is finished: and he bowed his head, and gave up the ghost.",
        literal="Tetelestai—finished, completed, paid in full. Perfect tense: completed action with abiding results. He bowed and handed over His spirit. Death was given, not taken.",
        allegorical="What was finished? The work the Father gave. The prophecies. The new creation. The defeat of Satan. Everything.",
        tropological="The reader's salvation depends on this finished work. Nothing can be added. The response is reception, not achievement.",
        anagogical="The finished work is the foundation of new creation. 'Worthy is the Lamb' is heaven's eternal response to 'It is finished.'",
        emotional_valence=0.40, theological_weight=1.0, sensory_intensity=0.90,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Triumphant surrender",
        dread_amplification=0.85,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="punctuated",
        typological_shadows=("Genesis 2:2", "Isaiah 53:10-12"),
        typological_fulfillments=("Hebrews 10:12-14", "Revelation 21:6"),
        cross_references=("John 17:4", "Romans 10:4", "Hebrews 9:12"),
        visual_seeds=("head bowing in chosen death", "last breath leaving"),
        auditory_seeds=("single word that ends all debt", "Tetelestai"),
        tactile_seeds=("vinegar on cracked lips", "head heavy, resting"),
        echoes_phrase="with his stripes we are healed"
    ),
}


# ============================================================================
# REVELATION - PLACED BEFORE THE CROSS IN NARRATIVE ORDER
# ============================================================================

REVELATION_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "Revelation 5:6": VerseExegesis(
        reference="Revelation 5:6",
        text="And I beheld, and, lo, in the midst of the throne and of the four beasts, and in the midst of the elders, stood a Lamb as it had been slain, having seven horns and seven eyes, which are the seven Spirits of God sent forth into all the earth.",
        literal="Central vision: a Lamb (arnion, diminutive) standing as though slain, bearing sacrifice's marks. Seven horns (perfect power), seven eyes (perfect knowledge). The Lamb at heaven's center.",
        allegorical="Every lamb of Scripture converges here. The Crucified One stands eternally in His sacrifice. The wounds are glorified.",
        tropological="We worship not despite the wounds but because of them. Our sufferings share in this eternal glory.",
        anagogical="This is the eternal reality. The Lamb at heaven's center is where creation has always been heading.",
        emotional_valence=0.90, theological_weight=1.0, sensory_intensity=0.95,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Overwhelming wonder at glorified sacrifice",
        dread_amplification=0.2,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="sustained",
        typological_shadows=("Genesis 22:8", "Exodus 12:5", "Isaiah 53:7", "John 1:29"),
        typological_fulfillments=(),
        cross_references=("John 1:29", "1 Peter 1:19", "Revelation 5:12"),
        visual_seeds=("Lamb standing as slain", "throne surrounded by living creatures"),
        auditory_seeds=("hush before worship begins", "silence of recognition"),
        tactile_seeds=("weight of glory", "wounds transformed to radiance"),
        echoes_phrase="as a lamb to the slaughter"
    ),
    
    "Revelation 21:4": VerseExegesis(
        reference="Revelation 21:4",
        text="And God shall wipe away all tears from their eyes; and there shall be no more death, neither sorrow, nor crying, neither shall there be any more pain: for the former things are passed away.",
        literal="Total restoration. God Himself wipes tears. Four negations: no death, no sorrow, no crying, no pain. The former order has passed.",
        allegorical="What began in Eden's curse ends in blessing. The sword that barred Paradise is sheathed. Death is reversed.",
        tropological="This hope transforms present suffering. Present tears are future joy in seed form.",
        anagogical="This IS the eschaton. Every prayer 'Thy kingdom come' finds answer here.",
        emotional_valence=1.0, theological_weight=0.95, sensory_intensity=0.85,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Joy beyond grief's memory",
        dread_amplification=0.0,
        narrative_function=NarrativeFunction.RESOLUTION,
        breath_rhythm="flowing",
        typological_shadows=("Genesis 3:17-19", "Isaiah 25:8"),
        typological_fulfillments=(),
        cross_references=("Isaiah 25:8", "Isaiah 35:10", "Revelation 7:17"),
        visual_seeds=("divine hand wiping tears", "radiance where tears were"),
        auditory_seeds=("silence where weeping was", "laughter replacing mourning"),
        tactile_seeds=("tears dried from cheeks", "lightness where burden was"),
        echoes_phrase="dust thou art"
    ),
}


# ============================================================================
# THE NARRATIVE ORDER - TERMINUS AT THE CROSS
# ============================================================================

# This is the precise verse-by-verse ordering where everything serves
# the terrible, beautiful ending: "He bows his head and gives up his spirit"

NARRATIVE_ORDER: List[str] = [
    # PROLOGUE: The Three-Thread Collapse (interwoven strands toward incarnation)
    # [These would be the opening sections per Hermeneutical.txt]
    
    # PART ONE: Before All Things / The Infant Breathes
    # Creation and Nativity interwoven
    "Genesis 1:1",      # Creation of light - paired with
    # The star (Matthew 2)
    "Genesis 1:3",      # Let there be light
    # ... interwoven with Magi following star
    
    # The Fall and the First Blood
    "Genesis 3:15",     # Protoevangelium - seed that will crush
    
    # The Patriarchs
    "Genesis 22:2",     # Take now thy son, thine only son
    "Genesis 22:8",     # God will provide himself a lamb
    
    # The Prophets
    "Isaiah 53:5",      # Wounded for our transgressions
    "Isaiah 53:7",      # As a lamb to the slaughter
    
    # The Incarnate Word
    "John 1:1",         # In the beginning was the Word
    "John 1:14",        # The Word became flesh
    "John 1:29",        # Behold the Lamb of God
    
    # BEFORE THE END: Revelation shown early, so its glory haunts what follows
    "Revelation 21:4",  # No more tears (shown before the Cross, so reader knows
                        # that THIS is what will cost everything)
    "Revelation 5:6",   # Lamb standing as slain (the vision that precedes
                        # the reality, so when we reach the Cross, we see
                        # what it becomes)
    
    # THE PASSION
    # [All events of Holy Week leading to...]
    
    # THE TERMINUS
    "John 19:30",       # It is finished. He bows his head. He gives up the ghost.
    
    # THE NARRATIVE ENDS HERE.
    # No resurrection. No tomb. No Pentecost.
    # Those are placed BEFORE in the narrative order.
    # The reader ends at the Cross, implicated, devastated, transformed.
]


# ============================================================================
# MASTER REGISTRY
# ============================================================================

ORTHODOX_STUDY_BIBLE: Dict[str, Dict[str, VerseExegesis]] = {
    'Genesis': GENESIS_EXEGESIS,
    'Isaiah': ISAIAH_EXEGESIS,
    'John': JOHN_EXEGESIS,
    'Revelation': REVELATION_EXEGESIS,
}


def get_verse_exegesis(reference: str) -> Optional[VerseExegesis]:
    """Get pre-computed exegesis for a verse reference."""
    for book_data in ORTHODOX_STUDY_BIBLE.values():
        if reference in book_data:
            return book_data[reference]
    return None


def get_book_exegesis(book_name: str) -> Dict[str, VerseExegesis]:
    """Get all pre-computed exegesis for a book."""
    return ORTHODOX_STUDY_BIBLE.get(book_name, {})


def get_narrative_order() -> List[str]:
    """Get the narrative ordering (terminus at the Cross)."""
    return NARRATIVE_ORDER.copy()


def get_statistics() -> Dict[str, Any]:
    """Get statistics about the pre-computed database."""
    total = sum(len(book_data) for book_data in ORTHODOX_STUDY_BIBLE.values())
    tonal_dist = {}
    for book_data in ORTHODOX_STUDY_BIBLE.values():
        for exegesis in book_data.values():
            w = exegesis.tonal_weight.value
            tonal_dist[w] = tonal_dist.get(w, 0) + 1
    return {
        'total_verses': total,
        'books_covered': len(ORTHODOX_STUDY_BIBLE),
        'tonal_distribution': tonal_dist,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Orthodox Study Bible Data')
    parser.add_argument('--verse', type=str, help='Get exegesis for a verse')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    args = parser.parse_args()
    
    if args.verse:
        ex = get_verse_exegesis(args.verse)
        if ex:
            print(f"\n{ex.reference}")
            print(f"{'='*60}")
            print(f"{ex.text}\n")
            print(f"LITERAL: {ex.literal}\n")
            print(f"ALLEGORICAL: {ex.allegorical}\n")
            print(f"TROPOLOGICAL: {ex.tropological}\n")
            print(f"ANAGOGICAL: {ex.anagogical}\n")
            print(f"Tonal: {ex.tonal_weight.value} | Mood: {ex.native_mood}")
    elif args.stats:
        stats = get_statistics()
        print(f"\nTotal Verses: {stats['total_verses']}")
        print(f"Books: {stats['books_covered']}")
        print(f"Tonal Distribution: {stats['tonal_distribution']}")
