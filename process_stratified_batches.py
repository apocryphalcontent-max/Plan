import json
import os
import time
import sys
import re
import textwrap
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import random
import math
import sympy as sp
import traceback
import hashlib
import logging
from contextlib import contextmanager
from functools import lru_cache
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config:
    """Configuration settings with validation"""
    batch_size: int = 2
    uniqueness_threshold: float = 0.10
    cooldown_between_batches: int = 2
    max_retries: int = 3
    continuous_mode: bool = True
    max_workers: int = 4  # For parallel processing
    
    # Paths
    base_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parent)
    
    @property
    def verses_path(self) -> Path:
        return self.base_dir / "orthodox_canon_complete.txt"
    
    @property
    def content_path(self) -> Path:
        return self.base_dir / "stratified_content.json"
    
    @property
    def output_path(self) -> Path:
        return Path("C:/Users/Edwin Boston/Desktop/Verses/ExegeticalOutput. txt")
    
    @property
    def processed_verses_path(self) -> Path:
        return self.base_dir / "processed_verses.json"
    
    @property
    def failed_verses_path(self) -> Path:
        return self.base_dir / "failed_verses.json"
    
    @property
    def log_path(self) -> Path:
        return self.base_dir / "processing_log.txt"


CONFIG = Config()


# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class BookCategory(Enum):
    PENTATEUCH = "pentateuch"
    HISTORICAL = "historical"
    POETIC = "poetic"
    MAJOR_PROPHET = "major_prophet"
    MINOR_PROPHET = "minor_prophet"
    DEUTEROCANONICAL = "deuterocanonical"
    GOSPEL = "gospel"
    ACTS = "acts"
    PAULINE = "pauline"
    GENERAL_EPISTLE = "general_epistle"
    APOCALYPTIC = "apocalyptic"
    UNKNOWN = "unknown"


# Template sections to exclude from uniqueness comparison
TEMPLATE_SECTIONS = frozenset([
    "VERSE NOTE TEMPLATE",
    "I. NINE MATRIX APPLICATION",
    "II. REGISTER SPECIFICATION",
    "III. SENSORY VOCABULARY CODEX APPLICATION",
    "IV. PROSODIC ENTRAINMENT PATTERN",
    "V. TEMPORAL FOLDING VOCABULARY",
    "VI. FOUR-PHASE RITUAL STRUCTURE",
    "VII. SUBLIMINAL READER FORMATION",
    "VIII. ANTI-AI MARKERS",
    "IX. STRATIFIED FOUNDATION ANALYSIS",
    "X. WORKED PROSE EXAMPLE",
    "Literal:",
    "Allegorical:",
    "Tropological:",
    "Anagogical:",
    "Liturgical:",
    "Patristic:",
    "Narrative:",
    "Sensory:",
    "Temporal:",
    "Emotional Valence:",
    "Theological Weight:",
    "Narrative Function:",
    "Sensory Intensity:",
    "Grammatical Complexity:",
    "Lexical Rarity:",
    "Breath Rhythm:",
    "Register Baseline:",
    "Verification Checklist:",
    "Generated on:",
    "Uniqueness verified against",
    "Layer One elements:",
    "Layer Two elements:",
    "Layer Three elements:",
    "Layer Four elements:",
    "Layer Five elements:",
    "Temporal folding echoes:",
    "Typological correspondences:",
    "TOTAL THREAD DENSITY:",
    "A. Active Layer Elements",
    "B. Thread Density Calculation",
    "Integration protocol:",
    "Integration Protocol:",
    "Vocabulary bridge:",
    "Future connection:",
    "Past connection:",
    "Orbital resonance:",
    "Semantic consistency:",
    "Harmonic position:",
    "Invisibility protocol:",
    "Visual:",
    "Tactile:",
    "Auditory:",
    "Kinesthetic:",
    "Olfactory:",
    "Gustatory:",
    "Emotional:",
    "Movement:",
    "Temperature:",
    "Intensity gradient:",
    "Sentence length variation:",
    "Breath rhythm markers:",
    "Pausing patterns:",
    "Stress patterns:",
    "Subordination placement:",
    "Repetition patterns:",
    "Cadence design:",
    "1. Separation:",
    "2. Liminality:",
    "3. Transformation:",
    "4. Incorporation:",
    "Ritual markers:",
    "Boundary indicators:",
    "Temporal shift:",
    "Suspended time:",
    "Role fluidity:",
    "Sacred ambiguity:",
    "Boundary permeability:",
    "Identity modification:",
    "Power transfer:",
    "Covenant renewal:",
    "Symbolic action:",
    "Return to ordinary time:",
    "New naming/identity:",
    "Commissioning:",
    "Communal witness:",
    "Tropological formation:",
    "Anagogical formation:",
    "Hapax Legomenon:",
    "Anaphoric Triple:",
    "Collocation Violation:",
    "Register Violation:",
    "Chiastic Emphasis:",
])

# Common words to exclude from uniqueness comparison
COMMON_WORDS = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "as", "is", "was", "are", "were", "been", "be", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may", "might", "must",
    "shall", "can", "this", "that", "these", "those", "it", "its", "they", "them",
    "their", "he", "she", "him", "her", "his", "hers", "we", "us", "our", "you", "your",
    "who", "whom", "which", "what", "where", "when", "why", "how", "all", "each", "every",
    "both", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "just", "also", "now", "here", "there",
    "then", "if", "because", "while", "although", "though", "after", "before", "since",
    "until", "unless", "through", "during", "about", "into", "over", "under", "again",
    "further", "once", "verse", "specific", "pattern", "structure", "element", "elements",
    "analysis", "formation", "connection", "based", "calculated", "target", "protocol",
})

def load_verse_texts(path: Path) -> Dict[str, str]:
    """Parse orthodox_canon_complete.txt into a reference->text map."""
    verse_texts: Dict[str, str] = {}
    if not path.exists():
        return verse_texts
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or set(line) == {"="}:
                continue
            if " - " in line:
                ref_part, text_part = line.split(" - ", 1)
                verse_ref = ref_part.strip()
                verse_texts[verse_ref] = text_part.strip()
            else:
                verse_texts[line] = ""
    except Exception as exc:
        get_logger().error(f"Failed to load verse texts: {exc}")
    return verse_texts

# Book order for canonical position calculation
BOOK_ORDER:  Dict[str, float] = {
    "Genesis":  1, "Exodus": 2, "Leviticus": 3, "Numbers": 4, "Deuteronomy": 5,
    "Joshua": 6, "Judges": 7, "Ruth": 8, "1 Samuel": 9, "2 Samuel": 10,
    "1 Kings": 11, "2 Kings": 12, "1 Chronicles": 13, "2 Chronicles": 14, "Ezra": 15,
    "Nehemiah": 16, "Esther": 17, "Job": 18, "Psalms": 19, "Proverbs": 20,
    "Ecclesiastes":  21, "Song":  22, "Song of Solomon": 22, "Isaiah": 23,
    "Jeremiah": 24, "Lamentations":  25, "Ezekiel": 26, "Daniel": 27,
    "Hosea": 28, "Joel": 29, "Amos": 30, "Obadiah": 31,
    "Jonah": 32, "Micah": 33, "Nahum": 34, "Habakkuk":  35, "Zephaniah": 36,
    "Haggai": 37, "Zechariah": 38, "Malachi": 39,
    # Deuterocanonical books
    "Tobit": 39.1, "Judith": 39.2, "1 Maccabees": 39.3, "2 Maccabees": 39.4,
    "Wisdom": 39.5, "Sirach": 39.6, "Baruch": 39.7,
    # New Testament
    "Matthew": 40, "Mark": 41, "Luke": 42, "John":  43, "Acts": 44,
    "Romans": 45, "1 Corinthians":  46, "2 Corinthians": 47, "Galatians": 48,
    "Ephesians": 49, "Philippians": 50, "Colossians":  51,
    "1 Thessalonians": 52, "2 Thessalonians": 53,
    "1 Timothy": 54, "2 Timothy": 55, "Titus": 56, "Philemon": 57, "Hebrews": 58,
    "James": 59, "1 Peter": 60, "2 Peter": 61, "1 John": 62, "2 John": 63,
    "3 John":  64, "Jude":  65, "Revelation": 66
}

# Book categories
BOOK_CATEGORIES:  Dict[str, BookCategory] = {}
_pentateuch = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]
_historical = ["Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
               "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther"]
_poetic = ["Job", "Psalms", "Proverbs", "Ecclesiastes", "Song", "Song of Solomon"]
_major_prophets = ["Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel"]
_minor_prophets = ["Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum",
                   "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"]
_deuterocanonical = ["Tobit", "Judith", "1 Maccabees", "2 Maccabees", "Wisdom", "Sirach", "Baruch"]
_gospels = ["Matthew", "Mark", "Luke", "John"]
_pauline = ["Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
            "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
            "1 Timothy", "2 Timothy", "Titus", "Philemon"]
_general_epistles = ["Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude"]

for book in _pentateuch: 
    BOOK_CATEGORIES[book] = BookCategory.PENTATEUCH
for book in _historical: 
    BOOK_CATEGORIES[book] = BookCategory.HISTORICAL
for book in _poetic: 
    BOOK_CATEGORIES[book] = BookCategory.POETIC
for book in _major_prophets:
    BOOK_CATEGORIES[book] = BookCategory.MAJOR_PROPHET
for book in _minor_prophets: 
    BOOK_CATEGORIES[book] = BookCategory.MINOR_PROPHET
for book in _deuterocanonical:
    BOOK_CATEGORIES[book] = BookCategory.DEUTEROCANONICAL
for book in _gospels:
    BOOK_CATEGORIES[book] = BookCategory. GOSPEL
BOOK_CATEGORIES["Acts"] = BookCategory.ACTS
for book in _pauline:
    BOOK_CATEGORIES[book] = BookCategory.PAULINE
for book in _general_epistles:
    BOOK_CATEGORIES[book] = BookCategory. GENERAL_EPISTLE
BOOK_CATEGORIES["Revelation"] = BookCategory.APOCALYPTIC


# ============================================================================
# LOGGING
# ============================================================================

class Logger:
    """Thread-safe logger with file and console output"""
    
    def __init__(self, log_path: Path):
        self.log_path = log_path
        self._lock = threading.Lock()
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup Python logging module"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_path, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def info(self, message: str) -> None:
        with self._lock:
            self. logger.info(message)
    
    def warning(self, message: str) -> None:
        with self._lock:
            self.logger.warning(message)
    
    def error(self, message: str) -> None:
        with self._lock:
            self.logger. error(message)
    
    def debug(self, message: str) -> None:
        with self._lock:
            self.logger.debug(message)


# Global logger instance
logger:  Optional[Logger] = None


def get_logger() -> Logger:
    """Get or create the global logger instance"""
    global logger
    if logger is None:
        logger = Logger(CONFIG.log_path)
    return logger


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class VerseReference:
    """Parsed verse reference with book, chapter, and verse"""
    book: str
    chapter: int
    verse: int
    original:  str
    
    @classmethod
    def parse(cls, verse_ref: str) -> 'VerseReference':
        """Parse a verse reference string"""
        match = re.match(r'((?:\d\s+)?[A-Za-z\s]+?)\s+(\d+):(\d+)', verse_ref)
        if match:
            book = match.group(1).strip()
            chapter = int(match.group(2))
            verse = int(match.group(3))
            return cls(book=book, chapter=chapter, verse=verse, original=verse_ref)
        
        # Fallback parsing
        parts = verse_ref.split()
        if len(parts) >= 2:
            book = ' '.join(parts[:-1]) if any(c.isdigit() for c in parts[0]) else parts[0]
            chapter_verse = parts[-1]. split(':')
            chapter = int(chapter_verse[0]) if chapter_verse[0].isdigit() else 1
            verse = int(chapter_verse[1]) if len(chapter_verse) > 1 and chapter_verse[1].isdigit() else 1
            return cls(book=book, chapter=chapter, verse=verse, original=verse_ref)
        
        return cls(book=verse_ref, chapter=1, verse=1, original=verse_ref)
    
    @property
    def category(self) -> BookCategory:
        """Get the book category"""
        return BOOK_CATEGORIES. get(self.book, BookCategory.UNKNOWN)
    
    @property
    def canonical_position(self) -> float:
        """Calculate canonical position (0.0 to 1.0)"""
        book_pos = BOOK_ORDER.get(self.book, 40)
        position = (book_pos + self.chapter / 100 + self.verse / 10000) / 67
        return min(1.0, max(0.0, position))
    
    def __str__(self) -> str:
        return self.original


