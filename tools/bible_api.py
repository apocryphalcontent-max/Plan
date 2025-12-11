#!/usr/bin/env python3
"""
ΒΊΒΛΟΣ ΛΌΓΟΥ Bible API Integration
Fetch verse text from various Bible APIs.

This module provides:
- Integration with Bible API services
- Offline-first architecture with caching
- Automatic retry logic for transient failures
"""

import sys
import json
import logging
import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin
import urllib.request
import urllib.error

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import config, CANONICAL_ORDER

logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class BibleAPIError(Exception):
    """Base exception for Bible API operations."""
    pass


class APIConnectionError(BibleAPIError):
    """Raised when unable to connect to the Bible API."""
    pass


class APIKeyError(BibleAPIError):
    """Raised when the API key is missing or invalid."""
    pass


class VerseNotFoundError(BibleAPIError):
    """Raised when a verse cannot be found."""
    pass


# ============================================================================
# BIBLE API CLIENT
# ============================================================================

class BibleAPIClient:
    """
    Client for fetching Bible verses from APIs.
    
    Supports multiple Bible versions and provides automatic retry
    logic for transient failures.
    """
    
    # API.Bible version IDs
    VERSION_IDS: Dict[str, str] = {
        'kjv': 'de4e12af7f28f599-02',  # King James Version
        'asv': '06125adad2d5898a-01',  # American Standard Version
        'web': '9879dbb7cfe39e4d-01',  # World English Bible
    }
    
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    
    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initialize the Bible API client.
        
        Args:
            api_key: Optional API key. Uses config if not provided.
        """
        self.api_key: str = api_key or config.api.bible_api_key
        self.base_url: str = config.api.bible_api_base_url
        self.timeout: int = config.api.request_timeout
    
    @property
    def is_configured(self) -> bool:
        """Check if the API key is configured."""
        return bool(self.api_key)
    
    def _make_request(
        self, 
        endpoint: str, 
        retries: int = 0
    ) -> Optional[Dict[str, Any]]:
        """
        Make an API request with retry logic.
        
        Args:
            endpoint: API endpoint to call.
            retries: Current retry count.
            
        Returns:
            JSON response as dictionary, or None if request failed.
        """
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
            if e.code == 401:
                logger.error("Invalid API key")
            elif e.code == 404:
                logger.debug(f"Resource not found: {endpoint}")
            elif e.code >= 500 and retries < self.MAX_RETRIES:
                logger.warning(f"Server error {e.code}, retrying...")
                time.sleep(self.RETRY_DELAY * (retries + 1))
                return self._make_request(endpoint, retries + 1)
            else:
                logger.error(f"HTTP error {e.code}: {e.reason}")
            return None
        except urllib.error.URLError as e:
            if retries < self.MAX_RETRIES:
                logger.warning(f"Connection error, retrying: {e.reason}")
                time.sleep(self.RETRY_DELAY * (retries + 1))
                return self._make_request(endpoint, retries + 1)
            logger.error(f"URL error: {e.reason}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            return None
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def get_verse(
        self, 
        book: str, 
        chapter: int, 
        verse: int, 
        version: str = 'kjv'
    ) -> Optional[str]:
        """
        Fetch a single verse.
        
        Args:
            book: Book name (e.g., "Genesis").
            chapter: Chapter number.
            verse: Verse number.
            version: Bible version (default: 'kjv').
            
        Returns:
            Verse text, or None if not found.
        """
        if not book or chapter <= 0 or verse <= 0:
            return None
            
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
    
    def get_chapter(
        self, 
        book: str, 
        chapter: int, 
        version: str = 'kjv'
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch an entire chapter.
        
        Args:
            book: Book name (e.g., "Genesis").
            chapter: Chapter number.
            version: Bible version (default: 'kjv').
            
        Returns:
            List of verse dictionaries, or None if not found.
        """
        if not book or chapter <= 0:
            return None
            
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
            verses: List[Dict[str, Any]] = []
            for v in response['data']:
                verses.append({
                    'reference': v.get('reference'),
                    'verse_number': v.get('verseNumber'),
                    'text': self._strip_html(v.get('text', ''))
                })
            return verses
        
        return None
    
    def _get_book_id(self, book_name: str) -> Optional[str]:
        """
        Convert book name to API book ID.
        
        Args:
            book_name: Book name in any case.
            
        Returns:
            API book ID, or None if not found.
        """
        if not book_name:
            return None
            
        # API.Bible book ID mapping
        book_ids: Dict[str, str] = {
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
        """
        Strip HTML tags from text.
        
        Args:
            text: Text potentially containing HTML tags.
            
        Returns:
            Text with HTML tags removed.
        """
        if not text:
            return ''
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
    
    The fetch order is:
    1. Memory cache (fastest, no I/O)
    2. Offline database (fast, no network)
    3. Bible API (slow, requires network)
    """
    
    RATE_LIMIT_DELAY: float = 0.2  # Seconds between API calls
    
    def __init__(self, db: Optional[Any] = None) -> None:
        """
        Initialize the verse fetcher.
        
        Args:
            db: Optional database manager for persisting fetched verses.
        """
        self.api = BibleAPIClient()
        self.db = db
        self._cache: Dict[str, str] = {}
        self._offline_provider: Optional[Any] = None
        self._offline_checked: bool = False
        self._stats: Dict[str, int] = {
            'offline_hits': 0, 
            'api_calls': 0, 
            'cache_hits': 0
        }
    
    @property
    def offline_provider(self) -> Optional[Any]:
        """
        Lazy-load offline provider to avoid circular imports.
        
        Returns:
            Offline provider instance, or None if not available.
        """
        if not self._offline_checked:
            self._offline_checked = True
            try:
                from data.offline_bible import get_offline_provider
                self._offline_provider = get_offline_provider()
            except ImportError:
                logger.debug("Offline provider not available")
                self._offline_provider = None
        return self._offline_provider
    
    def clear_cache(self) -> None:
        """Clear the in-memory verse cache."""
        self._cache.clear()
        logger.debug("Verse cache cleared")
    
    def fetch_verse(
        self, 
        book: str, 
        chapter: int, 
        verse: int,
        version: str = 'kjv', 
        use_cache: bool = True
    ) -> Optional[str]:
        """
        Fetch a verse with intelligent fallback.
        
        Args:
            book: Book name.
            chapter: Chapter number.
            verse: Verse number.
            version: Bible version (default: 'kjv').
            use_cache: Whether to use the memory cache.
            
        Returns:
            Verse text, or None if not found.
        """
        if not book or chapter <= 0 or verse <= 0:
            return None
            
        cache_key = f"{book}_{chapter}_{verse}_{version}"
        
        # Layer 1: Memory cache
        if use_cache and cache_key in self._cache:
            self._stats['cache_hits'] += 1
            return self._cache[cache_key]
        
        # Layer 2: Offline database (KJV only for now)
        if version.lower() == 'kjv' and self.offline_provider is not None:
            try:
                text = self.offline_provider.get_verse(book, chapter, verse)
                if text:
                    self._cache[cache_key] = text
                    self._stats['offline_hits'] += 1
                    return text
            except Exception as e:
                logger.warning(f"Offline provider error: {e}")
        
        # Layer 3: API fallback
        text = self.api.get_verse(book, chapter, verse, version)
        self._stats['api_calls'] += 1
        
        if text:
            self._cache[cache_key] = text
        
        return text
    
    def get_fetch_statistics(self) -> Dict[str, Any]:
        """
        Get statistics on fetch sources.
        
        Returns:
            Dictionary with hit counts and rates.
        """
        total = sum(self._stats.values())
        return {
            **self._stats,
            'total_requests': total,
            'cache_size': len(self._cache),
            'offline_rate': self._stats['offline_hits'] / max(total, 1),
            'api_rate': self._stats['api_calls'] / max(total, 1)
        }
    
    def fetch_chapter_batch(
        self, 
        book: str, 
        chapter: int,
        version: str = 'kjv'
    ) -> List[Dict[str, Any]]:
        """
        Fetch all verses in a chapter.
        
        Args:
            book: Book name.
            chapter: Chapter number.
            version: Bible version (default: 'kjv').
            
        Returns:
            List of verse dictionaries.
        """
        if not book or chapter <= 0:
            return []
            
        verses = self.api.get_chapter(book, chapter, version)
        
        if verses:
            # Cache all verses
            for v in verses:
                cache_key = f"{book}_{chapter}_{v['verse_number']}_{version}"
                self._cache[cache_key] = v['text']
        
        return verses or []
    
    def populate_missing_verses(
        self, 
        book_name: Optional[str] = None, 
        limit: int = 100
    ) -> int:
        """
        Populate missing verse text in database.
        
        Args:
            book_name: Optional book name to filter by.
            limit: Maximum number of verses to populate.
            
        Returns:
            Number of verses updated.
        """
        if not self.db:
            logger.error("Database not configured")
            return 0
        
        if limit <= 0:
            return 0
        
        # Get verses without text
        query = """
            SELECT v.id, v.verse_reference, cb.name as book_name, v.chapter, v.verse_number
            FROM verses v
            JOIN canonical_books cb ON v.book_id = cb.id
            WHERE v.text_kjv IS NULL
        """
        params: List[Any] = []
        
        if book_name:
            query += " AND cb.name = %s"
            params.append(book_name)
        
        query += " ORDER BY cb.canonical_order, v.chapter, v.verse_number LIMIT %s"
        params.append(limit)
        
        try:
            verses = self.db.fetch_all(query, tuple(params))
        except Exception as e:
            logger.error(f"Failed to fetch verses: {e}")
            return 0
        
        updated = 0
        for verse in verses:
            text = self.fetch_verse(
                verse['book_name'], 
                verse['chapter'], 
                verse['verse_number']
            )
            
            if text:
                try:
                    self.db.execute(
                        "UPDATE verses SET text_kjv = %s WHERE id = %s",
                        (text, verse['id'])
                    )
                    updated += 1
                    logger.info(f"Updated: {verse['verse_reference']}")
                except Exception as e:
                    logger.error(f"Failed to update verse {verse['id']}: {e}")
            
            time.sleep(self.RATE_LIMIT_DELAY)  # Rate limiting
        
        return updated


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

_verse_fetcher: Optional[VerseFetcher] = None


def get_verse_fetcher() -> VerseFetcher:
    """
    Get the global verse fetcher singleton.
    
    Returns:
        The singleton VerseFetcher instance.
    """
    global _verse_fetcher
    if _verse_fetcher is None:
        _verse_fetcher = VerseFetcher()
    return _verse_fetcher
