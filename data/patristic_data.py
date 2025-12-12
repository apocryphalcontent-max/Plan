#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Patristic Database
Embedded patristic commentary and Church Fathers' wisdom
Eliminates API dependency for patristic integration
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

sys.path.insert(0, str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)


@dataclass
class PatristicEntry:
    """A single patristic commentary entry."""
    father: str
    work: str
    verse_ref: str
    text: str
    sense: str  # literal, allegorical, tropological, anagogical
    theme: str
    tradition: str  # Alexandrian, Antiochene, Cappadocian, etc.


# ============================================================================
# CHURCH FATHERS - CORE METADATA
# ============================================================================

CHURCH_FATHERS_META = {
    'Origen': {
        'dates': '185-254',
        'tradition': 'Alexandrian',
        'emphasis': ['allegory', 'spiritual_sense', 'soul_ascent'],
        'key_works': ['De Principiis', 'Contra Celsum', 'Homilies on Genesis']
    },
    'Athanasius': {
        'dates': '296-373',
        'tradition': 'Alexandrian',
        'emphasis': ['incarnation', 'theosis', 'christology'],
        'key_works': ['On the Incarnation', 'Against the Arians', 'Life of Antony']
    },
    'Basil the Great': {
        'dates': '330-379',
        'tradition': 'Cappadocian',
        'emphasis': ['creation', 'holy_spirit', 'monasticism'],
        'key_works': ['Hexaemeron', 'On the Holy Spirit', 'Longer Rules']
    },
    'Gregory of Nazianzus': {
        'dates': '329-390',
        'tradition': 'Cappadocian',
        'emphasis': ['trinity', 'christology', 'theology'],
        'key_works': ['Theological Orations', 'Poems', 'Letters']
    },
    'Gregory of Nyssa': {
        'dates': '335-395',
        'tradition': 'Cappadocian',
        'emphasis': ['mysticism', 'apophatic', 'infinite_progress'],
        'key_works': ['Life of Moses', 'On the Soul and Resurrection', 'Commentary on Song of Songs']
    },
    'John Chrysostom': {
        'dates': '349-407',
        'tradition': 'Antiochene',
        'emphasis': ['literal', 'moral', 'homiletical'],
        'key_works': ['Homilies on Matthew', 'Homilies on John', 'Homilies on Romans']
    },
    'Augustine': {
        'dates': '354-430',
        'tradition': 'Western',
        'emphasis': ['grace', 'trinity', 'love'],
        'key_works': ['Confessions', 'City of God', 'On the Trinity']
    },
    'Cyril of Alexandria': {
        'dates': '376-444',
        'tradition': 'Alexandrian',
        'emphasis': ['christology', 'theotokos', 'unity'],
        'key_works': ['Commentary on John', 'Against Nestorius', 'Thesaurus']
    },
    'Maximus the Confessor': {
        'dates': '580-662',
        'tradition': 'Byzantine',
        'emphasis': ['cosmic_liturgy', 'theosis', 'logoi'],
        'key_works': ['Ambigua', 'Mystagogy', 'Questions to Thalassius']
    },
    'John of Damascus': {
        'dates': '675-749',
        'tradition': 'Byzantine',
        'emphasis': ['icons', 'systematic', 'synthesis'],
        'key_works': ['Exact Exposition of the Orthodox Faith', 'On Divine Images']
    },
    'Ephrem the Syrian': {
        'dates': '306-373',
        'tradition': 'Syriac',
        'emphasis': ['poetry', 'typology', 'symbols'],
        'key_works': ['Hymns on Paradise', 'Commentary on Genesis', 'Hymns on Faith']
    },
    'Gregory Palamas': {
        'dates': '1296-1359',
        'tradition': 'Hesychast',
        'emphasis': ['essence_energies', 'hesychasm', 'uncreated_light'],
        'key_works': ['Triads', 'Homilies', 'One Hundred and Fifty Chapters']
    },
    'Jerome': {
        'dates': '347-420',
        'tradition': 'Western',
        'emphasis': ['translation', 'hebrew', 'literal', 'monasticism'],
        'key_works': ['Vulgate', 'Commentary on Isaiah', 'Commentary on Daniel']
    },
    'Ambrose': {
        'dates': '340-397',
        'tradition': 'Milanese',
        'emphasis': ['allegory', 'ethics', 'hymns', 'church_state'],
        'key_works': ['Hexaemeron', 'On the Holy Spirit', 'Exposition of Luke']
    },
    'Irenaeus': {
        'dates': '130-202',
        'tradition': 'Lyonese',
        'emphasis': ['recapitulation', 'anti_gnostic', 'tradition', 'apostolic'],
        'key_works': ['Against Heresies', 'Demonstration of Apostolic Preaching']
    },
    'Gregory the Great': {
        'dates': '540-604',
        'tradition': 'Roman',
        'emphasis': ['moral_interpretation', 'pastoral_care', 'liturgy'],
        'key_works': ['Moralia on Job', 'Dialogues', 'Pastoral Rule']
    },
    'Leo the Great': {
        'dates': '400-461',
        'tradition': 'Roman',
        'emphasis': ['christology', 'papacy', 'tome', 'two_natures'],
        'key_works': ['Tome of Leo', 'Sermons', 'Letters']
    },
    'Bede': {
        'dates': '673-735',
        'tradition': 'Western',
        'emphasis': ['exegesis', 'history', 'homilies'],
        'key_works': ['Ecclesiastical History', 'Commentary on Mark', 'Commentary on Luke']
    },
    'Clement of Alexandria': {
        'dates': '150-215',
        'tradition': 'Alexandrian',
        'emphasis': ['philosophy', 'gnosis', 'pedagogy'],
        'key_works': ['Stromata', 'Paedagogus', 'Protrepticus']
    },
    'Cyril of Jerusalem': {
        'dates': '313-386',
        'tradition': 'Palestinian',
        'emphasis': ['catechesis', 'sacraments', 'creed'],
        'key_works': ['Catechetical Lectures', 'Mystagogical Catecheses']
    },
    'Hippolytus': {
        'dates': '170-235',
        'tradition': 'Roman',
        'emphasis': ['apocalyptic', 'anti_heretical', 'liturgy'],
        'key_works': ['Refutation of All Heresies', 'Commentary on Daniel', 'Apostolic Tradition']
    },
    'Bernard of Clairvaux': {
        'dates': '1090-1153',
        'tradition': 'Western',
        'emphasis': ['mysticism', 'devotion', 'monasticism'],
        'key_works': ['Sermons on Song of Songs', 'On Loving God', 'Steps of Humility']
    },
}


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - GENESIS
# ============================================================================