@dataclass
class MatrixElements:
    """Nine-matrix theological elements"""
    emotional_valence: float
    theological_weight: float
    narrative_function: str
    sensory_intensity: float
    grammatical_complexity: float
    lexical_rarity:  float
    breath_rhythm: str
    register_baseline: str


@dataclass
class SensoryVocabulary: 
    """Sensory vocabulary for verse"""
    visual: str
    auditory: str
    tactile: str
    olfactory: str
    kinesthetic: str


@dataclass
class EmotionalArc:
    """Emotional/psychological arc"""
    valence: str
    weight: str
    movement: str


@dataclass
class VerseAnalysis:
    """Complete analysis for a verse"""
    reference: VerseReference
    title: str
    literal:  str
    allegorical: str
    tropological: str
    anagogical: str
    liturgical: str
    patristic: str
    sensory: SensoryVocabulary
    emotional: EmotionalArc
    matrix: MatrixElements
    content_hash: str
    timestamp: str


# ============================================================================
# FILE OPERATIONS
# ============================================================================

class AtomicFileWriter:
    """Context manager for atomic file writes"""
    
    def __init__(self, path: Path, mode: str = 'w', encoding: str = 'utf-8'):
        self.path = path
        self.temp_path = path.with_suffix('.tmp')
        self.mode = mode
        self.encoding = encoding
        self.file = None
    
    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.file = open(self.temp_path, self.mode, encoding=self.encoding)
        return self. file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        if exc_type is None:
            self.temp_path.replace(self.path)
        else:
            # Clean up temp file on error
            if self.temp_path.exists():
                self.temp_path. unlink()
        return False


class DataStore:
    """Handles all data persistence operations"""
    
    def __init__(self, config: Config):
        self.config = config
        self._lock = threading.Lock()
    
    def load_verses(self) -> List[str]:
        """Load verses with proper format detection"""
        verses = []
        log = get_logger()
        
        try:
            if not self.config.verses_path.exists():
                log.error(f"Verses file not found: {self.config. verses_path}")
                return []
            
            raw_lines = self.config.verses_path.read_text(encoding="utf-8").splitlines()
            verse_pattern = re.compile(r'\d+:\d+')
            
            for raw in raw_lines:
                line = raw.strip()
                
                # Skip empty lines, comments, and separators
                if not line or line.startswith("#"):
                    continue
                if set(line) <= {"=", "-", "*"}:
                    continue
                
                # Must contain chapter:verse pattern
                if ":" not in line or not verse_pattern.search(line):
                    continue
                
                # Extract verse reference
                verse_ref = line
                for sep in [" — ", " - ", "—", "-"]:
                    if sep in verse_ref:
                        verse_ref = verse_ref.split(sep, 1)[0].strip()
                        break
                
                verse_ref = verse_ref.rstrip('.,;:!?)]').strip()
                if verse_ref:
                    verses. append(verse_ref)
            
            log.info(f"Loaded {len(verses)} verses from file")
            
        except Exception as e:
            log.error(f"Error loading verses: {e}")
            traceback.print_exc()
        
        return verses
    
    def load_json(self, path: Path, default:  Any = None) -> Any:
        """Load JSON file with error handling"""
        if not path.exists():
            return default if default is not None else {}
        
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            get_logger().warning(f"Error loading {path}: {e}")
            return default if default is not None else {}
    
    def save_json(self, path: Path, data: Any, sort_keys: bool = True) -> bool:
        """Save JSON file atomically"""
        try:
            with AtomicFileWriter(path) as f:
                json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=sort_keys)
            return True
        except Exception as e: 
            get_logger().error(f"Failed to save {path}: {e}")
            return False
    
    def load_content_map(self) -> Dict[str, str]:
        """Load existing content map"""
        content = self.load_json(self. config.content_path, {})
        get_logger().info(f"Loaded {len(content)} existing content entries")
        return content
    
    def save_content_map(self, content_map: Dict[str, str]) -> bool:
        """Save content map"""
        with self._lock:
            success = self.save_json(self.config.content_path, content_map)
            if success: 
                get_logger().debug(f"Content map saved with {len(content_map)} entries")
            return success
    
    def load_processed_verses(self) -> List[str]:
        """Load processed verses list"""
        return self.load_json(self. config.processed_verses_path, [])
    
    def save_processed_verses(self, processed_list: List[str]) -> bool:
        """Save processed verses list"""
        with self._lock:
            return self.save_json(self. config.processed_verses_path, processed_list, sort_keys=False)
    
    def load_failed_verses(self) -> Dict[str, str]:
        """Load failed verses map"""
        return self.load_json(self.config.failed_verses_path, {})
    
    def save_failed_verses(self, failed_map: Dict[str, str]) -> bool:
        """Save failed verses map"""
        with self._lock:
            return self.save_json(self.config.failed_verses_path, failed_map)
    
    def append_to_output(self, verse: str, content: str) -> bool:
        """Append to output file"""
        try:
            self.config.output_path.parent.mkdir(parents=True, exist_ok=True)
            separator = "\n" + "=" * 80 + "\n\n"
            
            with self._lock:
                with open(self.config.output_path, 'a', encoding='utf-8') as f:
                    f.write(separator + content + "\n")
            return True
        except Exception as e: 
            get_logger().error(f"Failed to append to output file: {e}")
            return False


# ============================================================================
# CONTENT GENERATORS
# ============================================================================

# Expanded full verse texts - merge with KJV/Septuagint texts for better key_phrase detection
FULL_VERSE_TEXTS: Dict[str, str] = {
    "Genesis 23:1": "And Sarah was an hundred and seven and twenty years old: these were the years of the life of Sarah.",
    "Genesis 23:2": "And Sarah died in Kirjatharba; the same is Hebron in the land of Canaan: and Abraham came to mourn for Sarah, and to weep for her.",
    # Add more as available from sources
}

# Patristic commentary pool per verse/book for deeper Orthodox depth
PATRISTICS_POOL: Dict[str, List[str]] = {
    "Genesis 23:1": [
        "Chrysostom on mourning as covenant fidelity",
        "Origen: Sarah typifies Church's eternal life",
        "Ephrem: Sarah's years as measure of virtue",
    ],
    "Genesis 23:2": [
        "Chrysostom: Abraham's mourning as model of faith through grief",
        "Ambrose: Hebron as place of covenant memory",
        "Augustine: weeping as natural response before resurrection hope",
    ],
}

VERSE_TEXTS: Dict[str, str] = FULL_VERSE_TEXTS.copy()


