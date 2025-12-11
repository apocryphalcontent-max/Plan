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
# PSALMS - THE PRAYER BOOK OF SCRIPTURE
# ============================================================================

PSALMS_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "Psalm 22:1": VerseExegesis(
        reference="Psalm 22:1",
        text="My God, my God, why hast thou forsaken me? why art thou so far from helping me, and from the words of my roaring?",
        literal="David's cry of utter abandonment. Eli, Eli, lama azavtani. The sense of divine absence at the moment of greatest need. The 'roaring' suggests the cry of a wounded animal.",
        allegorical="Christ's cry from the Cross (Matt 27:46). The sinless One bears the curse of separation so that we might never be forsaken. The Father turns His face from the Son bearing sin.",
        tropological="The reader learns that even the deepest sense of God's absence does not mean God has truly abandoned. The psalm that begins in abandonment ends in triumph.",
        anagogical="The cry of dereliction is answered in eternal communion. The forsaking was real but temporary; the reunion is eternal.",
        emotional_valence=0.15, theological_weight=1.0, sensory_intensity=0.95,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Absolute abandonment",
        dread_amplification=1.0,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="punctuated",
        typological_shadows=(),
        typological_fulfillments=("Matthew 27:46", "Mark 15:34"),
        cross_references=("Matthew 27:46", "Hebrews 5:7"),
        visual_seeds=("face turned away", "darkness at noon"),
        auditory_seeds=("the cry that shakes heaven", "roaring from the dust"),
        tactile_seeds=("weight of cosmic abandonment", "bones out of joint"),
        plants_phrase="My God, my God, why hast thou forsaken me"
    ),
    
    "Psalm 22:16": VerseExegesis(
        reference="Psalm 22:16",
        text="For dogs have compassed me: the assembly of the wicked have inclosed me: they pierced my hands and my feet.",
        literal="The psalmist surrounded by enemies. The piercing of hands and feet - prophetic anticipation of crucifixion, a form of execution unknown in David's time.",
        allegorical="Exact description of crucifixion written centuries before the practice existed. The 'assembly of the wicked' - the Sanhedrin, the mob, the Romans.",
        tropological="The reader contemplates the specific, physical suffering of Christ. Not abstract 'atonement' but real nails, real flesh, real piercing.",
        anagogical="The wounds remain. The risen Christ shows Thomas His hands. The glorified Lamb bears the marks of slaughter.",
        emotional_valence=0.10, theological_weight=0.98, sensory_intensity=1.0,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Physical torture described",
        dread_amplification=0.95,
        narrative_function=NarrativeFunction.INTENSIFICATION,
        breath_rhythm="staccato",
        typological_shadows=(),
        typological_fulfillments=("John 19:37", "John 20:25", "Zechariah 12:10"),
        cross_references=("Zechariah 12:10", "John 19:23-24", "Revelation 1:7"),
        visual_seeds=("hands stretched on wood", "feet overlapped and nailed"),
        auditory_seeds=("hammer on iron", "dogs circling"),
        tactile_seeds=("iron through flesh", "weight on pierced hands"),
        plants_phrase="they pierced my hands and my feet"
    ),
    
    "Psalm 23:4": VerseExegesis(
        reference="Psalm 23:4",
        text="Yea, though I walk through the valley of the shadow of death, I will fear no evil: for thou art with me; thy rod and thy staff they comfort me.",
        literal="The shepherd imagery shifts to darkest passage - gey tsalmaveth, the valley of death's shadow. Yet the presence of the Shepherd transforms fear into comfort.",
        allegorical="Christ the Good Shepherd walks before us through death itself. He has gone through the valley; we follow. His presence is the answer to death's terror.",
        tropological="The reader learns to face mortality with confidence not in self but in the Shepherd's presence. 'I will fear no evil' is not denial but trust.",
        anagogical="The valley is traversed, not inhabited. There is an 'after' to death's shadow. The Shepherd leads through to 'the house of the LORD for ever.'",
        emotional_valence=0.45, theological_weight=0.95, sensory_intensity=0.75,
        tonal_weight=TonalWeight.UNSETTLING,
        native_mood="Peace in darkness",
        dread_amplification=0.5,
        narrative_function=NarrativeFunction.DEVELOPMENT,
        breath_rhythm="sustained",
        typological_shadows=(),
        typological_fulfillments=("John 10:11", "Hebrews 2:14-15"),
        cross_references=("John 10:11", "John 10:28", "Romans 8:38-39"),
        visual_seeds=("dark valley", "shepherd's silhouette ahead", "rod and staff visible"),
        auditory_seeds=("shepherd's voice in darkness", "footsteps ahead"),
        tactile_seeds=("cold of the valley", "staff guiding", "rod protecting"),
        plants_phrase="valley of the shadow of death"
    ),
}


# ============================================================================
# MATTHEW - THE PASSION NARRATIVE
# ============================================================================

MATTHEW_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "Matthew 26:39": VerseExegesis(
        reference="Matthew 26:39",
        text="And he went a little further, and fell on his face, and prayed, saying, O my Father, if it be possible, let this cup pass from me: nevertheless not as I will, but as thou wilt.",
        literal="Gethsemane. Christ prostrate, praying for the cup to pass. The cup - wrath, judgment, separation. The surrender: 'not as I will.'",
        allegorical="The second Adam succeeds where the first failed. In a garden, humanity fell through self-will; in a garden, humanity is redeemed through surrender.",
        tropological="The pattern of Christian prayer: honest desire + complete surrender. The reader learns that submission is not suppression but offering.",
        anagogical="The cup will be drunk; the victory won; the will of God accomplished. The surrender in Gethsemane enables the triumph of Easter.",
        emotional_valence=0.25, theological_weight=0.98, sensory_intensity=0.85,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Crushing surrender",
        dread_amplification=0.9,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="punctuated",
        typological_shadows=("Genesis 3:6", "Genesis 22:2"),
        typological_fulfillments=("Hebrews 5:7-8",),
        cross_references=("Mark 14:36", "Luke 22:42", "John 18:11", "Hebrews 5:7"),
        visual_seeds=("face pressed to earth", "sweat falling", "disciples sleeping"),
        auditory_seeds=("prayer through tears", "silence of the garden"),
        tactile_seeds=("cold ground beneath prostrate body", "weight of the cup"),
        plants_phrase="not as I will, but as thou wilt"
    ),
    
    "Matthew 27:46": VerseExegesis(
        reference="Matthew 27:46",
        text="And about the ninth hour Jesus cried with a loud voice, saying, Eli, Eli, lama sabachthani? that is to say, My God, my God, why hast thou forsaken me?",
        literal="The ninth hour - the hour of the evening sacrifice. Christ's cry in Aramaic, quoting Psalm 22:1. The cry is 'loud' - a shout into darkness.",
        allegorical="The sinless One experiences the consequence of sin: separation from God. He who knew no sin became sin.",
        tropological="The reader must not sentimentalize this. This is not acting; this is actual abandonment experienced. Our sin caused this.",
        anagogical="This is the moment sin is finally dealt with. The cry of dereliction is the cry of victory in disguise.",
        emotional_valence=0.05, theological_weight=1.0, sensory_intensity=1.0,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Ultimate desolation",
        dread_amplification=1.0,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="punctuated",
        typological_shadows=("Psalm 22:1",),
        typological_fulfillments=(),
        cross_references=("Mark 15:34", "Psalm 22:1", "2 Corinthians 5:21"),
        visual_seeds=("darkness covering the land", "mouth opened in cry"),
        auditory_seeds=("the cry that rends heaven", "Eli, Eli"),
        tactile_seeds=("throat raw from the shout", "body at the limit"),
        echoes_phrase="My God, my God, why hast thou forsaken me"
    ),
    
    "Matthew 27:51": VerseExegesis(
        reference="Matthew 27:51",
        text="And, behold, the veil of the temple was rent in twain from the top to the bottom; and the earth did quake, and the rocks rent;",
        literal="The veil - the curtain separating the Holy Place from the Most Holy Place. Torn from top to bottom, from God's side. The earth quakes; rocks split.",
        allegorical="The barrier between God and humanity is destroyed. The way into the presence is opened through Christ's flesh.",
        tropological="The reader now has access. The veil that kept humanity out is gone. 'Let us draw near.' The death of Christ means the death of separation.",
        anagogical="The tearing of the earthly veil anticipates the opening of heaven itself. The final state has no temple because God dwells directly with His people.",
        emotional_valence=0.60, theological_weight=0.98, sensory_intensity=0.95,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Cosmic rupture",
        dread_amplification=0.7,
        narrative_function=NarrativeFunction.RESOLUTION,
        breath_rhythm="staccato",
        typological_shadows=("Exodus 26:33", "Leviticus 16:2"),
        typological_fulfillments=("Hebrews 10:19-20", "Revelation 21:22"),
        cross_references=("Mark 15:38", "Luke 23:45", "Hebrews 6:19", "Hebrews 10:20"),
        visual_seeds=("veil tearing from invisible hands", "rocks splitting", "earth shaking"),
        auditory_seeds=("the sound of tearing", "the roar of earthquake"),
        tactile_seeds=("ground shaking beneath feet", "stones breaking"),
        plants_phrase="the veil was rent"
    ),
}


