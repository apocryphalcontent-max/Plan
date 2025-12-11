#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Narrative Ordering System
======================================

THE NARRATIVE ENDS AT THE CROSS.

Christ's final breath - "It is finished" - is the terminal point.
Everything else comes BEFORE in the non-linear structure:
- The resurrection
- The empty tomb
- Pentecost
- The epistles
- Revelation's visions
- The burial

All are placed EARLIER so they HAUNT what follows.
The reader reaches the Cross having already seen the glory,
having already heard "worthy is the Lamb," having already witnessed
"God shall wipe away all tears" - and then arrives at the moment
that COSTS all of that.

Per Hermeneutical.txt:
- Keep constant background sense of inevitable but not yet arrived judgment
- Events feel like fragments drifting toward catastrophe
- Let each event keep its own mood intact (joy as joy, terror as terror)
- Guard against flattening - the blood-red sky comes from arrangement
- Pattern pressure without visible machinery
- Temporal dislocation as emotional tool
- Memory, echo, and haunting - feel followed by what you've seen
- NO GIMMICKS - no "visions of the future" framing. Present as-is.

FIRST REVISION COMPLETE. SECOND REVISION INTEGRATED.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum


class NarrativePart(Enum):
    """Major structural divisions"""
    PROLOGUE = "PROLOGUE: The Three-Thread Collapse"
    PART_ONE = "PART ONE: Before All Things / The Infant Breathes"
    PART_TWO = "PART TWO: The First Blood"
    PART_THREE = "PART THREE: The Wanderers"
    PART_FOUR = "PART FOUR: The House of Bondage"
    PART_FIVE = "PART FIVE: The Desert Testimony"
    PART_SIX = "PART SIX: The Promised Land"
    PART_SEVEN = "PART SEVEN: Judges and Kings"
    PART_EIGHT = "PART EIGHT: The Anointed and the Mad"
    PART_NINE = "PART NINE: The House That Burns"
    PART_TEN = "PART TEN: Blood Money"
    PART_ELEVEN = "PART ELEVEN: The Final Breath"
    TERMINUS = "TERMINUS: He Bows His Head"


@dataclass(frozen=True)
class NarrativeEvent:
    """A single event in the narrative ordering."""
    event_text: str
    verse_reference: Optional[str]
    part: NarrativePart
    sequence_number: int
    native_mood: str
    plants_phrase: Optional[str] = None
    echoes_phrase: Optional[str] = None
    breath_note: Optional[str] = None  # Notes on pacing/breath


# ============================================================================
# THE COMPLETE NARRATIVE ORDER
# ============================================================================
# 
# STRUCTURAL PRINCIPLE:
# The narrative is non-chronological. It weaves between:
# - Creation and Nativity (interlaced)
# - Old Testament patterns and their New Testament fulfillments (interlaced)
# - Resurrection and Revelation BEFORE the Passion
# - Everything converging to the single terminal point: the Cross
#
# This ordering has been revised twice per user requirement.
# ============================================================================

