#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Data Ingestion System
Comprehensive ingestion of all source files into PostgreSQL database
"""

import sys
import re
import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config, CANONICAL_ORDER, PRIMARY_MOTIFS, DATA_DIR
from scripts.database import get_db, DatabaseManager

logger = logging.getLogger(__name__)


# ============================================================================
# BOOK NAME NORMALIZATION
# ============================================================================

BOOK_ALIASES = {
    'song of songs': 'Song of Solomon',
    'song': 'Song of Solomon',
    'canticles': 'Song of Solomon',
    'ecclesiasticus': 'Sirach',
    'wisdom of solomon': 'Wisdom',
    'wisdom of sirach': 'Sirach',
    'ben sira': 'Sirach',
    '1 sam': '1 Samuel',
    '2 sam': '2 Samuel',
    '1 kgs': '1 Kings',
    '2 kgs': '2 Kings',
    '1 chr': '1 Chronicles',
    '2 chr': '2 Chronicles',
    '1 cor': '1 Corinthians',
    '2 cor': '2 Corinthians',
    '1 thess': '1 Thessalonians',
    '2 thess': '2 Thessalonians',
    '1 tim': '1 Timothy',
    '2 tim': '2 Timothy',
    '1 pet': '1 Peter',
    '2 pet': '2 Peter',
    '1 jn': '1 John',
    '2 jn': '2 John',
    '3 jn': '3 John',
    '1 macc': '1 Maccabees',
    '2 macc': '2 Maccabees',
    'gen': 'Genesis',
    'exod': 'Exodus',
    'lev': 'Leviticus',
    'num': 'Numbers',
    'deut': 'Deuteronomy',
    'josh': 'Joshua',
    'judg': 'Judges',
    'matt': 'Matthew',
    'mk': 'Mark',
    'lk': 'Luke',
    'jn': 'John',
    'rom': 'Romans',
    'gal': 'Galatians',
    'eph': 'Ephesians',
    'phil': 'Philippians',
    'col': 'Colossians',
    'heb': 'Hebrews',
    'jas': 'James',
    'rev': 'Revelation',
    'ps': 'Psalms',
    'prov': 'Proverbs',
    'eccl': 'Ecclesiastes',
    'isa': 'Isaiah',
    'jer': 'Jeremiah',
    'lam': 'Lamentations',
    'ezek': 'Ezekiel',
    'dan': 'Daniel',
    'hos': 'Hosea',
    'ob': 'Obadiah',
    'mic': 'Micah',
    'nah': 'Nahum',
    'hab': 'Habakkuk',
    'zeph': 'Zephaniah',
    'hag': 'Haggai',
    'zech': 'Zechariah',
    'mal': 'Malachi',
}


def normalize_book_name(name: str) -> str:
    """Normalize book name to canonical form"""
    name_lower = name.lower().strip()
    return BOOK_ALIASES.get(name_lower, name.strip().title())


def parse_verse_reference(ref: str) -> Optional[Tuple[str, int, int]]:
    """Parse verse reference like 'Genesis 1:1' into (book, chapter, verse)"""
    # Handle numbered books (1 Samuel, 2 Kings, etc.)
    patterns = [
        r'^(\d?\s*[A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(\d+):(\d+)',  # Standard: "Genesis 1:1"
        r'^(\d?\s*[A-Za-z]+(?:\s+[A-Za-z]+)*)\s+(\d+)\.(\d+)',  # Period: "Genesis 1.1"
    ]
    
    for pattern in patterns:
        match = re.match(pattern, ref.strip())
        if match:
            book = normalize_book_name(match.group(1))
            chapter = int(match.group(2))
            verse = int(match.group(3))
            return (book, chapter, verse)
    
    return None


# ============================================================================
# BASE INGESTER CLASS
# ============================================================================

class BaseIngester:
    """Base class for all ingesters"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.stats = {
            'processed': 0,
            'inserted': 0,
            'updated': 0,
            'errors': 0
        }
    
    def log_stats(self, name: str):
        """Log ingestion statistics"""
        logger.info(f"{name} ingestion complete:")
        logger.info(f"  Processed: {self.stats['processed']}")
        logger.info(f"  Inserted: {self.stats['inserted']}")
        logger.info(f"  Updated: {self.stats['updated']}")
        logger.info(f"  Errors: {self.stats['errors']}")


# ============================================================================
# VERSE INGESTER
# ============================================================================

