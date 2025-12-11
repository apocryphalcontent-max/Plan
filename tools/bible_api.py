#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Bible API Integration
Fetch verse text from various Bible APIs
"""

import sys
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin
import urllib.request
import urllib.error

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config, CANONICAL_ORDER

logger = logging.getLogger(__name__)


# ============================================================================
# BIBLE API CLIENT
# ============================================================================

class BibleAPIClient:
    """Client for fetching Bible verses from APIs"""
    
    # API.Bible version IDs
    VERSION_IDS = {
        'kjv': 'de4e12af7f28f599-02',  # King James Version
        'asv': '06125adad2d5898a-01',  # American Standard Version
        'web': '9879dbb7cfe39e4d-01',  # World English Bible
    }
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.api.bible_api_key
        self.base_url = config.api.bible_api_base_url
        self.timeout = config.api.request_timeout
    
    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """Make an API request"""
        if not self.api_key:
            logger.warning("Bible API key not configured")
            return None
        
        url = urljoin(self.base_url + '/', endpoint)
        headers = {
            'api-key': self.api_key,
            'Accept': 'application/json'
        }
        
        request = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            logger.error(f"HTTP error {e.code}: {e.reason}")
            return None
        except urllib.error.URLError as e:
            logger.error(f"URL error: {e.reason}")
            return None
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def get_verse(self, book: str, chapter: int, verse: int, 
                  version: str = 'kjv') -> Optional[str]:
        """Fetch a single verse"""
        version_id = self.VERSION_IDS.get(version.lower())
        if not version_id:
            logger.error(f"Unknown version: {version}")
            return None
        
        # Convert book name to API format
        book_id = self._get_book_id(book)
        if not book_id:
            return None
        
        verse_id = f"{book_id}.{chapter}.{verse}"
        endpoint = f"bibles/{version_id}/verses/{verse_id}"
        
        response = self._make_request(endpoint)
        if response and 'data' in response:
            # Strip HTML tags from content
            content = response['data'].get('content', '')
            return self._strip_html(content)
        
        return None
    
    def get_chapter(self, book: str, chapter: int, 
                    version: str = 'kjv') -> Optional[List[Dict]]:
        """Fetch an entire chapter"""
        version_id = self.VERSION_IDS.get(version.lower())
        if not version_id:
            return None
        
        book_id = self._get_book_id(book)
        if not book_id:
            return None
        
        chapter_id = f"{book_id}.{chapter}"
        endpoint = f"bibles/{version_id}/chapters/{chapter_id}/verses"
        
        response = self._make_request(endpoint)
        if response and 'data' in response:
            verses = []
            for v in response['data']:
                verses.append({
                    'reference': v.get('reference'),
                    'verse_number': v.get('verseNumber'),
                    'text': self._strip_html(v.get('text', ''))
                })
            return verses
        
        return None
    
    def _get_book_id(self, book_name: str) -> Optional[str]:
        """Convert book name to API book ID"""
        # API.Bible book ID mapping
        book_ids = {
            'genesis': 'GEN', 'exodus': 'EXO', 'leviticus': 'LEV',
            'numbers': 'NUM', 'deuteronomy': 'DEU', 'joshua': 'JOS',
            'judges': 'JDG', 'ruth': 'RUT', '1 samuel': '1SA',
            '2 samuel': '2SA', '1 kings': '1KI', '2 kings': '2KI',
            '1 chronicles': '1CH', '2 chronicles': '2CH', 'ezra': 'EZR',
            'nehemiah': 'NEH', 'esther': 'EST', 'job': 'JOB',
            'psalms': 'PSA', 'proverbs': 'PRO', 'ecclesiastes': 'ECC',
            'song of solomon': 'SNG', 'isaiah': 'ISA', 'jeremiah': 'JER',
            'lamentations': 'LAM', 'ezekiel': 'EZK', 'daniel': 'DAN',
            'hosea': 'HOS', 'joel': 'JOL', 'amos': 'AMO',
            'obadiah': 'OBA', 'jonah': 'JON', 'micah': 'MIC',
            'nahum': 'NAM', 'habakkuk': 'HAB', 'zephaniah': 'ZEP',
            'haggai': 'HAG', 'zechariah': 'ZEC', 'malachi': 'MAL',
            'matthew': 'MAT', 'mark': 'MRK', 'luke': 'LUK',
            'john': 'JHN', 'acts': 'ACT', 'romans': 'ROM',
            '1 corinthians': '1CO', '2 corinthians': '2CO', 'galatians': 'GAL',
            'ephesians': 'EPH', 'philippians': 'PHP', 'colossians': 'COL',
            '1 thessalonians': '1TH', '2 thessalonians': '2TH',
            '1 timothy': '1TI', '2 timothy': '2TI', 'titus': 'TIT',
            'philemon': 'PHM', 'hebrews': 'HEB', 'james': 'JAS',
            '1 peter': '1PE', '2 peter': '2PE', '1 john': '1JN',
            '2 john': '2JN', '3 john': '3JN', 'jude': 'JUD',
            'revelation': 'REV'
        }
        return book_ids.get(book_name.lower())
    
    def _strip_html(self, text: str) -> str:
        """Strip HTML tags from text"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()