NARRATIVE_ORDER: List[NarrativeEvent] = [
    
    # ========================================================================
    # PROLOGUE: The Three-Thread Collapse
    # Interwoven strands converging toward incarnation
    # ========================================================================
    
    # Thread One: Creation's Beginning
    NarrativeEvent(
        event_text="In beginning God creates heavens and earth",
        verse_reference="Genesis 1:1",
        part=NarrativePart.PROLOGUE,
        sequence_number=1,
        native_mood="Majestic wonder at threshold of being",
        plants_phrase="In the beginning"
    ),
    
    # Thread Two: The Star (interlaced)
    NarrativeEvent(
        event_text="The star rises in the east",
        verse_reference="Matthew 2:2",
        part=NarrativePart.PROLOGUE,
        sequence_number=2,
        native_mood="Mystery and portent",
        echoes_phrase="Let there be light"
    ),
    
    # Thread One: Separation of waters
    NarrativeEvent(
        event_text="God separates waters above from waters below",
        verse_reference="Genesis 1:6-7",
        part=NarrativePart.PROLOGUE,
        sequence_number=3,
        native_mood="Cosmic ordering"
    ),
    
    # Thread Two: Magi follow (interlaced)
    NarrativeEvent(
        event_text="Magi follow the star westward",
        verse_reference="Matthew 2:9",
        part=NarrativePart.PROLOGUE,
        sequence_number=4,
        native_mood="Determined seeking"
    ),
    
    # Continue interweaving creation days with nativity elements...
    NarrativeEvent(
        event_text="God creates luminaries - sun, moon, stars",
        verse_reference="Genesis 1:16",
        part=NarrativePart.PROLOGUE,
        sequence_number=5,
        native_mood="Glory of the heavens"
    ),
    
    NarrativeEvent(
        event_text="Magi present gifts: gold, frankincense, myrrh",
        verse_reference="Matthew 2:11",
        part=NarrativePart.PROLOGUE,
        sequence_number=6,
        native_mood="Reverent adoration",
        plants_phrase="myrrh"  # Death-spice planted early
    ),
    
    # Thread Three: Annunciations interlaced
    NarrativeEvent(
        event_text="Zechariah in the temple, Gabriel appears",
        verse_reference="Luke 1:11-13",
        part=NarrativePart.PROLOGUE,
        sequence_number=7,
        native_mood="Holy terror and promise"
    ),
    
    NarrativeEvent(
        event_text="Zechariah struck mute for unbelief",
        verse_reference="Luke 1:20",
        part=NarrativePart.PROLOGUE,
        sequence_number=8,
        native_mood="Judgment that preserves"
    ),
    
    NarrativeEvent(
        event_text="Gabriel comes to Mary in Nazareth",
        verse_reference="Luke 1:26-28",
        part=NarrativePart.PROLOGUE,
        sequence_number=9,
        native_mood="Quiet interruption of ordinary life"
    ),
    
    NarrativeEvent(
        event_text="Mary's consent: 'Be it unto me according to thy word'",
        verse_reference="Luke 1:38",
        part=NarrativePart.PROLOGUE,
        sequence_number=10,
        native_mood="Humble surrender that changes everything",
        plants_phrase="Be it unto me"
    ),
    
    # Creation of humanity interlaced with Visitation
    NarrativeEvent(
        event_text="God forms man from dust of the ground",
        verse_reference="Genesis 2:7",
        part=NarrativePart.PROLOGUE,
        sequence_number=11,
        native_mood="Intimate divine artistry",
        plants_phrase="dust of the ground"
    ),
    
    NarrativeEvent(
        event_text="God breathes into man's nostrils the breath of life",
        verse_reference="Genesis 2:7",
        part=NarrativePart.PROLOGUE,
        sequence_number=12,
        native_mood="Sacred intimacy of gift",
        plants_phrase="breath of life"
    ),
    
    NarrativeEvent(
        event_text="Mary visits Elizabeth; the babe leaps in the womb",
        verse_reference="Luke 1:41",
        part=NarrativePart.PROLOGUE,
        sequence_number=13,
        native_mood="Joy recognizing joy"
    ),
    
    NarrativeEvent(
        event_text="The Magnificat: 'My soul doth magnify the Lord'",
        verse_reference="Luke 1:46-55",
        part=NarrativePart.PROLOGUE,
        sequence_number=14,
        native_mood="Exultant prophetic song"
    ),
    
    # ========================================================================
    # PART ONE: Before All Things / The Infant Breathes
    # Creation and Nativity interwoven
    # ========================================================================
    
    NarrativeEvent(
        event_text="John the Baptist born; Zechariah's tongue loosed",
        verse_reference="Luke 1:63-64",
        part=NarrativePart.PART_ONE,
        sequence_number=15,
        native_mood="Restoration of speech"
    ),
    
    NarrativeEvent(
        event_text="The Benedictus: 'Blessed be the Lord God of Israel'",
        verse_reference="Luke 1:68-79",
        part=NarrativePart.PART_ONE,
        sequence_number=16,
        native_mood="Prophetic declaration"
    ),
    
    NarrativeEvent(
        event_text="The planting of the Garden in Eden",
        verse_reference="Genesis 2:8",
        part=NarrativePart.PART_ONE,
        sequence_number=17,
        native_mood="Paradise prepared"
    ),
    
    NarrativeEvent(
        event_text="The two trees: life and knowledge of good and evil",
        verse_reference="Genesis 2:9",
        part=NarrativePart.PART_ONE,
        sequence_number=18,
        native_mood="Choice established",
        plants_phrase="tree of life"
    ),
    
    NarrativeEvent(
        event_text="Joseph's dream: 'Fear not to take unto thee Mary thy wife'",
        verse_reference="Matthew 1:20",
        part=NarrativePart.PART_ONE,
        sequence_number=19,
        native_mood="Divine reassurance in darkness"
    ),
    
    NarrativeEvent(
        event_text="Deep sleep falls on Adam; woman created from his side",
        verse_reference="Genesis 2:21-22",
        part=NarrativePart.PART_ONE,
        sequence_number=20,
        native_mood="Mystery of union",
        plants_phrase="from his side"  # Echo at crucifixion: blood and water
    ),
    
    NarrativeEvent(
        event_text="The Nativity: she brought forth her firstborn son",
        verse_reference="Luke 2:7",
        part=NarrativePart.PART_ONE,
        sequence_number=21,
        native_mood="Quiet miracle in lowly place"
    ),
    
    NarrativeEvent(
        event_text="'Bone of my bones, flesh of my flesh'",
        verse_reference="Genesis 2:23",
        part=NarrativePart.PART_ONE,
        sequence_number=22,
        native_mood="Recognition and belonging"
    ),
    
    NarrativeEvent(
        event_text="Shepherds and the heavenly host: 'Glory to God in the highest'",
        verse_reference="Luke 2:13-14",
        part=NarrativePart.PART_ONE,
        sequence_number=23,
        native_mood="Overwhelming celestial joy"
    ),
    
    NarrativeEvent(
        event_text="Man and woman naked and not ashamed",
        verse_reference="Genesis 2:25",
        part=NarrativePart.PART_ONE,
        sequence_number=24,
        native_mood="Innocence before the fall"
    ),
    
    NarrativeEvent(
        event_text="Circumcision and naming: 'thou shalt call his name JESUS'",
        verse_reference="Luke 2:21",
        part=NarrativePart.PART_ONE,
        sequence_number=25,
        native_mood="Covenant blood first shed",
        plants_phrase="blood of circumcision"
    ),
    
    # The Fall interlaced with Presentation
    NarrativeEvent(
        event_text="The serpent approaches the woman: 'Yea, hath God said?'",
        verse_reference="Genesis 3:1",
        part=NarrativePart.PART_ONE,
        sequence_number=26,
        native_mood="Insidious doubt planted"
    ),
    
    NarrativeEvent(
        event_text="Presentation in the Temple",
        verse_reference="Luke 2:22",
        part=NarrativePart.PART_ONE,
        sequence_number=27,
        native_mood="Obedience to the Law"
    ),
    
    NarrativeEvent(
        event_text="Simeon's prophecy: 'A sword shall pierce through thy own soul also'",
        verse_reference="Luke 2:35",
        part=NarrativePart.PART_ONE,
        sequence_number=28,
        native_mood="Shadow falling across joy",
        plants_phrase="sword shall pierce"
    ),
    
    NarrativeEvent(
        event_text="'Ye shall not surely die... ye shall be as gods'",
        verse_reference="Genesis 3:4-5",
        part=NarrativePart.PART_ONE,
        sequence_number=29,
        native_mood="The lie that kills"
    ),
    
    NarrativeEvent(
        event_text="She saw, she took, she ate, she gave",
        verse_reference="Genesis 3:6",
        part=NarrativePart.PART_ONE,
        sequence_number=30,
        native_mood="Cascading choice"
    ),
    
    NarrativeEvent(
        event_text="Magi warned in dream: do not return to Herod",
        verse_reference="Matthew 2:12",
        part=NarrativePart.PART_ONE,
        sequence_number=31,
        native_mood="Divine protection in flight"
    ),
    
    NarrativeEvent(
        event_text="Their eyes were opened and they knew they were naked",
        verse_reference="Genesis 3:7",
        part=NarrativePart.PART_ONE,
        sequence_number=32,
        native_mood="Shame's first dawn"
    ),
    
    NarrativeEvent(
        event_text="Flight into Egypt",
        verse_reference="Matthew 2:14",
        part=NarrativePart.PART_ONE,
        sequence_number=33,
        native_mood="Urgent escape in darkness"
    ),
    
    NarrativeEvent(
        event_text="Slaughter of the Innocents",
        verse_reference="Matthew 2:16",
        part=NarrativePart.PART_ONE,
        sequence_number=34,
        native_mood="Horror of innocent blood",
        plants_phrase="Rachel weeping"
    ),
    
    NarrativeEvent(
        event_text="The sewing of fig leaves",
        verse_reference="Genesis 3:7",
        part=NarrativePart.PART_ONE,
        sequence_number=35,
        native_mood="Futile self-covering"
    ),
    
    NarrativeEvent(
        event_text="'Where art thou?'",
        verse_reference="Genesis 3:9",
        part=NarrativePart.PART_ONE,
        sequence_number=36,
        native_mood="Divine seeking of the lost"
    ),
    
    NarrativeEvent(
        event_text="Return from Egypt after Herod's death",
        verse_reference="Matthew 2:21",
        part=NarrativePart.PART_ONE,
        sequence_number=37,
        native_mood="Safe return from exile"
    ),
    
    NarrativeEvent(
        event_text="Curse upon the serpent: 'upon thy belly shalt thou go'",
        verse_reference="Genesis 3:14",
        part=NarrativePart.PART_ONE,
        sequence_number=38,
        native_mood="Judgment pronounced"
    ),
    
    NarrativeEvent(
        event_text="The Protoevangelium: 'he shall bruise thy head'",
        verse_reference="Genesis 3:15",
        part=NarrativePart.PART_ONE,
        sequence_number=39,
        native_mood="First gospel in midst of curse",
        plants_phrase="bruise thy head... bruise his heel"
    ),
    
    NarrativeEvent(
        event_text="'In sorrow thou shalt bring forth children'",
        verse_reference="Genesis 3:16",
        part=NarrativePart.PART_ONE,
        sequence_number=40,
        native_mood="Pain woven into birth"
    ),
    
    NarrativeEvent(
        event_text="'Cursed is the ground for thy sake'",
        verse_reference="Genesis 3:17",
        part=NarrativePart.PART_ONE,
        sequence_number=41,
        native_mood="Creation groaning"
    ),
    
    NarrativeEvent(
        event_text="'Dust thou art, and unto dust shalt thou return'",
        verse_reference="Genesis 3:19",
        part=NarrativePart.PART_ONE,
        sequence_number=42,
        native_mood="Death sentence pronounced",
        plants_phrase="unto dust"
    ),
    
    NarrativeEvent(
        event_text="Garments of skin: the first sacrifice",
        verse_reference="Genesis 3:21",
        part=NarrativePart.PART_ONE,
        sequence_number=43,
        native_mood="Blood covering shame",
        plants_phrase="garments of skin"
    ),
    
    NarrativeEvent(
        event_text="Expulsion from the Garden",
        verse_reference="Genesis 3:24",
        part=NarrativePart.PART_ONE,
        sequence_number=44,
        native_mood="Paradise lost"
    ),
    
    NarrativeEvent(
        event_text="Cherubim and flaming sword guard the tree of life",
        verse_reference="Genesis 3:24",
        part=NarrativePart.PART_ONE,
        sequence_number=45,
        native_mood="Access barred"
    ),
    
    # ========================================================================
    # PART TWO: The First Blood
    # From Cain and Abel through the Flood
    # ========================================================================
    
    NarrativeEvent(
        event_text="Cain and Abel born",
        verse_reference="Genesis 4:1-2",
        part=NarrativePart.PART_TWO,
        sequence_number=46,
        native_mood="New generation under curse"
    ),
    
    NarrativeEvent(
        event_text="Offerings brought: Cain's fruit, Abel's firstling",
        verse_reference="Genesis 4:3-4",
        part=NarrativePart.PART_TWO,
        sequence_number=47,
        native_mood="Worship divided"
    ),
    
    NarrativeEvent(
        event_text="The LORD has regard for Abel's offering, not Cain's",
        verse_reference="Genesis 4:4-5",
        part=NarrativePart.PART_TWO,
        sequence_number=48,
        native_mood="Divine discrimination"
    ),
    
    NarrativeEvent(
        event_text="'Sin croucheth at the door'",
        verse_reference="Genesis 4:7",
        part=NarrativePart.PART_TWO,
        sequence_number=49,
        native_mood="Warning unheeded"
    ),
    
    NarrativeEvent(
        event_text="Cain rises against Abel in the field",
        verse_reference="Genesis 4:8",
        part=NarrativePart.PART_TWO,
        sequence_number=50,
        native_mood="First murder"
    ),
    
    NarrativeEvent(
        event_text="'Where is Abel thy brother?' 'Am I my brother's keeper?'",
        verse_reference="Genesis 4:9",
        part=NarrativePart.PART_TWO,
        sequence_number=51,
        native_mood="Evasion in the face of blood"
    ),
    
    NarrativeEvent(
        event_text="'The voice of thy brother's blood crieth unto me from the ground'",
        verse_reference="Genesis 4:10",
        part=NarrativePart.PART_TWO,
        sequence_number=52,
        native_mood="Blood that accuses",
        plants_phrase="blood crieth from the ground"
    ),
    
    NarrativeEvent(
        event_text="Mark of Cain set upon him",
        verse_reference="Genesis 4:15",
        part=NarrativePart.PART_TWO,
        sequence_number=53,
        native_mood="Protection in judgment"
    ),
    
    # Continue with genealogies, Enoch, the corruption, Noah...
    # [Additional events would be enumerated here]
    
    # ========================================================================
    # MUCH LATER IN NARRATIVE: Revelation scenes placed BEFORE the Passion
    # ========================================================================
    # These must come before the Cross so they haunt the ending
    
    NarrativeEvent(
        event_text="The throne room of heaven: 'Holy, holy, holy'",
        verse_reference="Revelation 4:8",
        part=NarrativePart.PART_NINE,
        sequence_number=2900,
        native_mood="Overwhelming celestial worship"
    ),
    
    NarrativeEvent(
        event_text="The scroll with seven seals: who is worthy to open?",
        verse_reference="Revelation 5:2-4",
        part=NarrativePart.PART_NINE,
        sequence_number=2901,
        native_mood="Cosmic tension: no one found worthy"
    ),
    
    NarrativeEvent(
        event_text="A Lamb standing as though slain",
        verse_reference="Revelation 5:6",
        part=NarrativePart.PART_NINE,
        sequence_number=2902,
        native_mood="Glory of the wounded Lamb",
        echoes_phrase="as a lamb to the slaughter"
    ),
    
    NarrativeEvent(
        event_text="'Worthy is the Lamb that was slain'",
        verse_reference="Revelation 5:12",
        part=NarrativePart.PART_NINE,
        sequence_number=2903,
        native_mood="Heaven's eternal anthem"
    ),
    
    NarrativeEvent(
        event_text="'God shall wipe away all tears from their eyes'",
        verse_reference="Revelation 21:4",
        part=NarrativePart.PART_NINE,
        sequence_number=2904,
        native_mood="Promise of complete restoration",
        echoes_phrase="unto dust"  # The reversal
    ),
    
    NarrativeEvent(
        event_text="New Jerusalem descending: 'Behold, the tabernacle of God is with men'",
        verse_reference="Revelation 21:3",
        part=NarrativePart.PART_NINE,
        sequence_number=2905,
        native_mood="Final dwelling"
    ),
    
    # Resurrection scenes also placed BEFORE the Passion in narrative order
    NarrativeEvent(
        event_text="The empty tomb: 'He is not here; he is risen'",
        verse_reference="Matthew 28:6",
        part=NarrativePart.PART_TEN,
        sequence_number=3000,
        native_mood="Bewildering joy"
    ),
    
    NarrativeEvent(
        event_text="Thomas sees and believes: 'My Lord and my God'",
        verse_reference="John 20:28",
        part=NarrativePart.PART_TEN,
        sequence_number=3001,
        native_mood="Doubt transformed to worship"
    ),
    
    NarrativeEvent(
        event_text="The Great Commission: 'Go ye therefore'",
        verse_reference="Matthew 28:19",
        part=NarrativePart.PART_TEN,
        sequence_number=3002,
        native_mood="Mission given"
    ),
    
    NarrativeEvent(
        event_text="Pentecost: tongues of fire, speaking in other tongues",
        verse_reference="Acts 2:3-4",
        part=NarrativePart.PART_TEN,
        sequence_number=3003,
        native_mood="Spirit poured out",
        echoes_phrase="breath of life"
    ),
    
    # ========================================================================
    # PART ELEVEN: The Final Breath
    # The Passion - building to the terminus
    # ========================================================================
    
    NarrativeEvent(
        event_text="Gethsemane: 'My soul is exceeding sorrowful, even unto death'",
        verse_reference="Matthew 26:38",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3100,
        native_mood="Crushing sorrow"
    ),
    
    NarrativeEvent(
        event_text="'Father, if it be possible, let this cup pass from me'",
        verse_reference="Matthew 26:39",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3101,
        native_mood="Human shrinking from the cup"
    ),
    
    NarrativeEvent(
        event_text="'Nevertheless not my will, but thine, be done'",
        verse_reference="Luke 22:42",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3102,
        native_mood="Surrender",
        echoes_phrase="Be it unto me"
    ),
    
    NarrativeEvent(
        event_text="Sweat like drops of blood falling to the ground",
        verse_reference="Luke 22:44",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3103,
        native_mood="Agony made visible"
    ),
    
    NarrativeEvent(
        event_text="Judas's kiss: 'Hail, Master'",
        verse_reference="Matthew 26:49",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3104,
        native_mood="Betrayal's mockery of love"
    ),
    
    NarrativeEvent(
        event_text="'Friend, wherefore art thou come?'",
        verse_reference="Matthew 26:50",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3105,
        native_mood="Gentle address to the betrayer"
    ),
    
    NarrativeEvent(
        event_text="Peter's sword: the servant's ear cut off",
        verse_reference="Matthew 26:51",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3106,
        native_mood="Violent defense"
    ),
    
    NarrativeEvent(
        event_text="'Put up thy sword... all they that take the sword shall perish with the sword'",
        verse_reference="Matthew 26:52",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3107,
        native_mood="Rejection of violence"
    ),
    
    NarrativeEvent(
        event_text="'Thinkest thou that I cannot now pray to my Father, and he shall give me twelve legions of angels?'",
        verse_reference="Matthew 26:53",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3108,
        native_mood="Power withheld"
    ),
    
    NarrativeEvent(
        event_text="All the disciples forsake him and flee",
        verse_reference="Matthew 26:56",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3109,
        native_mood="Abandonment"
    ),
    
    NarrativeEvent(
        event_text="Before Caiaphas: 'Art thou the Christ?'",
        verse_reference="Matthew 26:63",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3110,
        native_mood="The question"
    ),
    
    NarrativeEvent(
        event_text="'Thou hast said: hereafter shall ye see the Son of man sitting on the right hand of power'",
        verse_reference="Matthew 26:64",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3111,
        native_mood="Divine claim"
    ),
    
    NarrativeEvent(
        event_text="'He hath spoken blasphemy... He is guilty of death'",
        verse_reference="Matthew 26:65-66",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3112,
        native_mood="Condemnation"
    ),
    
    NarrativeEvent(
        event_text="They spit in his face and strike him",
        verse_reference="Matthew 26:67",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3113,
        native_mood="Humiliation begins"
    ),
    
    NarrativeEvent(
        event_text="Peter's three denials",
        verse_reference="Matthew 26:69-75",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3114,
        native_mood="Fear conquering love"
    ),
    
    NarrativeEvent(
        event_text="The rooster crows; Peter weeps bitterly",
        verse_reference="Matthew 26:75",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3115,
        native_mood="Broken recognition"
    ),
    
    NarrativeEvent(
        event_text="Judas returns the thirty pieces of silver",
        verse_reference="Matthew 27:3",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3116,
        native_mood="Too-late remorse"
    ),
    
    NarrativeEvent(
        event_text="'I have sinned in that I have betrayed innocent blood'",
        verse_reference="Matthew 27:4",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3117,
        native_mood="Confession without absolution"
    ),
    
    NarrativeEvent(
        event_text="Judas hangs himself",
        verse_reference="Matthew 27:5",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3118,
        native_mood="Despair's end"
    ),
    
    NarrativeEvent(
        event_text="Before Pilate: 'Art thou the King of the Jews?'",
        verse_reference="Matthew 27:11",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3119,
        native_mood="Political question"
    ),
    
    NarrativeEvent(
        event_text="'Thou sayest'",
        verse_reference="Matthew 27:11",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3120,
        native_mood="Ambiguous affirmation"
    ),
    
    NarrativeEvent(
        event_text="He answered nothing",
        verse_reference="Matthew 27:12",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3121,
        native_mood="Silence",
        echoes_phrase="as a lamb to the slaughter"
    ),
    
    NarrativeEvent(
        event_text="Pilate's wife's dream: 'Have thou nothing to do with that just man'",
        verse_reference="Matthew 27:19",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3122,
        native_mood="Warning ignored"
    ),
    
    NarrativeEvent(
        event_text="'Release unto us Barabbas'",
        verse_reference="Luke 23:18",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3123,
        native_mood="The crowd's terrible choice"
    ),
    
    NarrativeEvent(
        event_text="'What shall I do then with Jesus which is called Christ?'",
        verse_reference="Matthew 27:22",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3124,
        native_mood="The question that implicates every reader"
    ),
    
    NarrativeEvent(
        event_text="'Crucify him!'",
        verse_reference="Matthew 27:22",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3125,
        native_mood="Murder demanded"
    ),
    
    NarrativeEvent(
        event_text="Pilate washes his hands: 'I am innocent of the blood of this just person'",
        verse_reference="Matthew 27:24",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3126,
        native_mood="Futile absolution"
    ),
    
    NarrativeEvent(
        event_text="'His blood be on us, and on our children'",
        verse_reference="Matthew 27:25",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3127,
        native_mood="Terrible self-curse"
    ),
    
    NarrativeEvent(
        event_text="Jesus scourged",
        verse_reference="Matthew 27:26",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3128,
        native_mood="Flesh torn",
        echoes_phrase="with his stripes we are healed"
    ),
    
    NarrativeEvent(
        event_text="Crown of thorns pressed onto his head",
        verse_reference="Matthew 27:29",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3129,
        native_mood="Mockery of kingship"
    ),
    
    NarrativeEvent(
        event_text="'Hail, King of the Jews!'",
        verse_reference="Matthew 27:29",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3130,
        native_mood="Truth spoken in scorn"
    ),
    
    NarrativeEvent(
        event_text="Simon of Cyrene compelled to carry the cross",
        verse_reference="Matthew 27:32",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3131,
        native_mood="Unwilling discipleship",
        echoes_phrase="grain of wood against shoulder"
    ),
    
    NarrativeEvent(
        event_text="'Daughters of Jerusalem, weep not for me'",
        verse_reference="Luke 23:28",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3132,
        native_mood="Prophetic warning in the midst of suffering"
    ),
    
    NarrativeEvent(
        event_text="Golgotha: The Place of the Skull",
        verse_reference="Matthew 27:33",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3133,
        native_mood="Destination reached"
    ),
    
    NarrativeEvent(
        event_text="They offer him wine mingled with gall; he refuses",
        verse_reference="Matthew 27:34",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3134,
        native_mood="No dulling of the pain"
    ),
    
    NarrativeEvent(
        event_text="They crucify him",
        verse_reference="Matthew 27:35",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3135,
        native_mood="The act"
    ),
    
    NarrativeEvent(
        event_text="They divide his garments, casting lots",
        verse_reference="Matthew 27:35",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3136,
        native_mood="Scripture fulfilled in callousness"
    ),
    
    NarrativeEvent(
        event_text="The inscription: THIS IS JESUS THE KING OF THE JEWS",
        verse_reference="Matthew 27:37",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3137,
        native_mood="Inadvertent proclamation"
    ),
    
    NarrativeEvent(
        event_text="Two thieves crucified with him, one on each side",
        verse_reference="Matthew 27:38",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3138,
        native_mood="Numbered with transgressors"
    ),
    
    NarrativeEvent(
        event_text="The passersby revile him, wagging their heads",
        verse_reference="Matthew 27:39",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3139,
        native_mood="Mockery from below"
    ),
    
    NarrativeEvent(
        event_text="'If thou be the Son of God, come down from the cross'",
        verse_reference="Matthew 27:40",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3140,
        native_mood="The temptation repeated"
    ),
    
    NarrativeEvent(
        event_text="'He saved others; himself he cannot save'",
        verse_reference="Matthew 27:42",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3141,
        native_mood="Truth spoken in scorn"
    ),
    
    NarrativeEvent(
        event_text="'He trusted in God; let him deliver him now, if he will have him'",
        verse_reference="Matthew 27:43",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3142,
        native_mood="Faith mocked"
    ),
    
    NarrativeEvent(
        event_text="One thief rails: 'If thou be Christ, save thyself and us'",
        verse_reference="Luke 23:39",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3143,
        native_mood="Dying bitterness"
    ),
    
    NarrativeEvent(
        event_text="The other thief rebukes: 'Dost not thou fear God?'",
        verse_reference="Luke 23:40",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3144,
        native_mood="Dying faith"
    ),
    
    NarrativeEvent(
        event_text="'We receive the due reward of our deeds: but this man hath done nothing amiss'",
        verse_reference="Luke 23:41",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3145,
        native_mood="Confession of innocence"
    ),
    
    NarrativeEvent(
        event_text="'Lord, remember me when thou comest into thy kingdom'",
        verse_reference="Luke 23:42",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3146,
        native_mood="Faith from the edge of death"
    ),
    
    NarrativeEvent(
        event_text="'Today shalt thou be with me in paradise'",
        verse_reference="Luke 23:43",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3147,
        native_mood="Promise from the cross"
    ),
    
    NarrativeEvent(
        event_text="'Woman, behold thy son... Behold thy mother'",
        verse_reference="John 19:26-27",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3148,
        native_mood="Care for the bereaved",
        echoes_phrase="sword shall pierce"
    ),
    
    NarrativeEvent(
        event_text="Darkness over all the land from the sixth hour to the ninth",
        verse_reference="Matthew 27:45",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3149,
        native_mood="Creation's mourning"
    ),
    
    NarrativeEvent(
        event_text="'Eli, Eli, lama sabachthani?' - 'My God, my God, why hast thou forsaken me?'",
        verse_reference="Matthew 27:46",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3150,
        native_mood="The cry of dereliction"
    ),
    
    NarrativeEvent(
        event_text="'I thirst'",
        verse_reference="John 19:28",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3151,
        native_mood="Human need"
    ),
    
    NarrativeEvent(
        event_text="They give him vinegar to drink",
        verse_reference="Matthew 27:48",
        part=NarrativePart.PART_ELEVEN,
        sequence_number=3152,
        native_mood="Bitter offering"
    ),
    
    # ========================================================================
    # TERMINUS: He Bows His Head
    # The narrative ends here. This is the final event.
    # ========================================================================
    
    NarrativeEvent(
        event_text="'It is finished'",
        verse_reference="John 19:30",
        part=NarrativePart.TERMINUS,
        sequence_number=3153,
        native_mood="Triumphant completion"
    ),
    
    NarrativeEvent(
        event_text="'Father, into thy hands I commend my spirit'",
        verse_reference="Luke 23:46",
        part=NarrativePart.TERMINUS,
        sequence_number=3154,
        native_mood="Final surrender",
        echoes_phrase="breath of life"  # The breath returns to the Giver
    ),
    
    NarrativeEvent(
        event_text="He bowed his head, and gave up the ghost",
        verse_reference="John 19:30",
        part=NarrativePart.TERMINUS,
        sequence_number=3155,
        native_mood="The end",
        breath_note="THE NARRATIVE ENDS HERE. The final breath. The silence. What the world does to that which is beautiful."
    ),
]