# ============================================================================
# LUKE - PASSION DETAILS
# ============================================================================

LUKE_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "Luke 22:42": VerseExegesis(
        reference="Luke 22:42",
        text="Saying, Father, if thou be willing, remove this cup from me: nevertheless not my will, but thine, be done.",
        literal="Luke's version of the Gethsemane prayer. 'Father' - the intimate address. The surrender is complete: 'thine be done.'",
        allegorical="The Son's will perfectly conforms to the Father's. This is the model of all true prayer.",
        tropological="The reader learns the grammar of surrender. Honest expression + complete submission = true prayer.",
        anagogical="The will of God accomplished here is accomplished forever. 'Thy will be done on earth as in heaven.'",
        emotional_valence=0.30, theological_weight=0.98, sensory_intensity=0.80,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Anguished submission",
        dread_amplification=0.85,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="sustained",
        typological_shadows=("Genesis 22:2",),
        typological_fulfillments=("Philippians 2:8", "Hebrews 5:8"),
        cross_references=("Matthew 26:39", "Mark 14:36", "John 18:11"),
        visual_seeds=("sweat like drops of blood", "prostrate figure"),
        auditory_seeds=("whispered prayer", "silence of acceptance"),
        tactile_seeds=("cold ground", "weight of the world"),
        echoes_phrase="Be it unto me"
    ),
    
    "Luke 23:43": VerseExegesis(
        reference="Luke 23:43",
        text="And Jesus said unto him, Verily I say unto thee, To day shalt thou be with me in paradise.",
        literal="The thief's faith is answered. 'Today' - not future, not conditional. 'With me' - personal presence. 'Paradise' - the garden restored.",
        allegorical="The first fruit of the Cross. While still on the cross, Christ is saving. The thief enters paradise before the apostles.",
        tropological="The reader sees that it is never too late. Deathbed conversion is real conversion. The thief had nothing to offer but his need.",
        anagogical="Paradise is opened. The cherubim's sword is sheathed. The way to the tree of life is clear.",
        emotional_valence=0.85, theological_weight=0.95, sensory_intensity=0.70,
        tonal_weight=TonalWeight.LIGHT,
        native_mood="Unexpected grace in extremity",
        dread_amplification=0.2,
        narrative_function=NarrativeFunction.RESOLUTION,
        breath_rhythm="flowing",
        typological_shadows=("Genesis 3:24",),
        typological_fulfillments=("Revelation 2:7", "Revelation 22:14"),
        cross_references=("Genesis 3:24", "2 Corinthians 12:4", "Revelation 2:7"),
        visual_seeds=("two crosses side by side", "eyes meeting"),
        auditory_seeds=("promise spoken through pain", "Today"),
        tactile_seeds=("same nails, different destinies"),
        echoes_phrase="tree of life"
    ),
    
    "Luke 23:46": VerseExegesis(
        reference="Luke 23:46",
        text="And when Jesus had cried with a loud voice, he said, Father, into thy hands I commend my spirit: and having said thus, he gave up the ghost.",
        literal="The final word from Luke. Quoting Psalm 31:5. 'Father' - the relationship restored even in death. 'I commend' - I entrust. Active, not passive.",
        allegorical="The Son returns to the Father. The mission is complete. The spirit given at creation returns to the Giver.",
        tropological="The reader learns how to die. Commending the spirit to the Father transforms death from defeat to homecoming.",
        anagogical="The commended spirit will be raised. Entrusting to God is never loss but gain.",
        emotional_valence=0.50, theological_weight=0.98, sensory_intensity=0.85,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Peaceful surrender",
        dread_amplification=0.6,
        narrative_function=NarrativeFunction.RESOLUTION,
        breath_rhythm="sustained",
        typological_shadows=("Psalm 31:5", "Genesis 2:7"),
        typological_fulfillments=("Acts 7:59",),
        cross_references=("Psalm 31:5", "Matthew 27:50", "John 19:30", "Acts 7:59"),
        visual_seeds=("face lifted to heaven", "final breath released"),
        auditory_seeds=("the cry: Father!", "then stillness"),
        tactile_seeds=("spirit departing body", "weight of flesh remaining"),
        echoes_phrase="breath of life"
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
# EXODUS - DELIVERANCE AND SACRIFICE
# ============================================================================

EXODUS_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "Exodus 3:14": VerseExegesis(
        reference="Exodus 3:14",
        text="And God said unto Moses, I AM THAT I AM: and he said, Thus shalt thou say unto the children of Israel, I AM hath sent me unto you.",
        literal="The divine name revealed. 'Ehyeh asher ehyeh' - I AM WHO I AM. God's self-definition by pure existence. The Name by which He will be known.",
        allegorical="Christ's 'I AM' statements (John 8:58) claim this Name. The voice from the bush speaks again in the flesh.",
        tropological="Before this Name, all other identities fail. The reader is constituted by 'I AM,' not the reverse.",
        anagogical="The eternal I AM will be all in all. Every knee bows to the Name above all names.",
        emotional_valence=0.85, theological_weight=1.0, sensory_intensity=0.60,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Awe at self-revealing deity",
        dread_amplification=0.4,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="sustained",
        typological_shadows=(),
        typological_fulfillments=("John 8:58", "Revelation 1:8"),
        cross_references=("John 8:58", "Hebrews 13:8", "Revelation 1:8"),
        visual_seeds=("bush burning unconsumed", "fire that does not destroy"),
        auditory_seeds=("voice from the flame", "I AM"),
        tactile_seeds=("ground made holy", "sandals removed"),
        plants_phrase="I AM"
    ),
    
    "Exodus 12:13": VerseExegesis(
        reference="Exodus 12:13",
        text="And the blood shall be to you for a token upon the houses where ye are: and when I see the blood, I will pass over you, and the plague shall not be upon you to destroy you, when I smite the land of Egypt.",
        literal="The Passover institution. Blood on doorposts. The LORD sees and passes over. Death comes to Egypt but not to the blood-marked houses.",
        allegorical="The blood of Christ marks His people. When judgment falls, those under the blood are spared. 'Christ our Passover' (1 Cor 5:7).",
        tropological="The reader must be under the blood. There is no safety outside the mark. Faith applies the blood.",
        anagogical="The final judgment will pass over those covered by the Lamb's blood. The Passover is eternal.",
        emotional_valence=0.55, theological_weight=1.0, sensory_intensity=0.85,
        tonal_weight=TonalWeight.UNSETTLING,
        native_mood="Dread and deliverance intertwined",
        dread_amplification=0.75,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="punctuated",
        typological_shadows=(),
        typological_fulfillments=("1 Corinthians 5:7", "1 Peter 1:18-19", "Revelation 7:14"),
        cross_references=("1 Corinthians 5:7", "Hebrews 11:28", "Revelation 12:11"),
        visual_seeds=("blood on doorposts", "death passing through streets"),
        auditory_seeds=("wailing from unmarked houses", "silence in the marked"),
        tactile_seeds=("hyssop dipped in blood", "trembling behind closed doors"),
        plants_phrase="when I see the blood"
    ),
    
    "Exodus 14:14": VerseExegesis(
        reference="Exodus 14:14",
        text="The LORD shall fight for you, and ye shall hold your peace.",
        literal="At the Red Sea, trapped between Pharaoh and the waters. Moses declares: YHWH fights; you be still.",
        allegorical="Christ has fought the battle. Our work is to cease striving and trust the victory already won.",
        tropological="The reader learns that salvation is not achieved but received. Stillness is faith.",
        anagogical="The final battle is the LORD's. We enter rest; He completes victory.",
        emotional_valence=0.65, theological_weight=0.90, sensory_intensity=0.70,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Peace before impossible odds",
        dread_amplification=0.3,
        narrative_function=NarrativeFunction.DEVELOPMENT,
        breath_rhythm="sustained",
        typological_shadows=(),
        typological_fulfillments=("Romans 8:31", "2 Chronicles 20:17"),
        cross_references=("Psalm 46:10", "Isaiah 30:15", "2 Chronicles 20:17"),
        visual_seeds=("sea before, army behind", "pillar of cloud"),
        auditory_seeds=("chariots approaching", "voice commanding peace"),
        tactile_seeds=("trembling bodies learning stillness"),
        plants_phrase="hold your peace"
    ),
    
    "Exodus 20:2-3": VerseExegesis(
        reference="Exodus 20:2-3",
        text="I am the LORD thy God, which have brought thee out of the land of Egypt, out of the house of bondage. Thou shalt have no other gods before me.",
        literal="The Decalogue begins with identity: I am YHWH who delivered you. The first command follows from the first fact. No other gods because there is no other deliverer.",
        allegorical="Christ delivers from greater bondage. His claim to exclusive worship rests on His exclusive salvation.",
        tropological="The reader must examine: what other gods compete? What deliverances am I trusting beyond Him?",
        anagogical="In the age to come, no idols remain. God alone is worshiped because God alone is seen.",
        emotional_valence=0.70, theological_weight=1.0, sensory_intensity=0.50,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Solemn exclusive claim",
        dread_amplification=0.35,
        narrative_function=NarrativeFunction.SCENE_SETTING,
        breath_rhythm="sustained",
        typological_shadows=(),
        typological_fulfillments=("Matthew 4:10", "Acts 4:12"),
        cross_references=("Deuteronomy 5:6-7", "Isaiah 45:5", "Matthew 4:10"),
        visual_seeds=("Sinai smoking", "tablets of stone"),
        auditory_seeds=("thunder of divine voice", "first command"),
        tactile_seeds=("mountain trembling", "weight of law"),
        plants_phrase="no other gods"
    ),
}