class ContentGenerator:
    """Generates exegetical content for verses"""
    
    def __init__(self):
        self.verse_texts = load_verse_texts(CONFIG.verses_path)
        if not self.verse_texts:
            self.verse_texts = FULL_VERSE_TEXTS.copy()
        # Merge FULL_VERSE_TEXTS into loaded texts for comprehensive coverage
        for ref, text in FULL_VERSE_TEXTS.items():
            if ref not in self.verse_texts or not self.verse_texts[ref]:
                self.verse_texts[ref] = text
    
    # Special verse titles cache
    SPECIAL_TITLES:  Dict[str, str] = {
        "Genesis 1:1": "Cosmic Creation Foundation",
        "Genesis 1:2": "Spirit Over Primordial Waters",
        "Genesis 1:3": "Divine Speech Bringing Light",
        "Genesis 1:26": "Imago Dei Foundation",
        "Genesis 1:27": "Divine Image in Humanity",
        "Genesis 2:7": "Breath of Life Formation",
        "Genesis 3:15": "Protoevangelium Promise",
        "Genesis 12:1": "Abrahamic Call Narrative",
        "Genesis 22:8": "Divine Provision Foreshadowing",
        "Exodus 3:14": "Divine Name Revelation",
        "Exodus 12:13": "Blood Protection Pattern",
        "Exodus 14:21": "Sea Crossing Salvation",
        "Exodus 19:18": "Sinai Theophany Pattern",
        "Exodus 20:1": "Decalogue Introduction",
        "Leviticus 17:11": "Blood Atonement Foundation",
        "Deuteronomy 6:4": "Shema Declaration",
        "Psalm 22:1": "Messianic Suffering Cry",
        "Psalm 23:1": "Shepherd Provision Pattern",
        "Psalm 51:1": "Penitential Prayer Model",
        "Psalm 110:1": "Messianic Enthronement",
        "Isaiah 7:14": "Virgin Birth Prophecy",
        "Isaiah 9:6": "Divine Child Names",
        "Isaiah 40:3": "Wilderness Voice Prophecy",
        "Isaiah 52:13": "Servant Exaltation Beginning",
        "Isaiah 53:5": "Suffering Servant Atonement",
        "Jeremiah 31:31": "New Covenant Promise",
        "Ezekiel 37:1": "Valley of Dry Bones Vision",
        "Daniel 7:13": "Son of Man Vision Pattern",
        "Micah 5:2": "Bethlehem Prophecy",
        "Malachi 3:1": "Messenger Preparation",
        "Matthew 1:1": "Genealogical Foundation",
        "Matthew 3:16": "Baptismal Anointing Pattern",
        "Matthew 5:3": "Beatitude Opening",
        "Matthew 16:18": "Church Foundation Declaration",
        "Matthew 26:26": "Eucharistic Institution Pattern",
        "Matthew 28:19": "Great Commission Mandate",
        "Mark 1:1": "Gospel Beginning Declaration",
        "Mark 10:45": "Ransom Purpose Statement",
        "Luke 1:35": "Incarnation Announcement",
        "Luke 2:11": "Savior Birth Proclamation",
        "Luke 24:27": "Christological Hermeneutic",
        "John 1:1": "Logos Incarnation Pattern",
        "John 1:14": "Word Made Flesh Pattern",
        "John 3:3": "New Birth Requirement",
        "John 3:16": "Divine Love Summary",
        "John 6:35": "Bread of Life Declaration",
        "John 11:25": "Resurrection and Life Declaration",
        "John 14:6": "Way-Truth-Life Pattern",
        "John 19:30": "Tetelestai Completion",
        "Acts 1:8": "Spirit Empowerment Promise",
        "Acts 2:1": "Pentecostal Outpouring Pattern",
        "Acts 2:38": "Repentance-Baptism Command",
        "Romans 1:16": "Gospel Power Declaration",
        "Romans 3:23": "Universal Sin Pattern",
        "Romans 5:8": "Divine Love Demonstration",
        "Romans 6:4": "Baptismal Death-Resurrection Pattern",
        "Romans 8:28": "Providence Assurance",
        "Romans 12:1": "Living Sacrifice Appeal",
        "1 Corinthians 11:23":  "Eucharistic Memory Pattern",
        "1 Corinthians 13:1": "Love Excellence Beginning",
        "1 Corinthians 15:3": "Gospel Core Summary",
        "2 Corinthians 5:17": "New Creation Declaration",
        "2 Corinthians 5:21": "Great Exchange Pattern",
        "Galatians 2:20": "Cruciform Identity",
        "Ephesians 2:8": "Grace-Faith Salvation",
        "Ephesians 5:25": "Bridal Love Sacrifice Pattern",
        "Philippians 2:5": "Kenotic Mind Introduction",
        "Philippians 2:6": "Kenotic Humility Pattern",
        "Colossians 1:15": "Cosmic Christ Pattern",
        "Colossians 1:16": "Christ as Creator",
        "1 Timothy 3:16": "Mystery of Godliness",
        "2 Timothy 3:16": "Scripture Inspiration",
        "Hebrews 1:1": "Progressive Revelation Pattern",
        "Hebrews 1:3": "Divine Radiance Pattern",
        "Hebrews 4:12": "Living Word Pattern",
        "Hebrews 9:12": "Heavenly Tabernacle Pattern",
        "Hebrews 11:1": "Faith Definition",
        "James 1:17": "Divine Giving Pattern",
        "1 Peter 2:9": "Royal Priesthood Identity",
        "1 John 1:9": "Confession-Cleansing Promise",
        "1 John 4:8": "God Is Love Declaration",
        "Revelation 1:8": "Alpha-Omega Declaration",
        "Revelation 4:8": "Trisagion Worship Pattern",
        "Revelation 21:1": "New Creation Vision",
        "Revelation 22:13": "Alpha-Omega Fulfillment Pattern",
        "Revelation 22:20": "Maranatha Conclusion"
    }
    
    def __init__(self):
        self._category_titles = self._build_category_titles()
        self._sensory_sets = self._build_sensory_sets()
    
    @staticmethod
    def _build_category_titles() -> Dict[BookCategory, List[str]]:
        """Build category-based title templates"""
        return {
            BookCategory.PENTATEUCH: [
                "{book} Covenant Foundation",
                "Torah Instruction in {book} {chapter}",
                "Divine Law Pattern in {book}",
                "Covenant Narrative in {book}",
                "Foundational Pattern from {book}"
            ],
            BookCategory. HISTORICAL: [
                "{book} Kingdom Narrative",
                "Historical Witness in {book} {chapter}",
                "Divine Faithfulness in {book}",
                "Covenant History Pattern",
                "Redemptive History in {book}"
            ],
            BookCategory. POETIC: [
                "{book} Wisdom Pattern",
                "Poetic Theology in {book} {chapter}",
                "Contemplative Pattern in {book}",
                "Worship Pattern from {book}",
                "Sapiential Reflection in {book}"
            ],
            BookCategory.MAJOR_PROPHET: [
                "{book} Prophetic Declaration",
                "Divine Oracle in {book} {chapter}",
                "Prophetic Vision in {book}",
                "Covenant Lawsuit in {book}",
                "Eschatological Hope in {book}"
            ],
            BookCategory.MINOR_PROPHET: [
                "{book} Prophetic Word",
                "Divine Message in {book}",
                "Prophetic Witness from {book}",
                "Covenant Call in {book}",
                "Day of the Lord Pattern in {book}"
            ],
            BookCategory.GOSPEL: [
                "{book} Gospel Witness",
                "Christ Revelation in {book} {chapter}",
                "Kingdom Pattern in {book}",
                "Messianic Fulfillment in {book}",
                "Incarnate Word in {book}"
            ],
            BookCategory.ACTS: [
                "Apostolic Mission Pattern",
                "Spirit Movement in Acts {chapter}",
                "Church Formation Narrative",
                "Gospel Expansion Pattern",
                "Pentecostal Church Pattern"
            ],
            BookCategory.PAULINE:  [
                "{book} Apostolic Instruction",
                "Pauline Theology in {book}",
                "Gospel Application in {book}",
                "Church Formation in {book}",
                "Christological Ethics in {book}"
            ],
            BookCategory.GENERAL_EPISTLE: [
                "{book} Apostolic Exhortation",
                "Catholic Instruction in {book}",
                "Faith Formation in {book}",
                "Community Ethics in {book}",
                "Practical Wisdom in {book}"
            ],
            BookCategory.APOCALYPTIC: [
                "Apocalyptic Vision Pattern",
                "Revelation Vision in Chapter {chapter}",
                "Eschatological Fulfillment Pattern",
                "New Creation Vision",
                "Divine Victory Pattern"
            ],
            BookCategory.DEUTEROCANONICAL: [
                "{book} Wisdom Pattern",
                "Intertestamental Witness in {book}",
                "Second Temple Theology in {book}",
                "Hellenistic Jewish Wisdom in {book}",
                "Deuterocanonical Pattern in {book}"
            ],
            BookCategory.UNKNOWN: [
                "{book} Theological Pattern"
            ]
        }
    
    @staticmethod
    def _build_sensory_sets() -> Dict[BookCategory, Dict[str, List[str]]]: 
        """Build sensory vocabulary sets by category"""
        return {
            BookCategory.PENTATEUCH:  {
                "visual": [
                    "primordial darkness giving way to light",
                    "pillar of fire illuminating wilderness",
                    "mountain shrouded in smoke and glory"
                ],
                "auditory": [
                    "thunderous divine voice from Sinai",
                    "still whisper in sacred silence",
                    "trumpet blast announcing presence"
                ],
                "tactile": [
                    "stone tablets cold with commandment",
                    "desert sand beneath pilgrim feet",
                    "blood warm on doorpost wood"
                ],
                "olfactory": [
                    "incense rising as prayer",
                    "burnt offering smoke ascending",
                    "manna sweet in morning dew"
                ],
                "kinesthetic": [
                    "prostration before holiness",
                    "processional movement toward promise",
                    "hand raised in covenant oath"
                ]
            },
            BookCategory.HISTORICAL: {
                "visual": [
                    "crown glinting in throne room light",
                    "battle standard raised over conquest",
                    "temple gold reflecting lamplight"
                ],
                "auditory": [
                    "war trumpet summoning warriors",
                    "coronation shout echoing",
                    "prophetic oracle piercing silence"
                ],
                "tactile": [
                    "sword hilt firm in grip",
                    "anointing oil flowing over head",
                    "scepter weight of authority"
                ],
                "olfactory": [
                    "battlefield iron and dust",
                    "feast preparation aromas",
                    "cedar of palace construction"
                ],
                "kinesthetic": [
                    "march cadence toward battle",
                    "bowing before royal presence",
                    "dance of victory celebration"
                ]
            },
            BookCategory.POETIC: {
                "visual":  [
                    "shepherd's green pastures stretching",
                    "tears glistening on night pillow",
                    "morning light breaking over mountains"
                ],
                "auditory": [
                    "harp strings vibrating praise",
                    "groaning too deep for words",
                    "creation's silent testimony"
                ],
                "tactile": [
                    "rod and staff reassuring touch",
                    "dust of mortality beneath",
                    "embrace of divine comfort"
                ],
                "olfactory": [
                    "anointing oil fragrant excess",
                    "tears salt on lips",
                    "earth after rain renewing"
                ],
                "kinesthetic": [
                    "soul lifted in praise",
                    "knees bent in supplication",
                    "heart expanding with joy"
                ]
            },
            BookCategory.MAJOR_PROPHET: {
                "visual": [
                    "throne room vision overwhelming",
                    "valley of dry bones stretching",
                    "suffering servant marred beyond recognition"
                ],
                "auditory": [
                    "seraphim crying holy",
                    "prophetic commission voice",
                    "lament echoing through ruins"
                ],
                "tactile": [
                    "coal burning lips clean",
                    "scroll bitter-sweet consuming",
                    "chains of exile heavy"
                ],
                "olfactory": [
                    "temple incense filling space",
                    "destruction's acrid smoke",
                    "new creation freshness promised"
                ],
                "kinesthetic": [
                    "falling before glory",
                    "standing to prophesy",
                    "walking through vision landscape"
                ]
            },
            BookCategory.MINOR_PROPHET: {
                "visual":  [
                    "locusts darkening sky",
                    "plumb line measuring wall",
                    "day of the Lord darkness"
                ],
                "auditory": [
                    "lion roar of judgment",
                    "trumpet warning blast",
                    "restoration song beginning"
                ],
                "tactile": [
                    "earthquake foundation shaking",
                    "wind of Spirit moving",
                    "rain of blessing falling"
                ],
                "olfactory": [
                    "sacrifice smoke ascending",
                    "drought dust choking",
                    "harvest abundance fragrance"
                ],
                "kinesthetic": [
                    "running from divine call",
                    "returning with repentance",
                    "leaping in restoration joy"
                ]
            },
            BookCategory.GOSPEL: {
                "visual": [
                    "Jesus' face shining transfigured",
                    "crowd pressing close",
                    "cross silhouetted against darkness"
                ],
                "auditory": [
                    "authoritative teaching voice",
                    "storm stilled by command",
                    "cry of dereliction piercing"
                ],
                "tactile": [
                    "healing touch restoring",
                    "bread broken in hands",
                    "nails piercing flesh"
                ],
                "olfactory": [
                    "ointment poured extravagant",
                    "tomb spices prepared",
                    "fish grilling on shore"
                ],
                "kinesthetic": [
                    "walking on water faith",
                    "kneeling in garden anguish",
                    "rising from death triumphant"
                ]
            },
            BookCategory.ACTS: {
                "visual": [
                    "tongues of fire descending",
                    "light blinding on Damascus road",
                    "vision sheet descending"
                ],
                "auditory": [
                    "rushing wind filling house",
                    "speaking in other tongues",
                    "earthquake shaking prison"
                ],
                "tactile": [
                    "hands laying for Spirit",
                    "chains falling from wrists",
                    "shipwreck waves battering"
                ],
                "olfactory": [
                    "baptismal water freshness",
                    "prison mustiness giving way",
                    "journey dust of mission"
                ],
                "kinesthetic": [
                    "standing to preach boldly",
                    "running to share good news",
                    "sailing toward unknown mission"
                ]
            },
            BookCategory.PAULINE:  {
                "visual": [
                    "veil removed seeing glory",
                    "armor of God gleaming",
                    "letter ink on parchment"
                ],
                "auditory": [
                    "gospel proclaimed clearly",
                    "tongues and prophecy sounding",
                    "trumpet of resurrection calling"
                ],
                "tactile": [
                    "thorn in flesh pressing",
                    "embrace of reconciliation",
                    "seal of Spirit marking"
                ],
                "olfactory": [
                    "fragrance of Christ spreading",
                    "sacrifice aroma pleasing",
                    "freedom freshness breathing"
                ],
                "kinesthetic": [
                    "running race with endurance",
                    "fighting good fight",
                    "standing firm in truth"
                ]
            },
            BookCategory.GENERAL_EPISTLE: {
                "visual": [
                    "mirror reflecting true self",
                    "crown of life gleaming",
                    "judge standing at door"
                ],
                "auditory": [
                    "word implanted hearing",
                    "prayer of faith rising",
                    "warning against error sounding"
                ],
                "tactile": [
                    "fire testing faith",
                    "living stones built together",
                    "hand of fellowship extended"
                ],
                "olfactory": [
                    "incense prayers ascending",
                    "world's corruption avoided",
                    "grace freshness received"
                ],
                "kinesthetic": [
                    "enduring under trial",
                    "approaching throne boldly",
                    "resisting devil firmly"
                ]
            },
            BookCategory.APOCALYPTIC: {
                "visual": [
                    "throne room glory blazing",
                    "Lamb standing as slain",
                    "New Jerusalem descending"
                ],
                "auditory": [
                    "thunder voices proclaiming",
                    "heavenly choir singing",
                    "final trumpet sounding"
                ],
                "tactile": [
                    "scroll unsealed opening",
                    "white robes soft with victory",
                    "tears wiped away forever"
                ],
                "olfactory": [
                    "incense prayers of saints",
                    "sulfur judgment descending",
                    "tree of life fragrance healing"
                ],
                "kinesthetic": [
                    "falling before throne",
                    "standing among multitude",
                    "reigning forever with Christ"
                ]
            },
            BookCategory.DEUTEROCANONICAL: {
                "visual": [
                    "wisdom radiance shining",
                    "temple rededication lights",
                    "angel guide appearing"
                ],
                "auditory": [
                    "prayer ascending heard",
                    "wisdom calling in streets",
                    "thanksgiving hymn rising"
                ],
                "tactile": [
                    "healing touch applying",
                    "scroll wisdom grasping",
                    "journey hardship enduring"
                ],
                "olfactory": [
                    "incense prayer rising",
                    "feast celebration aromas",
                    "tomb preparation spices"
                ],
                "kinesthetic": [
                    "bowing in prayer",
                    "walking in wisdom's way",
                    "dancing in celebration"
                ]
            }
        }
    
    def generate_title(self, ref: VerseReference) -> str:
        """Generate thematic title for verse"""
        # Check special titles first
        if ref.original in self. SPECIAL_TITLES:
            return self.SPECIAL_TITLES[ref.original]
        
        # Get category titles
        titles = self._category_titles.get(ref.category, self._category_titles[BookCategory.UNKNOWN])
        
        # Select based on verse position for consistency
        idx = (ref.chapter + ref.verse) % len(titles)
        template = titles[idx]
        
        return template.format(book=ref. book, chapter=ref.chapter)
    
    def generate_literal_analysis(self, ref: VerseReference) -> str:
        """Generate literal sense analysis"""
        category = ref.category
        
        analyses = {
            BookCategory. PENTATEUCH: [
                f"Foundational Torah instruction in {ref.book} {ref.chapter}:{ref.verse} establishing covenantal patterns that shape Israel's identity and relationship with YHWH through specific command, narrative context, and theological significance within the Mosaic revelation.",
                f"Primordial or patriarchal narrative in {ref.book} {ref. chapter}:{ref.verse} grounding Israel's self-understanding in divine action and promise, establishing patterns of faith, obedience, and covenant relationship that form the theological bedrock of Scripture.",
                f"Legal and ritual instruction in {ref.book} {ref.chapter}:{ref.verse} establishing Israel's unique covenant identity through specific command, contextual application, and theological rationale within the wilderness generation's formation."
            ],
            BookCategory. HISTORICAL: [
                f"Historical narrative in {ref.book} {ref.chapter}:{ref.verse} recording God's faithfulness to covenant promises through concrete events, character development, and divine intervention in national history, demonstrating the outworking of blessing and curse according to covenant fidelity.",
                f"Royal or judicial narrative in {ref.book} {ref.chapter}:{ref.verse} examining leadership under YHWH's covenant, with specific events serving as theological commentary on faithfulness, judgment, and the need for perfect kingship.",
                f"Post-exilic restoration narrative in {ref.book} {ref.chapter}:{ref.verse} demonstrating God's faithfulness to return His people while establishing patterns of worship, identity, and hope that prepare for messianic fulfillment."
            ],
            BookCategory.POETIC: [
                f"Poetic expression in {ref.book} {ref.chapter}:{ref.verse} of human experience before God through metaphor, parallelism, and emotional language that invites reader participation in theological reflection and worship response.",
                f"Wisdom instruction in {ref.book} {ref.chapter}:{ref.verse} grounding practical ethics in creation order and fear of the Lord, with specific teachings applicable across cultural contexts while maintaining theological depth.",
                f"Hymnic or lament expression in {ref.book} {ref.chapter}:{ref.verse} providing liturgical language for Israel's worship, shaping communal and individual response to divine action through structured poetic forms."
            ],
            BookCategory.MAJOR_PROPHET: [
                f"Prophetic oracle in {ref.book} {ref.chapter}:{ref.verse} declaring God's word to specific historical circumstances while pointing toward future fulfillment, combining judgment announcement with restoration hope.",
                f"Vision or symbolic action in {ref.book} {ref.chapter}:{ref.verse} communicating divine truth through dramatic imagery that transcends immediate historical context while remaining grounded in covenant relationship.",
                f"Covenant lawsuit or salvation oracle in {ref.book} {ref.chapter}:{ref.verse} addressing Israel's unfaithfulness while proclaiming YHWH's ultimate redemptive purpose that will overcome human failure."
            ],
            BookCategory.MINOR_PROPHET:  [
                f"Prophetic word in {ref.book} {ref.chapter}:{ref.verse} addressing specific community circumstances with covenant enforcement, calling for repentance while announcing either judgment or restoration according to divine purpose.",
                f"Day of the Lord proclamation in {ref.book} {ref.chapter}:{ref.verse} pointing toward divine intervention in history, with immediate and eschatological dimensions woven together in prophetic declaration.",
                f"Restoration promise in {ref.book} {ref.chapter}:{ref.verse} announcing hope beyond judgment, with specific details grounding future expectation in covenant faithfulness."
            ],
            BookCategory.GOSPEL: [
                f"Gospel narrative in {ref.book} {ref.chapter}:{ref.verse} revealing Christ's identity and mission through specific action, teaching, or encounter that demonstrates the kingdom of God's presence and invitation.",
                f"Dominical teaching in {ref.book} {ref.chapter}:{ref.verse} presenting Jesus' authoritative instruction on kingdom life, ethics, or theological truth with immediate application for disciples and enduring significance for the Church.",
                f"Passion or resurrection narrative in {ref.book} {ref.chapter}:{ref.verse} recording the climactic events of Christ's saving work with theological interpretation woven through historical account."
            ],
            BookCategory.ACTS: [
                f"Historical-theological narrative in Acts {ref.chapter}:{ref.verse} recording the early Church's formation and mission through Spirit empowerment, apostolic witness, and divine guidance across cultural boundaries.",
                f"Apostolic preaching or mission account in Acts {ref.chapter}:{ref. verse} demonstrating the gospel's power to transform individuals and communities while establishing patterns for ongoing church life.",
                f"Church conflict or resolution narrative in Acts {ref.chapter}:{ref.verse} showing the Spirit's guidance in addressing challenges while maintaining unity and advancing the gospel witness."
            ],
            BookCategory.PAULINE: [
                f"Apostolic instruction in {ref.book} {ref.chapter}:{ref.verse} addressing specific community challenges while developing theological foundations for Christian identity, practice, and hope.",
                f"Doctrinal exposition in {ref.book} {ref.chapter}:{ref.verse} articulating the gospel's implications for understanding God, Christ, salvation, or Christian life with logical argumentation and scriptural support.",
                f"Ethical exhortation in {ref.book} {ref.chapter}:{ref.verse} applying gospel truth to concrete situations, with specific commands grounded in theological indicatives of identity in Christ."
            ],
            BookCategory.GENERAL_EPISTLE: [
                f"Catholic instruction in {ref.book} {ref.chapter}:{ref.verse} addressing practical challenges of Christian community life through ethical exhortation, doctrinal correction, or encouragement in trials.",
                f"Wisdom exhortation in {ref.book} {ref.chapter}:{ref. verse} combining Jewish ethical tradition with Christian confession to form communities of faith, hope, and love.",
                f"Apologetic or polemical instruction in {ref.book} {ref.chapter}:{ref.verse} defending orthodox faith against false teaching while encouraging perseverance in sound doctrine."
            ],
            BookCategory.APOCALYPTIC: [
                f"Apocalyptic vision in Revelation {ref.chapter}:{ref.verse} disclosing Christ's ultimate victory and cosmic renewal through symbolic imagery that interprets present suffering in light of future hope.",
                f"Heavenly worship scene in Revelation {ref.chapter}:{ref.verse} revealing the eternal dimension of reality where God and the Lamb receive continuous praise, providing context for earthly perseverance.",
                f"Prophetic proclamation in Revelation {ref.chapter}:{ref.verse} combining Old Testament imagery with Christological interpretation to announce divine judgment and salvation."
            ],
            BookCategory. DEUTEROCANONICAL: [
                f"Wisdom instruction in {ref.book} {ref.chapter}:{ref.verse} reflecting Second Temple Jewish piety and theological reflection, bridging Testaments with ethical teaching grounded in creation and covenant.",
                f"Historical narrative in {ref.book} {ref.chapter}:{ref.verse} recording divine faithfulness during the intertestamental period, demonstrating continuity of God's care for His people.",
                f"Devotional or liturgical text in {ref.book} {ref.chapter}:{ref.verse} providing language and patterns for Jewish worship and piety that shaped the context for New Testament faith."
            ]
        }
        
        options = analyses.get(category, [f"Context-specific meaning for {ref.original} grounded in its literary genre, historical setting, and narrative function. "])
        idx = (ref.chapter * ref.verse) % len(options)
        return options[idx]
    
    def generate_allegorical_analysis(self, ref: VerseReference) -> str:
        """Generate Christological allegorical interpretation"""
        category = ref.category
        
        analyses = {
            BookCategory. PENTATEUCH: [
                f"Prefigures Christ's redemptive work through {ref.book}'s covenant pattern, with specific elements serving as types that find fulfillment in His person, offices, and saving acts.",
                f"Anticipates the new exodus in Christ through {ref.book}'s liberation narrative, establishing patterns of bondage, divine intervention, and covenant formation fulfilled in the gospel.",
                f"Foreshadows Christ as the true Temple through {ref.book}'s tabernacle/worship instructions, with sacrificial and priestly elements pointing to His once-for-all offering."
            ],
            BookCategory. HISTORICAL: [
                f"Prefigures Christ as the true Davidic King through {ref.book}'s monarchy narrative, with faithful and failed kings alike pointing to the need for and character of perfect kingship.",
                f"Anticipates Christ's victory through {ref.book}'s conquest and battle narratives, establishing patterns of divine warfare and rest that find fulfillment in His triumph over sin and death.",
                f"Foreshadows the Church through {ref.book}'s community formation, with patterns of gathering, worship, and identity preparation for the new covenant people."
            ],
            BookCategory.POETIC: [
                f"Prefigures Christ as divine Wisdom through {ref.book}'s sapiential tradition, with wisdom's characteristics and work fulfilled in Him who is the wisdom of God.",
                f"Anticipates Christ's suffering and vindication through {ref.book}'s lament and praise patterns, with the righteous sufferer's experience typologically fulfilled in His passion and exaltation.",
                f"Foreshadows the Church's worship through {ref.book}'s hymnic tradition, with praise patterns finding their ultimate object and expression in Christ-centered doxology."
            ],
            BookCategory.MAJOR_PROPHET: [
                f"Prophetically declares Christ through {ref.book}'s messianic oracles, with specific predictions and patterns finding fulfillment in His advent, ministry, and glorification.",
                f"Anticipates the new covenant in Christ through {ref.book}'s restoration promises, with prophetic vision of renewed relationship fulfilled in His mediation.",
                f"Prefigures Christ's judgment and salvation through {ref.book}'s day-of-the-Lord imagery, with prophetic patterns fulfilled in His first and second advents."
            ],
            BookCategory.MINOR_PROPHET:  [
                f"Points to Christ through {ref.book}'s covenant enforcement, with patterns of judgment and mercy fulfilled in His atoning work and coming kingdom.",
                f"Anticipates Christ's universal reign through {ref.book}'s nations oracles, with prophetic vision of Gentile inclusion fulfilled in the gospel's expansion.",
                f"Foreshadows Christ's restoration work through {ref.book}'s renewal promises, with specific hopes fulfilled in His redemptive accomplishment."
            ],
            BookCategory.GOSPEL: [
                f"Reveals Christ directly in {ref.book}'s narrative, with each detail serving theological purpose in presenting His identity, mission, and saving significance.",
                f"Fulfills Old Testament patterns in {ref.book}'s presentation of Jesus, with specific correspondences demonstrating Scripture's unified witness to Christ.",
                f"Establishes Christ as the interpretive key in {ref.book}'s theological narrative, with His words and works defining the meaning of all Scripture."
            ],
            BookCategory.ACTS: [
                f"Demonstrates Christ's continuing work through Acts' Spirit narrative, with apostolic mission extending His presence and kingdom authority.",
                f"Reveals Christ's exaltation through Acts' apostolic preaching, with resurrection proclamation as the theological center of early Christian witness.",
                f"Fulfills Christ's commission through Acts' geographical expansion, with gospel advance demonstrating His lordship over all peoples and places."
            ],
            BookCategory.PAULINE: [
                f"Exposits Christ's person and work through {ref.book}'s theological argument, with doctrinal formulation serving the gospel's proclamation and application.",
                f"Applies Christ's redemption through {ref.book}'s ethical instruction, with moral exhortation grounded in union with Christ and Spirit empowerment.",
                f"Anticipates Christ's return through {ref.book}'s eschatological teaching, with present Christian life oriented toward future consummation."
            ],
            BookCategory.GENERAL_EPISTLE: [
                f"Applies Christ's lordship through {ref.book}'s practical instruction, with ethical exhortation grounded in His example and coming judgment.",
                f"Defends Christ's sufficiency through {ref.book}'s apologetic argument, with false teaching refuted by appeal to His complete saving work.",
                f"Encourages perseverance in Christ through {ref.book}'s exhortation, with suffering interpreted through His passion and promised vindication."
            ],
            BookCategory.APOCALYPTIC: [
                f"Reveals Christ's triumph through Revelation's symbolic vision, with apocalyptic imagery disclosing His ultimate victory and eternal reign.",
                f"Anticipates Christ's return through Revelation's prophetic declaration, with present persecution interpreted in light of coming vindication.",
                f"Celebrates Christ's worthiness through Revelation's heavenly worship, with doxological scenes revealing the eternal significance of His redemption."
            ],
            BookCategory.DEUTEROCANONICAL:  [
                f"Anticipates Christ through {ref.book}'s wisdom tradition, with Second Temple theological development preparing for Logos incarnation.",
                f"Foreshadows Christ's victory through {ref.book}'s faithful resistance narrative, with patterns of suffering and vindication fulfilled in His passion.",
                f"Prefigures the Church through {ref.book}'s diaspora community, with identity maintenance in hostile culture anticipating Christian pilgrimage."
            ]
        }
        
        options = analyses.get(category, [f"Christological typology emerging from {ref.original} that finds fulfillment in Christ's person and work. "])
        idx = (ref. chapter + ref.verse * 2) % len(options)
        return options[idx]
    
    def generate_tropological_analysis(self, ref:  VerseReference) -> str:
        """Generate moral formation (tropological) analysis"""
        category = ref.category
        
        analyses = {
            BookCategory.PENTATEUCH: [
                f"Forms covenant fidelity through {ref.book}'s instruction, shaping habits of reverence, obedience, and communal responsibility that reflect identity as God's people.",
                f"Cultivates holiness through {ref.book}'s purity teaching, forming practices of separation from sin and dedication to God that manifest covenant relationship.",
                f"Shapes memory and gratitude through {ref.book}'s narrative, forming habits of recalling God's faithfulness and responding with thanksgiving and trust."
            ],
            BookCategory.HISTORICAL: [
                f"Forms discernment through {ref.book}'s leadership narrative, cultivating wisdom to recognize faithful and unfaithful patterns and choose accordingly.",
                f"Shapes perseverance through {ref.book}'s conflict narrative, forming habits of trust in divine deliverance through prolonged difficulty and opposition.",
                f"Cultivates hope through {ref.book}'s restoration narrative, forming expectation of God's redemptive action even after failure and judgment."
            ],
            BookCategory.POETIC: [
                f"Forms emotional honesty before God through {ref.book}'s expression, cultivating habits of bringing the full range of human experience into prayerful dialogue.",
                f"Shapes wisdom and prudence through {ref.book}'s instruction, forming habits of discernment that navigate life's complexity with godly understanding.",
                f"Cultivates worship through {ref.book}'s doxological patterns, forming habits of praise, thanksgiving, and adoration that orient the heart toward God."
            ],
            BookCategory.MAJOR_PROPHET: [
                f"Forms prophetic courage through {ref.book}'s proclamation, cultivating habits of speaking truth regardless of opposition and maintaining hope amid judgment.",
                f"Shapes repentance through {ref.book}'s covenant lawsuit, forming habits of self-examination, confession, and return to God in response to divine word.",
                f"Cultivates justice advocacy through {ref.book}'s social critique, forming habits of defending the vulnerable and challenging systemic oppression."
            ],
            BookCategory.MINOR_PROPHET:  [
                f"Forms responsive hearing through {ref.book}'s prophetic call, cultivating habits of attentiveness to God's word and immediate obedience.",
                f"Shapes eschatological awareness through {ref.book}'s day-of-the-Lord teaching, forming habits of living in light of divine judgment and hope.",
                f"Cultivates covenant loyalty through {ref.book}'s restoration promise, forming habits of faithful endurance grounded in God's ultimate purposes."
            ],
            BookCategory.GOSPEL: [
                f"Forms Christlike character through {ref.book}'s narrative, cultivating habits of compassion, forgiveness, sacrificial love, and kingdom allegiance.",
                f"Shapes discipleship through {ref.book}'s teaching, forming habits of following Jesus in concrete obedience and communal accountability.",
                f"Cultivates faith through {ref.book}'s miracle and encounter narratives, forming habits of trust in Jesus' power and willingness to save."
            ],
            BookCategory.ACTS: [
                f"Forms missional courage through Acts' apostolic witness, cultivating habits of bold proclamation and willingness to suffer for the gospel.",
                f"Shapes communal generosity through Acts' church life narrative, forming habits of sharing resources and caring for community members.",
                f"Cultivates Spirit-dependence through Acts' empowerment narrative, forming habits of prayer, waiting, and responsive obedience to divine leading."
            ],
            BookCategory.PAULINE: [
                f"Forms cruciform identity through {ref.book}'s gospel application, cultivating habits of self-denial, other-centeredness, and participation in Christ's sufferings.",
                f"Shapes communal unity through {ref.book}'s church instruction, forming habits of mutual submission, diverse gifting, and shared mission.",
                f"Cultivates hope through {ref.book}'s eschatological teaching, forming habits of patient endurance and joyful anticipation of Christ's return."
            ],
            BookCategory.GENERAL_EPISTLE: [
                f"Forms perseverance through {ref.book}'s exhortation, cultivating habits of faithful endurance in trials and resistance to apostasy.",
                f"Shapes practical wisdom through {ref.book}'s ethical instruction, forming habits of speech, relationship, and resource use that honor God.",
                f"Cultivates doctrinal discernment through {ref.book}'s teaching, forming habits of testing claims against apostolic truth and rejecting error."
            ],
            BookCategory.APOCALYPTIC: [
                f"Forms faithful witness through Revelation's martyr theology, cultivating habits of testimony maintenance even unto death.",
                f"Shapes worship resistance through Revelation's anti-idolatry theme, forming habits of exclusive allegiance to God and the Lamb.",
                f"Cultivates patient hope through Revelation's victory vision, forming habits of perseverance grounded in certainty of Christ's triumph."
            ],
            BookCategory.DEUTEROCANONICAL:  [
                f"Forms wisdom virtue through {ref.book}'s instruction, cultivating habits of prudent living grounded in fear of the Lord.",
                f"Shapes faithful resistance through {ref.book}'s persecution narrative, forming habits of identity maintenance amid cultural pressure.",
                f"Cultivates prayerful dependence through {ref.book}'s devotional patterns, forming habits of petition, confession, and trust."
            ]
        }
        
        options = analyses.get(category, [f"Moral formation from {ref.original} shaping habits of virtue and godly character."])
        idx = (ref.chapter * 3 + ref.verse) % len(options)
        return options[idx]
    
    def generate_anagogical_analysis(self, ref: VerseReference) -> str:
        """Generate eschatological (anagogical) analysis"""
        category = ref. category
        
        analyses = {
            BookCategory.PENTATEUCH: [
                f"Orients hope toward new creation through {ref.book}'s foundational patterns, with creation, covenant, and land promises finding ultimate fulfillment in the eternal state.",
                f"Anticipates final rest through {ref.book}'s conquest narrative, with land inheritance pointing toward the heavenly country.",
                f"Points to glorified community through {ref.book}'s people-formation narrative, with covenant assembly fulfilled in the heavenly Jerusalem."
            ],
            BookCategory. POETIC: [
                f"Orients hope toward eternal praise through {ref.book}'s worship patterns, with temporal doxology anticipating unending heavenly worship.",
                f"Anticipates vindication through {ref.book}'s lament resolution, with present suffering interpreted in light of eschatological justice.",
                f"Points to fulfilled desire through {ref.book}'s longing expressions, with human yearning finding satisfaction in eternal divine presence."
            ],
            BookCategory.MAJOR_PROPHET:  [
                f"Orients hope toward new creation through {ref.book}'s restoration oracles, with prophetic vision of renewed cosmos fulfilled in Revelation's consummation.",
                f"Anticipates resurrection through {ref.book}'s restoration-from-death imagery, with prophetic metaphor finding literal fulfillment in bodily resurrection.",
                f"Points to nations' ingathering through {ref.book}'s universal scope, with prophetic vision fulfilled in the countless multitude before the throne."
            ],
            BookCategory.MINOR_PROPHET: [
                f"Orients hope toward the Day of the Lord through {ref.book}'s eschatological proclamation, with judgment and salvation finding ultimate expression in Christ's return.",
                f"Anticipates cosmic restoration through {ref.book}'s creation renewal imagery, with prophetic vision fulfilled in new heavens and new earth.",
                f"Points to universal worship through {ref.book}'s nations oracles, with prophetic expectation fulfilled in every tribe and tongue gathered in praise."
            ],
            BookCategory.GOSPEL: [
                f"Orients hope toward Christ's return through {ref.book}'s eschatological teaching, with kingdom inauguration pointing toward consummation.",
                f"Anticipates resurrection through {ref.book}'s miracle and raising narratives, with Jesus' power over death guaranteeing believers' resurrection.",
                f"Points to eternal feast through {ref.book}'s table fellowship, with meals anticipating the marriage supper of the Lamb."
            ],
            BookCategory. ACTS: [
                f"Orients hope toward Christ's return through Acts' ascension and promise, with apostolic preaching proclaiming His coming again.",
                f"Anticipates global completion through Acts' mission expansion, with gospel advance pointing toward the full number of the saved.",
                f"Points to Spirit's consummation through Acts' Pentecost, with first-fruits empowerment anticipating full harvest of resurrection life."
            ],
            BookCategory.PAULINE: [
                f"Orients hope toward resurrection through {ref.book}'s eschatological teaching, with present transformation anticipating glorified existence.",
                f"Anticipates Christ's return through {ref.book}'s parousia expectation, with ethical exhortation grounded in imminent hope.",
                f"Points to eternal inheritance through {ref.book}'s adoption theology, with present Spirit-possession guaranteeing future glory."
            ],
            BookCategory.GENERAL_EPISTLE:  [
                f"Orients hope toward inheritance through {ref.book}'s promise emphasis, with present trials interpreted in light of eternal reward.",
                f"Anticipates judgment through {ref.book}'s accountability teaching, with moral exhortation grounded in eschatological reckoning.",
                f"Points to divine encounter through {ref.book}'s holiness emphasis, with present purification preparing for face-to-face vision."
            ],
            BookCategory.APOCALYPTIC: [
                f"Directly depicts eschatological consummation through Revelation's vision, with symbolic imagery revealing the ultimate destiny of creation and humanity.",
                f"Orients hope toward New Jerusalem through Revelation's city vision, with present pilgrimage directed toward eternal dwelling with God.",
                f"Anticipates eternal reign through Revelation's throne room scenes, with worship anticipating unending communion with the Lamb."
            ],
            BookCategory.DEUTEROCANONICAL:  [
                f"Orients hope toward resurrection through {ref.book}'s afterlife teaching, with Second Temple development preparing for New Testament fullness.",
                f"Anticipates vindication through {ref.book}'s martyr theology, with righteous suffering interpreted in light of eternal reward.",
                f"Points to wisdom's triumph through {ref.book}'s cosmic scope, with present pursuit anticipating eternal possession of divine wisdom."
            ]
        }
        
        options = analyses. get(category, [f"Eschatological hope emerging from {ref.original} pointing toward ultimate fulfillment. "])
        idx = (ref. chapter + ref.verse * 3) % len(options)
        return options[idx]
    
    def generate_liturgical_connection(self, ref: VerseReference) -> str:
        """Generate liturgical connection"""
        category = ref.category
        
        connections = {
            BookCategory. PENTATEUCH: [
                "Paschal Vigil reading connecting creation/exodus to baptismal regeneration",
                "Lenten lectionary emphasizing covenant renewal and repentance themes",
                "Easter season reading connecting liberation to resurrection freedom",
                "Ordinary Time instruction on covenant life and faithful obedience"
            ],
            BookCategory.HISTORICAL: [
                "Advent lectionary anticipating the coming Davidic King",
                "Kingdomtide readings on divine sovereignty and human stewardship",
                "Saints' day connections with faithful witnesses from Israel's history",
                "Ordinary Time instruction on God's faithfulness through history"
            ],
            BookCategory.POETIC: [
                "Daily Office psalmody shaping the Church's prayer rhythm",
                "Responsorial psalm connecting Old Testament reading to Gospel",
                "Funeral liturgy providing language for grief and resurrection hope",
                "Festal celebration expressing appropriate joy and thanksgiving"
            ],
            BookCategory.MAJOR_PROPHET: [
                "Advent lectionary proclaiming messianic expectation and preparation",
                "Holy Week readings connecting prophetic suffering to Christ's passion",
                "Lenten call to repentance through prophetic covenant lawsuit",
                "Easter proclamation of new covenant and restoration fulfillment"
            ],
            BookCategory.MINOR_PROPHET: [
                "Advent preparation through prophetic announcement themes",
                "Lenten repentance emphasis through prophetic call to return",
                "Justice and mercy themes for Ordinary Time ethical formation",
                "Eschatological hope for kingdom season anticipation"
            ],
            BookCategory.GOSPEL: [
                "Sunday Gospel proclamation as liturgical centerpiece",
                "Feast day Gospel specific to celebration (Nativity, Epiphany, etc.)",
                "Holy Week passion narrative for Triduum observance",
                "Easter season resurrection appearances and commissioning"
            ],
            BookCategory.ACTS: [
                "Easter season second reading tracing Church's Spirit-empowered birth",
                "Pentecost celebration of Spirit's descent and Church formation",
                "Apostles' feast days connecting to their Acts narratives",
                "Mission emphasis connecting to evangelization and witness"
            ],
            BookCategory.PAULINE: [
                "Epistle reading providing apostolic instruction for gathered assembly",
                "Baptismal liturgy connecting to union with Christ theology",
                "Eucharistic liturgy drawing on Lord's Supper institution and theology",
                "Ordination liturgy connecting to ministry and gift theology"
            ],
            BookCategory.GENERAL_EPISTLE:  [
                "Epistle reading for ethical formation of the assembly",
                "Baptismal instruction connecting to new birth and identity themes",
                "Suffering and persecution contexts providing comfort and exhortation",
                "Doctrinal instruction defending faith against error"
            ],
            BookCategory. APOCALYPTIC: [
                "Christ the King celebration of Lamb's sovereignty",
                "All Saints/All Souls connection to heavenly worship and faithful dead",
                "Advent eschatological expectation and watchfulness themes",
                "Easter Vigil new creation and victory proclamation"
            ],
            BookCategory.DEUTEROCANONICAL: [
                "Funeral liturgy drawing on resurrection hope themes",
                "Lenten instruction on prayer, fasting, and almsgiving",
                "Marian feast connections where applicable",
                "Wisdom literature instruction for Ordinary Time formation"
            ]
        }
        
        options = connections.get(category, ["Liturgical reading connecting Scripture to worship assembly"])
        idx = (ref.chapter + ref.verse) % len(options)
        return options[idx]
    
    def generate_patristic_echo(self, ref: VerseReference) -> str:
        """Generate patristic interpretive tradition echo"""
        category = ref.category
        
        echoes = {
            BookCategory. PENTATEUCH: [
                "Origen's allegorical reading finding Christ in Torah's every detail",
                "Augustine's typological interpretation connecting figure to fulfillment",
                "Cyril of Alexandria's christological exegesis of Pentateuchal narratives",
                "John Chrysostom's moral application drawing ethical instruction from narrative"
            ],
            BookCategory.HISTORICAL: [
                "Gregory the Great's moral interpretation of historical narrative",
                "Theodoret's historical-literal reading with typological extension",
                "Ambrose's christological interpretation of royal and prophetic figures",
                "Jerome's attention to historical detail with spiritual application"
            ],
            BookCategory.POETIC: [
                "Augustine's Enarrationes reading Psalms as voice of Christ and Church",
                "Cassiodorus's comprehensive psalm commentary for monastic formation",
                "Gregory of Nyssa's mystical reading of Song as soul's journey to God",
                "Athanasius's christological interpretation of messianic psalms"
            ],
            BookCategory.MAJOR_PROPHET:  [
                "Jerome's literal-historical commentary with messianic identification",
                "Cyril of Alexandria's christological fulfillment reading",
                "Theodoret's attention to historical context with prophetic extension",
                "Origen's spiritual interpretation finding multiple senses in prophetic text"
            ],
            BookCategory.MINOR_PROPHET: [
                "Jerome's commentary emphasizing historical context and messianic fulfillment",
                "Cyril of Alexandria's christological reading of prophetic oracles",
                "Theodore of Mopsuestia's historical-grammatical approach",
                "Augustine's typological interpretation connecting prophecy to Church"
            ],
            BookCategory.GOSPEL: [
                "John Chrysostom's homiletical exposition for moral formation",
                "Augustine's harmony and theological interpretation of Gospel narratives",
                "Cyril of Alexandria's christological commentary on John's Gospel",
                "Origen's allegorical reading finding spiritual meaning in every detail"
            ],
            BookCategory.ACTS: [
                "John Chrysostom's homilies on Acts for ecclesial formation",
                "Bede's commentary combining historical and spiritual interpretation",
                "Ephrem's poetic meditation on apostolic witness",
                "Ambrosiaster's attention to church order and practice"
            ],
            BookCategory.PAULINE: [
                "John Chrysostom's extensive homiletical treatment of Pauline letters",
                "Augustine's interpretation emphasizing grace and predestination themes",
                "Ambrosiaster's careful grammatical and theological commentary",
                "Theodore of Mopsuestia's historical-contextual approach"
            ],
            BookCategory.GENERAL_EPISTLE:  [
                "Bede's commentary combining grammatical and spiritual interpretation",
                "Oecumenius's Greek commentary tradition",
                "Didymus the Blind's Alexandrian spiritual reading",
                "Cassiodorus's compilation of patristic interpretation"
            ],
            BookCategory.APOCALYPTIC: [
                "Victorinus of Pettau's early Latin commentary on Revelation",
                "Andrew of Caesarea's influential Greek Apocalypse commentary",
                "Tyconius's rules-based spiritual interpretation",
                "Primasius's synthesis of earlier Latin interpretation"
            ],
            BookCategory.DEUTEROCANONICAL:  [
                "Origen's inclusion in canonical interpretation",
                "Augustine's acceptance and theological use",
                "Ambrose's moral and christological reading",
                "Jerome's qualified acceptance with scholarly attention"
            ]
        }
        
        options = echoes. get(category, ["Patristic interpretive tradition reading Scripture christologically and ecclesially"])
        idx = (ref.chapter * 2 + ref.verse) % len(options)
        return options[idx]
    
    def generate_sensory_vocabulary(self, ref: VerseReference) -> SensoryVocabulary:
        """Generate sensory vocabulary appropriate to verse content"""
        cat_sensory = self._sensory_sets.get(ref.category, self._sensory_sets[BookCategory.PENTATEUCH])
        
        def select_item(sense:  str, options: List[str]) -> str:
            idx = (ref.chapter + ref.verse + hash(sense)) % len(options)
            return options[idx]
        
        return SensoryVocabulary(
            visual=select_item("visual", cat_sensory. get("visual", ["light and shadow interplay"])),
            auditory=select_item("auditory", cat_sensory.get("auditory", ["sacred silence and divine voice"])),
            tactile=select_item("tactile", cat_sensory.get("tactile", ["texture of encounter"])),
            olfactory=select_item("olfactory", cat_sensory.get("olfactory", ["fragrance of presence"])),
            kinesthetic=select_item("kinesthetic", cat_sensory.get("kinesthetic", ["movement of response"]))
        )
    
    def generate_emotional_arc(self, ref: VerseReference) -> EmotionalArc:
        """Generate emotional/psychological arc appropriate to verse"""
        # Calculate position in chapter for emotional arc
        if ref.verse <= 5:
            position = "opening"
        elif ref.verse <= 15:
            position = "development"
        elif ref.verse <= 25:
            position = "climax"
        else: 
            position = "resolution"
        
        patterns = {
            "opening": EmotionalArc(
                valence="anticipatory tension building toward revelation",
                weight="foundation-laying with gravitas appropriate to new section",
                movement="gathering momentum as theme introduced"
            ),
            "development":  EmotionalArc(
                valence="deepening engagement with complexifying elements",
                weight="increasing density as argument or narrative builds",
                movement="accelerating toward central concern"
            ),
            "climax": EmotionalArc(
                valence="peak intensity of emotional or theological impact",
                weight="maximum density of meaning concentrated",
                movement="arrival at crucial turning point"
            ),
            "resolution": EmotionalArc(
                valence="settling into implications and applications",
                weight="integrating intensity with sustainable practice",
                movement="transition toward continued reflection"
            )
        }
        
        return patterns.get(position, patterns["development"])
    
    def generate_matrix_elements(self, ref: VerseReference) -> MatrixElements:
        """Generate nine-matrix theological elements for verse"""
        category = ref.category
        base_score = 0.5
        
        # Emotional valence:  higher for psalms, laments, passion narratives
        emotional_valence = base_score
        if category == BookCategory.POETIC:
            emotional_valence = 0.7 + (ref.verse % 3) * 0.1
        elif category == BookCategory.GOSPEL and ref.chapter > 20:
            emotional_valence = 0.8
        elif category == BookCategory. APOCALYPTIC:
            emotional_valence = 0.75
        
        # Theological weight: higher for doctrinal passages
        theological_weight = base_score
        if category == BookCategory. PAULINE:
            theological_weight = 0.75
        elif category in [BookCategory.MAJOR_PROPHET, BookCategory.GOSPEL]:
            theological_weight = 0.7
        elif ref.original. startswith("John 1") or ref.original.startswith("Romans"):
            theological_weight = 0.85
        
        # Narrative function
        narrative_functions = [
            "scene-setting", "character-development", "conflict-introduction",
            "rising-action", "climax", "falling-action", "resolution", "transition"
        ]
        narrative_idx = (ref.chapter + ref. verse) % len(narrative_functions)
        narrative_function = narrative_functions[narrative_idx]
        
        # Sensory intensity
        sensory_intensity = 0.5
        if category in [BookCategory.APOCALYPTIC, BookCategory.MAJOR_PROPHET]:
            sensory_intensity = 0.8
        elif category == BookCategory.POETIC:
            sensory_intensity = 0.7
        elif category == BookCategory.GOSPEL: 
            sensory_intensity = 0.65
        
        # Grammatical complexity (estimated)
        grammatical_complexity = 0.5
        if category == BookCategory.PAULINE: 
            grammatical_complexity = 0.75
        elif category == BookCategory.POETIC:
            grammatical_complexity = 0.6
        
        # Lexical rarity
        lexical_rarity = 0.3 + (hash(ref.original) % 40) / 100
        
        # Breath rhythm
        breath_options = ["sustained", "punctuated", "flowing"]
        breath_rhythm = breath_options[ref.verse % 3]
        
        # Register baseline
        if category in [BookCategory.APOCALYPTIC, BookCategory.POETIC]: 
            register_baseline = "elevated-liturgical"
        elif category == BookCategory.PAULINE:
            register_baseline = "instructional-pastoral"
        else:
            register_baseline = "narrative-testimonial"
        
        return MatrixElements(
            emotional_valence=round(emotional_valence, 2),
            theological_weight=round(theological_weight, 2),
            narrative_function=narrative_function,
            sensory_intensity=round(sensory_intensity, 2),
            grammatical_complexity=round(grammatical_complexity, 2),
            lexical_rarity=round(lexical_rarity, 2),
            breath_rhythm=breath_rhythm,
            register_baseline=register_baseline
        )
    
    def generate_analysis(self, verse_ref: str) -> VerseAnalysis:
        """Generate complete analysis for a verse using dynamic content."""
        if not hasattr(self, "verse_texts"):
            self.verse_texts = load_verse_texts(CONFIG.verses_path) or FULL_VERSE_TEXTS.copy()
        ref = VerseReference.parse(verse_ref)
        # Get verse text with fallback chain
        verse_text = self.verse_texts.get(verse_ref, FULL_VERSE_TEXTS.get(verse_ref, "Verse text not found."))

        matches = re.findall(r"\b\w{5,}\b", verse_text)
        key_phrase = matches[0] if matches else "Covenant"
        title = f"{ref.book} {key_phrase} Foundation"

        # Theme detection for death/mourning typology pointing to Christ's resurrection
        if "died" in verse_text.lower() or "death" in verse_text.lower():
            literal = (
                f"Historical account of {ref.book} {ref.chapter}:{ref.verse} "
                f"detailing mortality and covenant continuity through {key_phrase.lower()}."
            )
            allegorical = (
                f"Typifies Christ's victory over death, foreshadowing resurrection within {ref.book}'s arc."
            )
        elif "mourn" in verse_text.lower() or "weep" in verse_text.lower():
            literal = (
                f"Historical account of {ref.book} {ref.chapter}:{ref.verse} "
                f"recording grief transformed through covenant faithfulness."
            )
            allegorical = (
                f"Anticipates the mourning turned to joy in Christ's resurrection victory."
            )
        else:
            literal = f"Primordial narrative in {ref.original} grounding covenant identity through {key_phrase.lower()}."
            allegorical = f"Prefigures Christ's redemptive work through {ref.book}'s {key_phrase.lower()} pattern."

        tropological = f"Forms moral response to {key_phrase.lower()}, shaping habits of faith and fidelity."
        anagogical = f"Points toward eternal life beyond {key_phrase.lower()} in the eschatological horizon."

        pos = ref.canonical_position
        emotional_valence = round(random.uniform(0.4, 0.6) + pos * 0.3, 2)
        # Guard against division by zero
        try:
            theological_weight = float(sp.sympify(f"{ref.chapter} / {ref.verse}").evalf()) if ref.verse != 0 else 0.5
        except Exception:
            theological_weight = 0.5

        # Extended sensory pools (20+ options per domain for reduced repetition)
        sensory_pools = {
            "visual": [
                "mountain shrouded in glory",
                "primordial light emerging",
                f"{key_phrase.lower()} in dawn's glow",
                "pillar of cloud by day",
                "stars beyond counting overhead",
                "burning bush unconsumed",
                "tabernacle gold gleaming",
                "desert wilderness stretching",
                "aged form in morning light",
                "covenant rainbow spanning sky",
                "altar stones arranged",
                "scroll unrolled before reader",
                "veil of temple hanging",
                "well of living water",
                "flock grazing green pastures",
                "city walls rising",
                "throne room vision",
                "lampstand burning bright",
                "ark of covenant resting",
                "sacrifice smoke ascending",
            ],
            "auditory": [
                "thunderous voice from heaven",
                "still whisper in silence",
                "mourning lament" if "mourn" in verse_text.lower() else "covenant echo resounding",
                "shofar blast announcing",
                "weeping turning to song",
                "crackling fire of offering",
                "rushing wind of Spirit",
                "footsteps on holy ground",
                "blessing words pronounced",
                "creation's silent testimony",
                "seraphim crying holy",
                "hammer on tent peg",
                "water from rock gushing",
                "camp of Israel murmuring",
                "praise psalm ascending",
                "prophetic oracle declared",
                "covenant renewal spoken",
                "name of God proclaimed",
                "judgment trumpet sounding",
                "resurrection cry piercing",
            ],
            "tactile": [
                "stone-cold ground beneath",
                "warmth of firelight near",
                "rough altar stones stacked",
                "dust of mortality beneath",
                "scroll parchment unrolling",
                "oil of anointing flowing",
                "water of purification",
                "bread broken in hands",
                "staff of shepherd gripped",
                "chains of bondage heavy",
                "freedom's weight lifted",
                "embrace of covenant kin",
                "rock of ages firm",
                "wind of desert crossing",
                "garment hem touched",
                "nail-pierced hands",
                "tomb stone cold",
                "risen body glorified",
                "baptismal water immersing",
                "eucharistic bread received",
            ],
            "olfactory": [
                "incense rising as prayer",
                "desert dust and sage",
                "fragrant offering ascending",
                "burnt sacrifice smoke",
                "myrrh and aloes prepared",
                "manna sweet in morning",
                "frankincense of worship",
                "cedar of temple beams",
                "harvest grain threshed",
                "wine of celebration",
                "lamb prepared for feast",
                "tomb spices gathered",
                "garden of resurrection",
                "bread of presence",
                "oil of gladness",
                "rain on parched earth",
                "flowers of field",
                "sulfur of judgment",
                "new creation freshness",
                "heaven's pure air",
            ],
            "kinesthetic": [
                "kneeling in reverence",
                "journeying under starfield",
                "embrace of covenant kin",
                "prostration before holiness",
                "walking in obedience",
                "running to proclaim",
                "standing firm in faith",
                "bowing before throne",
                "dancing in celebration",
                "climbing holy mountain",
                "crossing sea on dry ground",
                "wrestling until blessing",
                "lifting hands in praise",
                "falling on face in awe",
                "rising to serve",
                "carrying burden of mission",
                "pressing toward goal",
                "resting in Sabbath peace",
                "ascending to glory",
                "reigning with Christ eternal",
            ],
        }

        sensory = SensoryVocabulary(
            visual=random.choice(sensory_pools["visual"]),
            auditory=random.choice(sensory_pools["auditory"]),
            tactile=random.choice(sensory_pools["tactile"]),
            olfactory=random.choice(sensory_pools["olfactory"]),
            kinesthetic=random.choice(sensory_pools["kinesthetic"]),
        )

        # Emotional valence adjusted by canonical position
        if ref.category == BookCategory.PENTATEUCH:
            valence = "anticipatory tension building" if ref.verse % 2 == 0 else "reflective sorrow yielding hope"
        elif ref.category == BookCategory.POETIC:
            valence = "contemplative stillness deepening"
        elif ref.category == BookCategory.APOCALYPTIC:
            valence = "eschatological urgency heightening"
        else:
            valence = "steady reverence sustaining"

        # Patristics with verse-specific lookup, then fallback to expanded pool
        patristics_default = [
            "Athanasius on incarnation and deification",
            "Gregory of Nyssa on freedom and ascent",
            "John Chrysostom on moral application and virtue",
            "Basil the Great on creation and Spirit",
            "Irenaeus on recapitulation in Christ",
            "Cyril of Alexandria on christological unity",
            "Maximus the Confessor on cosmic liturgy",
            "Gregory Palamas on uncreated light",
            "Ephrem the Syrian on typological reading",
            "Augustine on grace and predestination",
            "Jerome on textual precision and translation",
            "Origen on allegorical depth and ascent",
            "Theodore of Mopsuestia on historical sense",
            "Theodoret on prophetic fulfillment",
            "Ambrose on moral and mystical reading",
        ]
        patristic = random.choice(PATRISTICS_POOL.get(verse_ref, patristics_default))

        # Matrix with sympy-based variety and additional math formulas
        matrix = MatrixElements(
            emotional_valence=emotional_valence,
            theological_weight=round(theological_weight, 2),
            narrative_function="covenant-continuity" if ref.category == BookCategory.PENTATEUCH else "narrative-pivot",
            sensory_intensity=round(0.4 + pos * 0.4 + random.uniform(0.0, 0.2), 2),
            grammatical_complexity=round(0.35 + random.uniform(0.0, 0.25) + math.sin(ref.verse) * 0.1, 2),
            lexical_rarity=round(0.3 + random.uniform(0.0, 0.3), 2),
            breath_rhythm=random.choice(["sustained", "punctuated", "flowing", "meditative", "urgent"]),
            register_baseline=(
                "elevated-liturgical"
                if ref.category in [BookCategory.APOCALYPTIC, BookCategory.POETIC]
                else "instructional-pastoral"
                if ref.category == BookCategory.PAULINE
                else "narrative-testimonial"
            ),
        )

        content_str = f"{title}{literal}{allegorical}{tropological}{anagogical}{patristic}{random.random()}"
        content_hash = hashlib.md5(content_str.encode()).hexdigest()[:12]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return VerseAnalysis(
            reference=ref,
            title=title,
            literal=literal,
            allegorical=allegorical,
            tropological=tropological,
            anagogical=anagogical,
            liturgical=self.generate_liturgical_connection(ref),
            patristic=patristic,
            sensory=sensory,
            emotional=EmotionalArc(valence=valence, weight="foundation-laying", movement="gathering momentum"),
            matrix=matrix,
            content_hash=content_hash,
            timestamp=timestamp,
        )
    
    @staticmethod
    def _generate_content_hash(verse_ref:  str) -> str:
        """Generate a hash for content verification"""
        combined = f"{verse_ref}:{datetime.now().isoformat()}"
        return hashlib.md5(combined.encode()).hexdigest()[:12]


