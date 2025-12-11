#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Patristic Integration System
Integration with Church Fathers' commentary and patristic sources
"""

import sys
import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config
from scripts.database import get_db, DatabaseManager

logger = logging.getLogger(__name__)


# ============================================================================
# CHURCH FATHERS DATABASE
# ============================================================================

CHURCH_FATHERS = {
    'early': [
        {'name': 'Clement of Rome', 'dates': '35-99', 'tradition': 'Roman'},
        {'name': 'Ignatius of Antioch', 'dates': '35-108', 'tradition': 'Antiochene'},
        {'name': 'Polycarp', 'dates': '69-155', 'tradition': 'Asian'},
        {'name': 'Justin Martyr', 'dates': '100-165', 'tradition': 'Apologetic'},
        {'name': 'Irenaeus', 'dates': '130-202', 'tradition': 'Lyonese'},
        {'name': 'Clement of Alexandria', 'dates': '150-215', 'tradition': 'Alexandrian'},
        {'name': 'Tertullian', 'dates': '155-220', 'tradition': 'African'},
        {'name': 'Origen', 'dates': '185-254', 'tradition': 'Alexandrian'},
        {'name': 'Cyprian', 'dates': '200-258', 'tradition': 'African'},
    ],
    'nicene': [
        {'name': 'Athanasius', 'dates': '296-373', 'tradition': 'Alexandrian'},
        {'name': 'Basil the Great', 'dates': '330-379', 'tradition': 'Cappadocian'},
        {'name': 'Gregory of Nazianzus', 'dates': '329-390', 'tradition': 'Cappadocian'},
        {'name': 'Gregory of Nyssa', 'dates': '335-395', 'tradition': 'Cappadocian'},
        {'name': 'John Chrysostom', 'dates': '349-407', 'tradition': 'Antiochene'},
        {'name': 'Ambrose', 'dates': '340-397', 'tradition': 'Milanese'},
        {'name': 'Jerome', 'dates': '347-420', 'tradition': 'Western'},
        {'name': 'Augustine', 'dates': '354-430', 'tradition': 'African'},
        {'name': 'Cyril of Alexandria', 'dates': '376-444', 'tradition': 'Alexandrian'},
    ],
    'post_nicene': [
        {'name': 'Leo the Great', 'dates': '400-461', 'tradition': 'Roman'},
        {'name': 'Maximus the Confessor', 'dates': '580-662', 'tradition': 'Byzantine'},
        {'name': 'John of Damascus', 'dates': '675-749', 'tradition': 'Byzantine'},
        {'name': 'Gregory Palamas', 'dates': '1296-1359', 'tradition': 'Hesychast'},
    ],
    'desert': [
        {'name': 'Anthony the Great', 'dates': '251-356', 'tradition': 'Egyptian'},
        {'name': 'Macarius the Great', 'dates': '300-391', 'tradition': 'Egyptian'},
        {'name': 'Evagrius Ponticus', 'dates': '345-399', 'tradition': 'Egyptian'},
        {'name': 'John Cassian', 'dates': '360-435', 'tradition': 'Gallic'},
        {'name': 'Isaac of Nineveh', 'dates': '613-700', 'tradition': 'Syriac'},
    ],
    'syriac': [
        {'name': 'Ephrem the Syrian', 'dates': '306-373', 'tradition': 'Syriac'},
        {'name': 'Jacob of Serugh', 'dates': '451-521', 'tradition': 'Syriac'},
    ]
}


# ============================================================================
# PATRISTIC THEMES AND EMPHASES
# ============================================================================

FATHER_EMPHASES = {
    'Origen': ['allegory', 'spiritual_sense', 'platonism', 'soul_ascent'],
    'John Chrysostom': ['literal', 'moral', 'homiletical', 'practical'],
    'Augustine': ['grace', 'predestination', 'trinity', 'city_of_god', 'love'],
    'Athanasius': ['incarnation', 'theosis', 'anti_arian', 'christology'],
    'Basil the Great': ['creation', 'holy_spirit', 'monasticism', 'liturgy'],
    'Gregory of Nazianzus': ['trinity', 'christology', 'poetry', 'theology'],
    'Gregory of Nyssa': ['mysticism', 'apophatic', 'soul_journey', 'infinite_progress'],
    'Cyril of Alexandria': ['christology', 'theotokos', 'eucharist', 'unity'],
    'Maximus the Confessor': ['cosmic_liturgy', 'theosis', 'will', 'logoi'],
    'John of Damascus': ['icons', 'systematic', 'synthesis', 'orthodox_faith'],
    'Irenaeus': ['recapitulation', 'anti_gnostic', 'tradition', 'apostolic'],
    'Ephrem the Syrian': ['poetry', 'typology', 'symbols', 'paradise'],
    'Gregory Palamas': ['essence_energies', 'hesychasm', 'theosis', 'uncreated_light'],
    'Jerome': ['translation', 'hebrew', 'literal', 'monasticism'],
    'Ambrose': ['allegory', 'ethics', 'hymns', 'church_state'],
    'Leo the Great': ['christology', 'papacy', 'tome', 'two_natures'],
    'Isaac of Nineveh': ['mercy', 'humility', 'tears', 'solitude'],
}


# ============================================================================
# PATRISTIC SOURCE MANAGER - OFFLINE-FIRST ARCHITECTURE
# ============================================================================

class PatristicSourceManager:
    """
    Manage patristic commentary sources with offline-first architecture.
    Uses embedded patristic data first, falls back to database when needed.
    """
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self._offline_db = None
    
    @property
    def offline_db(self):
        """Lazy-load offline patristic database."""
        if self._offline_db is None:
            try:
                from data.patristic_data import get_patristic_database
                self._offline_db = get_patristic_database()
            except ImportError:
                logger.debug("Offline patristic database not available")
                self._offline_db = False
        return self._offline_db if self._offline_db else None
    
    def get_all_fathers(self) -> Dict[str, List[Dict]]:
        """Get all Church Fathers organized by era"""
        return CHURCH_FATHERS
    
    def get_father_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific Father"""
        # Try offline database first
        if self.offline_db:
            info = self.offline_db.get_father_info(name)
            if info:
                return info
        
        # Fall back to local constant
        for era, fathers in CHURCH_FATHERS.items():
            for father in fathers:
                if father['name'].lower() == name.lower():
                    return {
                        **father,
                        'era': era,
                        'emphases': FATHER_EMPHASES.get(father['name'], [])
                    }
        return None
    
    def find_fathers_by_emphasis(self, emphasis: str) -> List[Dict]:
        """Find Fathers who emphasize a particular theme"""
        results = []
        for name, emphases in FATHER_EMPHASES.items():
            if emphasis.lower() in [e.lower() for e in emphases]:
                info = self.get_father_info(name)
                if info:
                    results.append(info)
        return results
    
    def get_commentary_for_verse(self, verse_ref: str) -> List[Dict[str, Any]]:
        """
        Get patristic commentary for a verse.
        Uses offline data first, then database.
        """
        results = []
        
        # Layer 1: Offline embedded commentary
        if self.offline_db:
            entries = self.offline_db.get_commentary_for_verse(verse_ref)
            for entry in entries:
                results.append({
                    'father_name': entry.father,
                    'work_title': entry.work,
                    'verse_reference': entry.verse_ref,
                    'original_text': entry.text,
                    'theological_topic': entry.theme,
                    'sense': entry.sense,
                    'tradition': entry.tradition,
                    'source': 'offline'
                })
        
        # Layer 2: Database (if available and we want more)
        if self.db:
            try:
                db_results = self.db.fetch_all("""
                    SELECT 
                        ps.*,
                        v.verse_reference
                    FROM patristic_sources ps
                    LEFT JOIN verses v ON ps.verse_id = v.id
                    WHERE v.verse_reference = %s
                    OR ps.section_reference LIKE %s
                    ORDER BY ps.base_relevance_score DESC
                """, (verse_ref, f"%{verse_ref}%"))
                
                for r in db_results:
                    result_dict = dict(r)
                    result_dict['source'] = 'database'
                    results.append(result_dict)
            except Exception as e:
                logger.debug(f"Database query failed: {e}")
        
        return results
    
    def get_commentary_by_sense(self, verse_ref: str, sense: str) -> List[Dict[str, Any]]:
        """Get commentary filtered by sense (literal, allegorical, etc.)"""
        if self.offline_db:
            entries = self.offline_db.suggest_commentary_for_sense(verse_ref, sense)
            return [{
                'father_name': e.father,
                'work_title': e.work,
                'verse_reference': e.verse_ref,
                'text': e.text,
                'sense': e.sense,
                'theme': e.theme
            } for e in entries]
        return []
    
    def search_commentary(self, keywords: List[str], 
                         father_name: str = None,
                         limit: int = 20) -> List[Dict[str, Any]]:
        """Search patristic commentary by keywords"""
        results = []
        
        # Search offline first
        if self.offline_db:
            for kw in keywords:
                entries = self.offline_db.search_text(kw)
                for entry in entries:
                    if father_name and entry.father.lower() != father_name.lower():
                        continue
                    results.append({
                        'father_name': entry.father,
                        'work_title': entry.work,
                        'verse_reference': entry.verse_ref,
                        'original_text': entry.text,
                        'source': 'offline'
                    })
        
        # Then database
        if self.db and len(results) < limit:
            query = """
                SELECT * FROM patristic_sources
                WHERE 1=1
            """
            params = []
            
            if father_name:
                query += " AND father_name ILIKE %s"
                params.append(f"%{father_name}%")
            
            for kw in keywords:
                query += " AND (original_text ILIKE %s OR condensed_summary ILIKE %s)"
                params.extend([f"%{kw}%", f"%{kw}%"])
            
            query += " ORDER BY base_relevance_score DESC LIMIT %s"
            params.append(limit - len(results))
            
            try:
                db_results = self.db.fetch_all(query, tuple(params))
                for r in db_results:
                    result_dict = dict(r)
                    result_dict['source'] = 'database'
                    results.append(result_dict)
            except Exception as e:
                logger.debug(f"Database search failed: {e}")
        
        return results[:limit]
    
    def suggest_fathers_for_verse(self, verse_ref: str, 
                                  book_category: str) -> List[Dict[str, Any]]:
        """Suggest which Fathers might have relevant commentary"""
        suggestions = []
        
        # Category-based suggestions
        category_fathers = {
            'pentateuch': ['Origen', 'Ephrem the Syrian', 'Augustine', 'Basil the Great'],
            'gospel': ['John Chrysostom', 'Augustine', 'Cyril of Alexandria', 'Origen'],
            'pauline': ['John Chrysostom', 'Augustine', 'Origen', 'Theodore of Mopsuestia'],
            'poetic': ['Augustine', 'Gregory of Nyssa', 'Origen', 'Jerome'],
            'major_prophet': ['Jerome', 'Origen', 'Cyril of Alexandria', 'Theodoret'],
            'apocalyptic': ['Origen', 'Victorinus', 'Andrew of Caesarea'],
        }
        
        recommended = category_fathers.get(book_category, 
                                          ['John Chrysostom', 'Augustine', 'Origen'])
        
        for name in recommended:
            info = self.get_father_info(name)
            if info:
                suggestions.append({
                    **info,
                    'recommendation_reason': f"Known for {book_category} commentary"
                })
        
        return suggestions