# ============================================================================
# ROMANS - THE GOSPEL SYSTEMATIZED
# ============================================================================

ROMANS_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "Romans 3:23-24": VerseExegesis(
        reference="Romans 3:23-24",
        text="For all have sinned, and come short of the glory of God; Being justified freely by his grace through the redemption that is in Christ Jesus:",
        literal="Universal diagnosis: all sinned, all fall short. Universal remedy: justified freely (dorean - as a gift), by grace, through redemption in Christ.",
        allegorical="The glory we fell short of is restored in Christ. Adam's loss becomes Christ's gain for all.",
        tropological="The reader cannot boast. The justification is free, unearned, grace-given. Self-salvation is impossible.",
        anagogical="The glory of God becomes the destiny of the redeemed. What we lacked we shall possess.",
        emotional_valence=0.75, theological_weight=1.0, sensory_intensity=0.40,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Devastating diagnosis, glorious remedy",
        dread_amplification=0.3,
        narrative_function=NarrativeFunction.EXPOSITION,
        breath_rhythm="sustained",
        typological_shadows=("Genesis 3:23", "Isaiah 53:6"),
        typological_fulfillments=(),
        cross_references=("Romans 6:23", "Ephesians 2:8-9", "Titus 3:7"),
        visual_seeds=("glory falling short", "gift extended"),
        auditory_seeds=("verdict: all sinned", "verdict reversed: justified"),
        tactile_seeds=("weight of sin lifted", "freedom of justification"),
        plants_phrase="justified freely by his grace"
    ),
    
    "Romans 5:8": VerseExegesis(
        reference="Romans 5:8",
        text="But God commendeth his love toward us, in that, while we were yet sinners, Christ died for us.",
        literal="God demonstrates (sunistemi - proves, establishes) His love. The timing: while we were sinners. Not after reform, but during rebellion.",
        allegorical="The Cross is the demonstration. Every question about God's love is answered at Golgotha.",
        tropological="The reader is loved before being lovable. This transforms self-understanding and neighbor-love.",
        anagogical="This love is eternal. What was demonstrated in time is the eternal nature of God.",
        emotional_valence=0.95, theological_weight=1.0, sensory_intensity=0.65,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Wonder at initiative of divine love",
        dread_amplification=0.15,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="sustained",
        typological_shadows=("Genesis 3:21", "Hosea 3:1"),
        typological_fulfillments=(),
        cross_references=("John 3:16", "1 John 4:10", "Ephesians 2:4-5"),
        visual_seeds=("Cross standing", "sinners watching"),
        auditory_seeds=("declaration: while yet sinners"),
        tactile_seeds=("love reaching the unlovely"),
        echoes_phrase="God will provide himself a lamb"
    ),
    
    "Romans 6:23": VerseExegesis(
        reference="Romans 6:23",
        text="For the wages of sin is death; but the gift of God is eternal life through Jesus Christ our Lord.",
        literal="Two economies contrasted. Wages (opsonia - soldier's pay) of sin: death earned. Gift (charisma) of God: eternal life unearned. Through Christ.",
        allegorical="Adam earned death for humanity; Christ gives life. Two representatives, two outcomes.",
        tropological="The reader must choose which economy to live in. Wage-earning leads to death; gift-receiving leads to life.",
        anagogical="Eternal life is the final gift. Death is swallowed up in victory.",
        emotional_valence=0.70, theological_weight=0.98, sensory_intensity=0.45,
        tonal_weight=TonalWeight.NEUTRAL,
        native_mood="Stark contrast, clear choice",
        dread_amplification=0.4,
        narrative_function=NarrativeFunction.EXPOSITION,
        breath_rhythm="punctuated",
        typological_shadows=("Genesis 2:17", "Genesis 3:19"),
        typological_fulfillments=(),
        cross_references=("James 1:15", "1 John 5:11-12", "John 3:36"),
        visual_seeds=("two paths diverging", "death and life"),
        auditory_seeds=("wages announced", "gift offered"),
        tactile_seeds=("weight of earned death", "lightness of given life"),
        plants_phrase="wages of sin is death"
    ),
    
    "Romans 8:28": VerseExegesis(
        reference="Romans 8:28",
        text="And we know that all things work together for good to them that love God, to them who are the called according to his purpose.",
        literal="All things (panta) work together (sunergei) for good. Conditions: those who love God, those called according to His purpose. Providence is comprehensive.",
        allegorical="What Joseph said to his brothers becomes universal: 'You meant it for evil; God meant it for good.'",
        tropological="The reader can face suffering differently. Not that all things ARE good, but that all things WORK for good.",
        anagogical="In the end, all purposes converge. The good toward which all works is glorification.",
        emotional_valence=0.85, theological_weight=0.95, sensory_intensity=0.40,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Confidence in sovereign providence",
        dread_amplification=0.1,
        narrative_function=NarrativeFunction.RESOLUTION,
        breath_rhythm="sustained",
        typological_shadows=("Genesis 50:20",),
        typological_fulfillments=(),
        cross_references=("Genesis 50:20", "Ephesians 1:11", "Philippians 1:6"),
        visual_seeds=("tangled threads becoming pattern", "all things converging"),
        auditory_seeds=("we know - confidence"),
        tactile_seeds=("broken pieces fitting together"),
        plants_phrase="all things work together for good"
    ),
    
    "Romans 8:38-39": VerseExegesis(
        reference="Romans 8:38-39",
        text="For I am persuaded, that neither death, nor life, nor angels, nor principalities, nor powers, nor things present, nor things to come, Nor height, nor depth, nor any other creature, shall be able to separate us from the love of God, which is in Christ Jesus our Lord.",
        literal="Paul's exhaustive list of potential separators: death/life, angels/principalities/powers, present/future, height/depth, any creature. None can separate.",
        allegorical="Every possible force is named and defeated. The love of God in Christ is invincible.",
        tropological="The reader's security is not in circumstances but in Christ. Nothing can separate; therefore, nothing need be feared.",
        anagogical="This love endures into eternity. The nothing that can separate now will remain nothing forever.",
        emotional_valence=1.0, theological_weight=1.0, sensory_intensity=0.50,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Triumphant assurance",
        dread_amplification=0.0,
        narrative_function=NarrativeFunction.RESOLUTION,
        breath_rhythm="flowing",
        typological_shadows=(),
        typological_fulfillments=(),
        cross_references=("John 10:28-29", "Ephesians 3:18-19", "1 John 4:18"),
        visual_seeds=("all powers arrayed and failing", "love standing unbreached"),
        auditory_seeds=("I am persuaded - conviction"),
        tactile_seeds=("grip that cannot be broken"),
        echoes_phrase="I will never leave thee"
    ),
}