class VerseIngester(BaseIngester):
    """Ingest verses from various file formats"""
    
    def __init__(self, db: DatabaseManager = None):
        super().__init__(db)
        self._book_id_cache = {}
        self._load_book_ids()
    
    def _load_book_ids(self):
        """Cache book IDs for fast lookup"""
        rows = self.db.fetch_all("SELECT id, name FROM canonical_books")
        for row in rows:
            self._book_id_cache[row['name'].lower()] = row['id']
    
    def _get_book_id(self, book_name: str) -> Optional[int]:
        """Get book ID from name"""
        normalized = normalize_book_name(book_name)
        return self._book_id_cache.get(normalized.lower())
    
    def ingest_from_text(self, content: str, format_type: str = 'standard') -> int:
        """Ingest verses from text content"""
        verses_data = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Try different separators
            for sep in [' — ', ' - ', '—', '\t']:
                if sep in line:
                    parts = line.split(sep, 1)
                    ref_str = parts[0].strip()
                    text = parts[1].strip() if len(parts) > 1 else None
                    
                    parsed = parse_verse_reference(ref_str)
                    if parsed:
                        book, chapter, verse = parsed
                        book_id = self._get_book_id(book)
                        
                        if book_id:
                            verses_data.append({
                                'book_id': book_id,
                                'chapter': chapter,
                                'verse_number': verse,
                                'verse_reference': f"{book} {chapter}:{verse}",
                                'text_kjv': text if text and '[Text not found]' not in text else None
                            })
                            self.stats['processed'] += 1
                    break
        
        # Bulk insert/update
        if verses_data:
            self._bulk_upsert_verses(verses_data)
        
        return len(verses_data)
    
    def ingest_from_file(self, file_path: Path) -> int:
        """Ingest verses from a file"""
        logger.info(f"Ingesting verses from {file_path}")
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        count = self.ingest_from_text(content)
        self.log_stats("Verse")
        return count
    
    def _bulk_upsert_verses(self, verses_data: List[Dict]):
        """Bulk insert/update verses"""
        query = """
            INSERT INTO verses (book_id, chapter, verse_number, verse_reference, text_kjv, status)
            VALUES (%(book_id)s, %(chapter)s, %(verse_number)s, %(verse_reference)s, %(text_kjv)s, 'raw')
            ON CONFLICT (book_id, chapter, verse_number) 
            DO UPDATE SET 
                text_kjv = COALESCE(EXCLUDED.text_kjv, verses.text_kjv),
                updated_at = CURRENT_TIMESTAMP
        """
        
        for verse in verses_data:
            try:
                result = self.db.execute(query, (
                    verse['book_id'], verse['chapter'], verse['verse_number'],
                    verse['verse_reference'], verse['text_kjv']
                ))
                self.stats['inserted'] += 1
            except Exception as e:
                logger.error(f"Error inserting verse {verse['verse_reference']}: {e}")
                self.stats['errors'] += 1


# ============================================================================
# EVENT INGESTER
# ============================================================================

class EventIngester(BaseIngester):
    """Ingest biblical events for tonal arrangement"""
    
    WEIGHT_KEYWORDS = {
        'light': ['joy', 'blessing', 'birth', 'creation', 'promise', 'covenant', 
                  'praise', 'wedding', 'celebration', 'peace', 'restore'],
        'heavy': ['death', 'curse', 'judgment', 'plague', 'slaughter', 'destruction', 
                  'crucifixion', 'exile', 'war', 'wrath', 'darkness'],
        'unsettling': ['temptation', 'betrayal', 'fear', 'warning', 'serpent', 
                       'fleeing', 'conflict', 'jealousy', 'deception'],
        'transcendent': ['theophany', 'glory', 'transfiguration', 'resurrection', 
                         'ascension', 'vision', 'angel', 'heaven', 'throne']
    }
    
    def _determine_emotional_weight(self, description: str) -> str:
        """Determine emotional weight based on event description"""
        desc_lower = description.lower()
        
        for weight, keywords in self.WEIGHT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in desc_lower:
                    return weight
        
        return 'neutral'
    
    def _is_load_bearing(self, description: str) -> bool:
        """Determine if event is structurally load-bearing"""
        load_bearing_indicators = [
            'covenant', 'sacrifice', 'death', 'birth', 'naming',
            'blessing', 'curse', 'creation', 'exodus', 'crucifixion',
            'resurrection', 'ascension', 'pentecost', 'flood', 'baptism'
        ]
        desc_lower = description.lower()
        return any(ind in desc_lower for ind in load_bearing_indicators)
    
    def ingest_events(self, events_list: List[Dict]) -> int:
        """Ingest a list of events"""
        query = """
            INSERT INTO events (part_number, part_title, event_number, event_description, 
                               emotional_weight, load_bearing, status)
            VALUES (%(part_number)s, %(part_title)s, %(event_number)s, %(event_description)s,
                    %(emotional_weight)s, %(load_bearing)s, 'raw')
            ON CONFLICT (part_number, event_number) DO UPDATE SET
                event_description = EXCLUDED.event_description,
                emotional_weight = EXCLUDED.emotional_weight,
                updated_at = CURRENT_TIMESTAMP
        """
        
        for event in events_list:
            try:
                # Auto-calculate emotional weight if not provided
                if 'emotional_weight' not in event:
                    event['emotional_weight'] = self._determine_emotional_weight(
                        event['event_description']
                    )
                if 'load_bearing' not in event:
                    event['load_bearing'] = self._is_load_bearing(event['event_description'])
                
                self.db.execute(query, event)
                self.stats['inserted'] += 1
            except Exception as e:
                logger.error(f"Error inserting event: {e}")
                self.stats['errors'] += 1
        
        self.log_stats("Event")
        return self.stats['inserted']


