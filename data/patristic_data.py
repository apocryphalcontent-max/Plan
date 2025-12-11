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
# MASTER PATRISTIC DATABASE
# ============================================================================

ALL_PATRISTIC_ENTRIES = (
    GENESIS_COMMENTARY +
    JOHN_COMMENTARY +
    PSALMS_COMMENTARY +
    ISAIAH_COMMENTARY +
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