# ============================================================================
# HEBREWS - CHRIST THE HIGH PRIEST
# ============================================================================

HEBREWS_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "Hebrews 4:12": VerseExegesis(
        reference="Hebrews 4:12",
        text="For the word of God is quick, and powerful, and sharper than any twoedged sword, piercing even to the dividing asunder of soul and spirit, and of the joints and marrow, and is a discerner of the thoughts and intents of the heart.",
        literal="The Word is living (zon), active (energes), sharp (tomoteros). It penetrates to the division of soul/spirit, joints/marrow. It discerns (kritikos) thoughts and intentions.",
        allegorical="Christ the Logos is the surgeon. His word on the Cross divides all things to their truth.",
        tropological="The reader is laid open. Scripture is not merely read; it reads us. No hiding before this word.",
        anagogical="The final judgment will be by this Word. The discerning sword of now is the judgment sword of then.",
        emotional_valence=0.55, theological_weight=0.95, sensory_intensity=0.90,
        tonal_weight=TonalWeight.UNSETTLING,
        native_mood="Exposure before the living Word",
        dread_amplification=0.7,
        narrative_function=NarrativeFunction.INTENSIFICATION,
        breath_rhythm="punctuated",
        typological_shadows=("Genesis 3:24", "Isaiah 49:2"),
        typological_fulfillments=("Revelation 1:16", "Revelation 19:15"),
        cross_references=("Ephesians 6:17", "Revelation 1:16", "Revelation 19:15"),
        visual_seeds=("sword dividing", "innermost parts exposed"),
        auditory_seeds=("word that cuts", "silence of the exposed"),
        tactile_seeds=("blade passing through", "nothing hidden"),
        plants_phrase="sharper than any twoedged sword"
    ),
    
    "Hebrews 9:22": VerseExegesis(
        reference="Hebrews 9:22",
        text="And almost all things are by the law purged with blood; and without shedding of blood is no remission.",
        literal="The principle stated baldly: purification requires blood; forgiveness (aphesis) requires blood-shedding. No exceptions in the economy of salvation.",
        allegorical="Every Old Testament sacrifice pointed here. The blood of bulls and goats anticipated the blood that would actually remit.",
        tropological="The reader must not sentimentalize forgiveness. It cost blood. Our sin required death.",
        anagogical="The blood shed once is eternally effective. The altar in heaven bears the evidence.",
        emotional_valence=0.35, theological_weight=1.0, sensory_intensity=0.85,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Unflinching necessity of blood",
        dread_amplification=0.85,
        narrative_function=NarrativeFunction.EXPOSITION,
        breath_rhythm="punctuated",
        typological_shadows=("Leviticus 17:11", "Exodus 24:8"),
        typological_fulfillments=(),
        cross_references=("Leviticus 17:11", "Matthew 26:28", "1 John 1:7"),
        visual_seeds=("altar drenched", "blood poured out"),
        auditory_seeds=("no remission - verdict"),
        tactile_seeds=("blood warm and real", "life poured out"),
        echoes_phrase="when I see the blood"
    ),
    
    "Hebrews 11:1": VerseExegesis(
        reference="Hebrews 11:1",
        text="Now faith is the substance of things hoped for, the evidence of things not seen.",
        literal="Faith defined: hupostasis (substance, foundation, assurance) of hoped-for things; elenchos (proof, conviction, evidence) of unseen things.",
        allegorical="The faith chapter follows: Abel, Enoch, Noah, Abraham - all lived by this definition.",
        tropological="The reader learns what faith is: not wish but substance, not feeling but evidence. Faith makes real what is not yet visible.",
        anagogical="Faith now becomes sight then. The substance becomes visible; the evidence becomes obvious.",
        emotional_valence=0.80, theological_weight=0.95, sensory_intensity=0.35,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Confident grasp of the invisible",
        dread_amplification=0.1,
        narrative_function=NarrativeFunction.SCENE_SETTING,
        breath_rhythm="sustained",
        typological_shadows=(),
        typological_fulfillments=(),
        cross_references=("Romans 8:24-25", "2 Corinthians 4:18", "2 Corinthians 5:7"),
        visual_seeds=("unseen realities taking shape", "hope becoming substance"),
        auditory_seeds=("definition spoken: this is faith"),
        tactile_seeds=("grasping what cannot be held"),
        plants_phrase="substance of things hoped for"
    ),
    
    "Hebrews 12:2": VerseExegesis(
        reference="Hebrews 12:2",
        text="Looking unto Jesus the author and finisher of our faith; who for the joy that was set before him endured the cross, despising the shame, and is set down at the right hand of the throne of God.",
        literal="Jesus as archegos (founder, pioneer, author) and teleiotes (perfecter, finisher) of faith. He endured cross, despised shame, for the joy ahead. Now enthroned.",
        allegorical="The race of faith has a forerunner who has already finished. We run toward One who has already arrived.",
        tropological="The reader is to look (aphorao - look away from distractions toward). Eyes on Jesus transforms the race.",
        anagogical="He is seated - the work complete. We run toward a finish that has already been reached by our Pioneer.",
        emotional_valence=0.85, theological_weight=1.0, sensory_intensity=0.70,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Fixed gaze on the enthroned Victor",
        dread_amplification=0.2,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="sustained",
        typological_shadows=(),
        typological_fulfillments=(),
        cross_references=("Philippians 2:8-9", "Acts 2:33", "Revelation 3:21"),
        visual_seeds=("eyes fixed on Jesus", "throne at journey's end"),
        auditory_seeds=("author and finisher - titles"),
        tactile_seeds=("running with eyes up", "weight laid aside"),
        echoes_phrase="It is finished"
    ),
}


# ============================================================================
# 1 PETER - SUFFERING AND GLORY
# ============================================================================