# ============================================================================
# PATRISTIC SOURCES INGESTER
# ============================================================================

class PatristicIngester(BaseIngester):
    """Ingest patristic commentary sources"""
    
    CHURCH_FATHERS = [
        'Augustine', 'Chrysostom', 'Origen', 'Basil', 'Gregory', 'Athanasius',
        'Cyril', 'Jerome', 'Ambrose', 'Irenaeus', 'Tertullian', 'Clement',
        'Maximus', 'Damascene', 'Ephrem', 'Theodore', 'Theodoret', 'Cassian',
        'Hilary', 'Leo', 'Gregory Palamas', 'Symeon', 'Isaac', 'Macarius'
    ]
    
    def _extract_father_name(self, text: str) -> Optional[str]:
        """Try to identify which Father authored this text"""
        for father in self.CHURCH_FATHERS:
            if father.lower() in text.lower()[:500]:
                return father
        return None
    
    def _extract_topic(self, text: str) -> str:
        """Extract theological topic from text"""
        topic_keywords = {
            'creation': ['creation', 'genesis', 'beginning', 'cosmos'],
            'trinity': ['trinity', 'three persons', 'father son spirit', 'godhead'],
            'incarnation': ['incarnation', 'became man', 'took flesh', 'word made flesh'],
            'salvation': ['salvation', 'redemption', 'atonement', 'soteriology'],
            'scripture': ['scripture', 'bible', 'holy writ', 'sacred text'],
            'allegorical': ['allegorical', 'allegory', 'spiritual sense', 'typology'],
            'literal': ['literal', 'historical', 'grammatical'],
            'moral': ['moral', 'tropological', 'ethical', 'virtue'],
            'eschatological': ['eschatological', 'anagogical', 'heaven', 'end times', 'parousia'],
            'christological': ['christology', 'christ', 'messiah', 'logos'],
            'ecclesiology': ['church', 'ecclesia', 'body of christ', 'bride'],
            'sacramental': ['sacrament', 'mystery', 'baptism', 'eucharist']
        }
        
        text_lower = text.lower()[:1000]
        for topic, keywords in topic_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    return topic
        return 'general'
    
    def ingest_patristic_text(self, father_name: str, work_title: str, 
                              content: str, section_ref: str = None) -> int:
        """Ingest a patristic text"""
        query = """
            INSERT INTO patristic_sources 
            (father_name, work_title, section_reference, original_text, 
             theological_topic, base_relevance_score, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'raw')
        """
        
        topic = self._extract_topic(content)
        relevance_score = len(content) // 100  # Simple heuristic
        
        try:
            self.db.execute(query, (
                father_name, work_title, section_ref, content[:10000],
                topic, relevance_score
            ))
            self.stats['inserted'] += 1
            return 1
        except Exception as e:
            logger.error(f"Error inserting patristic source: {e}")
            self.stats['errors'] += 1
            return 0


# ============================================================================
# MOTIF INITIALIZER
# ============================================================================