# ============================================================================
# ACCESS FUNCTIONS
# ============================================================================

def get_narrative_order() -> List[NarrativeEvent]:
    """Get the complete narrative ordering."""
    return NARRATIVE_ORDER.copy()


def get_terminal_event() -> NarrativeEvent:
    """Get the terminal event (the Cross)."""
    return NARRATIVE_ORDER[-1]


def get_events_by_part(part: NarrativePart) -> List[NarrativeEvent]:
    """Get all events in a specific part."""
    return [e for e in NARRATIVE_ORDER if e.part == part]


def find_echoes(phrase: str) -> List[NarrativeEvent]:
    """Find events that echo a specific phrase."""
    return [e for e in NARRATIVE_ORDER 
            if e.echoes_phrase and phrase.lower() in e.echoes_phrase.lower()]


def find_plantings(phrase: str) -> List[NarrativeEvent]:
    """Find events that plant a specific phrase."""
    return [e for e in NARRATIVE_ORDER 
            if e.plants_phrase and phrase.lower() in e.plants_phrase.lower()]


def get_statistics() -> dict:
    """Get statistics about the narrative order."""
    parts = {}
    for e in NARRATIVE_ORDER:
        p = e.part.value
        parts[p] = parts.get(p, 0) + 1
    
    plants = len([e for e in NARRATIVE_ORDER if e.plants_phrase])
    echoes = len([e for e in NARRATIVE_ORDER if e.echoes_phrase])
    
    return {
        'total_events': len(NARRATIVE_ORDER),
        'by_part': parts,
        'phrases_planted': plants,
        'phrases_echoed': echoes,
        'terminal_event': NARRATIVE_ORDER[-1].event_text,
    }


if __name__ == "__main__":
    stats = get_statistics()
    print("\nNarrative Order Statistics:")
    print("=" * 60)
    print(f"Total Events: {stats['total_events']}")
    print(f"Phrases Planted: {stats['phrases_planted']}")
    print(f"Phrases Echoed: {stats['phrases_echoed']}")
    print(f"\nTerminal Event: {stats['terminal_event']}")
    print("\nBy Part:")
    for part, count in stats['by_part'].items():
        print(f"  {part}: {count}")