PETER_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "1 Peter 1:18-19": VerseExegesis(
        reference="1 Peter 1:18-19",
        text="Forasmuch as ye know that ye were not redeemed with corruptible things, as silver and gold, from your vain conversation received by tradition from your fathers; But with the precious blood of Christ, as of a lamb without blemish and without spot:",
        literal="Redemption cost: not silver/gold (corruptible) but precious blood. Christ as lamb: unblemished (amomos), spotless (aspilos). The Passover lamb language is explicit.",
        allegorical="Every lamb sacrifice finds fulfillment. The blood that marks and saves is His blood.",
        tropological="The reader must value what redeemed them. Not cheap grace but precious blood. This transforms how we live.",
        anagogical="The precious blood speaks eternally. The Lamb in heaven bears the marks of purchase.",
        emotional_valence=0.70, theological_weight=1.0, sensory_intensity=0.80,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Sobered by the cost of redemption",
        dread_amplification=0.6,
        narrative_function=NarrativeFunction.EXPOSITION,
        breath_rhythm="sustained",
        typological_shadows=("Exodus 12:5", "Isaiah 53:7"),
        typological_fulfillments=(),
        cross_references=("John 1:29", "1 Corinthians 6:20", "Revelation 5:9"),
        visual_seeds=("lamb without spot", "blood poured out"),
        auditory_seeds=("precious - the valuation"),
        tactile_seeds=("gold and silver weighed and found wanting", "blood outweighing all"),
        echoes_phrase="God will provide himself a lamb"
    ),
    
    "1 Peter 2:24": VerseExegesis(
        reference="1 Peter 2:24",
        text="Who his own self bare our sins in his own body on the tree, that we, being dead to sins, should live unto righteousness: by whose stripes ye were healed.",
        literal="He Himself (autos) bore (anaphero - carried up as sacrifice) our sins. In His body. On the tree (xulon - wood, cross). Purpose: death to sin, life to righteousness. Isaiah 53:5 quoted: by His wounds, healing.",
        allegorical="The wood of the Cross is the tree of life. What was forbidden becomes the source of healing.",
        tropological="The reader is dead to sin and alive to righteousness. This is not aspiration but declaration.",
        anagogical="The wounds heal eternally. The stripes never stop healing.",
        emotional_valence=0.60, theological_weight=1.0, sensory_intensity=0.95,
        tonal_weight=TonalWeight.HEAVY,
        native_mood="Wounds that heal, death that gives life",
        dread_amplification=0.7,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="punctuated",
        typological_shadows=("Isaiah 53:5", "Leviticus 16:21-22"),
        typological_fulfillments=(),
        cross_references=("Isaiah 53:4-5", "2 Corinthians 5:21", "Galatians 3:13"),
        visual_seeds=("body on the tree", "stripes visible"),
        auditory_seeds=("bare our sins - declaration"),
        tactile_seeds=("wounds inflicted", "healing received"),
        echoes_phrase="with his stripes we are healed"
    ),
}


# ============================================================================
# 1 JOHN - GOD IS LOVE
# ============================================================================

JOHN_EPISTLE_EXEGESIS: Dict[str, VerseExegesis] = {
    
    "1 John 1:7": VerseExegesis(
        reference="1 John 1:7",
        text="But if we walk in the light, as he is in the light, we have fellowship one with another, and the blood of Jesus Christ his Son cleanseth us from all sin.",
        literal="Conditional: walking in light produces fellowship and ongoing cleansing. The blood keeps cleansing (katharizei - present tense, continuous).",
        allegorical="Light and blood together: the light reveals, the blood cleanses. Both are necessary.",
        tropological="The reader walks in light or darkness. Light brings fellowship and cleansing; darkness brings neither.",
        anagogical="The cleansing is complete in eternity. What was continuous becomes eternal purity.",
        emotional_valence=0.80, theological_weight=0.95, sensory_intensity=0.65,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Assurance through ongoing cleansing",
        dread_amplification=0.2,
        narrative_function=NarrativeFunction.DEVELOPMENT,
        breath_rhythm="sustained",
        typological_shadows=("Leviticus 16:30",),
        typological_fulfillments=(),
        cross_references=("John 8:12", "Hebrews 9:14", "Revelation 7:14"),
        visual_seeds=("walking in light", "blood continually applied"),
        auditory_seeds=("cleanseth - ongoing"),
        tactile_seeds=("filth washed", "clean garments"),
        echoes_phrase="when I see the blood"
    ),
    
    "1 John 4:8": VerseExegesis(
        reference="1 John 4:8",
        text="He that loveth not knoweth not God; for God is love.",
        literal="Negative and positive: no love = no knowledge of God. Why? Because God IS (estin) love. Not merely loving, but love itself.",
        allegorical="The Cross is the definition. God is love means God gives His Son. Any 'god' who doesn't give isn't God.",
        tropological="The reader's love (or lack) reveals their knowledge (or lack) of God. Love is the test of theology.",
        anagogical="God remains love eternally. The love that acted in time is the love that reigns in eternity.",
        emotional_valence=1.0, theological_weight=1.0, sensory_intensity=0.40,
        tonal_weight=TonalWeight.TRANSCENDENT,
        native_mood="Simple profundity",
        dread_amplification=0.1,
        narrative_function=NarrativeFunction.CLIMAX,
        breath_rhythm="sustained",
        typological_shadows=(),
        typological_fulfillments=(),
        cross_references=("John 3:16", "Romans 5:8", "1 John 4:16"),
        visual_seeds=("Cross as love's definition"),
        auditory_seeds=("God is love - simplest statement"),
        tactile_seeds=("love embodied and embraced"),
        plants_phrase="God is love"
    ),
    
    "1 John 4:19": VerseExegesis(
        reference="1 John 4:19",
        text="We love him, because he first loved us.",
        literal="The sequence is crucial: He first (protos), then we. Our love is response, not initiation. Grace precedes all.",
        allegorical="Before the foundation of the world, He loved. Our love across all time is response to prior love.",
        tropological="The reader's love is derivative. This removes both pride (I loved God) and despair (I can't love God).",
        anagogical="The first love continues. Our eternal love is eternal response.",
        emotional_valence=0.95, theological_weight=0.90, sensory_intensity=0.35,
        tonal_weight=TonalWeight.LIGHT,
        native_mood="Gratitude for initiative of grace",
        dread_amplification=0.0,
        narrative_function=NarrativeFunction.RESOLUTION,
        breath_rhythm="flowing",
        typological_shadows=(),
        typological_fulfillments=(),
        cross_references=("Romans 5:8", "Ephesians 2:4-5", "1 John 4:10"),
        visual_seeds=("love reaching first"),
        auditory_seeds=("he first - the sequence"),
        tactile_seeds=("loved before loving"),
        echoes_phrase="while we were yet sinners"
    ),
}


# ============================================================================
# ADDITIONAL GENESIS - EXPANDED
# ============================================================================

GENESIS_EXEGESIS["Genesis 1:26-27"] = VerseExegesis(
    reference="Genesis 1:26-27",
    text="And God said, Let us make man in our image, after our likeness: and let them have dominion... So God created man in his own image, in the image of God created he him; male and female created he them.",
    literal="Divine council: 'Let us make.' Humanity in God's image (tselem) and likeness (demuth). Dominion given. Male and female both bear the image.",
    allegorical="The 'us' is Trinitarian. The image finds its perfect expression in Christ, the image of the invisible God.",
    tropological="The reader bears God's image. This grounds human dignity and responsibility. We are icons, not accidents.",
    anagogical="The image will be fully restored. What was marred will be glorified. We shall be like Him.",
    emotional_valence=0.90, theological_weight=1.0, sensory_intensity=0.60,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Dignity of the creature made like Creator",
    dread_amplification=0.1,
    narrative_function=NarrativeFunction.CLIMAX,
    breath_rhythm="sustained",
    typological_shadows=(),
    typological_fulfillments=("Colossians 1:15", "2 Corinthians 3:18", "1 John 3:2"),
    cross_references=("Psalm 8:5-6", "Colossians 1:15", "Romans 8:29"),
    visual_seeds=("divine image impressed", "male and female as one humanity"),
    auditory_seeds=("Let us make - divine deliberation"),
    tactile_seeds=("dust formed into image-bearer"),
    plants_phrase="image of God"
)