# ============================================================================
# CONTENT FORMATTER
# ============================================================================

class ContentFormatter:
    """Formats verse analysis into output text"""
    
    @staticmethod
    def format(analysis: VerseAnalysis) -> str:
        """Format complete analysis into output string"""
        ref = analysis.reference
        
        return f"""
{'='*80}
VERSE NOTE TEMPLATE:  {ref.original}
{'='*80}

## {analysis.title}

**Verse Reference:** {ref.original}
**Book Category:** {ref.category.value.replace('_', ' ').title()}
**Canonical Position:** {ref.canonical_position:.4f}
**Content ID:** {analysis.content_hash}

{'='*80}
I. NINE MATRIX APPLICATION
{'='*80}

A.  Quantitative Measures:
   • Emotional Valence: {analysis.matrix.emotional_valence}
   • Theological Weight: {analysis.matrix.theological_weight}
   • Sensory Intensity: {analysis.matrix.sensory_intensity}
   • Grammatical Complexity: {analysis.matrix.grammatical_complexity}
   • Lexical Rarity: {analysis.matrix.lexical_rarity}

B. Qualitative Markers:
   • Narrative Function:  {analysis.matrix.narrative_function}
   • Breath Rhythm: {analysis.matrix. breath_rhythm}
   • Register Baseline: {analysis.matrix. register_baseline}

{'='*80}
II.  STRATIFIED FOUNDATION ANALYSIS (Quadriga)
{'='*80}

### Literal (Historical-Grammatical):
{analysis.literal}

### Allegorical (Christological-Typological):
{analysis.allegorical}

### Tropological (Moral-Formational):
{analysis.tropological}

### Anagogical (Eschatological-Heavenly):
{analysis.anagogical}

{'='*80}
III.  LITURGICAL & PATRISTIC CONNECTIONS
{'='*80}

### Liturgical Setting:
{analysis.liturgical}

### Patristic Echo: 
{analysis.patristic}

{'='*80}
IV.  SENSORY VOCABULARY CODEX
{'='*80}

• Visual: {analysis.sensory. visual}
• Auditory:  {analysis.sensory.auditory}
• Tactile: {analysis.sensory.tactile}
• Olfactory: {analysis.sensory.olfactory}
• Kinesthetic: {analysis.sensory.kinesthetic}

{'='*80}
V. EMOTIONAL-PSYCHOLOGICAL ARC
{'='*80}

• Valence: {analysis. emotional.valence}
• Weight: {analysis.emotional.weight}
• Movement: {analysis. emotional.movement}

{'='*80}
VI. INTEGRATION PROTOCOL
{'='*80}

This verse-note integrates: 
1. Four-fold exegetical tradition (Quadriga) grounding interpretation
2. Liturgical-ecclesial context anchoring communal reading
3. Patristic witness providing interpretive tradition
4. Sensory vocabulary enabling imaginative engagement
5. Emotional arc guiding reader formation
6. Matrix elements ensuring systematic coverage

{'='*80}
VII. ORBITAL RESONANCE & TEMPORAL FOLDING
{'='*80}

• Orbital Distance to Consummation: {1.0 - ref.canonical_position:.3f}
• Temporal Folding Anchor (next chapter): {ref.book} {ref.chapter + 1 if ref.chapter else 1}
• Harmonic Echo Ratio (book order / canon): {BOOK_ORDER.get(ref.book, 40) / 67:.3f}
• Resonance Directive: Repeat key sensory lexeme near harmonic anchor while varying register to maintain invisibility.

{'='*80}
VII.  METADATA
{'='*80}

Generated:  {analysis.timestamp}
Verse:  {ref.original}
Category: {ref.category.value}
Position: {ref.canonical_position:.4f}
Hash: {analysis.content_hash}

{'='*80}
END VERSE NOTE:  {ref.original}
{'='*80}
""".strip()