class MotifInitializer(BaseIngester):
    """Initialize primary orbital motifs"""
    
    def calculate_harmonic_pages(self, planting: int, convergence: int) -> List[int]:
        """Calculate harmonic reinforcement pages"""
        distance = convergence - planting
        ratios = config.orbital_resonance.harmonic_ratios
        return [planting + int(distance * r) for r in ratios]
    
    def initialize_motifs(self) -> int:
        """Initialize all primary motifs from configuration"""
        query = """
            INSERT INTO motifs (
                name, description, foundation_layer,
                planting_page, reinforcement_pages, convergence_page,
                planting_intensity, convergence_intensity,
                core_vocabulary, sensory_modalities,
                current_status, harmonic_ratios
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'planted', %s
            )
            ON CONFLICT (name) DO UPDATE SET
                description = EXCLUDED.description,
                planting_page = EXCLUDED.planting_page,
                convergence_page = EXCLUDED.convergence_page,
                updated_at = CURRENT_TIMESTAMP
        """
        
        ratios = config.orbital_resonance.harmonic_ratios
        
        for motif in PRIMARY_MOTIFS:
            try:
                harmonic_pages = self.calculate_harmonic_pages(
                    motif['planting_page'],
                    motif['convergence_page']
                )
                
                self.db.execute(query, (
                    motif['name'],
                    motif['description'],
                    motif['layer'],
                    motif['planting_page'],
                    harmonic_pages,
                    motif['convergence_page'],
                    config.orbital_resonance.intensity_curve['planting'],
                    config.orbital_resonance.intensity_curve['convergence'],
                    motif['vocabulary'],
                    motif['modalities'],
                    ratios
                ))
                self.stats['inserted'] += 1
            except Exception as e:
                logger.error(f"Error inserting motif {motif['name']}: {e}")
                self.stats['errors'] += 1
        
        self.log_stats("Motif")
        return self.stats['inserted']


# ============================================================================
# CROSS-REFERENCE INGESTER
# ============================================================================

class CrossReferenceIngester(BaseIngester):
    """Ingest scripture cross-references"""
    
    def ingest_cross_reference(self, from_ref: str, to_ref: str, 
                               rel_type: str = 'parallel', votes: int = 0) -> bool:
        """Ingest a single cross-reference"""
        # First, get verse IDs
        from_verse = self.db.fetch_one(
            "SELECT id FROM verses WHERE verse_reference = %s", (from_ref,)
        )
        to_verse = self.db.fetch_one(
            "SELECT id FROM verses WHERE verse_reference = %s", (to_ref,)
        )
        
        if not from_verse or not to_verse:
            return False
        
        query = """
            INSERT INTO cross_references (from_verse_id, to_verse_id, relationship_type, votes)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """
        
        try:
            self.db.execute(query, (from_verse['id'], to_verse['id'], rel_type, votes))
            self.stats['inserted'] += 1
            return True
        except Exception as e:
            logger.error(f"Error inserting cross-reference: {e}")
            self.stats['errors'] += 1
            return False


# ============================================================================
# MASTER INGESTION ORCHESTRATOR
# ============================================================================

class IngestionOrchestrator:
    """Orchestrate complete database ingestion"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or get_db()
        self.verse_ingester = VerseIngester(self.db)
        self.event_ingester = EventIngester(self.db)
        self.patristic_ingester = PatristicIngester(self.db)
        self.motif_initializer = MotifInitializer(self.db)
        self.xref_ingester = CrossReferenceIngester(self.db)
    
    def run_schema(self, schema_path: Path) -> bool:
        """Execute the database schema"""
        logger.info(f"Running schema from {schema_path}")
        return self.db.run_schema_file(schema_path)
    
    def initialize_system(self) -> Dict[str, int]:
        """Initialize the complete system"""
        stats = {}
        
        # Initialize motifs
        logger.info("Initializing primary motifs...")
        stats['motifs'] = self.motif_initializer.initialize_motifs()
        
        return stats
    
    def ingest_verses_from_file(self, file_path: Path) -> int:
        """Ingest verses from a file"""
        return self.verse_ingester.ingest_from_file(file_path)
    
    def get_ingestion_status(self) -> Dict[str, Any]:
        """Get current ingestion status"""
        status = {}
        
        # Check table counts
        tables = ['canonical_books', 'verses', 'events', 'motifs', 
                  'patristic_sources', 'cross_references']
        
        for table in tables:
            if self.db.table_exists(table):
                status[table] = self.db.get_table_count(table)
            else:
                status[table] = 0
        
        return status


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    """Main entry point for ingestion"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ΒΊΒΛΟΣ ΛΌΓΟΥ Data Ingestion')
    parser.add_argument('--schema', type=Path, help='Path to SQL schema file')
    parser.add_argument('--verses', type=Path, help='Path to verses file')
    parser.add_argument('--init-motifs', action='store_true', help='Initialize motifs')
    parser.add_argument('--status', action='store_true', help='Show ingestion status')
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize database
    from scripts.database import init_db
    if not init_db():
        logger.error("Failed to initialize database connection")
        return 1
    
    orchestrator = IngestionOrchestrator()
    
    if args.status:
        status = orchestrator.get_ingestion_status()
        print("\nIngestion Status:")
        print("=" * 40)
        for table, count in status.items():
            print(f"  {table}: {count:,}")
        return 0
    
    if args.schema:
        if not orchestrator.run_schema(args.schema):
            logger.error("Schema execution failed")
            return 1
    
    if args.init_motifs:
        orchestrator.initialize_system()
    
    if args.verses:
        orchestrator.ingest_verses_from_file(args.verses)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