GENESIS_EXEGESIS["Genesis 3:21"] = VerseExegesis(
    reference="Genesis 3:21",
    text="Unto Adam also and to his wife did the LORD God make coats of skins, and clothed them.",
    literal="God makes (asah) garments. Skins (or) require death. The first death to cover human shame. God Himself is the tailor.",
    allegorical="The first sacrifice: an animal dies to cover sin. The pattern is set: innocent blood covers the guilty.",
    tropological="The reader cannot cover their own shame. Fig leaves fail. Only God's provision clothes adequately.",
    anagogical="The white robes of Revelation are the final garments. What began in Eden's skins completes in heaven's robes.",
    emotional_valence=0.55, theological_weight=0.95, sensory_intensity=0.75,
    tonal_weight=TonalWeight.UNSETTLING,
    native_mood="Grace through death",
    dread_amplification=0.5,
    narrative_function=NarrativeFunction.RESOLUTION,
    breath_rhythm="sustained",
    typological_shadows=(),
    typological_fulfillments=("Revelation 7:14", "Isaiah 61:10"),
    cross_references=("Isaiah 61:10", "Zechariah 3:4", "Revelation 7:14"),
    visual_seeds=("animal slain", "skins prepared", "naked ones clothed"),
    auditory_seeds=("first death for sin", "rustling of new garments"),
    tactile_seeds=("fig leaves removed", "skins wrapped around"),
    plants_phrase="clothed them"
)

GENESIS_EXEGESIS["Genesis 15:6"] = VerseExegesis(
    reference="Genesis 15:6",
    text="And he believed in the LORD; and he counted it to him for righteousness.",
    literal="Abraham believed (he'emin). God counted/reckoned (chashav) it as righteousness. Faith credited, not earned.",
    allegorical="The pattern of justification established: faith, not works. Paul's gospel is Abraham's gospel.",
    tropological="The reader is justified the same way: by believing, not achieving. Abraham is the template.",
    anagogical="The righteousness credited endures. What God reckons, God maintains eternally.",
    emotional_valence=0.85, theological_weight=1.0, sensory_intensity=0.30,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Quiet wonder at grace",
    dread_amplification=0.1,
    narrative_function=NarrativeFunction.CLIMAX,
    breath_rhythm="sustained",
    typological_shadows=(),
    typological_fulfillments=("Romans 4:3", "Galatians 3:6", "James 2:23"),
    cross_references=("Romans 4:3-5", "Galatians 3:6", "James 2:23"),
    visual_seeds=("stars beyond counting", "faith rising"),
    auditory_seeds=("he believed - simple statement"),
    tactile_seeds=("nothing done, everything received"),
    plants_phrase="counted it to him for righteousness"
)


# ============================================================================
# ADDITIONAL PSALMS - EXPANDED
# ============================================================================

PSALMS_EXEGESIS["Psalm 51:10"] = VerseExegesis(
    reference="Psalm 51:10",
    text="Create in me a clean heart, O God; and renew a right spirit within me.",
    literal="David's plea after his sin with Bathsheba. 'Create' (bara) - the word of Genesis 1. Only God creates. A 'clean' (tahor) heart and 'right' (nachon - steadfast) spirit.",
    allegorical="The new creation in Christ. What David asked for, Christ provides. The clean heart is Christ's gift.",
    tropological="The reader must ask for creation, not reformation. Only God creates clean hearts; we cannot clean our own.",
    anagogical="The new heart promised in Ezekiel 36:26 finds fulfillment. Clean hearts populate the new creation.",
    emotional_valence=0.60, theological_weight=0.95, sensory_intensity=0.55,
    tonal_weight=TonalWeight.HEAVY,
    native_mood="Broken plea for recreation",
    dread_amplification=0.4,
    narrative_function=NarrativeFunction.CLIMAX,
    breath_rhythm="sustained",
    typological_shadows=(),
    typological_fulfillments=("Ezekiel 36:26", "2 Corinthians 5:17"),
    cross_references=("Ezekiel 36:26", "Jeremiah 24:7", "2 Corinthians 5:17"),
    visual_seeds=("broken heart offered", "Creator's hands reshaping"),
    auditory_seeds=("create - the plea for divine action"),
    tactile_seeds=("old heart removed", "new heart placed"),
    plants_phrase="create in me a clean heart"
)

PSALMS_EXEGESIS["Psalm 118:22"] = VerseExegesis(
    reference="Psalm 118:22",
    text="The stone which the builders refused is become the head stone of the corner.",
    literal="A rejected stone becomes the cornerstone. The builders (experts) refused what God chose.",
    allegorical="Christ explicitly applies this to Himself (Matt 21:42). Rejected by the religious builders, He becomes the foundation of the new temple.",
    tropological="The reader learns that human rejection is not final. What the world refuses, God exalts.",
    anagogical="The cornerstone of the eternal city. The rejected One is the foundation of all that stands forever.",
    emotional_valence=0.75, theological_weight=0.98, sensory_intensity=0.60,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Triumph of the rejected",
    dread_amplification=0.3,
    narrative_function=NarrativeFunction.RESOLUTION,
    breath_rhythm="sustained",
    typological_shadows=(),
    typological_fulfillments=("Matthew 21:42", "Acts 4:11", "1 Peter 2:7"),
    cross_references=("Isaiah 28:16", "Matthew 21:42", "Ephesians 2:20"),
    visual_seeds=("stone cast aside", "stone set as cornerstone"),
    auditory_seeds=("builders' refusal", "God's overruling"),
    tactile_seeds=("weight of the stone", "foundation set firm"),
    plants_phrase="head stone of the corner"
)

PSALMS_EXEGESIS["Psalm 110:1"] = VerseExegesis(
    reference="Psalm 110:1",
    text="The LORD said unto my Lord, Sit thou at my right hand, until I make thine enemies thy footstool.",
    literal="YHWH speaks to David's Lord (Adonai). Command: sit at the right hand. Promise: enemies as footstool. The most-quoted OT verse in the NT.",
    allegorical="Jesus uses this to prove His divine Lordship (Matt 22:44). David's Lord is David's son - the mystery of incarnation.",
    tropological="The reader worships a seated King. The work is done; He reigns. Our posture is submission to His Lordship.",
    anagogical="The reign continues until all enemies are subdued. The last enemy is death. Then the Son hands the kingdom to the Father.",
    emotional_valence=0.85, theological_weight=1.0, sensory_intensity=0.55,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Royal session at the Father's right hand",
    dread_amplification=0.25,
    narrative_function=NarrativeFunction.RESOLUTION,
    breath_rhythm="sustained",
    typological_shadows=(),
    typological_fulfillments=("Matthew 22:44", "Acts 2:34-35", "Hebrews 1:13"),
    cross_references=("Matthew 26:64", "Acts 2:34-35", "1 Corinthians 15:25"),
    visual_seeds=("throne at the right hand", "enemies becoming footstool"),
    auditory_seeds=("YHWH speaking to Adonai"),
    tactile_seeds=("seated reign", "enemies underfoot"),
    plants_phrase="Sit thou at my right hand"
)


# ============================================================================
# ADDITIONAL ISAIAH - EXPANDED
# ============================================================================