# ============================================================================
# PATRISTIC INTEGRATION ENGINE
# ============================================================================

class PatristicIntegrationEngine:
    """Integrate patristic insights into verse processing"""
    
    # Key patristic phrases and concepts
    PATRISTIC_VOCABULARY = {
        'theosis': 'deification, becoming god by grace',
        'economia': 'divine dispensation, salvation history',
        'theoria': 'spiritual contemplation, vision of God',
        'kenosis': 'self-emptying, divine condescension',
        'anakephalaiosis': 'recapitulation in Christ',
        'perichoresis': 'mutual indwelling, circumincession',
        'hypostasis': 'person, concrete existence',
        'ousia': 'essence, being, nature',
        'energeia': 'activity, operation, energy',
        'theotokos': 'God-bearer, Mother of God',
        'homoousios': 'of one essence, consubstantial',
        'logos': 'Word, reason, meaning',
        'nous': 'mind, intellect, spirit',
        'pneuma': 'spirit, breath',
        'sarx': 'flesh, humanity',
        'mysterion': 'mystery, sacrament',
        'typos': 'type, figure, pattern',
        'antitypos': 'antitype, fulfillment',
        'allegoria': 'allegory, hidden meaning',
        'anagoge': 'elevation, heavenly meaning',
    }
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.source_manager = PatristicSourceManager(db)
    
    def find_relevant_concepts(self, verse_text: str, 
                              senses: Dict[str, str]) -> List[Dict[str, Any]]:
        """Find patristic concepts relevant to verse content"""
        relevant = []
        
        combined_text = f"{verse_text} {' '.join(senses.values())}".lower()
        
        # Check for concept resonances
        concept_keywords = {
            'theosis': ['god', 'divine', 'glory', 'transfigure', 'transform', 'partake'],
            'economia': ['plan', 'dispensation', 'fulfill', 'time', 'salvation'],
            'kenosis': ['empty', 'humble', 'servant', 'descend', 'lowly'],
            'anakephalaiosis': ['restore', 'gather', 'head', 'sum up', 'all things'],
            'mysterion': ['mystery', 'hidden', 'reveal', 'secret', 'sacrament'],
            'typos': ['pattern', 'shadow', 'figure', 'copy', 'example'],
        }
        
        for concept, keywords in concept_keywords.items():
            if any(kw in combined_text for kw in keywords):
                relevant.append({
                    'concept': concept,
                    'meaning': self.PATRISTIC_VOCABULARY.get(concept, ''),
                    'keywords_found': [kw for kw in keywords if kw in combined_text]
                })
        
        return relevant
    
    def generate_patristic_note(self, verse_ref: str, 
                               concepts: List[Dict]) -> Optional[str]:
        """Generate a patristic note for a verse"""
        if not concepts:
            return None
        
        notes = []
        
        for concept in concepts[:3]:  # Limit to top 3 concepts
            greek_term = concept['concept']
            meaning = concept['meaning']
            notes.append(f"The Fathers speak here of {greek_term} ({meaning})")
        
        return ". ".join(notes) + "."
    
    def suggest_patristic_expansion(self, verse_ref: str,
                                    current_sense: str,
                                    sense_type: str) -> Dict[str, Any]:
        """Suggest how to expand a sense with patristic insight"""
        suggestions = {
            'verse': verse_ref,
            'sense_type': sense_type,
            'expansions': []
        }
        
        # Get relevant Fathers
        verse = self.db.fetch_one("""
            SELECT cb.category FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.verse_reference = %s
        """, (verse_ref,))
        
        if verse:
            fathers = self.source_manager.suggest_fathers_for_verse(
                verse_ref, verse['category']
            )
            
            for father in fathers[:3]:
                emphases = father.get('emphases', [])
                
                # Match emphases to sense type
                relevant_emphases = []
                if sense_type == 'literal' and 'literal' in emphases:
                    relevant_emphases.append('literal interpretation')
                if sense_type == 'allegorical' and ('allegory' in emphases or 'typology' in emphases):
                    relevant_emphases.append('allegorical reading')
                if sense_type == 'tropological' and ('moral' in emphases or 'ethics' in emphases):
                    relevant_emphases.append('moral application')
                if sense_type == 'anagogical' and ('mysticism' in emphases or 'theosis' in emphases):
                    relevant_emphases.append('mystical interpretation')
                
                if relevant_emphases:
                    suggestions['expansions'].append({
                        'father': father['name'],
                        'tradition': father['tradition'],
                        'relevant_emphases': relevant_emphases,
                        'suggestion': f"Consider {father['name']}'s {', '.join(relevant_emphases)}"
                    })
        
        return suggestions