# ============================================================================
# UNIQUENESS CHECKER
# ============================================================================

class UniquenessChecker:
    """Checks content uniqueness against existing content"""
    
    def __init__(self, threshold: float = 0.10):
        self.threshold = threshold
        self._template_pattern = re.compile(
            '|'.join(re.escape(s) for s in TEMPLATE_SECTIONS),
            re.IGNORECASE
        )
    
    def extract_variable_content(self, content: str) -> str:
        """Extract only variable content, removing template boilerplate"""
        # Remove template sections
        variable_text = self._template_pattern.sub(' ', content)
        
        # Remove common formatting
        variable_text = re. sub(r'[=\-*]{3,}', ' ', variable_text)
        variable_text = re.sub(r'\d+\.\d+', ' ', variable_text)  # Decimal numbers
        variable_text = re.sub(r'\[\d+\]', ' ', variable_text)  # Bracketed numbers
        variable_text = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', ' ', variable_text)  # Dates
        
        # Normalize whitespace
        return ' '.join(variable_text. lower().split())

    @staticmethod
    def _ngrams(tokens: List[str], n: int) -> Set[str]:
        return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)} if len(tokens) >= n else set()
    
    def calculate_score(self, new_content: str, existing_contents: List[str],
                        sample_size: int = 50) -> float:
        """Calculate uniqueness score comparing only variable content"""
        if not existing_contents:
            return 1.0
        
        # Extract variable content only
        new_variable = self.extract_variable_content(new_content)
        new_tokens = new_variable.split()
        new_words = set(new_tokens) - COMMON_WORDS
        new_bigrams = self._ngrams(new_tokens, 2)
        new_trigrams = self._ngrams(new_tokens, 3)
        
        if not new_words:
            return 0.5  # Default if no significant words
        
        # Sample from existing contents for efficiency (increased to 100 for better history)
        effective_sample_size = max(sample_size, 100)
        sample = existing_contents[-effective_sample_size:] if len(existing_contents) > effective_sample_size else existing_contents
        
        total_similarity = 0.0
        total_ngram_penalty = 0.0
        valid_comparisons = 0
        
        for existing in sample:
            existing_variable = self.extract_variable_content(existing)
            existing_tokens = existing_variable.split()
            existing_words = set(existing_tokens) - COMMON_WORDS
            existing_bigrams = self._ngrams(existing_tokens, 2)
            existing_trigrams = self._ngrams(existing_tokens, 3)
            
            if not existing_words:
                continue
            
            # Jaccard similarity on variable content only
            intersection = len(new_words & existing_words)
            union = len(new_words | existing_words)
            
            if union > 0:
                similarity = intersection / union
                total_similarity += similarity
                # n-gram penalty (max of bigram/trigram overlaps)
                bigram_overlap = len(new_bigrams & existing_bigrams) / max(1, len(new_bigrams | existing_bigrams)) if new_bigrams else 0
                trigram_overlap = len(new_trigrams & existing_trigrams) / max(1, len(new_trigrams | existing_trigrams)) if new_trigrams else 0
                total_ngram_penalty += max(bigram_overlap, trigram_overlap)
                valid_comparisons += 1
        
        if valid_comparisons == 0:
            return 1.0
        
        avg_similarity = total_similarity / valid_comparisons
        avg_ngram = total_ngram_penalty / valid_comparisons
        combined = max(avg_similarity, avg_ngram)
        uniqueness = 1.0 - combined
        
        return max(0.0, min(1.0, uniqueness))
    
    def is_unique(self, content: str, existing_contents: List[str]) -> Tuple[bool, float]:
        """Check if content meets uniqueness threshold"""
        score = self.calculate_score(content, existing_contents)
        return score >= self. threshold, score