ISAIAH_EXEGESIS["Isaiah 7:14"] = VerseExegesis(
    reference="Isaiah 7:14",
    text="Therefore the Lord himself shall give you a sign; Behold, a virgin shall conceive, and bear a son, and shall call his name Immanuel.",
    literal="A sign from the Lord Himself. 'Almah' - young woman/virgin. She conceives, bears, names: Immanuel (God with us).",
    allegorical="Matthew explicitly applies this to Christ's birth (1:23). The virgin is Mary; the child is Jesus; God is literally with us.",
    tropological="The reader is not alone. Immanuel is not just a name but a reality. God with us transforms everything.",
    anagogical="God with us in incarnation leads to God with us eternally. 'The tabernacle of God is with men' (Rev 21:3).",
    emotional_valence=0.90, theological_weight=1.0, sensory_intensity=0.65,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Wonder at promise of divine presence",
    dread_amplification=0.1,
    narrative_function=NarrativeFunction.SEED,
    breath_rhythm="sustained",
    typological_shadows=(),
    typological_fulfillments=("Matthew 1:22-23", "Revelation 21:3"),
    cross_references=("Matthew 1:23", "Isaiah 8:8", "Revelation 21:3"),
    visual_seeds=("virgin with child", "the Name revealed"),
    auditory_seeds=("Immanuel - God with us"),
    tactile_seeds=("divine presence embodied"),
    plants_phrase="Immanuel"
)

ISAIAH_EXEGESIS["Isaiah 9:6"] = VerseExegesis(
    reference="Isaiah 9:6",
    text="For unto us a child is born, unto us a son is given: and the government shall be upon his shoulder: and his name shall be called Wonderful, Counsellor, The mighty God, The everlasting Father, The Prince of Peace.",
    literal="Child born, son given. Government on His shoulder. Four (or five) throne names: Wonderful Counselor, Mighty God, Everlasting Father, Prince of Peace.",
    allegorical="The Messiah is divine: 'Mighty God' cannot be said of mere man. The child is God; the government is eternal.",
    tropological="The reader submits to this government. Every area of life comes under His shoulder.",
    anagogical="'Of the increase of his government there shall be no end' (v.7). The reign is eternal.",
    emotional_valence=0.95, theological_weight=1.0, sensory_intensity=0.60,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Exultation at the coming King",
    dread_amplification=0.05,
    narrative_function=NarrativeFunction.CLIMAX,
    breath_rhythm="flowing",
    typological_shadows=(),
    typological_fulfillments=("Luke 1:32-33", "Luke 2:11"),
    cross_references=("Luke 1:32-33", "Luke 2:11", "Revelation 19:16"),
    visual_seeds=("child born", "government on shoulder", "throne names proclaimed"),
    auditory_seeds=("unto us - the gift", "the names - Wonderful, Counselor..."),
    tactile_seeds=("weight of government", "peace established"),
    plants_phrase="Mighty God, Everlasting Father, Prince of Peace"
)

ISAIAH_EXEGESIS["Isaiah 40:31"] = VerseExegesis(
    reference="Isaiah 40:31",
    text="But they that wait upon the LORD shall renew their strength; they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and not faint.",
    literal="Waiting (qavah - hoping, expecting) on YHWH produces renewed strength. Three images: soaring like eagles, running without weariness, walking without fainting.",
    allegorical="Christ is the strength. Those in Him soar, run, walk. The power is His, not ours.",
    tropological="The reader waits. The activity is waiting; the result is strength. This inverts natural expectation.",
    anagogical="The final rest is the culmination of waiting. Those who waited in faith will soar eternally.",
    emotional_valence=0.90, theological_weight=0.90, sensory_intensity=0.75,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Strength through surrender",
    dread_amplification=0.05,
    narrative_function=NarrativeFunction.RESOLUTION,
    breath_rhythm="sustained",
    typological_shadows=(),
    typological_fulfillments=(),
    cross_references=("Psalm 27:14", "Psalm 40:1", "Lamentations 3:25"),
    visual_seeds=("eagles soaring", "runners without fatigue", "walkers without stumbling"),
    auditory_seeds=("wait - the command", "renew - the promise"),
    tactile_seeds=("weariness lifted", "strength flooding in"),
    plants_phrase="mount up with wings as eagles"
)

ISAIAH_EXEGESIS["Isaiah 53:3"] = VerseExegesis(
    reference="Isaiah 53:3",
    text="He is despised and rejected of men; a man of sorrows, and acquainted with grief: and we hid as it were our faces from him; he was despised, and we esteemed him not.",
    literal="The Servant's reception: despised, rejected, sorrowful, grief-stricken. The response: faces hidden, no esteem. He knows suffering intimately.",
    allegorical="Every rejection of Christ throughout history is here. The Cross is the culmination of a lifetime of rejection.",
    tropological="The reader is among the 'we' who hid faces. Confession of complicity precedes salvation.",
    anagogical="The despised One will be exalted. Every knee will bow to the One who was not esteemed.",
    emotional_valence=0.15, theological_weight=0.98, sensory_intensity=0.85,
    tonal_weight=TonalWeight.HEAVY,
    native_mood="Crushing loneliness of the rejected",
    dread_amplification=0.9,
    narrative_function=NarrativeFunction.INTENSIFICATION,
    breath_rhythm="sustained",
    typological_shadows=(),
    typological_fulfillments=("Mark 9:12", "John 1:11", "Luke 23:18"),
    cross_references=("John 1:10-11", "Mark 9:12", "Luke 23:18"),
    visual_seeds=("faces turning away", "man of sorrows alone"),
    auditory_seeds=("despised - the verdict repeated"),
    tactile_seeds=("isolation", "grief carried alone"),
    plants_phrase="man of sorrows"
)


# ============================================================================
# ADDITIONAL JOHN - EXPANDED
# ============================================================================

JOHN_EXEGESIS["John 3:16"] = VerseExegesis(
    reference="John 3:16",
    text="For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
    literal="God's love for the world (kosmos) measured by His gift: the only begotten Son. Result: belief leads to eternal life, not perishing.",
    allegorical="The giving prefigured in Abraham's offering of Isaac is here fulfilled. God gives what Abraham was prepared to give.",
    tropological="The reader responds to this love by believing. The 'whosoever' includes everyone who will respond.",
    anagogical="Eternal life is the destiny of the believing. The love that gave once gives forever.",
    emotional_valence=1.0, theological_weight=1.0, sensory_intensity=0.55,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Overwhelming love measured by ultimate gift",
    dread_amplification=0.1,
    narrative_function=NarrativeFunction.CLIMAX,
    breath_rhythm="sustained",
    typological_shadows=("Genesis 22:2", "Genesis 22:16"),
    typological_fulfillments=(),
    cross_references=("Romans 5:8", "Romans 8:32", "1 John 4:9"),
    visual_seeds=("world loved", "Son given"),
    auditory_seeds=("so loved - the measure"),
    tactile_seeds=("gift received", "perishing avoided"),
    echoes_phrase="thine only son"
)

JOHN_EXEGESIS["John 11:25-26"] = VerseExegesis(
    reference="John 11:25-26",
    text="Jesus said unto her, I am the resurrection, and the life: he that believeth in me, though he were dead, yet shall he live: And whosoever liveth and believeth in me shall never die. Believest thou this?",
    literal="Jesus' 'I AM' statement to Martha. Not 'I give resurrection' but 'I AM resurrection.' Death is not final for believers; life never ends for believers.",
    allegorical="The One who IS resurrection will demonstrate it by raising Lazarus. The claim precedes the proof.",
    tropological="The question lands on the reader: 'Believest thou this?' Faith is personal response to personal claim.",
    anagogical="The resurrection and the life is eternal identity of Christ. What He IS, believers share.",
    emotional_valence=0.90, theological_weight=1.0, sensory_intensity=0.60,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Absolute claim requiring response",
    dread_amplification=0.1,
    narrative_function=NarrativeFunction.CLIMAX,
    breath_rhythm="sustained",
    typological_shadows=(),
    typological_fulfillments=("1 Corinthians 15:20-22", "Revelation 1:18"),
    cross_references=("John 5:24", "John 14:6", "1 Corinthians 15:20-22"),
    visual_seeds=("I AM standing before the mourning", "tomb in the background"),
    auditory_seeds=("I AM the resurrection - the claim"),
    tactile_seeds=("life defeating death", "living after dying"),
    plants_phrase="I am the resurrection and the life"
)