# ============================================================================
# VERSE FETCHER - OFFLINE-FIRST ARCHITECTURE
# ============================================================================

class VerseFetcher:
    """
    Fetch and cache Bible verses with offline-first architecture.
    Uses embedded data when available, falls back to API only when necessary.
    This minimizes API calls and ensures system reliability.
    """
    
    def __init__(self, db=None):
        self.api = BibleAPIClient()
        self.db = db
        self._cache = {}
        self._offline_provider = None
        self._stats = {'offline_hits': 0, 'api_calls': 0, 'cache_hits': 0}
    
    @property
    def offline_provider(self):
        """Lazy-load offline provider to avoid circular imports."""
        if self._offline_provider is None:
            try:
                from data.offline_bible import get_offline_provider
                self._offline_provider = get_offline_provider()
            except ImportError:
                logger.debug("Offline provider not available")
                self._offline_provider = False  # Mark as unavailable
        return self._offline_provider if self._offline_provider else None
    
    def fetch_verse(self, book: str, chapter: int, verse: int,
                    version: str = 'kjv', use_cache: bool = True) -> Optional[str]:
        """
        Fetch a verse with intelligent fallback:
        1. Check memory cache (fastest)
        2. Check offline database (fast, no network)
        3. Fall back to API (slow, requires network)
        """
        cache_key = f"{book}_{chapter}_{verse}_{version}"
        
        # Layer 1: Memory cache
        if use_cache and cache_key in self._cache:
            self._stats['cache_hits'] += 1
            return self._cache[cache_key]
        
        # Layer 2: Offline database (KJV only for now)
        if version.lower() == 'kjv' and self.offline_provider:
            text = self.offline_provider.get_verse(book, chapter, verse)
            if text:
                self._cache[cache_key] = text
                self._stats['offline_hits'] += 1
                return text
        
        # Layer 3: API fallback
        text = self.api.get_verse(book, chapter, verse, version)
        self._stats['api_calls'] += 1
        
        if text:
            self._cache[cache_key] = text
        
        return text
    
    def get_fetch_statistics(self) -> Dict[str, Any]:
        """Get statistics on fetch sources."""
        total = sum(self._stats.values())
        return {
            **self._stats,
            'total_requests': total,
            'offline_rate': self._stats['offline_hits'] / max(total, 1),
            'api_rate': self._stats['api_calls'] / max(total, 1)
        }
    
    def fetch_chapter_batch(self, book: str, chapter: int,
                           version: str = 'kjv') -> List[Dict]:
        """Fetch all verses in a chapter"""
        verses = self.api.get_chapter(book, chapter, version)
        
        if verses:
            # Cache all verses
            for v in verses:
                cache_key = f"{book}_{chapter}_{v['verse_number']}_{version}"
                self._cache[cache_key] = v['text']
        
        return verses or []
    
    def populate_missing_verses(self, book_name: str = None, 
                                limit: int = 100) -> int:
        """Populate missing verse text in database"""
        if not self.db:
            logger.error("Database not configured")
            return 0
        
        # Get verses without text
        query = """
            SELECT v.id, v.verse_reference, cb.name as book_name, v.chapter, v.verse_number
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.text_kjv IS NULL
        """
        params = []
        
        if book_name:
            query += " AND cb.name = %s"
            params.append(book_name)
        
        query += " ORDER BY cb.canonical_order, v.chapter, v.verse_number LIMIT %s"
        params.append(limit)
        
        verses = self.db.fetch_all(query, tuple(params))
        
        updated = 0
        for verse in verses:
            text = self.fetch_verse(
                verse['book_name'], 
                verse['chapter'], 
                verse['verse_number']
            )
            
            if text:
                self.db.execute(
                    "UPDATE verses SET text_kjv = %s WHERE id = %s",
                    (text, verse['id'])
                )
                updated += 1
                logger.info(f"Updated: {verse['verse_reference']}")
            
            time.sleep(0.2)  # Rate limiting
        
        return updated


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

verse_fetcher = VerseFetcher()


def get_verse_fetcher() -> VerseFetcher:
    """Get the global verse fetcher"""
    return verse_fetcher