# ============================================================================
# CATENA GENERATOR
# ============================================================================

class CatenaGenerator:
    """Generate catena-style compilations of patristic commentary"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.source_manager = PatristicSourceManager(db)
    
    def generate_catena(self, verse_ref: str) -> Dict[str, Any]:
        """Generate a catena for a verse"""
        catena = {
            'verse': verse_ref,
            'entries': [],
            'themes': set()
        }
        
        # Get all commentary for the verse
        commentaries = self.source_manager.get_commentary_for_verse(verse_ref)
        
        for commentary in commentaries:
            entry = {
                'father': commentary.get('father_name'),
                'work': commentary.get('work_title'),
                'text': commentary.get('condensed_summary') or commentary.get('original_text', '')[:500],
                'topic': commentary.get('theological_topic')
            }
            catena['entries'].append(entry)
            
            if entry['topic']:
                catena['themes'].add(entry['topic'])
        
        catena['themes'] = list(catena['themes'])
        return catena
    
    def generate_thematic_catena(self, theme: str, 
                                limit: int = 10) -> Dict[str, Any]:
        """Generate a catena organized by theological theme"""
        catena = {
            'theme': theme,
            'entries': []
        }
        
        # Search for theme
        results = self.source_manager.search_commentary([theme], limit=limit)
        
        for r in results:
            catena['entries'].append({
                'father': r.get('father_name'),
                'work': r.get('work_title'),
                'verse': r.get('section_reference'),
                'text': r.get('condensed_summary', '')[:300]
            })
        
        return catena


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """CLI entry point for patristic integration"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Patristic Integration')
    parser.add_argument('--list-fathers', action='store_true', help='List all Church Fathers')
    parser.add_argument('--father', type=str, help='Get info about specific Father')
    parser.add_argument('--emphasis', type=str, help='Find Fathers by emphasis')
    parser.add_argument('--verse', type=str, help='Get commentary for verse')
    parser.add_argument('--catena', type=str, help='Generate catena for verse')
    parser.add_argument('--theme-catena', type=str, help='Generate thematic catena')
    parser.add_argument('--concepts', type=str, help='Find patristic concepts in text')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    from scripts.database import init_db
    init_db()
    
    source_manager = PatristicSourceManager()
    
    if args.list_fathers:
        fathers = source_manager.get_all_fathers()
        print("\nChurch Fathers by Era:")
        print("=" * 60)
        for era, father_list in fathers.items():
            print(f"\n{era.upper().replace('_', ' ')}:")
            for f in father_list:
                print(f"  • {f['name']} ({f['dates']}) - {f['tradition']}")
    
    elif args.father:
        info = source_manager.get_father_info(args.father)
        if info:
            print(f"\n{info['name']}")
            print("=" * 40)
            print(f"Dates: {info['dates']}")
            print(f"Tradition: {info['tradition']}")
            print(f"Era: {info['era']}")
            print(f"Emphases: {', '.join(info.get('emphases', []))}")
        else:
            print(f"Father not found: {args.father}")
    
    elif args.emphasis:
        fathers = source_manager.find_fathers_by_emphasis(args.emphasis)
        print(f"\nFathers emphasizing '{args.emphasis}':")
        for f in fathers:
            print(f"  • {f['name']} ({f['tradition']})")
    
    elif args.verse:
        commentaries = source_manager.get_commentary_for_verse(args.verse)
        print(f"\nPatristic commentary for {args.verse}:")
        if commentaries:
            for c in commentaries:
                print(f"\n  {c.get('father_name', 'Unknown')}:")
                print(f"    {c.get('condensed_summary', c.get('original_text', ''))[:200]}...")
        else:
            print("  No commentary found in database")
            print("\n  Suggested Fathers to consult:")
            verse = get_db().fetch_one("""
                SELECT cb.category FROM verses v
                JOIN canonical_books cb ON v.book_id = cb.id  
                WHERE v.verse_reference = %s
            """, (args.verse,))
            if verse:
                suggestions = source_manager.suggest_fathers_for_verse(args.verse, verse['category'])
                for s in suggestions:
                    print(f"    • {s['name']} ({s['tradition']})")
    
    elif args.catena:
        generator = CatenaGenerator()
        catena = generator.generate_catena(args.catena)
        print(f"\nCatena for {args.catena}:")
        print("=" * 60)
        if catena['entries']:
            for entry in catena['entries']:
                print(f"\n{entry['father']} ({entry['work']}):")
                print(f"  {entry['text'][:300]}...")
        else:
            print("  No catena entries found")
    
    elif args.theme_catena:
        generator = CatenaGenerator()
        catena = generator.generate_thematic_catena(args.theme_catena)
        print(f"\nThematic Catena: {args.theme_catena}")
        print("=" * 60)
        for entry in catena['entries']:
            print(f"\n{entry['father']} on {entry['verse']}:")
            print(f"  {entry['text'][:200]}...")
    
    elif args.concepts:
        engine = PatristicIntegrationEngine()
        concepts = engine.find_relevant_concepts(args.concepts, {})
        print(f"\nPatristic concepts in text:")
        for c in concepts:
            print(f"  • {c['concept']}: {c['meaning']}")
            print(f"    Keywords found: {', '.join(c['keywords_found'])}")
    
    else:
        parser.print_help()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