JOHN_EXEGESIS["John 14:6"] = VerseExegesis(
    reference="John 14:6",
    text="Jesus saith unto him, I am the way, the truth, and the life: no man cometh unto the Father, but by me.",
    literal="Triple 'I AM': way, truth, life. Exclusive claim: no one comes to the Father except through Jesus. The only path to the Father.",
    allegorical="Every Old Testament path (law, sacrifice, priesthood) finds fulfillment in this Way. Christ is what all pointed to.",
    tropological="The reader must come through Christ. No alternative routes. This is the scandal of particularity.",
    anagogical="The Way leads to eternal dwelling. The Truth is eternal. The Life is everlasting.",
    emotional_valence=0.85, theological_weight=1.0, sensory_intensity=0.45,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Absolute exclusivity of the Way",
    dread_amplification=0.25,
    narrative_function=NarrativeFunction.CLIMAX,
    breath_rhythm="punctuated",
    typological_shadows=("Exodus 33:13", "Psalm 16:11"),
    typological_fulfillments=("Acts 4:12", "1 Timothy 2:5"),
    cross_references=("John 10:9", "Acts 4:12", "1 Timothy 2:5"),
    visual_seeds=("one door", "narrow way"),
    auditory_seeds=("I am the way - no other"),
    tactile_seeds=("path underfoot", "hand of the Guide"),
    plants_phrase="the way, the truth, and the life"
)


# ============================================================================
# ADDITIONAL REVELATION - EXPANDED
# ============================================================================

REVELATION_EXEGESIS["Revelation 1:8"] = VerseExegesis(
    reference="Revelation 1:8",
    text="I am Alpha and Omega, the beginning and the ending, saith the Lord, which is, and which was, and which is to come, the Almighty.",
    literal="God speaks directly: Alpha and Omega (first and last Greek letters). Triple temporal description: is, was, is to come. Title: Pantokrator (Almighty).",
    allegorical="Christ speaks with the voice of YHWH. The 'I AM' of Exodus speaks from the throne.",
    tropological="The reader is addressed by the Almighty. Everything between Alpha and Omega is under His sovereignty.",
    anagogical="The ending is as certain as the beginning. He who began will complete. Alpha guarantees Omega.",
    emotional_valence=0.85, theological_weight=1.0, sensory_intensity=0.55,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Absolute sovereignty declared",
    dread_amplification=0.3,
    narrative_function=NarrativeFunction.SCENE_SETTING,
    breath_rhythm="sustained",
    typological_shadows=("Exodus 3:14", "Isaiah 44:6"),
    typological_fulfillments=(),
    cross_references=("Isaiah 44:6", "Isaiah 48:12", "Revelation 22:13"),
    visual_seeds=("Alpha and Omega inscribed", "throne of the Almighty"),
    auditory_seeds=("I AM - divine voice"),
    tactile_seeds=("weight of eternity", "encompassed by the First and Last"),
    echoes_phrase="I AM"
)

REVELATION_EXEGESIS["Revelation 5:12"] = VerseExegesis(
    reference="Revelation 5:12",
    text="Saying with a loud voice, Worthy is the Lamb that was slain to receive power, and riches, and wisdom, and strength, and honour, and glory, and blessing.",
    literal="Angelic chorus: 'Worthy is the Lamb.' Seven-fold ascription: power, riches, wisdom, strength, honor, glory, blessing. The slain Lamb receives all.",
    allegorical="The slaughter qualified Him for glory. The wounds are His credentials. Death became enthronement.",
    tropological="The reader joins this worship. The Lamb's worth calls forth our praise.",
    anagogical="This worship is eternal. What begins in Revelation 5 never ends.",
    emotional_valence=1.0, theological_weight=1.0, sensory_intensity=0.90,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Overwhelming worship of the worthy Lamb",
    dread_amplification=0.0,
    narrative_function=NarrativeFunction.CLIMAX,
    breath_rhythm="flowing",
    typological_shadows=("Genesis 22:8", "Isaiah 53:7"),
    typological_fulfillments=(),
    cross_references=("Philippians 2:9-11", "Revelation 5:9", "Revelation 7:12"),
    visual_seeds=("myriad angels", "Lamb at center", "sevenfold glory"),
    auditory_seeds=("loud voice", "Worthy! - the acclamation"),
    tactile_seeds=("worship rising", "all creation bowed"),
    echoes_phrase="Behold the Lamb of God"
)

REVELATION_EXEGESIS["Revelation 21:1"] = VerseExegesis(
    reference="Revelation 21:1",
    text="And I saw a new heaven and a new earth: for the first heaven and the first earth were passed away; and there was no more sea.",
    literal="John's vision: new heaven, new earth. The first passed away. No more sea (symbol of chaos, separation, death in ancient thought).",
    allegorical="Genesis 1 fulfilled and exceeded. What began as 'very good' becomes glorified beyond corruption.",
    tropological="The reader's hope is new creation, not mere improvement. God makes all things new.",
    anagogical="This IS the eschaton. The new creation is the final state. Sea's chaos is eternally abolished.",
    emotional_valence=0.95, theological_weight=0.98, sensory_intensity=0.80,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Wonder at new creation unveiled",
    dread_amplification=0.0,
    narrative_function=NarrativeFunction.RESOLUTION,
    breath_rhythm="sustained",
    typological_shadows=("Genesis 1:1", "Isaiah 65:17"),
    typological_fulfillments=(),
    cross_references=("Isaiah 65:17", "Isaiah 66:22", "2 Peter 3:13"),
    visual_seeds=("old passing away", "new appearing", "sea absent"),
    auditory_seeds=("new heaven, new earth - announcement"),
    tactile_seeds=("corruption gone", "newness complete"),
    echoes_phrase="In the beginning"
)

REVELATION_EXEGESIS["Revelation 22:20"] = VerseExegesis(
    reference="Revelation 22:20",
    text="He which testifieth these things saith, Surely I come quickly. Amen. Even so, come, Lord Jesus.",
    literal="Christ's testimony: 'I come quickly.' The response: 'Amen. Come, Lord Jesus.' (Maranatha in Aramaic tradition)",
    allegorical="The whole Bible ends with longing for Christ's return. The story that began 'In the beginning' ends 'Come.'",
    tropological="The reader joins the cry: 'Come.' This is the proper Christian posture: expectant longing.",
    anagogical="The coming will happen. 'Quickly' is divine timing. The cry and the answer will meet.",
    emotional_valence=0.95, theological_weight=0.95, sensory_intensity=0.50,
    tonal_weight=TonalWeight.TRANSCENDENT,
    native_mood="Longing and assurance intertwined",
    dread_amplification=0.1,
    narrative_function=NarrativeFunction.RESOLUTION,
    breath_rhythm="flowing",
    typological_shadows=(),
    typological_fulfillments=(),
    cross_references=("1 Corinthians 16:22", "Philippians 4:5", "2 Peter 3:12"),
    visual_seeds=("horizon of expectation", "Lord approaching"),
    auditory_seeds=("I come - the promise", "Come - the response"),
    tactile_seeds=("longing stretching toward fulfillment"),
    plants_phrase="Come, Lord Jesus"
)


# ============================================================================
# MASTER REGISTRY
# ============================================================================

ORTHODOX_STUDY_BIBLE: Dict[str, Dict[str, VerseExegesis]] = {
    'Genesis': GENESIS_EXEGESIS,
    'Exodus': EXODUS_EXEGESIS,
    'Psalms': PSALMS_EXEGESIS,
    'Isaiah': ISAIAH_EXEGESIS,
    'Matthew': MATTHEW_EXEGESIS,
    'Luke': LUKE_EXEGESIS,
    'John': JOHN_EXEGESIS,
    'Romans': ROMANS_EXEGESIS,
    'Hebrews': HEBREWS_EXEGESIS,
    '1 Peter': PETER_EXEGESIS,
    '1 John': JOHN_EPISTLE_EXEGESIS,
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