# ============================================================================
# VERSE PROCESSOR
# ============================================================================

class VerseProcessor:
    """Processes verses and manages the workflow"""
    
    def __init__(self, config: Config):
        self.config = config
        self.data_store = DataStore(config)
        self.generator = ContentGenerator()
        self.formatter = ContentFormatter()
        self.uniqueness_checker = UniquenessChecker(config.uniqueness_threshold)
        self.log = get_logger()
    
    def process_verse(self, verse_ref: str, existing_contents: List[str],
                      content_map: Dict[str, str], processed_list: List[str],
                      failed_map: Dict[str, str]) -> bool:
        """Process a single verse with uniqueness verification"""
        self.log.info(f"Processing {verse_ref}...")
        
        best_content = None
        best_score = 0.0
        
        for attempt in range(self.config.max_retries):
            try:
                # Generate content
                analysis = self.generator.generate_analysis(verse_ref)
                content = self.formatter.format(analysis)
                
                # Check uniqueness
                is_unique, score = self.uniqueness_checker. is_unique(content, existing_contents)
                
                if is_unique:
                    self.log.info(f"✅ {verse_ref} processed with uniqueness score {score:.2f}")
                    
                    # Save to all storage
                    content_map[verse_ref] = content
                    if verse_ref not in processed_list: 
                        processed_list.append(verse_ref)
                    existing_contents.append(content)
                    
                    # Append to output file
                    self.data_store.append_to_output(verse_ref, content)
                    
                    return True
                else:
                    if score > best_score:
                        best_score = score
                        best_content = content
                    
                    if attempt < self.config.max_retries - 1:
                        self.log.warning(
                            f"Uniqueness {score:.2f} below threshold "
                            f"{self.config.uniqueness_threshold}, attempt {attempt + 2}/{self.config.max_retries}"
                        )
                        # Exponential backoff for retries
                        time.sleep(0.5 * (attempt + 1))
            
            except Exception as e: 
                self.log.error(f"Error processing {verse_ref}: {e}")
                traceback.print_exc()
                if attempt < self.config.max_retries - 1:
                    time.sleep(1)
        
        # Accept best attempt even if below threshold
        if best_content is not None:
            self.log.warning(f"Accepting {verse_ref} with best score {best_score:.2f} (below threshold)")
            
            content_map[verse_ref] = best_content
            if verse_ref not in processed_list: 
                processed_list.append(verse_ref)
            existing_contents.append(best_content)
            self.data_store.append_to_output(verse_ref, best_content)
            
            return True
        
        # Record failure
        failed_map[verse_ref] = f"Failed after {self.config.max_retries} attempts, best score:  {best_score:.2f}"
        self.log.error(f"Failed to generate acceptable content for {verse_ref}")
        return False
    
    def process_batch(self, verses: List[str], existing_contents: List[str],
                      content_map: Dict[str, str], processed_list: List[str],
                      failed_map: Dict[str, str]) -> int:
        """Process a batch of verses"""
        success_count = 0
        
        for verse in verses:
            if verse in content_map:
                self.log.info(f"⏭️ Skipping {verse} (already processed)")
                continue
            
            if self.process_verse(verse, existing_contents, content_map, processed_list, failed_map):
                success_count += 1
        
        return success_count
    
    def run(self) -> None:
        """Main processing loop"""
        self.log. info("=" * 80)
        self.log.info("🚀 STRATIFIED FOUNDATION AUTO-PROCESSOR (Enhanced)")
        self.log.info("=" * 80)
        self.log.info(f"Mode: {'Continuous' if self.config.continuous_mode else 'Single Run'}")
        self.log.info(f"Batch size: {self.config.batch_size}")
        self.log.info(f"Uniqueness threshold: {self.config.uniqueness_threshold}")
        self.log.info(f"Output file: {self.config.output_path}")
        self.log.info("=" * 80)
        
        # Load all data
        all_verses = self. data_store.load_verses()
        if not all_verses:
            self.log.error("No verses loaded.  Exiting.")
            return
        
        content_map = self.data_store.load_content_map()
        processed_list = self.data_store.load_processed_verses()
        failed_map = self.data_store.load_failed_verses()
        
        # Build existing contents list from content map
        existing_contents = list(content_map.values())
        
        self.log.info(f"📚 Total verses: {len(all_verses)}")
        self.log.info(f"💾 Already processed: {len(content_map)}")
        self.log.info(f"❌ Previously failed: {len(failed_map)}")
        
        # Filter to unprocessed verses
        unprocessed = [v for v in all_verses if v not in content_map and v not in failed_map]
        self.log.info(f"🆕 Unprocessed verses: {len(unprocessed)}")
        
        if not unprocessed: 
            self.log.info("✅ All verses have been processed!")
            return
        
        self.log.info(f"🔍 Starting from:  {unprocessed[0]}")
        
        iteration = 0
        total_processed = len(content_map)
        
        try:
            while unprocessed: 
                iteration += 1
                
                # Get next batch
                batch = unprocessed[:self.config.batch_size]
                self.log.info(f"\n📦 Batch {iteration}:  {batch}")
                
                # Process batch
                success_count = self. process_batch(
                    batch, existing_contents, content_map, processed_list, failed_map
                )
                total_processed += success_count
                
                # Save progress
                self.data_store.save_content_map(content_map)
                self.data_store.save_processed_verses(processed_list)
                self.data_store.save_failed_verses(failed_map)
                
                # Update unprocessed list
                unprocessed = [v for v in all_verses if v not in content_map and v not in failed_map]
                
                # Progress report
                progress_pct = (total_processed / len(all_verses)) * 100
                self.log.info(f"📊 Progress: {total_processed}/{len(all_verses)} ({progress_pct:.1f}%)")
                
                if not self.config.continuous_mode:
                    break
                
                if unprocessed:
                    self. log.info(f"⏳ Cooldown {self.config.cooldown_between_batches}s...")
                    time.sleep(self.config.cooldown_between_batches)
        
        except KeyboardInterrupt:
            self.log.warning("\n⚠️ Interrupted by user.  Saving progress...")
            self._save_progress(content_map, processed_list, failed_map)
            self.log.info("✅ Progress saved.  Exiting.")
        
        except Exception as e:
            self. log.error(f"\n❌ Unexpected error: {e}")
            traceback.print_exc()
            self._save_progress(content_map, processed_list, failed_map)
            self.log.info("✅ Progress saved despite error.")
        
        self._print_summary(content_map, all_verses, failed_map)
    
    def _save_progress(self, content_map: Dict[str, str], processed_list:  List[str],
                       failed_map: Dict[str, str]) -> None:
        """Save all progress data"""
        self.data_store.save_content_map(content_map)
        self.data_store.save_processed_verses(processed_list)
        self.data_store.save_failed_verses(failed_map)
    
    def _print_summary(self, content_map: Dict[str, str], all_verses:  List[str],
                       failed_map: Dict[str, str]) -> None:
        """Print final summary"""
        self.log. info("\n" + "=" * 80)
        self.log.info("🏁 PROCESSING COMPLETE")
        self.log.info(f"📊 Final:  {len(content_map)}/{len(all_verses)} verses processed")
        self.log.info(f"❌ Failed:  {len(failed_map)} verses")
        self.log.info("=" * 80)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    processor = VerseProcessor(CONFIG)
    processor.run()


if __name__ == "__main__":
    main()