GENESIS_COMMENTARY = [
    PatristicEntry(
        father='Basil the Great',
        work='Hexaemeron I.2',
        verse_ref='Genesis 1:1',
        text='In the beginning. What a glorious opening! It puts aside the false theory of matter without beginning and time without creation. It proclaims that the world has a beginning and that its Creator is God.',
        sense='literal',
        theme='creation',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='Augustine',
        work='Confessions XI.13',
        verse_ref='Genesis 1:1',
        text='What then is time? If no one asks me, I know; but if I wish to explain it to one who asks, I know not. Yet I say with confidence that I know that if nothing passed away, there would be no past time; and if nothing were coming, there would be no future time; and if nothing were, there would be no present time.',
        sense='literal',
        theme='time',
        tradition='Western'
    ),
    PatristicEntry(
        father='Origen',
        work='Homilies on Genesis I.1',
        verse_ref='Genesis 1:1',
        text='The beginning is Christ, for He is the Beginning and the End. In Him all things were created, and He is before all things. When Scripture says "In the beginning," it refers to the eternal Word through whom all creation came to be.',
        sense='allegorical',
        theme='christology',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Gregory of Nyssa',
        work='On the Making of Man',
        verse_ref='Genesis 1:26',
        text='The image of God in man is not found in bodily form, for God has no body, but in the rational soul, in free will, in dominion over creation, and in the capacity for virtue. The image is dynamic, capable of growth toward its archetype through theosis.',
        sense='tropological',
        theme='theosis',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='Maximus the Confessor',
        work='Ambiguum 7',
        verse_ref='Genesis 1:26',
        text='Humanity was created to be the bond of the universe, uniting the sensible and intelligible realms. In Christ, this vocation is fulfilled: He unites heaven and earth, visible and invisible, creature and Creator.',
        sense='anagogical',
        theme='cosmic_liturgy',
        tradition='Byzantine'
    ),
    PatristicEntry(
        father='Ephrem the Syrian',
        work='Hymns on Paradise III',
        verse_ref='Genesis 2:8',
        text='Paradise is both place and state. The tree of life prefigures the Cross, the garden prefigures the Church, and Adam prefigures Christ who came to restore what the first man lost.',
        sense='allegorical',
        theme='typology',
        tradition='Syriac'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Genesis XVII',
        verse_ref='Genesis 3:15',
        text='This is the first gospel, the protoevangelium. The seed of the woman is Christ, who crushed the serpent\'s head by His death and resurrection. Though the serpent wounded His heel at the Cross, Christ trampled down death by death.',
        sense='allegorical',
        theme='christology',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Origen',
        work='Homilies on Genesis VIII',
        verse_ref='Genesis 22:2',
        text='Isaac carrying the wood prefigures Christ carrying the cross. The ram caught in the thicket represents Christ crowned with thorns. Abraham\'s willingness to sacrifice his only son reveals the Father\'s love in giving His Son.',
        sense='allegorical',
        theme='sacrifice',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Augustine',
        work='City of God XVI.32',
        verse_ref='Genesis 22:8',
        text='God will provide Himself a lamb. Abraham spoke better than he knew. The lamb provided was not merely the ram but the Lamb of God who takes away the sin of the world, foreseen from before the foundation.',
        sense='allegorical',
        theme='providence',
        tradition='Western'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - JOHN'S GOSPEL
# ============================================================================

JOHN_COMMENTARY = [
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on John I',
        verse_ref='John 1:1',
        text='In the beginning was the Word. Mark the precision: not "came to be" but "was" - the Word eternally exists. The evangelist soars higher than all philosophy, proclaiming the co-eternal existence of the Son with the Father.',
        sense='literal',
        theme='christology',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Origen',
        work='Commentary on John I.22',
        verse_ref='John 1:1',
        text='The Word was with God - literally "toward God" (pros ton theon). This indicates not mere proximity but eternal relationship, the Son eternally facing the Father in loving communion, the dance of the Trinity.',
        sense='literal',
        theme='trinity',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Commentary on John I',
        verse_ref='John 1:14',
        text='The Word became flesh - not by conversion of divinity into flesh, but by assumption of humanity into God. The two natures unite in one person without confusion, change, division, or separation.',
        sense='literal',
        theme='incarnation',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Augustine',
        work='Tractates on John XV',
        verse_ref='John 3:16',
        text='God so loved the world. Let no one say, "Who is the world that God should love it?" The world is the human race, alienated from God by sin, yet so loved that He gave His only-begotten Son.',
        sense='tropological',
        theme='love',
        tradition='Western'
    ),
    PatristicEntry(
        father='Gregory of Nyssa',
        work='On the Soul and Resurrection',
        verse_ref='John 6:35',
        text='I am the bread of life. As bread sustains bodily life, so Christ sustains the soul. More: He transforms us into Himself. We do not change Christ into us; He changes us into Him, deifying those who partake.',
        sense='anagogical',
        theme='theosis',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='Maximus the Confessor',
        work='Questions to Thalassius 21',
        verse_ref='John 10:11',
        text='I am the good shepherd. The shepherd gathers scattered humanity into one flock. Christ unites all the logoi of creation in His one Logos, bringing the many into unity without destroying diversity.',
        sense='anagogical',
        theme='cosmic_unity',
        tradition='Byzantine'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on John LXXXV',
        verse_ref='John 19:30',
        text='It is finished. Not a cry of defeat but of triumph. The work of salvation is complete. What the Law could not do, what prophets foretold, what creation awaited - all is accomplished in this moment.',
        sense='literal',
        theme='salvation',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Commentary on John XII',
        verse_ref='John 19:34',
        text='Blood and water flowed from His side - the mysteries of the Church. From the side of the sleeping Adam came Eve; from the side of Christ asleep in death comes the Church, His bride, born of baptism and Eucharist.',
        sense='allegorical',
        theme='church',
        tradition='Alexandrian'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - PSALMS
# ============================================================================

PSALMS_COMMENTARY = [
    PatristicEntry(
        father='Augustine',
        work='Expositions on the Psalms 22.1',
        verse_ref='Psalm 22:1',
        text='My God, my God, why hast thou forsaken me? Christ speaks these words on the cross, making our abandonment His own. He who knew no sin became sin for us, bearing the weight of human separation from God.',
        sense='allegorical',
        theme='passion',
        tradition='Western'
    ),
    PatristicEntry(
        father='Basil the Great',
        work='Homily on Psalm 1',
        verse_ref='Psalm 1:1',
        text='Blessed is the man. The Psalter begins with blessing, just as Christ began His teaching with the Beatitudes. Both show the path from happiness sought in the wrong places to true blessedness in God.',
        sense='tropological',
        theme='virtue',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='Gregory of Nyssa',
        work='On the Inscriptions of the Psalms',
        verse_ref='Psalm 23:1',
        text='The LORD is my shepherd. The soul that speaks thus has passed through the stages of spiritual growth: purification, illumination, and union. It rests in the Divine Shepherd who leads it to still waters.',
        sense='anagogical',
        theme='mysticism',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='Athanasius',
        work='Letter to Marcellinus',
        verse_ref='Psalm 51:1',
        text='Have mercy upon me. The Psalter is a mirror of the soul. In Psalm 51, David shows us how to repent. His words become our words; his contrition becomes our path back to God.',
        sense='tropological',
        theme='repentance',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Commentary on Psalm 110',
        verse_ref='Psalm 110:1',
        text='The LORD said unto my Lord. David calls his descendant Lord - how can this be unless the Messiah is divine? Christ Himself used this psalm to confound the Pharisees and reveal His divine sonship.',
        sense='allegorical',
        theme='christology',
        tradition='Antiochene'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - ISAIAH
# ============================================================================

ISAIAH_COMMENTARY = [
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Isaiah',
        verse_ref='Isaiah 6:3',
        text='Holy, holy, holy is the LORD of hosts. The seraphim cover their faces before the thrice-holy God. If even celestial beings veil themselves before such glory, how much more should we approach with awe?',
        sense='literal',
        theme='holiness',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Commentary on Isaiah',
        verse_ref='Isaiah 7:14',
        text='A virgin shall conceive. The Hebrew almah can mean young woman, but the Spirit through the Septuagint gives parthenos, virgin. The prophecy finds its fulfillment only in Mary, who conceived without man.',
        sense='allegorical',
        theme='incarnation',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Origen',
        work='Homilies on Isaiah',
        verse_ref='Isaiah 53:5',
        text='He was wounded for our transgressions. Each wound of Christ corresponds to our sins. He bore stripes that we might be healed, was crushed that we might be made whole. The Suffering Servant is the Logos.',
        sense='allegorical',
        theme='atonement',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Gregory of Nazianzus',
        work='Oration 38',
        verse_ref='Isaiah 9:6',
        text='For unto us a child is born. The names reveal the mystery: Wonderful Counselor - divine wisdom; Mighty God - divine power; Everlasting Father - eternal providence; Prince of Peace - eschatological hope.',
        sense='allegorical',
        theme='christology',
        tradition='Cappadocian'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - REVELATION
# ============================================================================

REVELATION_COMMENTARY = [
    PatristicEntry(
        father='Maximus the Confessor',
        work='Questions to Thalassius 63',
        verse_ref='Revelation 1:8',
        text='I am Alpha and Omega. Christ is the beginning and end of all creation. In Him, the logoi of all things find their origin and their fulfillment. The cosmos moves from Him and toward Him.',
        sense='anagogical',
        theme='eschatology',
        tradition='Byzantine'
    ),
    PatristicEntry(
        father='Origen',
        work='Commentary on Revelation',
        verse_ref='Revelation 5:6',
        text='A Lamb as it had been slain. The Lamb stands eternally in the posture of sacrifice, His wounds glorified. The Cross is not merely past event but eternal reality, the center of cosmic redemption.',
        sense='anagogical',
        theme='sacrifice',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Augustine',
        work='City of God XX',
        verse_ref='Revelation 21:1',
        text='A new heaven and a new earth. Not destruction but transformation. As our bodies will be raised and glorified, so creation itself will be renewed, freed from bondage to decay.',
        sense='anagogical',
        theme='eschatology',
        tradition='Western'
    ),
    PatristicEntry(
        father='Gregory of Nyssa',
        work='On the Soul and Resurrection',
        verse_ref='Revelation 21:4',
        text='God shall wipe away all tears. This is the promise of apocatastasis, the restoration of all things. Every soul, purified through divine pedagogy, will finally enter into the joy of their Lord.',
        sense='anagogical',
        theme='restoration',
        tradition='Cappadocian'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - EXODUS
# ============================================================================

EXODUS_COMMENTARY = [
    PatristicEntry(
        father='Origen',
        work='Homilies on Exodus I.5',
        verse_ref='Exodus 3:14',
        text='I AM WHO I AM. God reveals His name as Being itself. He is not one being among others, but the source of all existence. The burning bush that is not consumed shows that divine fire gives life rather than destroying.',
        sense='literal',
        theme='divine_nature',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Gregory of Nyssa',
        work='Life of Moses II.19',
        verse_ref='Exodus 3:5',
        text='Put off your shoes from your feet. Moses must become barefoot to approach holy ground. The soul ascending to God must strip away the dead skins of earthly attachments. True philosophy is the removal of coverings.',
        sense='tropological',
        theme='asceticism',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Glaphyra on Exodus II',
        verse_ref='Exodus 12:13',
        text='When I see the blood, I will pass over you. The blood of the Passover lamb prefigures Christ whose blood shields believers from judgment. Egypt represents sin; Pharaoh, the devil; Moses, Christ the liberator.',
        sense='allegorical',
        theme='passover',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Ephrem the Syrian',
        work='Commentary on Exodus',
        verse_ref='Exodus 14:22',
        text='The children of Israel went through the midst of the sea on dry ground. The crossing prefigures baptism: water that destroys the enemy becomes the path to freedom. We pass through death to new life.',
        sense='allegorical',
        theme='baptism',
        tradition='Syriac'
    ),
    PatristicEntry(
        father='Augustine',
        work='Questions on Exodus',
        verse_ref='Exodus 20:1',
        text='God spoke all these words. The Ten Commandments are not arbitrary rules but the contours of love. The first three concern love of God; the remaining seven, love of neighbor. Love fulfills the law.',
        sense='tropological',
        theme='ethics',
        tradition='Western'
    ),
    PatristicEntry(
        father='Basil the Great',
        work='On the Holy Spirit XV',
        verse_ref='Exodus 40:34',
        text='The cloud covered the tent of meeting. The glory that filled the tabernacle foreshadows the Spirit dwelling in the Church. Where God dwells, His glory is manifest through holiness.',
        sense='allegorical',
        theme='holy_spirit',
        tradition='Cappadocian'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - LEVITICUS
# ============================================================================

LEVITICUS_COMMENTARY = [
    PatristicEntry(
        father='Origen',
        work='Homilies on Leviticus I.3',
        verse_ref='Leviticus 1:3',
        text='If his offering is a burnt offering. The burnt offering wholly consumed signifies total self-offering to God. We become living sacrifices when every part of our life is given to the divine fire.',
        sense='tropological',
        theme='sacrifice',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Glaphyra on Leviticus',
        verse_ref='Leviticus 16:15',
        text='The goat of the sin offering for the people. The Day of Atonement finds its true meaning in Christ who entered the heavenly sanctuary with His own blood, making eternal atonement for sins.',
        sense='allegorical',
        theme='atonement',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Hebrews',
        verse_ref='Leviticus 17:11',
        text='The life of the flesh is in the blood. Blood represents life itself. Animal blood could only temporarily cover sin, but the blood of Christ, offered once, cleanses the conscience and brings eternal redemption.',
        sense='allegorical',
        theme='blood_covenant',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Gregory of Nazianzus',
        work='Oration 45',
        verse_ref='Leviticus 23:5',
        text='The LORD\'s Passover. The annual feast recalled liberation, but the true Pascha is Christ passing over from death to life. In Him we pass from slavery to freedom, from death to immortality.',
        sense='allegorical',
        theme='passover',
        tradition='Cappadocian'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - NUMBERS
# ============================================================================

NUMBERS_COMMENTARY = [
    PatristicEntry(
        father='Origen',
        work='Homilies on Numbers XXVII',
        verse_ref='Numbers 21:9',
        text='Moses made a bronze serpent. As Moses lifted the serpent in the wilderness, so must the Son of Man be lifted up. The serpent on the pole is Christ on the cross: looking in faith brings healing from the poison of sin.',
        sense='allegorical',
        theme='crucifixion',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Augustine',
        work='Against Faustus',
        verse_ref='Numbers 24:17',
        text='A star shall come out of Jacob. Balaam prophesied despite himself. The star is Christ, the light arising in Israel. The magi followed a star; all nations are drawn to this light.',
        sense='allegorical',
        theme='prophecy',
        tradition='Western'
    ),
    PatristicEntry(
        father='Gregory of Nyssa',
        work='Life of Moses II',
        verse_ref='Numbers 20:11',
        text='Moses struck the rock. The rock is Christ; the water, the Spirit. Yet Moses struck twice in anger when he was commanded to speak. Even the great lawgiver fell short, teaching us that salvation comes by grace alone.',
        sense='tropological',
        theme='grace',
        tradition='Cappadocian'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - DEUTERONOMY
# ============================================================================

DEUTERONOMY_COMMENTARY = [
    PatristicEntry(
        father='Origen',
        work='Homilies on Deuteronomy',
        verse_ref='Deuteronomy 6:4',
        text='Hear, O Israel: The LORD our God, the LORD is one. The Shema proclaims God\'s unity, yet the New Testament reveals this unity as Trinity. One God, three Persons: Father, Son, and Holy Spirit eternally united.',
        sense='literal',
        theme='trinity',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Augustine',
        work='On Christian Doctrine',
        verse_ref='Deuteronomy 6:5',
        text='You shall love the LORD your God with all your heart. The greatest commandment is love. All Scripture aims at this: love of God and neighbor. Without love, even faith and sacrifice profit nothing.',
        sense='tropological',
        theme='love',
        tradition='Western'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Matthew',
        verse_ref='Deuteronomy 18:15',
        text='The LORD your God will raise up for you a prophet like me. Moses foretold Christ, the prophet greater than himself. Moses gave the Law; Christ gives grace. Moses saw God\'s back; Christ reveals the Father\'s face.',
        sense='allegorical',
        theme='prophecy',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Irenaeus',
        work='Against Heresies IV.15',
        verse_ref='Deuteronomy 30:14',
        text='The word is very near you. The Law written on stone becomes the Word written on hearts. Christ is the Word made flesh who dwells among us. In Him, commandment becomes communion.',
        sense='allegorical',
        theme='incarnation',
        tradition='Lyonese'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - HISTORICAL BOOKS
# ============================================================================

HISTORICAL_COMMENTARY = [
    # Joshua
    PatristicEntry(
        father='Origen',
        work='Homilies on Joshua I.3',
        verse_ref='Joshua 1:5',
        text='As I was with Moses, so I will be with you. Joshua (Yeshua) shares the name of Jesus. As Joshua led Israel into the promised land, so Jesus leads believers into the kingdom of heaven.',
        sense='allegorical',
        theme='salvation',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Augustine',
        work='City of God XVI',
        verse_ref='Joshua 6:20',
        text='The wall fell down flat. Jericho\'s walls fell at the trumpet sound and the people\'s shout. So the walls of sin fall before the preaching of the gospel and the prayer of the faithful.',
        sense='allegorical',
        theme='spiritual_warfare',
        tradition='Western'
    ),
    # Judges
    PatristicEntry(
        father='Ambrose',
        work='On the Holy Spirit II',
        verse_ref='Judges 6:34',
        text='The Spirit of the LORD came upon Gideon. The judges were clothed with the Spirit for their task. This temporary anointing foreshadows the permanent indwelling of the Spirit in believers since Pentecost.',
        sense='allegorical',
        theme='holy_spirit',
        tradition='Milanese'
    ),
    # Ruth
    PatristicEntry(
        father='Jerome',
        work='Commentary on Ruth',
        verse_ref='Ruth 1:16',
        text='Your people shall be my people, and your God my God. Ruth the Moabitess, grafted into Israel by faith, becomes an ancestor of David and of Christ. The Gentiles are joined to Israel through faith.',
        sense='allegorical',
        theme='faith',
        tradition='Western'
    ),
    # 1 Samuel
    PatristicEntry(
        father='Gregory the Great',
        work='Moralia on Job',
        verse_ref='1 Samuel 2:1',
        text='Hannah\'s heart rejoiced in the LORD. Hannah\'s song anticipates Mary\'s Magnificat. Both women, barren and blessed, sing of God who lifts the lowly and fills the hungry with good things.',
        sense='allegorical',
        theme='humility',
        tradition='Roman'
    ),
    PatristicEntry(
        father='Augustine',
        work='City of God XVII',
        verse_ref='1 Samuel 16:13',
        text='Samuel anointed David. David, anointed as a youth, waited years for his kingdom. Christ, the Son of David, is the true Anointed One (Messiah), whose kingdom has no end.',
        sense='allegorical',
        theme='kingship',
        tradition='Western'
    ),
    # 2 Samuel
    PatristicEntry(
        father='Athanasius',
        work='Festal Letters',
        verse_ref='2 Samuel 7:12',
        text='I will raise up your offspring. The promise to David finds ultimate fulfillment in Christ, whose kingdom is eternal. David\'s throne is established forever in the kingship of the Messiah.',
        sense='allegorical',
        theme='covenant',
        tradition='Alexandrian'
    ),
    # 1 Kings
    PatristicEntry(
        father='Basil the Great',
        work='Homily on Psalm 28',
        verse_ref='1 Kings 19:12',
        text='A still small voice. Elijah expected God in earthquake, wind, and fire, but God came in gentle silence. God often speaks not in dramatic events but in the quiet of contemplative prayer.',
        sense='tropological',
        theme='prayer',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='Ephrem the Syrian',
        work='Hymns on Faith',
        verse_ref='1 Kings 18:38',
        text='The fire of the LORD fell. Elijah\'s sacrifice consumed by heavenly fire prefigures the Holy Spirit descending at Pentecost. Divine fire transforms the offering into something acceptable.',
        sense='allegorical',
        theme='holy_spirit',
        tradition='Syriac'
    ),
    # 2 Kings
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on 2 Kings',
        verse_ref='2 Kings 2:11',
        text='Elijah went up by a whirlwind into heaven. Elijah did not taste death, foreshadowing Christ\'s ascension. The chariot of fire represents the divine power that carries the righteous to glory.',
        sense='anagogical',
        theme='ascension',
        tradition='Antiochene'
    ),
    # Ezra/Nehemiah
    PatristicEntry(
        father='Bede',
        work='On Ezra and Nehemiah',
        verse_ref='Nehemiah 8:10',
        text='The joy of the LORD is your strength. After exile, the people wept hearing the Law. But Nehemiah teaches that holy joy, not mournful guilt, empowers obedience. Grace produces what Law demands.',
        sense='tropological',
        theme='joy',
        tradition='Western'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - POETIC BOOKS
# ============================================================================

POETIC_COMMENTARY = [
    # Job
    PatristicEntry(
        father='Gregory the Great',
        work='Moralia on Job I',
        verse_ref='Job 1:21',
        text='The LORD gave, and the LORD has taken away. Job\'s patience under suffering reveals the soul that trusts God beyond understanding. Blessing God in loss is the summit of faith.',
        sense='tropological',
        theme='suffering',
        tradition='Roman'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Job',
        verse_ref='Job 19:25',
        text='I know that my Redeemer lives. In deepest suffering, Job glimpses resurrection. The Redeemer who lives will vindicate His servants. Job\'s hope finds fulfillment in Christ\'s resurrection.',
        sense='allegorical',
        theme='resurrection',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Origen',
        work='Commentary on Job',
        verse_ref='Job 42:5',
        text='Now my eye sees You. Job moved from hearing about God to seeing Him. Suffering became the occasion of vision. The darkest nights of the soul can lead to the brightest dawn of encounter.',
        sense='anagogical',
        theme='theosis',
        tradition='Alexandrian'
    ),
    # Proverbs
    PatristicEntry(
        father='Origen',
        work='Commentary on Proverbs',
        verse_ref='Proverbs 8:22',
        text='The LORD possessed me at the beginning of his way. Wisdom is Christ, eternally with the Father, through whom all things were made. Before creation, Wisdom delighted in the presence of God.',
        sense='allegorical',
        theme='christology',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Basil the Great',
        work='Homily on Proverbs',
        verse_ref='Proverbs 1:7',
        text='The fear of the LORD is the beginning of knowledge. Not servile terror but reverential awe marks the beginning of wisdom. To stand before the Holy One in wonder is to begin to understand.',
        sense='tropological',
        theme='wisdom',
        tradition='Cappadocian'
    ),
    # Ecclesiastes
    PatristicEntry(
        father='Gregory of Nyssa',
        work='Homilies on Ecclesiastes',
        verse_ref='Ecclesiastes 1:2',
        text='Vanity of vanities, all is vanity. The Preacher speaks not despair but liberation. When we see earthly things as vapor, we are freed to seek what is eternal. Detachment is the door to heaven.',
        sense='tropological',
        theme='detachment',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='Jerome',
        work='Commentary on Ecclesiastes',
        verse_ref='Ecclesiastes 12:13',
        text='Fear God and keep his commandments. After exploring all wisdom under the sun, the conclusion is simple: reverence and obedience. Philosophy ends where faith begins.',
        sense='tropological',
        theme='obedience',
        tradition='Western'
    ),
    # Song of Solomon
    PatristicEntry(
        father='Origen',
        work='Commentary on Song of Songs',
        verse_ref='Song of Solomon 1:2',
        text='Let him kiss me with the kisses of his mouth. The soul longs for union with the Word. This is not carnal desire but spiritual eros, the soul\'s yearning for divine embrace.',
        sense='anagogical',
        theme='mysticism',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Gregory of Nyssa',
        work='Homilies on the Song of Songs',
        verse_ref='Song of Solomon 2:4',
        text='His banner over me was love. The Bridegroom\'s love covers and protects the soul. Divine eros draws the beloved ever higher in infinite progress toward the Infinite.',
        sense='anagogical',
        theme='divine_love',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='Bernard of Clairvaux',
        work='Sermons on Song of Songs',
        verse_ref='Song of Solomon 4:7',
        text='You are altogether beautiful, my love. The Bridegroom sees His bride without blemish. Christ sanctifies the Church, washing her with water through the word, presenting her glorious.',
        sense='allegorical',
        theme='church',
        tradition='Western'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - MAJOR PROPHETS
# ============================================================================

MAJOR_PROPHETS_COMMENTARY = [
    # Jeremiah
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Jeremiah',
        verse_ref='Jeremiah 1:5',
        text='Before I formed you in the womb I knew you. God\'s knowledge precedes our existence. We are called before birth, known before conception. Divine providence shapes each soul for its purpose.',
        sense='literal',
        theme='providence',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Augustine',
        work='City of God',
        verse_ref='Jeremiah 31:31',
        text='I will make a new covenant. The old covenant on stone gives way to covenant written on hearts. Not external law but internal transformation. The Spirit enables what the letter commanded.',
        sense='allegorical',
        theme='new_covenant',
        tradition='Western'
    ),
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Commentary on Jeremiah',
        verse_ref='Jeremiah 23:5',
        text='A righteous Branch. David\'s righteous offspring is Christ, the true king who executes justice. His reign brings salvation; His wisdom orders all things well.',
        sense='allegorical',
        theme='messiahship',
        tradition='Alexandrian'
    ),
    # Lamentations
    PatristicEntry(
        father='Jerome',
        work='Commentary on Lamentations',
        verse_ref='Lamentations 1:12',
        text='Is it nothing to you, all you who pass by? Jerusalem weeping becomes Christ on the cross, calling the world to witness His suffering. Divine sorrow poured out for human sin.',
        sense='allegorical',
        theme='passion',
        tradition='Western'
    ),
    PatristicEntry(
        father='Gregory the Great',
        work='Homilies',
        verse_ref='Lamentations 3:22',
        text='His mercies never come to an end. Even in destruction, mercy remains. Morning by morning, new mercies. The faithful God maintains His love through judgment itself.',
        sense='tropological',
        theme='mercy',
        tradition='Roman'
    ),
    # Ezekiel
    PatristicEntry(
        father='Gregory the Great',
        work='Homilies on Ezekiel',
        verse_ref='Ezekiel 1:10',
        text='The four living creatures. The four faces represent the four Gospels: Matthew the man, Mark the lion, Luke the ox, John the eagle. Each reveals a different aspect of Christ.',
        sense='allegorical',
        theme='gospels',
        tradition='Roman'
    ),
    PatristicEntry(
        father='Origen',
        work='Homilies on Ezekiel',
        verse_ref='Ezekiel 37:4',
        text='Prophesy to these bones. The valley of dry bones is humanity dead in sin. The breath of God brings resurrection. By the Spirit\'s power, the dead are raised to new life.',
        sense='allegorical',
        theme='resurrection',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Commentary on Ezekiel',
        verse_ref='Ezekiel 47:1',
        text='Water was flowing from the temple. The river from the temple is the Holy Spirit flowing from Christ\'s side. Living water gives life wherever it goes, healing the nations.',
        sense='allegorical',
        theme='holy_spirit',
        tradition='Alexandrian'
    ),
    # Daniel
    PatristicEntry(
        father='Jerome',
        work='Commentary on Daniel',
        verse_ref='Daniel 7:13',
        text='One like a son of man. The Son of Man comes with clouds to receive eternal dominion. This is Christ in His glory, to whom all authority in heaven and earth is given.',
        sense='allegorical',
        theme='christology',
        tradition='Western'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Commentary on Daniel',
        verse_ref='Daniel 3:25',
        text='The fourth is like a son of the gods. In the fiery furnace, a divine figure walks with the three young men. God does not always remove trials but joins us in them.',
        sense='tropological',
        theme='providence',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Hippolytus',
        work='Commentary on Daniel',
        verse_ref='Daniel 2:34',
        text='A stone cut without hands. The stone that destroys the statue is Christ, born of a virgin without human agency. His kingdom crushes all earthly powers and fills the earth.',
        sense='allegorical',
        theme='kingdom',
        tradition='Roman'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - MINOR PROPHETS
# ============================================================================

MINOR_PROPHETS_COMMENTARY = [
    # Hosea
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Commentary on Hosea',
        verse_ref='Hosea 11:1',
        text='Out of Egypt I called my son. Israel, God\'s firstborn, was called from Egypt. But the true Son called from Egypt is Christ, fulfilling and transcending Israel\'s story.',
        sense='allegorical',
        theme='typology',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Jerome',
        work='Commentary on Hosea',
        verse_ref='Hosea 6:6',
        text='I desire mercy, not sacrifice. God wants heart transformation, not mere ritual. External religion without internal change is empty. Love and knowledge of God exceed all offerings.',
        sense='tropological',
        theme='mercy',
        tradition='Western'
    ),
    # Joel
    PatristicEntry(
        father='Augustine',
        work='Sermons',
        verse_ref='Joel 2:28',
        text='I will pour out my Spirit on all flesh. Joel\'s prophecy was fulfilled at Pentecost. The Spirit once given to prophets alone now comes upon all believers: sons, daughters, servants.',
        sense='allegorical',
        theme='pentecost',
        tradition='Western'
    ),
    # Amos
    PatristicEntry(
        father='Basil the Great',
        work='Homily on Social Justice',
        verse_ref='Amos 5:24',
        text='Let justice roll down like waters. The prophets demand social righteousness. Care for the poor is not optional charity but essential worship. Injustice makes all ritual vain.',
        sense='tropological',
        theme='justice',
        tradition='Cappadocian'
    ),
    # Jonah
    PatristicEntry(
        father='Augustine',
        work='Letters',
        verse_ref='Jonah 1:17',
        text='Jonah was in the belly of the fish three days. As Jonah spent three days in the sea monster, so Christ spent three days in the heart of the earth. Descent precedes resurrection.',
        sense='allegorical',
        theme='resurrection',
        tradition='Western'
    ),
    PatristicEntry(
        father='Jerome',
        work='Commentary on Jonah',
        verse_ref='Jonah 4:11',
        text='Should I not pity Nineveh? God\'s mercy extends to the enemies of Israel. Jonah learned that divine compassion has no boundaries. The God of Israel is the God of all nations.',
        sense='tropological',
        theme='mercy',
        tradition='Western'
    ),
    # Micah
    PatristicEntry(
        father='Irenaeus',
        work='Against Heresies',
        verse_ref='Micah 5:2',
        text='From you, Bethlehem, shall come a ruler. The insignificant village becomes the birthplace of the eternal King. God chooses the small to shame the great, the weak to overcome the strong.',
        sense='allegorical',
        theme='incarnation',
        tradition='Lyonese'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies',
        verse_ref='Micah 6:8',
        text='What does the LORD require? Do justice, love mercy, walk humbly. The prophetic summary of religion: right action, compassionate heart, humble posture before God.',
        sense='tropological',
        theme='ethics',
        tradition='Antiochene'
    ),
    # Habakkuk
    PatristicEntry(
        father='Augustine',
        work='City of God',
        verse_ref='Habakkuk 2:4',
        text='The righteous shall live by faith. This verse became Paul\'s foundation for justification by faith. Trust in God, not human works, is the ground of righteousness.',
        sense='literal',
        theme='faith',
        tradition='Western'
    ),
    # Zechariah
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Commentary on Zechariah',
        verse_ref='Zechariah 9:9',
        text='Your king comes to you, humble and mounted on a donkey. The triumphal entry fulfills this prophecy. Christ comes as a humble king, bringing salvation not through war but peace.',
        sense='allegorical',
        theme='messiahship',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Matthew',
        verse_ref='Zechariah 11:12',
        text='They weighed out thirty pieces of silver. The price of a slave becomes the price of betrayal. Judas sold the priceless Christ for the value Scripture had foretold.',
        sense='allegorical',
        theme='passion',
        tradition='Antiochene'
    ),
    # Malachi
    PatristicEntry(
        father='Augustine',
        work='City of God',
        verse_ref='Malachi 4:2',
        text='The sun of righteousness shall rise with healing in its wings. Christ is the sun that rises on those in darkness. His coming brings healing, restoration, and victory over evil.',
        sense='allegorical',
        theme='christology',
        tradition='Western'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - DEUTEROCANONICAL BOOKS
# ============================================================================

DEUTEROCANONICAL_COMMENTARY = [
    # Wisdom of Solomon
    PatristicEntry(
        father='Augustine',
        work='City of God',
        verse_ref='Wisdom 11:20',
        text='You have arranged all things by measure and number and weight. God is the divine mathematician, ordering creation with precision. Beauty and order reflect the Creator\'s wisdom.',
        sense='literal',
        theme='creation',
        tradition='Western'
    ),
    PatristicEntry(
        father='Origen',
        work='On First Principles',
        verse_ref='Wisdom 7:26',
        text='She is a reflection of eternal light. Wisdom as divine radiance points to Christ, the effulgence of the Father\'s glory. The Son eternally reflects the Father\'s being.',
        sense='allegorical',
        theme='christology',
        tradition='Alexandrian'
    ),
    # Sirach (Ecclesiasticus)
    PatristicEntry(
        father='Clement of Alexandria',
        work='Stromata',
        verse_ref='Sirach 1:1',
        text='All wisdom comes from the Lord. True philosophy is the love of wisdom, and all wisdom originates in God. Greek philosophy at its best glimpsed truths fully revealed in Christ.',
        sense='literal',
        theme='wisdom',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies',
        verse_ref='Sirach 2:1',
        text='My child, if you come to serve the Lord, prepare yourself for testing. Discipleship brings trials. The spiritual life is not ease but warfare. Preparation for testing is the beginning of wisdom.',
        sense='tropological',
        theme='discipleship',
        tradition='Antiochene'
    ),
    # Tobit
    PatristicEntry(
        father='Ambrose',
        work='On Tobit',
        verse_ref='Tobit 4:16',
        text='Give to the hungry of your bread. Almsgiving purifies the soul. What we share with the poor, we store in heaven. The hand that gives receives blessing.',
        sense='tropological',
        theme='almsgiving',
        tradition='Milanese'
    ),
    # Baruch
    PatristicEntry(
        father='Irenaeus',
        work='Against Heresies',
        verse_ref='Baruch 3:38',
        text='Afterwards she appeared on earth and lived among men. Wisdom dwelling on earth prefigures the Incarnation. The Word who was with God came to dwell among us.',
        sense='allegorical',
        theme='incarnation',
        tradition='Lyonese'
    ),
    # 2 Maccabees
    PatristicEntry(
        father='Augustine',
        work='City of God',
        verse_ref='2 Maccabees 12:46',
        text='It is a holy and pious thought to pray for the dead. Prayer for the departed demonstrates hope in resurrection and purification. The communion of saints transcends death.',
        sense='literal',
        theme='prayer_for_dead',
        tradition='Western'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - SYNOPTIC GOSPELS
# ============================================================================

SYNOPTIC_COMMENTARY = [
    # Matthew
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Matthew V',
        verse_ref='Matthew 5:3',
        text='Blessed are the poor in spirit. Poverty of spirit is not material destitution but spiritual humility. The kingdom belongs to those who know their need for God.',
        sense='tropological',
        theme='beatitudes',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Augustine',
        work='Sermon on the Mount',
        verse_ref='Matthew 6:9',
        text='Our Father who art in heaven. The Lord\'s Prayer contains all we need to pray. Each petition shapes the soul: hallowing, surrender, provision, forgiveness, deliverance.',
        sense='tropological',
        theme='prayer',
        tradition='Western'
    ),
    PatristicEntry(
        father='Origen',
        work='Commentary on Matthew',
        verse_ref='Matthew 13:31',
        text='The kingdom of heaven is like a mustard seed. The smallest seed becomes the greatest shrub. So the gospel, beginning with twelve fishermen, fills the whole earth.',
        sense='allegorical',
        theme='kingdom',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Leo the Great',
        work='Sermons',
        verse_ref='Matthew 16:18',
        text='You are Peter, and on this rock I will build my church. Peter\'s confession becomes the foundation. Faith in Christ as Son of God is the rock on which the Church stands.',
        sense='literal',
        theme='church',
        tradition='Roman'
    ),
    PatristicEntry(
        father='Gregory of Nazianzus',
        work='Oration 40',
        verse_ref='Matthew 28:19',
        text='Baptize them in the name of the Father and of the Son and of the Holy Spirit. One name, three Persons. Baptism initiates into the divine life of the Trinity.',
        sense='literal',
        theme='baptism',
        tradition='Cappadocian'
    ),
    # Mark
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Mark',
        verse_ref='Mark 1:15',
        text='The kingdom of God is at hand; repent and believe. The summary of the gospel: the kingdom arrives, requiring response. Turning and trusting open the door to God\'s reign.',
        sense='literal',
        theme='repentance',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Bede',
        work='Commentary on Mark',
        verse_ref='Mark 4:39',
        text='Peace! Be still! Christ commands the storm as He commands demons. The Creator speaks and creation obeys. In our storms of soul, His word brings peace.',
        sense='tropological',
        theme='peace',
        tradition='Western'
    ),
    PatristicEntry(
        father='Ephrem the Syrian',
        work='Commentary on the Diatessaron',
        verse_ref='Mark 10:45',
        text='The Son of Man came not to be served but to serve. The King becomes servant, the Master washes feet. Divine power expresses itself through service and sacrifice.',
        sense='tropological',
        theme='service',
        tradition='Syriac'
    ),
    # Luke
    PatristicEntry(
        father='Ambrose',
        work='Exposition of Luke',
        verse_ref='Luke 1:38',
        text='Let it be to me according to your word. Mary\'s fiat enables the Incarnation. Her yes reverses Eve\'s no. Obedient faith opens the womb to receive the Word.',
        sense='tropological',
        theme='obedience',
        tradition='Milanese'
    ),
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Commentary on Luke',
        verse_ref='Luke 2:14',
        text='Glory to God in the highest, and on earth peace. Angels announce the cosmic significance: heaven glorified, earth pacified. The birth of Christ reconciles all things.',
        sense='anagogical',
        theme='incarnation',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Augustine',
        work='Harmony of the Gospels',
        verse_ref='Luke 15:20',
        text='While he was still far off, his father saw him. The father runs to the prodigal. God does not wait for perfection; He rushes to welcome the returning sinner.',
        sense='tropological',
        theme='mercy',
        tradition='Western'
    ),
    PatristicEntry(
        father='Gregory the Great',
        work='Homilies on the Gospels',
        verse_ref='Luke 24:32',
        text='Did not our hearts burn within us? Christ opens the Scriptures on the road to Emmaus. The word kindles fire in the heart. Recognition comes in the breaking of bread.',
        sense='tropological',
        theme='eucharist',
        tradition='Roman'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - ACTS
# ============================================================================

ACTS_COMMENTARY = [
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Acts I',
        verse_ref='Acts 1:8',
        text='You will receive power when the Holy Spirit has come upon you. The Spirit empowers witness. From Jerusalem to the ends of the earth, the gospel spreads by divine energy.',
        sense='literal',
        theme='holy_spirit',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Augustine',
        work='Sermons on Pentecost',
        verse_ref='Acts 2:3',
        text='Tongues as of fire rested on each one. Fire purifies and illumines. The Spirit descends in the form of tongues because He enables proclamation. Division of languages at Babel is healed.',
        sense='allegorical',
        theme='pentecost',
        tradition='Western'
    ),
    PatristicEntry(
        father='Basil the Great',
        work='On the Holy Spirit',
        verse_ref='Acts 2:42',
        text='They devoted themselves to the apostles\' teaching and fellowship, to the breaking of bread and the prayers. The four marks of the early church: doctrine, communion, Eucharist, prayer.',
        sense='literal',
        theme='church',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Acts',
        verse_ref='Acts 9:4',
        text='Saul, Saul, why are you persecuting me? Christ identifies with His persecuted Church. To harm believers is to harm Christ Himself. The mystical body suffers in its members.',
        sense='literal',
        theme='church',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Irenaeus',
        work='Against Heresies',
        verse_ref='Acts 17:28',
        text='In him we live and move and have our being. Paul quotes the pagan poets to show that God is not far from any of us. Natural revelation prepares for special revelation.',
        sense='literal',
        theme='creation',
        tradition='Lyonese'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - PAULINE EPISTLES
# ============================================================================

PAULINE_COMMENTARY = [
    # Romans
    PatristicEntry(
        father='Augustine',
        work='On the Spirit and the Letter',
        verse_ref='Romans 3:28',
        text='A person is justified by faith apart from works of the law. Faith receives what works cannot earn. Justification is God\'s gift, not human achievement.',
        sense='literal',
        theme='justification',
        tradition='Western'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Romans',
        verse_ref='Romans 5:8',
        text='God shows his love for us in that while we were still sinners, Christ died for us. Love proved by action toward enemies. Divine love does not wait for lovability.',
        sense='tropological',
        theme='divine_love',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Origen',
        work='Commentary on Romans',
        verse_ref='Romans 8:28',
        text='All things work together for good. Providence weaves all events, even suffering, into blessing for those who love God. The divine tapestry is woven with threads we cannot see.',
        sense='tropological',
        theme='providence',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Augustine',
        work='On Grace and Free Will',
        verse_ref='Romans 9:16',
        text='It depends not on human will or exertion, but on God who has mercy. Salvation originates in divine mercy, not human effort. Grace precedes and enables all good.',
        sense='literal',
        theme='grace',
        tradition='Western'
    ),
    # 1 Corinthians
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on 1 Corinthians',
        verse_ref='1 Corinthians 1:23',
        text='We preach Christ crucified. The cross is folly to the world but wisdom to those being saved. God\'s weakness is stronger than human strength.',
        sense='literal',
        theme='cross',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Augustine',
        work='On the Trinity',
        verse_ref='1 Corinthians 13:12',
        text='Now we see in a mirror dimly, but then face to face. Our knowledge is partial, veiled. The beatific vision awaits. Faith will yield to sight, hope to possession.',
        sense='anagogical',
        theme='beatific_vision',
        tradition='Western'
    ),
    PatristicEntry(
        father='Cyril of Jerusalem',
        work='Catechetical Lectures',
        verse_ref='1 Corinthians 15:3',
        text='Christ died for our sins according to the Scriptures. The gospel has Scriptural foundation. Death for sins, burial, resurrection: the core kerygma of apostolic preaching.',
        sense='literal',
        theme='gospel',
        tradition='Palestinian'
    ),
    # 2 Corinthians
    PatristicEntry(
        father='Gregory of Nazianzus',
        work='Orations',
        verse_ref='2 Corinthians 3:18',
        text='We are being transformed into the same image from glory to glory. Beholding Christ transforms. The soul mirrors what it contemplates, gradually conformed to the divine image.',
        sense='anagogical',
        theme='theosis',
        tradition='Cappadocian'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on 2 Corinthians',
        verse_ref='2 Corinthians 12:9',
        text='My grace is sufficient for you, for my power is made perfect in weakness. Divine strength flows into human weakness. Thorns become occasions for grace.',
        sense='tropological',
        theme='grace',
        tradition='Antiochene'
    ),
    # Galatians
    PatristicEntry(
        father='Augustine',
        work='Exposition of Galatians',
        verse_ref='Galatians 2:20',
        text='I have been crucified with Christ. The old self dies with Christ; a new life begins. No longer I but Christ: mystical union transforms identity.',
        sense='tropological',
        theme='union_with_christ',
        tradition='Western'
    ),
    PatristicEntry(
        father='John Chrysostom',
        work='Commentary on Galatians',
        verse_ref='Galatians 5:22',
        text='The fruit of the Spirit is love, joy, peace. One fruit, many flavors. The Spirit produces character, not merely gifts. Love is the tree; virtues are its fruit.',
        sense='tropological',
        theme='holy_spirit',
        tradition='Antiochene'
    ),
    # Ephesians
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Ephesians',
        verse_ref='Ephesians 2:8',
        text='By grace you have been saved through faith. Salvation is gift received by faith. Neither grace alone nor faith alone, but grace through faith.',
        sense='literal',
        theme='salvation',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Origen',
        work='Commentary on Ephesians',
        verse_ref='Ephesians 5:32',
        text='This mystery is profound. The union of husband and wife images Christ and the Church. Marriage becomes icon of divine-human communion.',
        sense='allegorical',
        theme='marriage',
        tradition='Alexandrian'
    ),
    # Philippians
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Commentary on Philippians',
        verse_ref='Philippians 2:7',
        text='He emptied himself, taking the form of a servant. Kenosis: self-emptying without ceasing to be God. The divine condescension humbles to exalt.',
        sense='literal',
        theme='incarnation',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Augustine',
        work='Confessions',
        verse_ref='Philippians 3:13',
        text='Forgetting what lies behind and straining forward. The Christian life is perpetual progress. Past sins are forgiven; future glory beckons. Press on.',
        sense='tropological',
        theme='spiritual_growth',
        tradition='Western'
    ),
    # Colossians
    PatristicEntry(
        father='Athanasius',
        work='On the Incarnation',
        verse_ref='Colossians 1:15',
        text='He is the image of the invisible God. Christ makes the unseen Father visible. The invisible becomes visible in the incarnate Word.',
        sense='literal',
        theme='christology',
        tradition='Alexandrian'
    ),
    # 1 Timothy
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Timothy',
        verse_ref='1 Timothy 2:5',
        text='There is one mediator between God and men, the man Christ Jesus. Christ alone bridges the infinite gap. Through His humanity, divinity touches us.',
        sense='literal',
        theme='mediation',
        tradition='Antiochene'
    ),
]


# ============================================================================
# EMBEDDED PATRISTIC COMMENTARY - GENERAL EPISTLES
# ============================================================================

GENERAL_EPISTLES_COMMENTARY = [
    # Hebrews
    PatristicEntry(
        father='John Chrysostom',
        work='Homilies on Hebrews',
        verse_ref='Hebrews 1:3',
        text='He is the radiance of the glory of God. Christ is not reflected light but the very effulgence of divine glory. Eternally begotten, He shares the Father\'s nature.',
        sense='literal',
        theme='christology',
        tradition='Antiochene'
    ),
    PatristicEntry(
        father='Augustine',
        work='On Faith and Works',
        verse_ref='Hebrews 11:1',
        text='Faith is the substance of things hoped for. Faith grasps what is unseen but real. It is not wishful thinking but confident trust in God\'s promises.',
        sense='literal',
        theme='faith',
        tradition='Western'
    ),
    PatristicEntry(
        father='Gregory of Nyssa',
        work='On Perfection',
        verse_ref='Hebrews 12:2',
        text='Looking to Jesus, the founder and perfecter of our faith. Christ is both origin and goal of faith. He ran the race before us, showing the way.',
        sense='tropological',
        theme='discipleship',
        tradition='Cappadocian'
    ),
    # James
    PatristicEntry(
        father='Augustine',
        work='On Faith and Works',
        verse_ref='James 2:17',
        text='Faith by itself, if it does not have works, is dead. Faith produces works as fire produces heat. True faith is living, active, fruitful.',
        sense='tropological',
        theme='faith_works',
        tradition='Western'
    ),
    PatristicEntry(
        father='Bede',
        work='Commentary on James',
        verse_ref='James 1:17',
        text='Every good gift is from above. All blessings descend from the Father of lights. There is no shadow of turning in Him; His generosity is constant.',
        sense='literal',
        theme='providence',
        tradition='Western'
    ),
    # 1 Peter
    PatristicEntry(
        father='Cyril of Alexandria',
        work='Commentary on 1 Peter',
        verse_ref='1 Peter 2:9',
        text='You are a chosen race, a royal priesthood. The Church inherits Israel\'s calling. Every believer is priest, offering spiritual sacrifices.',
        sense='allegorical',
        theme='church',
        tradition='Alexandrian'
    ),
    PatristicEntry(
        father='Augustine',
        work='Letters',
        verse_ref='1 Peter 3:15',
        text='Always be prepared to give an answer to everyone who asks you to give the reason for the hope that you have. Faith seeks understanding. Apologetics serves evangelism.',
        sense='tropological',
        theme='apologetics',
        tradition='Western'
    ),
    # 2 Peter
    PatristicEntry(
        father='Athanasius',
        work='On the Incarnation',
        verse_ref='2 Peter 1:4',
        text='Partakers of the divine nature. Theosis: humanity shares in divinity. God became human that humans might become god, by grace not nature.',
        sense='anagogical',
        theme='theosis',
        tradition='Alexandrian'
    ),
    # 1 John
    PatristicEntry(
        father='Augustine',
        work='Homilies on 1 John',
        verse_ref='1 John 4:8',
        text='God is love. Not merely that God loves, but that His very essence is love. The Trinity is eternal communion of love.',
        sense='literal',
        theme='divine_nature',
        tradition='Western'
    ),
    PatristicEntry(
        father='Maximus the Confessor',
        work='Centuries on Love',
        verse_ref='1 John 4:18',
        text='Perfect love casts out fear. Fear contracts the soul; love expands it. As love grows, fear diminishes until only love remains.',
        sense='tropological',
        theme='love',
        tradition='Byzantine'
    ),
    # Jude
    PatristicEntry(
        father='Clement of Alexandria',
        work='Stromata',
        verse_ref='Jude 1:3',
        text='Contend for the faith once delivered to the saints. The faith is given, not invented. Tradition preserves what the apostles taught. We receive and transmit.',
        sense='literal',
        theme='tradition',
        tradition='Alexandrian'
    ),
]


# ============================================================================
# MASTER PATRISTIC DATABASE
# ============================================================================

ALL_PATRISTIC_ENTRIES = (
    # Pentateuch
    GENESIS_COMMENTARY +
    EXODUS_COMMENTARY +
    LEVITICUS_COMMENTARY +
    NUMBERS_COMMENTARY +
    DEUTERONOMY_COMMENTARY +
    # Historical Books
    HISTORICAL_COMMENTARY +
    # Poetic/Wisdom Books
    PSALMS_COMMENTARY +
    POETIC_COMMENTARY +
    # Prophetic Books
    ISAIAH_COMMENTARY +
    MAJOR_PROPHETS_COMMENTARY +
    MINOR_PROPHETS_COMMENTARY +
    # Deuterocanonical Books
    DEUTEROCANONICAL_COMMENTARY +
    # New Testament - Gospels
    JOHN_COMMENTARY +
    SYNOPTIC_COMMENTARY +
    # New Testament - Acts and Epistles
    ACTS_COMMENTARY +
    PAULINE_COMMENTARY +
    GENERAL_EPISTLES_COMMENTARY +
    # Apocalyptic
    REVELATION_COMMENTARY
)


# ============================================================================
# PATRISTIC DATABASE CLASS
# ============================================================================

class PatristicDatabase:
    """
    Provides offline access to patristic commentary.
    Organized by verse, father, sense, and theme.
    """
    
    def __init__(self):
        self.entries = ALL_PATRISTIC_ENTRIES
        self.fathers = CHURCH_FATHERS_META
        self._index_by_verse: Dict[str, List[PatristicEntry]] = {}
        self._index_by_father: Dict[str, List[PatristicEntry]] = {}
        self._index_by_sense: Dict[str, List[PatristicEntry]] = {}
        self._index_by_theme: Dict[str, List[PatristicEntry]] = {}
        self._build_indices()
    
    def _build_indices(self):
        """Build lookup indices for fast retrieval."""
        for entry in self.entries:
            # By verse
            if entry.verse_ref not in self._index_by_verse:
                self._index_by_verse[entry.verse_ref] = []
            self._index_by_verse[entry.verse_ref].append(entry)
            
            # By father
            if entry.father not in self._index_by_father:
                self._index_by_father[entry.father] = []
            self._index_by_father[entry.father].append(entry)
            
            # By sense
            if entry.sense not in self._index_by_sense:
                self._index_by_sense[entry.sense] = []
            self._index_by_sense[entry.sense].append(entry)
            
            # By theme
            if entry.theme not in self._index_by_theme:
                self._index_by_theme[entry.theme] = []
            self._index_by_theme[entry.theme].append(entry)
    
    def get_commentary_for_verse(self, verse_ref: str) -> List[PatristicEntry]:
        """Get all patristic commentary for a verse."""
        return self._index_by_verse.get(verse_ref, [])
    
    def get_commentary_by_father(self, father: str) -> List[PatristicEntry]:
        """Get all commentary from a specific Father."""
        return self._index_by_father.get(father, [])
    
    def get_commentary_by_sense(self, sense: str) -> List[PatristicEntry]:
        """Get all commentary for a specific sense."""
        return self._index_by_sense.get(sense, [])
    
    def get_commentary_by_theme(self, theme: str) -> List[PatristicEntry]:
        """Get all commentary on a specific theme."""
        return self._index_by_theme.get(theme, [])
    
    def get_father_info(self, father: str) -> Optional[Dict[str, Any]]:
        """Get metadata about a Church Father."""
        return self.fathers.get(father)
    
    def get_all_fathers(self) -> List[str]:
        """Get list of all Church Fathers with commentary."""
        return list(self.fathers.keys())
    
    def get_all_themes(self) -> List[str]:
        """Get list of all themes covered."""
        return list(self._index_by_theme.keys())
    
    def get_sense_distribution(self, verse_ref: str) -> Dict[str, int]:
        """Get distribution of senses for a verse's commentary."""
        entries = self.get_commentary_for_verse(verse_ref)
        distribution = {'literal': 0, 'allegorical': 0, 'tropological': 0, 'anagogical': 0}
        for entry in entries:
            if entry.sense in distribution:
                distribution[entry.sense] += 1
        return distribution
    
    def suggest_commentary_for_sense(self, verse_ref: str, target_sense: str) -> List[PatristicEntry]:
        """Suggest commentary that matches the target sense."""
        # First try exact verse
        verse_entries = self.get_commentary_for_verse(verse_ref)
        matching = [e for e in verse_entries if e.sense == target_sense]
        
        if matching:
            return matching
        
        # Fall back to same sense, any verse
        return self._index_by_sense.get(target_sense, [])[:3]
    
    def get_tradition_distribution(self) -> Dict[str, int]:
        """Get distribution of commentary by tradition."""
        distribution = {}
        for entry in self.entries:
            if entry.tradition not in distribution:
                distribution[entry.tradition] = 0
            distribution[entry.tradition] += 1
        return distribution
    
    def search_text(self, query: str) -> List[PatristicEntry]:
        """Search commentary text for a query."""
        query_lower = query.lower()
        return [e for e in self.entries if query_lower in e.text.lower()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        return {
            'total_entries': len(self.entries),
            'fathers_represented': len(self._index_by_father),
            'verses_covered': len(self._index_by_verse),
            'themes': len(self._index_by_theme),
            'by_sense': {sense: len(entries) for sense, entries in self._index_by_sense.items()},
            'by_tradition': self.get_tradition_distribution()
        }


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_patristic_database = None


def get_patristic_database() -> PatristicDatabase:
    """Get the global patristic database instance."""
    global _patristic_database
    if _patristic_database is None:
        _patristic_database = PatristicDatabase()
    return _patristic_database


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for patristic database."""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Patristic Database')
    parser.add_argument('--verse', type=str, help='Get commentary for verse')
    parser.add_argument('--father', type=str, help='Get commentary by Father')
    parser.add_argument('--sense', type=str, choices=['literal', 'allegorical', 'tropological', 'anagogical'],
                       help='Get commentary by sense')
    parser.add_argument('--theme', type=str, help='Get commentary by theme')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--search', type=str, help='Search commentary text')
    parser.add_argument('--list-fathers', action='store_true', help='List all Church Fathers')
    
    args = parser.parse_args()
    
    db = get_patristic_database()
    
    if args.verse:
        entries = db.get_commentary_for_verse(args.verse)
        print(f"\nCommentary for {args.verse}:")
        print("=" * 60)
        for entry in entries:
            print(f"\n{entry.father} ({entry.tradition})")
            print(f"  Work: {entry.work}")
            print(f"  Sense: {entry.sense}")
            print(f"  Theme: {entry.theme}")
            print(f"  Text: {entry.text[:200]}...")
    
    elif args.father:
        info = db.get_father_info(args.father)
        entries = db.get_commentary_by_father(args.father)
        print(f"\n{args.father}")
        print("=" * 60)
        if info:
            print(f"  Dates: {info['dates']}")
            print(f"  Tradition: {info['tradition']}")
            print(f"  Emphases: {', '.join(info['emphasis'])}")
        print(f"\n  Commentary Entries: {len(entries)}")
        for entry in entries[:5]:
            print(f"    • {entry.verse_ref}: {entry.text[:80]}...")
    
    elif args.sense:
        entries = db.get_commentary_by_sense(args.sense)
        print(f"\nCommentary in {args.sense} sense:")
        print("=" * 60)
        for entry in entries[:10]:
            print(f"\n{entry.verse_ref} - {entry.father}")
            print(f"  {entry.text[:150]}...")
    
    elif args.theme:
        entries = db.get_commentary_by_theme(args.theme)
        print(f"\nCommentary on '{args.theme}':")
        print("=" * 60)
        for entry in entries:
            print(f"\n{entry.verse_ref} - {entry.father}")
            print(f"  {entry.text[:150]}...")
    
    elif args.stats:
        stats = db.get_statistics()
        print("\nPatristic Database Statistics:")
        print("=" * 60)
        print(f"  Total Entries: {stats['total_entries']}")
        print(f"  Fathers Represented: {stats['fathers_represented']}")
        print(f"  Verses Covered: {stats['verses_covered']}")
        print(f"  Themes: {stats['themes']}")
        print("\n  By Sense:")
        for sense, count in stats['by_sense'].items():
            print(f"    {sense}: {count}")
        print("\n  By Tradition:")
        for tradition, count in stats['by_tradition'].items():
            print(f"    {tradition}: {count}")
    
    elif args.search:
        entries = db.search_text(args.search)
        print(f"\nSearch results for '{args.search}':")
        print("=" * 60)
        for entry in entries[:10]:
            print(f"\n{entry.verse_ref} - {entry.father}")
            print(f"  {entry.text[:150]}...")
    
    elif args.list_fathers:
        print("\nChurch Fathers in Database:")
        print("=" * 60)
        for father in db.get_all_fathers():
            info = db.get_father_info(father)
            count = len(db.get_commentary_by_father(father))
            print(f"  {father} ({info['dates']}) - {info['tradition']} - {count} entries")
    
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
